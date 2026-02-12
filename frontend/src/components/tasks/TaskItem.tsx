"use client";

import { useState } from "react";
import Link from "next/link";
import { Task } from "@/types";
import { Button } from "@/components/ui/Button";
import { ConfirmDialog } from "@/components/ui/ConfirmDialog";
import { formatDate } from "@/lib/utils";
import { cn } from "@/lib/utils";

interface TaskItemProps {
  task: Task;
  userId: string;
  onToggle: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
}

export function TaskItem({ task, userId, onToggle, onDelete }: TaskItemProps) {
  const [showConfirm, setShowConfirm] = useState(false);
  const [isToggling, setIsToggling] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const handleToggle = async () => {
    setIsToggling(true);
    try {
      await onToggle(task.id);
    } finally {
      setIsToggling(false);
    }
  };

  const handleDelete = async () => {
    setIsDeleting(true);
    try {
      await onDelete(task.id);
    } finally {
      setIsDeleting(false);
      setShowConfirm(false);
    }
  };

  return (
    <>
      <div className="flex items-center gap-3 rounded-lg border border-gray-200 bg-white p-4">
        {/* PATCH - Toggle complete checkbox */}
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={handleToggle}
          disabled={isToggling}
          className="h-5 w-5 shrink-0 cursor-pointer rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          aria-label={`Mark "${task.title}" as ${task.is_completed ? "incomplete" : "complete"}`}
        />

        {/* Task info */}
        <div className="min-w-0 flex-1">
          <p
            className={cn(
              "font-medium",
              task.is_completed ? "text-gray-400 line-through" : "text-gray-900"
            )}
          >
            {task.title}
          </p>
          {task.description && (
            <p className={cn("mt-1 text-sm", task.is_completed ? "text-gray-300" : "text-gray-500")}>
              {task.description}
            </p>
          )}
          <p className="mt-1 text-xs text-gray-400">{formatDate(task.created_at)}</p>
        </div>

        {/* Action buttons */}
        <div className="flex shrink-0 gap-2">
          {/* GET + PUT - Edit page */}
          <Link href={`/dashboard/tasks/${task.id}`}>
            <Button variant="secondary" size="sm">
              Edit
            </Button>
          </Link>

          {/* DELETE */}
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowConfirm(true)}
            disabled={isDeleting}
            className="text-red-500 hover:text-red-700 hover:bg-red-50"
          >
            Delete
          </Button>
        </div>
      </div>
      <ConfirmDialog
        isOpen={showConfirm}
        title="Delete Task"
        message={`Are you sure you want to delete "${task.title}"? This action cannot be undone.`}
        onConfirm={handleDelete}
        onCancel={() => setShowConfirm(false)}
      />
    </>
  );
}
