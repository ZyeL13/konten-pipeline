// lib/projects.ts
export interface Project {
  slug: string
  title: string
  description: string
  stack: string[]
  impact?: string
  problem?: string
  solution?: string
  architecture?: string
  metrics?: { label: string; value: string }[]
  screenshots?: string[]
}

export const allProjects: Project[] = [
  {
    slug: "general-ledger-bot",
    title: "General Ledger Bot",
    description:
      "Telegram accounting bot with regex parser + Excel export for small businesses.",
    stack: ["Python", "SQLite", "OpenAI", "Telegram API"],
    impact: "Reduced monthly bookkeeping time by 80%",
    problem:
      "Manual entry of transactions into spreadsheets was error-prone and time-consuming.",
    solution:
      "Built a Telegram bot that parses natural language entries, categorizes them, and generates a real-time ledger with Excel export.",
    architecture: "Telegram → Parser → Queue → LLM → DB → Excel Export",
    metrics: [
      { label: "Time Saved", value: "80%" },
      { label: "Errors Reduced", value: "95%" },
    ],
    screenshots: [],
  },
  {
    slug: "self-healing-pipeline",
    title: "Self-Healing Pipeline",
    description:
      "Queue worker with retry logic and health monitoring for e-commerce data sync.",
    stack: ["Node.js", "BullMQ", "Redis", "PostgreSQL"],
    impact: "Achieved 99.9% uptime on critical sync process",
    problem:
      "Data sync between legacy ERP and cloud CRM kept failing silently, causing order delays.",
    solution:
      "Implemented a resilient queue worker with exponential backoff, dead-letter queues, and a health dashboard.",
    architecture: "CRON → Queue → Worker → ERP API → CRM → DB → Dashboard",
    metrics: [
      { label: "Uptime", value: "99.9%" },
      { label: "Failed jobs auto-recovered", value: "100%" },
    ],
  },
  {
    slug: "multi-agent-research",
    title: "Multi-Agent Research Assistant",
    description:
      "System of specialized LLM agents that research market trends and produce reports.",
    stack: ["Python", "LangChain", "OpenAI", "FastAPI", "React"],
    impact: "Generated 10x more research output with consistent quality",
    problem:
      "Analysts spent days manually gathering data and writing reports.",
    solution:
      "Orchestrated multiple AI agents (scraper, summarizer, critic) to produce structured reports with citations.",
    architecture:
      "User Query → Orchestrator → Scraper Agent + Summarizer Agent → Critic → Report Generator",
    metrics: [
      { label: "Reports per week", value: "50+" },
      { label: "Time per report", value: "< 1 hour" },
    ],
  },
]

export const featuredProjects = allProjects.slice(0, 3)
