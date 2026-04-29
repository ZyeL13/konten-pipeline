import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Card, CardContent } from "@/components/ui/card"

export default function ContactPage() {
  return (
    <div className="container py-20 max-w-2xl">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        Let's build something.
      </h1>
      <p className="text-zinc-400 mb-12">
        Ceritain sistem yang pengen kamu bangun atau otomasi. Gue bales dalam 24 jam dengan technical assessment.
      </p>
      <Card className="bg-zinc-900 border-zinc-800">
        <CardContent className="p-6 space-y-6">
          <form className="space-y-5">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-zinc-400 mb-1">Nama</label>
              <Input id="name" placeholder="Nama kamu" className="bg-zinc-950 border-zinc-700 text-white focus:border-cyan-500" />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-zinc-400 mb-1">Email</label>
              <Input id="email" type="email" placeholder="kamu@email.com" className="bg-zinc-950 border-zinc-700 text-white focus:border-cyan-500" />
            </div>
            <div>
              <label htmlFor="message" className="block text-sm font-medium text-zinc-400 mb-1">Detail project</label>
              <Textarea id="message" rows={4} placeholder="Jelaskan workflow sekarang dan apa yang mau di-automate..." className="bg-zinc-950 border-zinc-700 text-white focus:border-cyan-500" />
            </div>
            <Button type="submit" className="w-full bg-cyan-600 hover:bg-cyan-700 text-white">Kirim Inquiry</Button>
          </form>

          <div className="border-t border-zinc-800 pt-6 mt-6">
            <p className="text-sm text-zinc-500 mb-4">Atau kontak langsung:</p>
            <div className="grid gap-3">
              <a href="https://wa.me/6285814002445?text=Hai%2C%20saya%20berminat%20untuk%20buat%20bot%20custom..." target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-green-500/30 transition-colors group">
                <svg viewBox="0 0 24 24" className="h-5 w-5 fill-green-400" aria-hidden="true">
                  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z" />
                </svg>
                <div>
                  <div className="text-sm font-medium group-hover:text-white">WhatsApp</div>
                  <div className="text-xs text-zinc-500">+62 858 1400 2445</div>
                </div>
              </a>
              <a href="https://t.me/zyel13" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-cyan-500/30 transition-colors group">
                <svg viewBox="0 0 24 24" className="h-5 w-5 fill-cyan-400" aria-hidden="true">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.562 8.248l-1.813 8.545c-.136.602-.493.752-1 .468l-2.763-2.036-1.333 1.283c-.148.147-.272.27-.557.27-.37 0-.306-.142-.433-.498l-.97-3.186-2.708-.84c-.585-.183-.597-.585.122-.867l10.563-4.07c.48-.18.9.11.746.825z" />
                </svg>
                <div>
                  <div className="text-sm font-medium group-hover:text-white">Telegram</div>
                  <div className="text-xs text-zinc-500">@zyel13</div>
                </div>
              </a>
              <a href="mailto:aryandopurnama@gmail.com" className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-zinc-500/30 transition-colors group">
                <span className="text-lg">📧</span>
                <div>
                  <div className="text-sm font-medium group-hover:text-white">Email</div>
                  <div className="text-xs text-zinc-500">aryandopurnama@gmail.com</div>
                </div>
              </a>
              <a href="https://github.com/ZyeL13" target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 p-3 rounded-lg border border-zinc-800 bg-zinc-900 hover:border-zinc-500/30 transition-colors group">
                <svg viewBox="0 0 24 24" className="h-5 w-5 fill-zinc-300" aria-hidden="true">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.3 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61-.546-1.385-1.335-1.755-1.335-1.755-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.418-1.305.762-1.604-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 21.795 24 17.295 24 12c0-6.63-5.37-12-12-12z" />
                </svg>
                <div>
                  <div className="text-sm font-medium group-hover:text-white">GitHub</div>
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
