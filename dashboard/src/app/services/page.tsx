import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Services — Zyel Autonomous Hub',
  description:
    'Jasa automasi data, administrasi digital, dan bantuan personal oleh Zyel. Ditenagai script, dikerjakan manusia.',
  alternates: { canonical: 'https://zyel.vercel.app/services' },
  openGraph: {
    title: 'Services | Zyel Autonomous Hub',
    description:
      'Jasa automasi data, administrasi digital, dan bantuan personal oleh Zyel.',
    url: 'https://zyel.vercel.app/services',
  },
};

const WA_NUMBER = '6285714002445';

function waLink(label: string) {
  const msg = encodeURIComponent(`Halo Zyel, saya tertarik dengan jasa: ${label}`);
  return `https://wa.me/${WA_NUMBER}?text=${msg}`;
}

const categories = [
  {
    id: 'CAT-01',
    emoji: '🤖',
    title: 'Automasi & Data',
    subtitle: 'The Machine',
    accent: 'sky',
    description: 'Tugas membosankan untuk manusia, trivial untuk script. Serahkan ke mesin.',
    items: [
      { name: 'Web Scraping & Data Extraction', desc: 'Ambil data massal dari website ke Excel/JSON — harga properti, kontak bisnis, dll.' },
      { name: 'Workflow Automation', desc: 'Hubungkan satu aplikasi ke aplikasi lain. Contoh: Google Form → notif Telegram otomatis.' },
      { name: 'Bot Monitoring', desc: 'Pantau harga crypto atau flash sale, kirim notifikasi real-time ke HP kamu.' },
      { name: 'Data Cleaning', desc: 'Rapikan ribuan baris data berantakan pakai Python dalam hitungan menit.' },
    ],
    price: 'Mulai Rp 50.000',
    popular: true,
  },
  {
    id: 'CAT-02',
    emoji: '📋',
    title: 'Bantuan Administratif',
    subtitle: 'Data Entry',
    accent: 'violet',
    description: 'Pekerjaan repetitif yang butuh ketelitian tinggi. Dikerjakan cepat, rapi, dan sistematis.',
    items: [
      { name: 'Bulk Product Entry', desc: 'Input ratusan produk ke Shopee/Tokopedia atau platform lainnya.' },
      { name: 'Digitizing Documents', desc: 'Pindahkan data dari gambar atau PDF ke tabel digital yang bersih.' },
      { name: 'File Management', desc: 'Rapikan Google Drive/Dropbox kamu dengan struktur folder dan penamaan sistematis.' },
    ],
    price: 'Mulai Rp 30.000',
    popular: false,
  },
  {
    id: 'CAT-03',
    emoji: '🤝',
    title: 'Bantuan Personal & Fisik',
    subtitle: 'The Human',
    accent: 'emerald',
    description: 'Jasa yang butuh kehadiran dan kepercayaan. Bukan mesin — ini manusianya langsung.',
    items: [
      { name: 'Caregiver Companion (Non-Medis)', desc: 'Temani orang sakit atau lansia di rumah/RS, bantu mobilitas ringan, update kondisi ke keluarga.' },
      { name: 'Personal On-Site Assistant', desc: 'Cek fisik barang yang mau kamu beli (OLX/marketplace) atau keperluan on-site lainnya.' },
      { name: 'Courier Spesialis', desc: 'Antar dokumen penting atau barang sensitif dengan penanganan lebih personal dari kurir biasa.' },
    ],
    price: 'Hubungi untuk harga',
    popular: false,
  },
];

const accentMap: Record<string, { border: string; badge: string; tag: string; btn: string; price: string }> = {
  sky: {
    border: 'border-sky-700/40',
    badge:  'bg-sky-500/20 text-sky-400 border-sky-500/30',
    tag:    'bg-sky-950/50 text-sky-300 border-sky-800/50',
    btn:    'bg-sky-600 hover:bg-sky-500',
    price:  'text-sky-400',
  },
  violet: {
    border: 'border-violet-700/40',
    badge:  'bg-violet-500/20 text-violet-400 border-violet-500/30',
    tag:    'bg-violet-950/50 text-violet-300 border-violet-800/50',
    btn:    'bg-violet-600 hover:bg-violet-500',
    price:  'text-violet-400',
  },
  emerald: {
    border: 'border-emerald-700/40',
    badge:  'bg-emerald-500/20 text-emerald-400 border-emerald-500/30',
    tag:    'bg-emerald-950/50 text-emerald-300 border-emerald-800/50',
    btn:    'bg-emerald-600 hover:bg-emerald-500',
    price:  'text-emerald-400',
  },
};

export default function ServicesPage() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950">

      <div
        className="fixed inset-0 pointer-events-none opacity-[0.04]"
        style={{
          backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(148,163,184,0.8) 1px, transparent 0)',
          backgroundSize: '32px 32px',
        }}
      />

      <div className="relative z-10 max-w-xl mx-auto px-4 py-10 sm:py-16">

        <Link href="/" className="inline-block text-xs text-slate-500 hover:text-slate-300 mb-8 transition-colors">
          ← Dashboard
        </Link>

        <header className="mb-10">
          <p className="text-[11px] tracking-widest uppercase text-slate-500 mb-2 font-mono">
            zyel.vercel.app // services
          </p>
          <h1 className="text-3xl font-bold text-white mb-3 leading-tight">
            Human + Machine{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-sky-400 via-violet-400 to-emerald-400">
              for Rent
            </span>
          </h1>
          <p className="text-slate-400 text-sm leading-relaxed">
            Ditenagai script, dikerjakan manusia. Tiga kategori jasa — pilih yang paling cocok, atau{' '}
            <a href={waLink('Proyek Custom')} target="_blank" rel="noopener noreferrer"
               className="text-emerald-400 underline underline-offset-2 hover:text-emerald-300">
              diskusi custom
            </a>.
          </p>
        </header>

        <div className="flex flex-col gap-5">
          {categories.map((cat) => {
            const a = accentMap[cat.accent];
            return (
              <article key={cat.id} className={`rounded-2xl border bg-slate-900/50 p-5 ${a.border}`}>

                <div className="flex items-start justify-between gap-2 mb-1">
                  <div className="flex items-center gap-2.5">
                    <span className="text-2xl leading-none">{cat.emoji}</span>
                    <div>
                      <p className="text-[10px] font-mono text-slate-600">{cat.id}</p>
                      <h2 className="text-base font-bold text-white leading-snug">{cat.title}</h2>
                    </div>
                  </div>
                  <div className="flex flex-col items-end gap-1 shrink-0">
                    <span className={`text-[9px] font-mono tracking-widest px-2 py-0.5 rounded-full border ${a.badge}`}>
                      {cat.subtitle}
                    </span>
                    {cat.popular && (
                      <span className="text-[9px] font-mono tracking-widest px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-400 border border-amber-500/30">
                        POPULER
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-xs text-slate-500 mb-4 leading-relaxed">{cat.description}</p>

                <ul className="flex flex-col gap-2 mb-5">
                  {cat.items.map((item) => (
                    <li key={item.name} className={`rounded-xl px-3.5 py-3 border ${a.tag}`}>
                      <p className="text-xs font-semibold text-white mb-0.5">{item.name}</p>
                      <p className="text-[11px] text-slate-400 leading-relaxed">{item.desc}</p>
                    </li>
                  ))}
                </ul>

                <div className="flex items-center justify-between gap-3 pt-3 border-t border-slate-800">
                  <span className={`text-sm font-semibold ${a.price}`}>{cat.price}</span>
                  <a
                    href={waLink(cat.title)}
                    target="_blank"
                    rel="noopener noreferrer"
                    className={`flex items-center gap-1.5 text-xs font-semibold px-4 py-2 rounded-xl text-white transition-colors ${a.btn}`}
                  >
                    <span>💬</span>
                    <span>Tanya via WhatsApp</span>
                  </a>
                </div>
              </article>
            );
          })}
        </div>

        <div className="mt-6 rounded-2xl p-5 bg-slate-900/40 border border-slate-700/40 text-center">
          <p className="text-slate-400 text-sm mb-3">Punya kebutuhan lain? Ceritain dulu, gratis konsultasi.</p>
          <a
            href={waLink('Proyek Custom')}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 text-sm font-semibold px-5 py-2.5 rounded-xl bg-gradient-to-r from-sky-600 to-emerald-600 hover:from-sky-500 hover:to-emerald-500 text-white transition-all"
          >
            🚀 Diskusi Proyek Custom
          </a>
        </div>

        <footer className="mt-10 text-center text-xs text-slate-700 font-mono">
          zyel autonomous hub // {new Date().getFullYear()}
        </footer>
      </div>
    </main>
  );
}

