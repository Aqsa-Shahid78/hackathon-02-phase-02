"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/Button";
import { signOut } from "@/lib/auth";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();

  const handleSignOut = async () => {
    try {
      await signOut();
    } catch {
      // Continue even if signout API fails
    }
    router.push("/login");
  };

  return (
    <div className="min-h-screen">
      <nav className="border-b border-gray-200 bg-white">
        <div className="mx-auto flex max-w-4xl items-center justify-between px-4 py-3">
          <h1 className="text-lg font-semibold text-gray-900">Todo App</h1>
          <Button variant="ghost" size="sm" onClick={handleSignOut}>
            Sign Out
          </Button>
        </div>
      </nav>
      <main className="mx-auto max-w-4xl px-4 py-6">{children}</main>
    </div>
  );
}
