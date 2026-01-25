import {io} from "socket.io-client";
import {getToken} from "./auth"

export function createSocket() {
    const token = getToken();

    return io("http://localhost:8000", {
        auth: {
            token
        },
        transports: ["websocket"],
    });
}