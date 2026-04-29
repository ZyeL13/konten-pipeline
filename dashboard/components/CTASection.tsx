import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function CTASection() {
  return (
    <section className="border-t border-zinc-800 py-20 bg-zinc-900/50">
      <div className="container text-center max-w-2xl mx-auto space-y-6">
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
          Butuh custom automation system?
        </h2>
        <p className="text-zinc-400 text-lg">
          Kita mulai dari deep dive workflow kamu. No bullshit, langsung ke
          solusi teknis.
        </p>
        <div className="flex flex-col sm:flex-row gap-3 justify-center">
          <Button
            asChild
            size="lg"
            className="bg-cyan-600 hover:bg-cyan-700 text-white"
          >
            <Link href="/contact">Konsultasi Gratis</Link>
          </Button>
          <Button
            asChild
            size="lg"
            variant="outline"
            className="border-zinc-700 text-zinc-300 hover:bg-zinc-800"
          >
            <a
              href="https://wa.me/6285814002445?text=Hai%2C%20saya%20berminat%20untuk%20buat%20bot%20custom..."
              target="_blank"
              rel="noopener noreferrer"
            >
              Chat WhatsApp
            </a>
          </Button>
        </div>
      </div>
    </section>
  )
}
