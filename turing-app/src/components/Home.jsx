import { useAuth } from "@/context/AuthContext";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  return (
    <>
      <button
        className="group/btn shadow-input relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_#262626]"
        onClick={logout}
      >
        <span className="text-sm text-neutral-700 dark:text-neutral-300">Logout</span>
      </button>
      <div className="max-w-xl mx-auto mt-8 p-4 bg-white dark:bg-zinc-900 rounded shadow text-center">
        <h2 className="text-lg font-bold mb-2">Welcome to the Home Page!</h2>
        <p className="text-neutral-700 dark:text-neutral-300">Use the navigation to access the chat.</p>
        <button
          className="mt-4 px-6 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
          onClick={() => navigate('/chat')}
        >
          Go to Chat
        </button>
      </div>
    </>
  );
}
