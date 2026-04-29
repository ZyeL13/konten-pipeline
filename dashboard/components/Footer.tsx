import Link from "next/link"

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
            <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current" aria-hidden="true">
              <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.762-1.604-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z" />
            </svg>
            GitHub
          </a>
          <a
            href="https://t.me/zyel13"
            target="_blank"
            rel="noopener noreferrer"
            className="hover:text-zinc-300 inline-flex items-center gap-1"
          >
            <svg viewBox="0 0 24 24" className="h-4 w-4 fill-current" aria-hidden="true">
              <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-1.813 8.545c-.136.602-.493.752-1 .468l-2.763-2.036-1.333 1.283c-.148.147-.272.27-.557.27-.37 0-.306-.142-.433-.498l-.97-3.186-2.708-.84c-.585-.183-.597-.585.122-.867l10.563-4.07c.48-.18.9.11.746.825z" />
            </svg>
            Telegram
          </a>
        </div>
      </div>
    </footer>
  )
}
