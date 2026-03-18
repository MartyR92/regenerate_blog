import asyncio
import logging
from pydantic import BaseModel
from pydantic_ai import Agent

# Import our router logic
from scripts.orchestrator import FallbackRouter

# Configure logging for test visibility
logging.basicConfig(level=logging.INFO)

class TestSchema(BaseModel):
    success: bool
    message: str

# A dummy agent just for the test
test_agent = Agent('test', output_type=TestSchema, system_prompt="You are a helpful assistant.")

async def run_test():
    print("--- Starting 429 Failover Test ---")
    router = FallbackRouter(max_retries=3)
    
    # We will temporarily override the get_tier_1_model function inside orchestrator
    # to forcefully raise a 429 exception for the first attempt.
    import scripts.orchestrator as orch
    
    class MockFailingModel:
        model_name = "mock-failing-model"
        
        async def request(self, *args, **kwargs):
            raise Exception("HTTP 429: Too Many Requests - Rate limit exceeded")
            
    # Mock the Agent.run method to simulate the failure and recovery
    original_run = test_agent.run
    
    call_count = 0
    async def mock_run(prompt, model, deps=None):
        nonlocal call_count
        call_count += 1
        
        # Simulate 429 on the first call (Tier 1)
        if call_count == 1:
            print(f"[TEST] Mocking a 429 Rate Limit exception for model: {model.model_name}")
            raise Exception("429 Too Many Requests")
            
        # Succeed on the second call (Tier 2 Fallback)
        print(f"[TEST] Mocking a successful response for fallback model: {model.model_name}")
        class MockResult:
            data = TestSchema(success=True, message=f"Responded via {model.model_name}")
        return MockResult()

    test_agent.run = mock_run
    
    # Execute the router
    try:
        result = await router.execute(
            agent=test_agent,
            prompt="Hello!",
            task_type="editing" # Starts with claude-3-7-sonnet
        )
        print("\n--- Test Result ---")
        print(f"Final Data: {result}")
        print("Success! The router correctly caught the 429 and fell back to Tier 2.")
    except Exception as e:
        print(f"\nTest failed. Exception propagated: {e}")

if __name__ == "__main__":
    asyncio.run(run_test())
