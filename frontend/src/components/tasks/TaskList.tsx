"use client";

import { Task } from "@/types";
import { TaskItem } from "@/components/tasks/TaskItem";

interface TaskListProps {
  tasks: Task[];
  userId: string;
  onToggle: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
}

export function TaskList({ tasks, userId, onToggle, onDelete }: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="py-12 text-center">
        <p className="text-lg text-gray-500">No tasks yet</p>
        <p className="mt-1 text-sm text-gray-400">Create your first task above to get started.</p>
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          userId={userId}
          onToggle={onToggle}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
}
