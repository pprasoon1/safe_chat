import Navbar from "@/components/Navbar";
import Hero from "@/components/Hero";
import Workflow from "@/components/Workflow";
import Features from "@/components/Features";
import Pitch from "@/components/Pitch";

export default function Home() {
  return (
    <main className="bg-gradient-to-b from-black via-gray-900 to-black text-white moin-h-screen">
      <Navbar />
      <Hero />
      <Workflow />
      <Features />
      <Pitch />
      </main>
  )
}