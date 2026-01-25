import Link from "next/link";

export default function Navbar() {
    return (
        <nav className="flex justify-between items-center px-10 py-6 border-gray-800">
            <h1 className="text-2xl font-bold text-purple-400">SafeChat</h1>

            <div className="space-x-6">
                <Link href="login" className="hover:text-purple-400">Login</Link>
                <Link href="register" className="hover:text-purple-400">Register</Link>
            </div>
        </nav>
    );
}