// src/app/lab/membangun-openclaw-ai/page.tsx
import Link from 'next/link';

export default function ArticlePage() {
  return (
    <main className="min-h-screen p-6 md:p-20 bg-black text-green-500 font-mono selection:bg-green-500 selection:text-black">
      <div className="crt-overlay" />
      
      <Link href="/" className="text-xs hover:underline mb-10 inline-block">
        &lt;-- KEMBALI_KE_DASHBOARD
      </Link>

      <article className="max-w-3xl mx-auto">
        <header className="mb-12 border-b border-green-900 pb-6">
          <h1 className="text-3xl font-black uppercase italic neon-text mb-4">
            [LOG-001]: Membangun OpenClaw — Revolusi Otomatisasi Video
          </h1>
          <p className="text-xs opacity-50">DITERBITKAN: 2026-04-05 // KATEGORI: AI_AUTOMATION</p>
        </header>

        <section className="space-y-6 leading-relaxed text-sm md:text-base">
          <p>
            Membuat satu video berkualitas membutuhkan waktu berjam-jam. 
            <span className="font-bold"> OpenClaw</span> hadir sebagai solusi menggunakan kekuatan Multi-Agent Orchestrator.
          </p>
          
          <h2 className="text-xl font-bold border-l-4 border-green-500 pl-4 my-8">ARSITEKTUR MULTI-AGENT</h2>
          <p>
            Di dalam OpenClaw, agen bekerja secara otonom: <br/>
            - <span className="text-white">Script Agent:</span> Riset tren. <br/>
            - <span className="text-white">Visual Agent:</span> Komposisi gambar. <br/>
            - <span className="text-white">QC Agent:</span> Audit audit visual.
          </p>

          <blockquote className="bg-green-950/20 p-4 border-l-2 border-green-900 italic">
            "Efisiensi bukan tentang bekerja lebih keras, tapi tentang membangun sistem yang bekerja untuk Anda."
          </blockquote>
        </section>

        <footer className="mt-20 opacity-30 text-[10px]">
          END_OF_FILE // STAMP: {new Date().toISOString()}
        </footer>
      </article>
    </main>
  );
}

