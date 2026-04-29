// components/CapabilityGrid.tsx
import { Card, CardContent } from "@/components/ui/card"
import {
  Bot,
  MessageSquare,
  Workflow,
  BarChart3,
  DollarSign,
  Database,
} from "lucide-react"

const capabilities = [
  {
    title: "AI Agents",
    description:
      "Multi-step reasoning agents that execute complex tasks autonomously.",
    icon: Bot,
  },
  {
    title: "Telegram/WhatsApp Bots",
    description:
      "Chatbots that integrate with your business logic, payments, and CRMs.",
    icon: MessageSquare,
  },
  {
    title: "Workflow Automation",
    description:
      "End-to-end process automation connecting APIs, queues, and human-in-the-loop steps.",
    icon: Workflow,
  },
  {
    title: "Finance Systems",
    description:
      "Custom ledgers, invoice parsers, reconciliation bots, and financial dashboards.",
    icon: DollarSign,
  },
  {
    title: "Internal Dashboards",
    description:
      "Operational dashboards that give teams real-time visibility and control.",
    icon: BarChart3,
  },
  {
    title: "Data Pipelines",
    description:
      "Robust ETL pipelines, scraping, and data transformation for reliable data.",
    icon: Database,
  },
]

export default function CapabilityGrid() {
  return (
    <section className="py-20 border-t border-zinc-800">
      <div className="container">
        <div className="mb-12 text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            What we build
          </h2>
          <p className="mt-4 text-zinc-400 max-w-2xl mx-auto">
            Systems, not demos. Every solution is engineered for reliability and
            real-world operations.
          </p>
        </div>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {capabilities.map((cap) => (
            <Card
              key={cap.title}
              className="bg-zinc-900 border-zinc-800 hover:border-cyan-500/30 transition-colors group"
            >
              <CardContent className="p-6 space-y-3">
                <div className="inline-flex h-10 w-10 items-center justify-center rounded-md bg-zinc-800 text-cyan-400 group-hover:bg-cyan-500/10">
                  <cap.icon className="h-5 w-5" />
                </div>
                <h3 className="font-semibold text-lg">{cap.title}</h3>
                <p className="text-sm text-zinc-400 leading-relaxed">
                  {cap.description}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>
  )
}
