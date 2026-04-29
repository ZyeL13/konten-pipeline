// components/ProcessTimeline.tsx
"use client"

import { motion } from "framer-motion"

const steps = [
  {
    label: "Audit",
    description: "We map your existing workflows, data, and pain points.",
  },
  {
    label: "Design",
    description:
      "Architecture blueprints, tool selection, and interface mockups.",
  },
  {
    label: "Build",
    description: "Rapid MVP with iterative testing and integration.",
  },
  {
    label: "Deploy",
    description:
      "Production rollout with monitoring, logging, and documentation.",
  },
]

export default function ProcessTimeline() {
  return (
    <section className="py-20 border-t border-zinc-800">
      <div className="container">
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl text-center mb-16">
          How we work
        </h2>
        <div className="relative">
          <div className="hidden md:block absolute top-8 left-0 right-0 h-0.5 bg-zinc-800" />
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {steps.map((step, i) => (
              <motion.div
                key={step.label}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                viewport={{ once: true }}
                className="relative flex flex-col items-center text-center"
              >
                <div className="flex h-10 w-10 items-center justify-center rounded-full border-2 border-cyan-500 bg-zinc-950 text-cyan-400 font-mono font-bold z-10">
                  {i + 1}
                </div>
                <h3 className="mt-4 text-lg font-semibold">{step.label}</h3>
                <p className="mt-2 text-sm text-zinc-400 max-w-[200px]">
                  {step.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}
