export default function MessageBubble({ msg }: any) {
  const isCensored = msg.status === "censored";

  return (
    <div className="bg-gray-800 p-4 rounded-xl max-w-xl">
      <p className="text-sm text-purple-400">{msg.user}</p>

      {isCensored ? (
        <p className="italic text-yellow-400">{msg.moderated_text}</p>
      ) : (
        <p>{msg.message}</p>
      )}

      <div className="mt-2 text-xs text-gray-400">
        Toxicity: {(msg.toxicity * 100).toFixed(1)}%
      </div>
    </div>
  );
}
