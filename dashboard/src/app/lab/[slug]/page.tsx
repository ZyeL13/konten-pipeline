import fs from 'fs';
import path from 'path';
import { compileMDX } from 'next-mdx-remote/rsc';
import Link from 'next/link';

// Komponen yang bisa dipake di dalam MDX (opsional)
const components = {
  a: (props: any) => <a className="text-cyan-400 underline" {...props} />,
  blockquote: (props: any) => (
    <div className="p-4 bg-green-950/10 border border-green-900 my-10 italic text-sm" {...props} />
  ),
  h2: (props: any) => (
    <h2 className="text-xl font-bold text-white border-l-4 border-green-500 pl-4 uppercase italic mt-8 mb-4" {...props} />
  ),
};

// Generate slug statis (buat build time)
export async function generateStaticParams() {
  const postsDirectory = path.join(process.cwd(), 'src/posts');
  const filenames = fs.readdirSync(postsDirectory);
  
  return filenames
    .filter((filename) => filename.endsWith('.mdx'))
    .map((filename) => ({
      slug: filename.replace(/\.mdx$/, ''),
    }));
}

export default async function ArticlePage({ params }: { params: { slug: string } }) {
  const { slug } = await params;
  const filePath = path.join(process.cwd(), 'src/posts', `${slug}.mdx`);
  const source = fs.readFileSync(filePath, 'utf8');
  
  const { content, frontmatter } = await compileMDX({
    source,
    components,
    options: { parseFrontmatter: true },
  });

  const { title, date, status, author } = frontmatter as {
    title: string;
    date: string;
    status: string;
    author: string;
  };

  return (
    <main className="min-h-screen p-6 md:p-20 bg-black text-green-500 font-mono selection:bg-green-500 selection:text-black relative">
      <div className="crt-overlay" />
      
      <div className="max-w-3xl mx-auto relative z-10">
        <Link href="/lab" className="text-[10px] hover:text-white mb-10 inline-block border border-green-900 px-2 py-1">
          &lt;-- KEMBALI KE LAB
        </Link>

        <article>
          <header className="mb-12 border-b border-green-900 pb-8">
            <h1 className="text-3xl md:text-4xl font-black uppercase italic neon-text mb-4 leading-tight">
              {title}
            </h1>
            <div className="flex gap-4 text-[10px] opacity-50 uppercase">
              <span>Author: {author}</span>
              <span>Date: {date}</span>
              <span>Status: {status}</span>
            </div>
          </header>

          <section className="space-y-8 text-sm md:text-base leading-relaxed">
            {content}
          </section>

          <footer className="mt-20 pt-8 border-t border-green-900 opacity-20 text-[10px] flex justify-between">
            <span>FILE_ID: {slug.toUpperCase()}.MDX</span>
            <span>END_OF_TRANSMISSION</span>
          </footer>
        </article>
      </div>
    </main>
  );
}
