export default function Pitch() {
  return (
    <section className="py-32 px-10 text-center">
      <h2 className="text-5xl font-bold">Built Like a Real Company System</h2>

      <p className="mt-8 text-xl text-gray-300 max-w-4xl mx-auto">
        This platform demonstrates how modern AI systems are deployed in production:
        real-time messaging, distributed microservices, machine learning inference,
        scalable pub/sub systems, and secure authentication — all in one unified application.
      </p>

      <p className="mt-6 text-gray-400">
        Perfect for moderation-heavy platforms like social networks, gaming chats,
        live streams, and enterprise collaboration tools.
      </p>

      <div className="mt-12">
        <a
          href="/register"
          className="px-10 py-4 bg-purple-600 rounded-2xl text-lg hover:bg-purple-700"
        >
          Start Chatting Safely 🚀
        </a>
      </div>
    </section>
  );
}
