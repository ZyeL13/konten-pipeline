// components/Hero.tsx
"use client"

import { Button } from "@/components/ui/button"
import Link from "next/link"
import TerminalDemo from "./TerminalDemo"
import { motion } from "framer-motion"

export default function Hero() {
  return (
    <section className="relative overflow-hidden py-20 md:py-32">
      <div className="container grid lg:grid-cols-2 gap-12 items-center">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-6"
        >
          <h1 className="text-4xl font-bold tracking-tight sm:text-5xl lg:text-6xl">
            Build custom{" "}
            <span className="text-cyan-400">
              AI agents, workflow bots,
            </span>{" "}
            and internal automations.
          </h1>
          <p className="max-w-xl text-lg text-zinc-400">
            From Telegram bots to accounting pipelines and multi-agent systems.
            Designed for operators, founders, and teams who need systems, not
            demos.
          </p>
          <div className="flex flex-wrap gap-4">
            <Button
              asChild
              size="lg"
              className="bg-cyan-600 hover:bg-cyan-700 text-white"
            >
              <Link href="/lab">View Labs</Link>
            </Button>
            <Button
              asChild
              variant="outline"
              size="lg"
              className="border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-white"
            >
              <Link href="/contact">Book Consultation</Link>
            </Button>
          </div>
        </motion.div>
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
          className="relative"
        >
          <TerminalDemo />
        </motion.div>
      </div>
      <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top,_hsl(196_100%_47%_/0.15),transparent_70%)]" />
    </section>
  )
}
