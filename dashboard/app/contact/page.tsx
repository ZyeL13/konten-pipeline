import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"
import { Github, Send, Phone } from "lucide-react"

export default function ContactPage() {
  return (
    <div className="container py-20 max-w-2xl">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Let's build something.
      </h1>
      <p className="text-zinc-400 mb-12">
        Ceritain sistem yang pengen kamu bangun atau otomasi. Gue bales dalam
        24 jam dengan technical assessment.
      </p>
      <Card className="bg-zinc-900 border-zinc-800">
        <CardContent className="p-6 space-y-6">
          <form className="space-y-5">
            <div>
              <label
                htmlFor="name"
                className="block text-sm font-medium text-zinc-400 mb-1"
              >
                Nama
              </label>
              <Input
                id="name"
                placeholder="Nama kamu"
                className="bg-zinc-950 border-zinc-700 text-white focus:border-cyan-500"
              />
            </div>
            <div>
              <label
                htmlFor="email"
                className="block text-sm font-medium text-zinc-400 mb-1"
              >
                Email
              </label>
              <Input
                id="email"
                type="email"
                placeholder="kamu@email.com"
                className="bg-zinc-950 border-zinc-700 text-white focus:border-cyan-500"
              />
            </div>
            <div>
              <label
                htmlFor="message"
                className="block text-sm font-medium text-zinc-400 mb-1"
              >
                Detail project
              </label>
              <Textarea
                id="message"
                rows={4}
                placeholder="Jelaskan workflow sekarang dan apa yang mau di-automate..."
                className="bg-zinc-950 border-zinc-700 text-white focus:border-cyan-500"
              />
            </div>
            <Button
              type="submit"
              className="w-full bg-cyan-600 hover:bg-cyan-700 text-white"
            >
              Kirim Inquiry
            </Button>
          </form>

          {/* Direct contact methods */}
          <div className="border-t border-zinc-800 pt-6 mt-6">
            <p className="text-sm text-zinc-500 mb-4">
              Atau kontak langsung:
            </p>
            <div className="grid gap-3">
              <a
                href="https://wa.me/6285814002445?text=Hai%2C%20saya%20berminat%20untuk%20buat%20bot%20custom..."
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-green-500/30 transition-colors group"
              >
                <Phone className="h-5 w-5 text-green-400" />
                <div>
                  <div className="text-sm font-medium group-hover:text-white">
                    WhatsApp
                  </div>
                  <div className="text-xs text-zinc-500">
                    +62 858 1400 2445
                  </div>
                </div>
              </a>

              <a
                href="https://t.me/zyel13"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-cyan-500/30 transition-colors group"
              >
                <Send className="h-5 w-5 text-cyan-400" />
                <div>
                  <div className="text-sm font-medium group-hover:text-white">
                    Telegram
                  </div>
                  <div className="text-xs text-zinc-500">@zyel13</div>
                </div>
              </a>

              <a
                href="mailto:aryandopurnama@gmail.com"
                className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-zinc-500/30 transition-colors group"
              >
                <span className="text-lg">📧</span>
                <div>
                  <div className="text-sm font-medium group-hover:text-white">
                    Email
                  </div>
                  <div className="text-xs text-zinc-500">
                    aryandopurnama@gmail.com
                  </div>
                </div>
              </a>

              <a
                href="https://github.com/ZyeL13"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-zinc-500/30 transition-colors group"
              >
                <Github className="h-5 w-5 text-zinc-300" />
                <div>
                  <div className="text-sm font-medium group-hover:text-white">
                    GitHub
                  </div>
                  <div className="text-xs text-zinc-500">ZyeL13</div>
                </div>
              </a>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
