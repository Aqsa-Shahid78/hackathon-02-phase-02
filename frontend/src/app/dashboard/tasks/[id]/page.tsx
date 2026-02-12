"use client";

import { useEffect, useState } from "react";
import { useRouter, useParams } from "next/navigation";
import { Task } from "@/types";
import { apiFetch, ApiError } from "@/lib/api";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { Card } from "@/components/ui/Card";

export default function TaskDetailPage() {
  const router = useRouter();
  const params = useParams();
  const taskId = params.id as string;

  const [task, setTask] = useState<Task | null>(null);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    const fetchTask = async () => {
      const userId = localStorage.getItem("user_id");
      if (!userId) {
        router.push("/login");
        return;
      }

      try {
        const data = await apiFetch<Task>(`/users/${userId}/tasks/${taskId}`);
        setTask(data);
        setTitle(data.title);
        setDescription(data.description || "");
      } catch (err) {
        if (err instanceof ApiError && err.status === 404) {
          setError("Task not found");
        } else if (err instanceof ApiError && err.status === 401) {
          router.push("/login");
        } else {
          setError("Failed to load task");
        }
      } finally {
        setIsLoading(false);
      }
    };
    fetchTask();
  }, [taskId, router]);

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsSaving(true);

    const userId = localStorage.getItem("user_id");
    if (!userId) return;

    try {
      const updated = await apiFetch<Task>(`/users/${userId}/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify({
          title: title.trim(),
          description: description.trim() || null,
        }),
      });
      setTask(updated);
      setSuccess("Task updated successfully");
      setTimeout(() => setSuccess(""), 3000);
    } catch (err) {
      if (err instanceof ApiError) {
        setError(err.message);
      } else {
        setError("Failed to update task");
      }
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading) {
    return (
      <div className="space-y-4">
        <div className="h-8 w-32 animate-pulse rounded bg-gray-200" />
        <div className="h-64 animate-pulse rounded-lg bg-gray-200" />
      </div>
    );
  }

  if (!task) {
    return (
      <div className="py-12 text-center">
        <p className="text-lg text-gray-500">{error || "Task not found"}</p>
        <Button variant="secondary" className="mt-4" onClick={() => router.push("/dashboard")}>
          Back to Dashboard
        </Button>
      </div>
    );
  }

  return (
    <div>
      <button
        onClick={() => router.push("/dashboard")}
        className="mb-4 text-sm text-blue-600 hover:underline"
      >
        &larr; Back to Dashboard
      </button>
      <Card>
        <h2 className="mb-4 text-lg font-semibold text-gray-900">Edit Task</h2>
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">{error}</div>
        )}
        {success && (
          <div className="mb-4 rounded-md bg-green-50 p-3 text-sm text-green-700">{success}</div>
        )}
        <form onSubmit={handleSave} className="space-y-4">
          <Input
            id="title"
            label="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            required
            maxLength={255}
          />
          <div className="w-full">
            <label htmlFor="description" className="mb-1 block text-sm font-medium text-gray-700">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              maxLength={2000}
              rows={4}
              className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm shadow-sm transition-colors focus:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="flex gap-3">
            <Button type="submit" isLoading={isSaving}>
              Save Changes
            </Button>
            <Button type="button" variant="secondary" onClick={() => router.push("/dashboard")}>
              Cancel
            </Button>
          </div>
        </form>
      </Card>
    </div>
  );
}
