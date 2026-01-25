import { io } from "socket.io-client";
import { getToken } from "./auth";

const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL;

export function createSocket() {
  const token = getToken();

  return io(SOCKET_URL, {
    path: "/socket.io",
    auth: {
      token,
    },
    transports: ["websocket"],
    withCredentials: true,
  });
}
