// components/TerminalDemo.tsx
"use client"

import { useEffect, useState } from "react"

const logLines = [
  { text: "> parsing transaction...", delay: 0 },
  { text: "> generating ledger...", delay: 1200 },
  { text: "> exporting xlsx...", delay: 2400 },
  { text: "status: success ✓", delay: 3600, highlight: true },
]

export default function TerminalDemo() {
  const [visibleLines, setVisibleLines] = useState<string[]>([])

  useEffect(() => {
    const timers = logLines.map((line) =>
      setTimeout(() => {
        setVisibleLines((prev) => [...prev, line.text])
      }, line.delay)
    )
    return () => timers.forEach(clearTimeout)
  }, [])

  return (
    <div className="w-full max-w-lg mx-auto rounded-lg border border-zinc-800 bg-zinc-900/80 p-4 font-mono text-sm text-zinc-300 shadow-xl backdrop-blur">
      <div className="flex items-center gap-2 border-b border-zinc-800 pb-2 mb-3">
        <div className="h-3 w-3 rounded-full bg-red-500/80" />
        <div className="h-3 w-3 rounded-full bg-yellow-500/80" />
        <div className="h-3 w-3 rounded-full bg-green-500/80" />
        <span className="ml-2 text-xs text-zinc-500">
          terminal — workflow.log
        </span>
      </div>
      <div className="space-y-1 min-h-[120px]">
        {visibleLines.map((line, i) => (
          <div
            key={i}
            className={
              logLines.find((l) => l.text === line)?.highlight
                ? "text-cyan-400 font-semibold"
                : ""
            }
          >
            {line}
          </div>
        ))}
        <span className="animate-pulse text-cyan-400">▮</span>
      </div>
    </div>
  )
}
