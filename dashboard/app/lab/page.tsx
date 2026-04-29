// app/lab/page.tsx
import { allProjects } from "@/lib/projects"
import CaseStudyCard from "@/components/CaseStudyCard"

export default function LabPage() {
  return (
    <div className="container py-20">
      <h1 className="text-4xl font-bold tracking-tight mb-4">The Lab</h1>
      <p className="text-zinc-400 max-w-2xl mb-12">
        Deep dives into systems we've engineered. Technical breakdowns,
        architecture decisions, and real-world results.
      </p>
      <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
        {allProjects.map((project) => (
          <CaseStudyCard key={project.slug} {...project} />
        ))}
      </div>
    </div>
  )
}
