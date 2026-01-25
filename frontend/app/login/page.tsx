"use client";

import { useState } from "react";
import { saveToken } from "@/lib/auth";
import { useRouter } from "next/navigation";

export default function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const router = useRouter();

    async function handleLogin(e: any) {
        e.preventDefault()

        const res = await fetch("https://safe-chat-ovd9.onrender.com/auth/login", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({email, password})
        });

        const data = await res.json();

        if (data.access_token) {
            saveToken(data.access_token);
            router.push("/chat")
        } else {
            alert("Login failed");
        }
    }

    return (
        <div className="min-h-screen flex items-center justify-center bg-black text-white">
            <form onSubmit={handleLogin} className="bg-gray-900 p-10 rounded-xl w-96">
                <h2 className="text-2xl font-bold mb-6">Login</h2>

                <input
                className="w-full p-3 mb-4 bg-gray-800 rounded"
                placeholder="Email"
                onChange={e => setEmail(e.target.value)}
                />

                <input 
                type="password"
                className="w-full p-3 mb-6 g-gray-800 rounded"
                placeholder="Password"
                onChange={e => setPassword(e.target.value)}
                />

                <button className="w-full bg-purple-600 p-3 rounded hover:bg-purple-700">
                    Login
                </button>
            </form>

        </div>
    );
}