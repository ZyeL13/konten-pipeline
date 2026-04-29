// app/lab/[slug]/page.tsx
import { notFound } from "next/navigation"
import { allProjects } from "@/lib/projects"
import { Badge } from "@/components/ui/badge"
import { Card, CardContent } from "@/components/ui/card"

export function generateStaticParams() {
  return allProjects.map((p) => ({ slug: p.slug }))
}

export default function LabDetailPage({
  params,
}: {
  params: { slug: string }
}) {
  const project = allProjects.find((p) => p.slug === params.slug)
  if (!project) notFound()

  return (
    <div className="container py-20 max-w-4xl">
      <h1 className="text-4xl font-bold tracking-tight mb-4">
        {project.title}
      </h1>
      <p className="text-lg text-zinc-400 mb-8">{project.description}</p>

      <div className="flex flex-wrap gap-2 mb-12">
        {project.stack.map((tech) => (
          <Badge
            key={tech}
            variant="secondary"
            className="bg-zinc-800 text-zinc-300"
          >
            {tech}
          </Badge>
        ))}
      </div>

      <div className="grid md:grid-cols-2 gap-8 mb-16">
        <Card className="bg-zinc-900 border-zinc-800">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-red-400 mb-2">Problem</h3>
            <p className="text-zinc-400">{project.problem}</p>
          </CardContent>
        </Card>
        <Card className="bg-zinc-900 border-zinc-800">
          <CardContent className="p-6">
            <h3 className="text-lg font-semibold text-cyan-400 mb-2">
              Solution
            </h3>
            <p className="text-zinc-400">{project.solution}</p>
          </CardContent>
        </Card>
      </div>

      {project.architecture && (
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-4">System Architecture</h2>
          <div className="bg-zinc-900 border border-zinc-800 rounded-lg p-6 font-mono text-sm text-zinc-300 overflow-x-auto">
            <div className="flex flex-wrap items-center gap-2">
              {project.architecture.split(" → ").map((block, i, arr) => (
                <span key={i} className="flex items-center gap-2">
                  <span className="bg-zinc-800 px-2 py-1 rounded text-cyan-400">
                    {block}
                  </span>
                  {i < arr.length - 1 && (
                    <span className="text-zinc-600">→</span>
                  )}
                </span>
              ))}
            </div>
          </div>
        </div>
      )}

      {project.metrics && project.metrics.length > 0 && (
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-4">Key Metrics</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {project.metrics.map((m) => (
              <Card key={m.label} className="bg-zinc-900 border-zinc-800">
                <CardContent className="p-6 text-center">
                  <div className="text-3xl font-bold text-cyan-400">
                    {m.value}
                  </div>
                  <div className="text-sm text-zinc-500 mt-1">{m.label}</div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}

      {project.screenshots && project.screenshots.length > 0 && (
        <div className="mb-16">
          <h2 className="text-2xl font-bold mb-4">Screenshots</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {project.screenshots.map((src, idx) => (
              <img
                key={idx}
                src={src}
                alt={`${project.title} screenshot ${idx + 1}`}
                className="rounded-lg border border-zinc-800"
              />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
