const { execSync } = require('child_process');
const fs = require('fs');
const path = require('fs');

const articles = [
    "content/de/posts/2026-02-26-algorithmische-symbiose-wie-präzisionstechnologie-die-regenerative-landwirtschaft-transformiert-und-neues-kapital-generiert.md",
    "content/de/posts/2026-03-01-die-algorithmen-der-fülle-wie-präzisionslandwirtschaft-die-regenerative-wirtschaft-architekturiert.md",
    "content/de/posts/2026-03-02-die-architekten-des-atmenden-planeten-wie-digitale-ökosysteme-die-regenerative-fülle-entfesseln.md",
    "content/de/posts/2026-03-02-die-neuvermessung-des-ackerlands-praezision-als-katalysator-regenerativer-fuelle.de.md",
    "content/de/posts/2026-03-02-praezision-im-feld-wie-techno-organische-intelligenz-die-regenerative-agrikultur-transformiert.de.md",
    "content/de/posts/2026-03-03-das-myzel-als-bauplan-dezentrale-fuelle-in-der-regenerativen-wirtschaft.de.md",
    "content/en/posts/2026-03-02-die-neuvermessung-des-ackerlands-praezision-als-katalysator-regenerativer-fuelle.en.md",
    "content/en/posts/2026-03-02-praezision-im-feld-wie-techno-organische-intelligenz-die-regenerative-agrikultur-transformiert.en.md",
    "content/en/posts/2026-03-03-das-myzel-als-bauplan-dezentrale-fuelle-in-der-regenerativen-wirtschaft.en.md"
];

const env = {
    ...process.env,
    UNSPLASH_ACCESS_KEY: "UJ8s-5bxUwkGyqRAecD8rUXfFPYEAbdAPq_qLxbmY3Y",
    GEMINI_API_KEY: process.env.INTERACTIONS_API_KEY || process.env.GEMINI_API_KEY
};

console.log("🚀 Starting Milestone v5.0 Retrofit...");

// 1. Run Visual Agent (Hero Images)
console.log("\n--- Task 1: Retrofitting Hero Images ---");
try {
    execSync('python scripts/visual.py', { env, stdio: 'inherit' });
} catch (e) {
    console.error("❌ Visual Agent failed, but continuing...");
}

// 2. Run Image Agent (Technical Visuals)
console.log("\n--- Task 2: Retrofitting Technical Visuals ---");
try {
    execSync('python scripts/image.py', { env, stdio: 'inherit' });
} catch (e) {
    console.error("❌ Image Agent failed.");
}

console.log("\n✅ Retrofit process finished.");
