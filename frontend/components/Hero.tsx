export default function Hero() {
    return (
        <section className="text-center py-32 px-6">
            <h1 className="text-6xl font-extrabold leading-tight">
                Real-Time Chat <span className="text-purple-400">Moderated By AI</span>
            </h1>
        <p className="mt-6 text-xl text-gray-300 max-w-3xl mx-auto">
            A production-grade real-time messaging platform powered by Machine Learning,
            automatic toxicity detection, live moderation, and scalable microservices architecture.
        </p>

        <div className="mt-10 space-x-6">
        <a href="/register" className="px-8 py-3 g-purple-600 rounded-xl hover:bg-purple-700">
            Get Started
        </a>
        <a href="/chat" className="px-8 py-3 border border-gray-6600 rounded-xl hover:border-purple-400">
            Live Demo
        </a>
        </div>

        </section>
    );
}