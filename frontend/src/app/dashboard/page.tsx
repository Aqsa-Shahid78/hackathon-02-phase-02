"use client";

import { useEffect, useState, useCallback } from "react";
import { useRouter } from "next/navigation";
import { Task } from "@/types";
import { apiFetch, ApiError } from "@/lib/api";
import { TaskForm } from "@/components/forms/TaskForm";
import { TaskList } from "@/components/tasks/TaskList";
import { Card } from "@/components/ui/Card";

export default function DashboardPage() {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [userId, setUserId] = useState<string>("");
  const [isLoading, setIsLoading] = useState(true);

  const fetchTasks = useCallback(async (uid: string) => {
    try {
      const data = await apiFetch<{ tasks: Task[]; total: number }>(`/users/${uid}/tasks`);
      setTasks(data.tasks);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        router.push("/login");
      }
    }
  }, [router]);

  useEffect(() => {
    const init = async () => {
      try {
        // Get current user info by attempting to fetch tasks
        // First we need the user ID from the auth response stored in a cookie
        // Since we use httpOnly cookies, we get user info from the signup/signin response
        // For now, decode from a /auth/me-like approach or store in localStorage
        const storedUserId = localStorage.getItem("user_id");
        if (!storedUserId) {
          router.push("/login");
          return;
        }
        setUserId(storedUserId);
        await fetchTasks(storedUserId);
      } catch {
        router.push("/login");
      } finally {
        setIsLoading(false);
      }
    };
    init();
  }, [fetchTasks, router]);

  const handleCreateTask = async (title: string, description: string) => {
    const task = await apiFetch<Task>(`/users/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify({ title, description: description || null }),
    });
    setTasks((prev) => [task, ...prev]);
  };

  const handleToggle = async (taskId: string) => {
    const updated = await apiFetch<Task>(`/users/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
    setTasks((prev) => prev.map((t) => (t.id === taskId ? updated : t)));
  };

  const handleDelete = async (taskId: string) => {
    await apiFetch(`/users/${userId}/tasks/${taskId}`, { method: "DELETE" });
    setTasks((prev) => prev.filter((t) => t.id !== taskId));
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="h-32 animate-pulse rounded-lg bg-gray-200" />
        <div className="h-16 animate-pulse rounded-lg bg-gray-200" />
        <div className="h-16 animate-pulse rounded-lg bg-gray-200" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <Card>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">New Task</h2>
        <TaskForm onSubmit={handleCreateTask} />
      </Card>
      <div>
        <h2 className="mb-3 text-lg font-semibold text-gray-900">Your Tasks</h2>
        <TaskList tasks={tasks} userId={userId} onToggle={handleToggle} onDelete={handleDelete} />
      </div>
    </div>
  );
}
