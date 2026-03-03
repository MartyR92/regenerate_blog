const fs = require('fs');
const path = require('path');

const tasks = [
  "Bilingual Parity: Ensuring every post has both German (DE) and English (EN) versions.",
  "Visual Debugging: Fixing rendering issues for broken diagrams (SVG/WebP).",
  "Editorial Cleanup: Removing 'AI-agent' mentions from reader-facing descriptions and metadata.",
  "Content Repair: Using scripts like repair_posts.py to fix or replace low-quality German articles.",
  "UI/UX: Implementing the language switch toggle in the Hugo theme header."
];

const ROOT_DIR = "C:\\\\Users\\\\User\\\\.gemini\\\\extensions\\\\pickle-rick";
const JAR_ROOT = path.join(ROOT_DIR, 'jar');
const SESSIONS_ROOT = path.join(ROOT_DIR, 'sessions');
const day = "2026-03-03";
const repo_path = "C:\\\\Users\\\\User\\\\projects\\\\regenerate_blog";

if (!fs.existsSync(JAR_ROOT)) fs.mkdirSync(JAR_ROOT, { recursive: true });
const dayDir = path.join(JAR_ROOT, day);
if (!fs.existsSync(dayDir)) fs.mkdirSync(dayDir, { recursive: true });
if (!fs.existsSync(SESSIONS_ROOT)) fs.mkdirSync(SESSIONS_ROOT, { recursive: true });

tasks.forEach((task, index) => {
  const taskId = `task-${index + 1}`;
  const sessionDir = path.join(SESSIONS_ROOT, taskId);
  if (!fs.existsSync(sessionDir)) fs.mkdirSync(sessionDir, { recursive: true });
  
  const state = {
    "active": false,
    "working_dir": repo_path,
    "step": "prd",
    "iteration": 0,
    "max_iterations": 5,
    "max_time_minutes": 60,
    "worker_timeout_seconds": 1200,
    "start_time_epoch": Math.floor(Date.now() / 1000),
    "completion_promise": null,
    "original_prompt": task,
    "current_ticket": null,
    "history": [],
    "started_at": new Date().toISOString(),
    "session_dir": sessionDir
  };
  fs.writeFileSync(path.join(sessionDir, 'state.json'), JSON.stringify(state, null, 2));
  
  const taskJarDir = path.join(dayDir, taskId);
  if (!fs.existsSync(taskJarDir)) fs.mkdirSync(taskJarDir, { recursive: true });
  
  const meta = {
    "status": "marinating",
    "repo_path": repo_path
  };
  fs.writeFileSync(path.join(taskJarDir, 'meta.json'), JSON.stringify(meta, null, 2));
  console.log(`Marinated ${taskId}: ${task}`);
});
