export default function Workflow() {
  const steps = [
    "User sends message",
    "JWT authenticated WebSocket",
    "FastAPI Chat Gateway",
    "ML Toxicity Classifier",
    "Auto Moderation Engine",
    "Redis Pub/Sub Broadcast",
    "Safe message delivered"
  ];

  return (
    <section className="py-24 px-10">
      <h2 className="text-4xl font-bold text-center mb-12">How It Works</h2>

      <div className="grid md:grid-cols-4 gap-8 text-center">
        {steps.map((step, i) => (
          <div
            key={i}
            className="p-6 bg-gray-800 rounded-xl hover:scale-105 transition"
          >
            <span className="text-purple-400 font-bold">Step {i + 1}</span>
            <p className="mt-4 text-gray-300">{step}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
