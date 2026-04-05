import Link from 'next/link';

export default function ArticlePage() {
  return (
    <main className="min-h-screen p-6 md:p-20 bg-black text-green-500 font-mono selection:bg-green-500 selection:text-black relative">
      {/* Scanline Effect */}
      <div className="crt-overlay" />
      
      <div className="max-w-3xl mx-auto relative z-10">
        <Link href="/" className="text-[10px] hover:text-white mb-10 inline-block border border-green-900 px-2 py-1">
          &lt;-- RETURN_TO_DASHBOARD
        </Link>

        <article>
          <header className="mb-12 border-b border-green-900 pb-8">
            <h1 className="text-3xl md:text-4xl font-black uppercase italic neon-text mb-4 leading-tight">
              [LOG-001]: Membangun OpenClaw — Revolusi Otomatisasi Video
            </h1>
            <div className="flex gap-4 text-[10px] opacity-50 uppercase">
              <span>Author: Zyel</span>
              <span>Date: 2026-04-05</span>
              <span>Status: Published</span>
            </div>
          </header>

          <section className="space-y-8 text-sm md:text-base leading-relaxed">
            <p>
              Di era ekonomi perhatian, kecepatan adalah segalanya. **OpenClaw** lahir sebagai solusi untuk memotong waktu produksi video hingga 90% menggunakan kekuatan <span className="text-cyan-400 underline">Multi-Agent Orchestrator</span>.
            </p>

            <h2 className="text-xl font-bold text-white border-l-4 border-green-500 pl-4 uppercase italic">
              Arsitektur Sang Konduktor AI
            </h2>
            <p>
              Sistem ini tidak bekerja secara linear. Kami membagi beban kerja ke beberapa spesialis:
            </p>
            <ul className="list-disc list-inside space-y-2 ml-4 text-green-400/80">
              <li><span className="text-green-500 font-bold">Script Agent:</span> Riset tren konten.</li>
              <li><span className="text-green-500 font-bold">Visual Agent:</span> Mengatur komposisi video.</li>
              <li><span className="text-green-500 font-bold">QC Agent:</span> Audit hasil render FFmpeg.</li>
            </ul>

            <div className="p-4 bg-green-950/10 border border-green-900 my-10 italic text-sm">
              "Efisiensi bukan tentang bekerja lebih keras, tapi tentang membangun sistem yang bekerja secara otonom di latar belakang."
            </div>

            <h2 className="text-xl font-bold text-white border-l-4 border-green-500 pl-4 uppercase italic">
              Tech Stack: Produksi di Saku
            </h2>
            <p>
              Eksperimen ini membuktikan bahwa ponsel Android dengan **Termux** mampu menjadi studio produksi yang mumpuni. Dengan Python untuk logika dan Next.js untuk monitoring, OpenClaw adalah masa depan otomatisasi mobile.
            </p>
          </section>

          <footer className="mt-20 pt-8 border-t border-green-900 opacity-20 text-[10px] flex justify-between">
            <span>FILE_ID: OC-LOG-001.TSX</span>
            <span>END_OF_TRANSMISSION</span>
          </footer>
        </article>
      </div>
    </main>
  );
}

