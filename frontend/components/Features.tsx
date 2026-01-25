export default function Features() {
  const features = [
    {
      title: "Real-Time ML Moderation",
      desc: "Every message is classified by a custom NLP model before delivery."
    },
    {
      title: "Microservices Architecture",
      desc: "Independent ML and Chat services for scalability and fault isolation."
    },
    {
      title: "Redis-Powered Pub/Sub",
      desc: "Scalable broadcasting, typing indicators, and online presence tracking."
    },
    {
      title: "JWT Secured WebSockets",
      desc: "Authentication & authorization built directly into the real-time layer."
    },
    {
      title: "Live Toxicity Meter",
      desc: "Visual feedback that encourages respectful communication."
    },
    {
      title: "Auto-Moderation Engine",
      desc: "Approve, censor, or block messages automatically using AI."
    }
  ];

  return (
    <section className="py-24 px-10 bg-gray-950">
      <h2 className="text-4xl font-bold text-center mb-12">Why This Is Powerful</h2>

      <div className="grid md:grid-cols-3 gap-10">
        {features.map((f, i) => (
          <div
            key={i}
            className="p-8 bg-gray-800 rounded-xl hover:border-purple-400 border border-transparent transition"
          >
            <h3 className="text-xl font-semibold text-purple-400">{f.title}</h3>
            <p className="mt-4 text-gray-300">{f.desc}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
