export interface User {
  id: string;
  email: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  user: User;
  access_token: string;
}

export interface ApiError {
  error: {
    code: string;
    message: string;
    details: unknown[] | null;
  };
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}
