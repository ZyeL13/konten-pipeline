import Link from "next/link"
import { Button } from "@/components/ui/button"

export default function Nav() {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-zinc-800 bg-zinc-950/80 backdrop-blur supports-[backdrop-filter]:bg-zinc-950/60">
      <div className="container flex h-14 items-center justify-between">
        <Link
          href="/"
          className="flex items-center gap-2 font-mono text-sm font-bold tracking-tight text-cyan-400"
        >
          <span className="text-lg">&gt;_</span> zyel
        </Link>
        <nav className="hidden md:flex items-center gap-6 text-sm">
          <Link
            href="/services"
            className="text-zinc-400 hover:text-zinc-100 transition-colors"
          >
            Services
          </Link>
          <Link
            href="/lab"
            className="text-zinc-400 hover:text-zinc-100 transition-colors"
          >
            Lab
          </Link>
          <Link
            href="/contact"
            className="text-zinc-400 hover:text-zinc-100 transition-colors"
          >
            Contact
          </Link>
        </nav>
        <Button
          asChild
          size="sm"
          className="hidden md:inline-flex bg-cyan-600 hover:bg-cyan-700 text-white"
        >
          <Link href="/contact">Mulai Project</Link>
        </Button>
      </div>
    </header>
  )
}
