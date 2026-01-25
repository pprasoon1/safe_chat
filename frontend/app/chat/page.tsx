"use client";

import { useEffect, useState } from "react";
import { createSocket } from "@/lib/socket";
import ToxicityMeter from "@/components/ToxicityMeter";
import MessageBubble from "@/components/MessageBubble";
import TypingIndicator from "@/components/TypingIndicator";

export default function Chat() {
  const [socket, setSocket] = useState<any>(null);

  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState("");
  const [toxicity, setToxicity] = useState(0);

  const [typingUsers, setTypingUsers] = useState<string[]>([]);
  const [onlineUsers, setOnlineUsers] = useState<string[]>([]);

  const [currentRoom, setCurrentRoom] = useState("global");
  const [privateTarget, setPrivateTarget] = useState("");

  // -------------------------------------------------
  // 🔐 CONNECT SOCKET
  // -------------------------------------------------
  useEffect(() => {
    const s = createSocket();
    setSocket(s);

    s.on("connect", () => {
      console.log("🟢 Connected to socket");
      s.emit("join_room", { room: "global" });
    });

    s.on("new_message", (msg: any) => {
      setMessages(prev => [...prev, msg]);
    });

    s.on("moderation_notice", (data: any) => {
      alert(data.message);
      setToxicity(data.toxicity);
    });

    s.on("toxicity_update", (data: any) => {
      setToxicity(data.toxicity);
    });

    s.on("typing", (data: any) => {
      setTypingUsers(prev => [...new Set([...prev, data.user])]);

      setTimeout(() => {
        setTypingUsers(prev => prev.filter(u => u !== data.user));
      }, 2000);
    });

    s.on("online_users", (users: string[]) => {
      setOnlineUsers(users);
    });

    s.on("system", (data: any) => {
      setMessages(prev => [
        ...prev,
        { system: true, message: data.message }
      ]);
    });

    s.on("private_room_created", (data: any) => {
      setCurrentRoom(data.room);
      setMessages([]);
      s.emit("join_room", { room: data.room });
    });

    return () => {
      s.disconnect();
    };
  }, []);

  // -------------------------------------------------
  // 💬 SEND MESSAGE
  // -------------------------------------------------
  function sendMessage() {
    if (!input || !socket) return;

    socket.emit("chat_message", {
      room: currentRoom,
      message: input,
      chat_id: 1
    });

    setInput("");
  }

  // -------------------------------------------------
  // ✍️ TYPING
  // -------------------------------------------------
  function handleTyping() {
    if (socket) {
      socket.emit("typing", { room: currentRoom });
    }
  }

  // -------------------------------------------------
  // 🔐 START PRIVATE CHAT
  // -------------------------------------------------
  function startPrivateChat() {
    if (!privateTarget || !socket) return;

    socket.emit("start_private_chat", {
      target_user: privateTarget
    });

    setPrivateTarget("");
  }

  // -------------------------------------------------
  // 🌍 SWITCH TO GLOBAL
  // -------------------------------------------------
  function switchToGlobal() {
    if (!socket) return;

    socket.emit("leave_room", { room: currentRoom });
    socket.emit("join_room", { room: "global" });

    setCurrentRoom("global");
    setMessages([]);
  }

  // -------------------------------------------------
  // 🖥️ UI
  // -------------------------------------------------
  return (
    <div className="flex h-screen bg-black text-white">

      {/* 🟢 ONLINE USERS + PRIVATE CHAT */}
      <div className="w-72 bg-gray-900 p-4 border-r border-gray-800 flex flex-col">

        <h3 className="font-bold mb-4 text-purple-400">Online Users</h3>

        <div className="flex-1 overflow-y-auto space-y-2">
          {onlineUsers.map((u, i) => (
            <div key={i} className="text-green-400">● {u}</div>
          ))}
        </div>

        <div className="mt-6">
          <h4 className="font-semibold mb-2">Start Private Chat</h4>

          <input
            className="w-full p-2 mb-2 bg-gray-800 rounded"
            placeholder="Enter user email"
            value={privateTarget}
            onChange={e => setPrivateTarget(e.target.value)}
          />

          <button
            onClick={startPrivateChat}
            className="w-full bg-purple-600 py-2 rounded hover:bg-purple-700"
          >
            Start Private Chat 🔐
          </button>

          <button
            onClick={switchToGlobal}
            className="w-full mt-3 border border-gray-600 py-2 rounded hover:border-purple-400"
          >
            Back to Global 🌍
          </button>
        </div>
      </div>

      {/* 💬 CHAT AREA */}
      <div className="flex-1 flex flex-col">

        <div className="p-4 border-b border-gray-800">
          Current Room: <span className="text-purple-400">{currentRoom}</span>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {messages.map((msg, i) =>
            msg.system ? (
              <div key={i} className="text-center text-gray-500 italic">
                {msg.message}
              </div>
            ) : (
              <MessageBubble key={i} msg={msg} />
            )
          )}
        </div>

        <TypingIndicator users={typingUsers} />

        <div className="p-4 border-t border-gray-800">
          <input
            className="w-full p-3 bg-gray-800 rounded"
            placeholder={`Message in ${currentRoom}...`}
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleTyping}
          />

          <ToxicityMeter value={toxicity} />

          <button
            onClick={sendMessage}
            className="mt-3 bg-purple-600 px-6 py-2 rounded hover:bg-purple-700"
          >
            Send 🚀
          </button>
        </div>
      </div>
    </div>
  );
}
