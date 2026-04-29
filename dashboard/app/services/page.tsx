// app/services/page.tsx
import CapabilityGrid from "@/components/CapabilityGrid"
import CTASection from "@/components/CTASection"

export default function ServicesPage() {
  return (
    <div className="py-20">
      <div className="container text-center mb-16">
        <h1 className="text-4xl font-bold tracking-tight mb-4">
          What We Offer
        </h1>
        <p className="text-zinc-400 max-w-2xl mx-auto text-lg">
          We engineer custom automation solutions. No templates, no generic
          SaaS. Every engagement starts with an audit and a detailed proposal.
        </p>
      </div>
      <CapabilityGrid />
      <CTASection />
    </div>
  )
}
