import Link from "next/link"
import { Github, Send } from "lucide-react"

export default function Footer() {
  return (
    <footer className="border-t border-zinc-800 bg-zinc-950 py-8">
      <div className="container flex flex-col md:flex-row justify-between items-center gap-6 text-sm text-zinc-500">
        <div className="flex flex-col md:flex-row items-center gap-4">
          <span>© {new Date().getFullYear()} Zyel Lab — Aryando Purnama</span>
        </div>
        <div className="flex items-center gap-6">
          <Link href="/services" className="hover:text-zinc-300">
            Services
          </Link>
          <Link href="/lab" className="hover:text-zinc-300">
            Lab
          </Link>
          <Link href="/contact" className="hover:text-zinc-300">
            Contact
          </Link>
          <a
            href="https://github.com/ZyeL13"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-zinc-300 inline-flex items-center gap-1"
          >
            <Github className="h-4 w-4" />
            GitHub
          </a>
          <a
            href="https://t.me/zyel13"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-zinc-300 inline-flex items-center gap-1"
          >
            <Send className="h-4 w-4" />
            Telegram
          </a>
        </div>
      </div>
    </footer>
  )
}
