import os
import json
import random
import logging
import asyncio
from typing import Any, Callable, Dict, List, Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# PydanticAI Imports
from pydantic_ai import Agent, RunContext
from pydantic_ai.models.anthropic import AnthropicModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("FallbackRouter")

# ==========================================
# SECRETS MANAGEMENT & MODEL CONFIGURATION
# ==========================================

OPENROUTER_API_KEYS = [
    os.environ.get("OPENROUTER_API_KEY_1"),
    os.environ.get("OPENROUTER_API_KEY_2"),
    os.environ.get("OPENROUTER_API_KEY_3"),
    os.environ.get("OPENROUTER_API_KEY_4"),
    os.environ.get("OPENROUTER_API_KEY_5"),
]
OPENROUTER_API_KEYS = [k for k in OPENROUTER_API_KEYS if k]

def get_tier_1_model(task_type: str):
    """Returns the optimal Tier 1 model for the specific task and sets required env vars."""
    if task_type == "drafting":
        provider = OpenAIProvider(
            api_key=os.environ.get("INCEPTION_API_KEY", "missing_key"),
            base_url="https://api.inceptionlabs.ai/v1"
        )
        return OpenAIModel(model_name="mercury-2", provider=provider)
        
    elif task_type in ["editing", "logic", "research"]:
        # Temporarily using Nemotron 3 Super 120B Free on OpenRouter since Anthropic credits are exhausted
        # OpenRouter does NOT host any free Claude models.
        api_key = os.environ.get("OPENROUTER_API_KEY_1", "missing_key")
        provider = OpenAIProvider(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        return OpenAIModel(model_name="nvidia/nemotron-3-super-120b-a12b:free", provider=provider)
        
    elif task_type == "vision":
        os.environ["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY_1", "missing_key")
        return GeminiModel(model_name="gemini-2.5-pro")
        
    else:
        raise ValueError(f"Unknown task type: {task_type}")

def get_tier_2_model(retry_count: int):
    """Cycles through OpenRouter keys and models for bulletproof fallback."""
    if not OPENROUTER_API_KEYS:
         logger.warning("No OpenRouter API keys found in environment. Fallback may fail.")
         api_key = "missing_key"
    else:
         api_key = OPENROUTER_API_KEYS[retry_count % len(OPENROUTER_API_KEYS)]
    
    models = [
        "nvidia/nemotron-3-super-120b-a12b:free", 
        "meta-llama/llama-3.3-70b-instruct:free", 
        "mistralai/mistral-small-3.1-24b-instruct:free"
    ]
    selected_model = models[retry_count % len(models)]
    
    provider = OpenAIProvider(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1"
    )
    return OpenAIModel(model_name=selected_model, provider=provider)


def sanitize_log(msg: str) -> str:
    """Masks any API keys that might accidentally be logged."""
    sensitive_keys = [
        os.environ.get("INCEPTION_API_KEY"),
        os.environ.get("ANTHROPIC_API_KEY"),
        os.environ.get("GEMINI_API_KEY_1"),
        os.environ.get("GEMINI_API_KEY_2"),
        os.environ.get("GEMINI_API_KEY_3"),
    ] + OPENROUTER_API_KEYS
    
    sanitized = str(msg)
    for key in sensitive_keys:
        if key and key != "missing_key" and len(key) > 4:
            sanitized = sanitized.replace(key, f"{key[:4]}...[REDACTED]")
    return sanitized

def sanitize_input(user_input: str) -> str:
    """
    Prevents prompt injection by neutralizing instruction overrides
    and wrapping the input in strict delimiter boundaries.
    """
    # Remove characters often used in jailbreaks
    dangerous_patterns = [
        "Ignore all previous instructions", 
        "System override", 
        "You are now",
        "```", 
        "SYSTEM:", 
        "ASSISTANT:"
    ]
    safe_input = user_input
    for pattern in dangerous_patterns:
        # Case insensitive replacement
        import re
        safe_input = re.sub(pattern, "[REDACTED]", safe_input, flags=re.IGNORECASE)
        
    return f"---START_USER_INPUT---\n{safe_input}\n---END_USER_INPUT---"

# ==========================================
# FALLBACK ROUTER
# ==========================================

class FallbackRouter:
    def __init__(self, max_retries: int = 3):
        self.max_retries = max_retries

    async def execute(self, agent: Agent, prompt: str, task_type: str, deps: Any = None) -> Any:
        current_model = get_tier_1_model(task_type)
        logger.info(f"Attempting task '{task_type}' with Tier 1 model: {current_model.model_name}")

        for attempt in range(self.max_retries + 1):
            try:
                result = await agent.run(prompt, model=current_model, deps=deps)
                logger.info(f"Task '{task_type}' completed successfully on attempt {attempt + 1}.")
                return result.output
            except Exception as e:
                safe_error = sanitize_log(str(e))
                error_msg = safe_error.lower()
                is_recoverable = any(code in error_msg for code in ["429", "500", "502", "503", "timeout", "rate limit", "quota", "too many requests", "credit balance", "invalid response", "validation error"])
                
                if attempt == self.max_retries or not is_recoverable:
                    logger.error(f"Failed task '{task_type}'. Final error: {safe_error}")
                    raise RuntimeError(safe_error)

                logger.warning(f"Attempt {attempt + 1} failed with error: {safe_error}. Initiating Fallback (Tier 2).")
                current_model = get_tier_2_model(retry_count=attempt)
                logger.info(f"Swapped to Tier 2 Fallback Model: {current_model.model_name}")
                await asyncio.sleep(2 ** attempt)


# ==========================================
# PHASE 2: SCHEMAS & AGENT DEFINITIONS
# ==========================================

# 1. Pydantic BaseModels for strict state validation
class ResearchState(BaseModel):
    topic: str = Field(..., description="The core subject being researched.")
    key_findings: List[str] = Field(..., description="Bullet points of verified facts.")
    citations: List[str] = Field(..., description="URLs or reference materials.")
    outline: str = Field(..., description="Proposed markdown outline for the article.")

class DraftState(BaseModel):
    title: str = Field(..., description="SEO optimized title.")
    content: str = Field(..., description="The full drafted article in markdown.")
    seo_keywords: List[str] = Field(..., description="Target keywords used.")

class EditorialFeedback(BaseModel):
    approved: bool = Field(..., description="True if ready to publish, False if revisions needed.")
    critique: str = Field(..., description="Constructive feedback based on brand guidelines.")
    rewritten_content: Optional[str] = Field(None, description="The revised draft if changes were made.")

class VisualAssets(BaseModel):
    hero_image_prompt: str = Field(..., description="Prompt for NanoBanana/Gemini to generate a hero image.")
    echarts_json: Optional[str] = Field(None, description="Optional ECharts configuration for data visualization.")

class PublishState(BaseModel):
    final_markdown: str = Field(..., description="The final merged post with frontmatter.")
    social_posts: List[str] = Field(..., description="Short posts for LinkedIn/X/Mastodon.")


# 2. Agent Definitions injecting .gemini/skills via System Prompts

research_agent = Agent(
    'test',
    output_type=ResearchState,
    system_prompt=(
        "You are an elite Research Agent. You MUST utilize the methodologies from the following skills:\n"
        "- `deep-research`: Conduct autonomous, multi-step investigation.\n"
        "- `research-engineer` & `scientific-writing`: Maintain academic rigor.\n"
        "- `citation-management`: Ensure all claims are backed by credible sources.\n"
        "You must avoid repeating previously covered topics. Output a structured research state."
    )
)

writer_agent = Agent(
    'test',
    output_type=DraftState,
    system_prompt=(
        "You are a Master Content Creator. Adhere to these skills:\n"
        "- `beautiful-prose`: Write elegantly, forcefully, and clearly.\n"
        "- `avoid-ai-writing`: Strip all typical AI cliches (e.g., 'In conclusion', 'Delve into').\n"
        "- `seo-content-writer`: Naturally weave in semantic keywords without stuffing.\n"
        "Draft a compelling, high-signal post based on the provided research. NEVER reuse titles or exact themes from the blog memory."
    )
)

editor_agent = Agent(
    'test',
    output_type=EditorialFeedback,
    system_prompt=(
        "You are a Ruthless Editor. Follow these frameworks:\n"
        "- `professional-proofreader`: Fix grammar, flow, and pacing.\n"
        "- `brand-guidelines`: Ensure the tone matches the Organic Precision aesthetic.\n"
        "- `seo-content-auditor`: Verify readability and SEO structure.\n"
        "If the draft is perfect, approve it. Otherwise, provide a critique and the rewritten content."
    )
)

visual_agent = Agent(
    'test',
    output_type=VisualAssets,
    system_prompt=(
        "You are a Visual Architect. Utilize:\n"
        "- `ui-ux-pro-max` & `frontend-design`: Ensure aesthetics are modern and clean.\n"
        "- `data-visualization`: Provide valid ECharts JSON if data is present.\n"
        "Generate a highly specific prompt for NanoBanana (gemini-3.1-pro) for the hero image."
    )
)

distribution_agent = Agent(
    'test',
    output_type=PublishState,
    system_prompt=(
        "You are the Distribution Orchestrator. Apply:\n"
        "- `social-orchestrator`: Craft engaging, platform-specific social posts.\n"
        "- `seo-meta-optimizer`: Generate high-CTR meta descriptions.\n"
        "Combine the approved draft with generated assets and frontmatter."
    )
)

# ==========================================
# HYBRID WORKFLOW ORCHESTRATION (MOCK)
# ==========================================

def get_dynamic_topic() -> str:
    """Generates a dynamic topic from the ontology if the default is used."""
    ontology_path = "context/ontology.json"
    if os.path.exists(ontology_path):
        try:
            with open(ontology_path, "r", encoding="utf-8") as f:
                ontology = json.load(f)
            domain = random.choice(list(ontology.get("domains", {}).keys()))
            tags = ontology["domains"][domain].get("tags", [])
            tag = random.choice(tags) if tags else domain
            cross_tag = random.choice(ontology.get("cross-domain-tags", ["Innovation"]))
            return f"The intersection of {tag} in {domain} and {cross_tag}"
        except Exception as e:
            logger.error(f"Failed to load ontology: {e}")
    return "The future of regenerative agritech and open-source ecosystems"

def get_blog_memory() -> str:
    """Loads the blog memory to prevent repetition."""
    memory_path = "context/blog-memory.json"
    if os.path.exists(memory_path):
        try:
            with open(memory_path, "r", encoding="utf-8-sig") as f:
                return f.read()
        except Exception as e:
            logger.error(f"Failed to load blog memory: {e}")
    return "{}"

def update_blog_memory(new_title: str, new_keywords: List[str]):
    """Updates the blog memory with the new article to prevent future repetition."""
    memory_path = "context/blog-memory.json"
    try:
        if os.path.exists(memory_path):
            with open(memory_path, "r", encoding="utf-8-sig") as f:
                memory = json.load(f)
        else:
            memory = {"version": "1.0", "total_posts": 0, "posts": [], "recurring_themes": [], "avoid_repetition": []}
        
        memory["total_posts"] = memory.get("total_posts", 0) + 1
        
        # Add to recent posts
        memory.setdefault("posts", []).append({"title": new_title, "keywords": new_keywords})
        # Keep only last 20 to avoid memory bloat
        memory["posts"] = memory["posts"][-20:]
        
        # Add to avoid_repetition list
        for keyword in new_keywords:
            if keyword not in memory.setdefault("avoid_repetition", []):
                memory["avoid_repetition"].append(keyword)
                
        # Keep avoid list manageable
        memory["avoid_repetition"] = memory["avoid_repetition"][-50:]
        
        from datetime import datetime
        memory["last_updated"] = datetime.now().strftime("%Y-%m-%d")

        with open(memory_path, "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=2)
        logger.info(f"Updated blog memory with new title: '{new_title}'")
    except Exception as e:
        logger.error(f"Failed to update blog memory: {e}")

async def main(mode: str = "test", topic: str = "The intersection of regenerative agriculture and open-source AI in 2026."):
    router = FallbackRouter(max_retries=3)
    
    # If the default topic is passed (e.g., cron job), generate a dynamic one
    if topic == "The intersection of regenerative agriculture and open-source AI in 2026." or topic == "The future of regenerative agritech":
        topic = get_dynamic_topic()
        
    safe_topic = sanitize_input(topic)
    blog_memory = get_blog_memory()
    
    try:
        if mode == "draft":
            logger.info("--- Starting Local Draft Mode ---")
            
            logger.info("--- Starting Research Phase ---")
            research_prompt = f"Research this topic: {safe_topic}\n\nAVOID THESE PAST TOPICS:\n{blog_memory}"
            research_state = await router.execute(
                agent=research_agent,
                prompt=research_prompt,
                task_type="research"
            )
            print(f"Research Outline: {research_state.outline}")

            logger.info("--- Starting Drafting Phase ---")
            draft_prompt = f"Draft an article based on this research:\n{research_state.model_dump_json()}\n\nAVOID THESE PAST TOPICS:\n{blog_memory}"
            draft_state = await router.execute(
                agent=writer_agent,
                prompt=draft_prompt,
                task_type="drafting"
            )
            print(f"Draft Title: {draft_state.title}")
            
            # Save the draft
            import re
            from datetime import datetime
            os.makedirs("_drafts", exist_ok=True)
            slug = re.sub(r'[^a-z0-9]+', '-', draft_state.title.lower()).strip('-')
            date_prefix = datetime.now().strftime("%Y-%m-%d")
            draft_path = f"_drafts/{date_prefix}-{slug}.md"
            with open(draft_path, "w", encoding="utf-8") as f:
                f.write(f"---\ntitle: \"{draft_state.title}\"\n---\n\n{draft_state.content}")
            logger.info(f"Saved draft to {draft_path}")
            
            # Update memory since draft was successful
            update_blog_memory(draft_state.title, draft_state.seo_keywords)
            
            logger.info("Draft complete. Push to _drafts/ to trigger full cloud pipeline.")
            
        elif mode in ["publish", "test"]:
            logger.info(f"--- Starting Full Pipeline ({mode} mode) ---")
            
            logger.info("--- Starting Research Phase ---")
            research_prompt = f"Research this topic: {safe_topic}\n\nAVOID THESE PAST TOPICS:\n{blog_memory}"
            research_state = await router.execute(
                agent=research_agent,
                prompt=research_prompt,
                task_type="research"
            )
            print(f"Research Outline: {research_state.outline}")

            logger.info("--- Starting Drafting Phase ---")
            draft_prompt = f"Draft an article based on this research:\n{research_state.model_dump_json()}\n\nAVOID THESE PAST TOPICS:\n{blog_memory}"
            draft_state = await router.execute(
                agent=writer_agent,
                prompt=draft_prompt,
                task_type="drafting"
            )
            print(f"Draft Title: {draft_state.title}")
            
            logger.info("--- Starting Editing Phase ---")
            edit_state = await router.execute(
                agent=editor_agent,
                prompt=f"Review this draft:\n{draft_state.model_dump_json()}",
                task_type="editing"
            )
            print(f"Editor Approved: {edit_state.approved}")

            logger.info("--- Starting Visual Phase ---")
            visual_state = await router.execute(
                agent=visual_agent,
                prompt=f"Create visual concepts for this article:\n{draft_state.title}\n{draft_state.content[:500]}...",
                task_type="vision"
            )
            print(f"Hero Prompt: {visual_state.hero_image_prompt}")

            # Update memory on successful full run
            if mode == "publish":
                 update_blog_memory(draft_state.title, draft_state.seo_keywords)

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="PydanticAI Stateful Orchestrator")
    parser.add_argument("--test", action="store_true", help="Run the mock orchestration pipeline")
    parser.add_argument("--draft", action="store_true", help="Run locally to draft a post")
    parser.add_argument("--publish", action="store_true", help="Run full pipeline (usually in CI/CD)")
    parser.add_argument("--topic", type=str, default="The future of regenerative agritech", help="Topic to write about")
    args = parser.parse_args()
    
    mode = "test"
    if args.draft:
        mode = "draft"
    elif args.publish:
        mode = "publish"
        
    if args.test or args.draft or args.publish:
        asyncio.run(main(mode=mode, topic=args.topic))
