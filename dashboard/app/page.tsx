import Hero from "@/components/Hero"
import CapabilityGrid from "@/components/CapabilityGrid"
import CaseStudyCard from "@/components/CaseStudyCard"
import ProcessTimeline from "@/components/ProcessTimeline"
import CTASection from "@/components/CTASection"
import { featuredProjects } from "@/lib/projects"

export default function Home() {
  return (
    <>
      <Hero />
      <CapabilityGrid />
      <section className="py-20 border-t border-zinc-800">
        <div className="container">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl mb-4">
            Featured Labs
          </h2>
          <p className="text-zinc-400 mb-12 max-w-2xl">
            Technical breakdown dari system yang udah gue build. Real projects,
            real code, real results.
          </p>
          <div className="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
            {featuredProjects.map((project) => (
              <CaseStudyCard key={project.slug} {...project} />
            ))}
          </div>
        </div>
      </section>
      <ProcessTimeline />
      <CTASection />
    </>
  )
}
