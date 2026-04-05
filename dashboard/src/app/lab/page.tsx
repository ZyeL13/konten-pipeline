import Link from 'next/link';
import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

export default async function LabPage() {
  const postsDirectory = path.join(process.cwd(), 'src/posts');
  const filenames = fs.readdirSync(postsDirectory);
  
  const posts = filenames
    .filter((filename) => filename.endsWith('.mdx'))
    .map((filename) => {
      const filePath = path.join(postsDirectory, filename);
      const fileContent = fs.readFileSync(filePath, 'utf8');
      const { data } = matter(fileContent);
      const slug = filename.replace(/\.mdx$/, '');
      
      return {
        slug,
        title: data.title,
        date: data.date,
        status: data.status,
        excerpt: data.excerpt || data.title,
      };
    })
    .sort((a, b) => (a.date < b.date ? 1 : -1));

  return (
    <main className="min-h-screen p-6 md:p-20 bg-black text-green-500 font-mono">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-3xl font-black uppercase italic neon-text mb-8">
          /LAB — ARTICLES
        </h1>
        
        <div className="space-y-4">
          {posts.map((post) => (
            <Link
              key={post.slug}
              href={`/lab/${post.slug}`}
              className="block border border-green-900 p-4 hover:bg-green-950/20 transition-colors"
            >
              <div className="flex justify-between items-start">
                <div>
                  <h2 className="text-lg font-bold text-white">{post.title}</h2>
                  <p className="text-xs opacity-50 mt-1">{post.excerpt}</p>
                </div>
                <div className="text-right text-[10px] opacity-50">
                  <div>{post.date}</div>
                  <div>{post.status}</div>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  );
}
