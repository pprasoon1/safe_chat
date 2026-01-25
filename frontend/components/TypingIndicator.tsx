interface Props {
  users: string[];
}

export default function TypingIndicator({ users }: Props) {
  if (users.length === 0) return null;

  return (
    <div className="px-6 py-2 text-sm text-gray-400">
      {users.join(", ")} typing...
    </div>
  );
}
