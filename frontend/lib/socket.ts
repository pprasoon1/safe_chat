import { io } from "socket.io-client";
import { getToken } from "./auth";

export function createSocket() {
  const token = getToken();

  return io("https://safe-chat-ovd9.onrender.com", {
    path: "/socket.io",
    auth: {
      token,
    },
    transports: ["websocket"],
    withCredentials: true,
  });
}
