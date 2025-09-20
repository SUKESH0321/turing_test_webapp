import React from "react";
import { useAuth } from "@/context/AuthContext";

export default function Home() {
  const { user,logout } = useAuth();
  console.log("from home ");
  console.log(user);
  return (


    <>
     <button
            className="group/btn shadow-input relative flex h-10 w-full items-center justify-start space-x-2 rounded-md bg-gray-50 px-4 font-medium text-black dark:bg-zinc-900 dark:shadow-[0px_0px_1px_1px_#262626]"
      onClick={logout} >
             <span className="text-sm text-neutral-700 dark:text-neutral-300">
              Logout
            </span>
            
          </button>
   
    </>
  );
}
