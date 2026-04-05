// src/app/page.tsx
import Terminal from '@/components/Terminal';
import StatusCard from '@/components/StatusCard';
import VideoGrid from '@/components/VideoGrid';
import Link from 'next/link';

export default function Dashboard() {
  const labLogs = [
    "[INIT]: OpenClaw Lab Neural Link established...",
    "[LOG-001]: Membangun arsitektur Multi-Agent...",
    "[SEO]: Menerbitkan artikel 'Revolusi Otomatisasi Video'...",
    "[DATA]: Menghubungkan riset AI x Crypto...",
    "[SYS]: Menunggu feedback dari Google AdSense..."
  ];

  return (
    <main className="min-h-screen p-4 md:p-10 relative">
      <div className="crt-overlay" />
      {/* ... header tetap sama ... */}
      
      {/* Update pada Terminal Section */}
      <div className="xl:col-span-7">
        <div className="flex justify-between items-center mb-3">
          <h2 className="text-xs font-bold tracking-widest text-green-800 uppercase">Lab_Journal_v1</h2>
          <Link href="/lab/membangun-openclaw-ai" className="text-[9px] text-cyan-400 underline">BACA_RILIS_TERBARU</Link>
        </div>
        <Terminal logs={labLogs} />
      </div>
      
      {/* ... sisa kode tetap sama ... */}
    </main>
  );
}

