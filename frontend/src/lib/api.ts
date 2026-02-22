const API_URL = process.env.NEXT_PUBLIC_API_URL!;

interface FetchOptions extends RequestInit {
  skipAuth?: boolean;
}

export class ApiError extends Error {
  code: string;
  status: number;
  details: unknown[] | null;

  constructor(code: string, message: string, status: number, details: unknown[] | null = null) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

export async function apiFetch<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { skipAuth, ...fetchOptions } = options;

  const res = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...fetchOptions.headers,
    },
  });

  if (res.status === 401 && !skipAuth) {
    if (typeof window !== "undefined") {
      window.location.href = "/login";
    }
    throw new ApiError("UNAUTHORIZED", "Not authenticated", 401);
  }

  if (res.status === 204) {
    return undefined as T;
  }

  const data = await res.json();

  if (!res.ok) {
    const error = data.error || { code: "UNKNOWN", message: "An error occurred", details: null };
    throw new ApiError(error.code, error.message, res.status, error.details);
  }

  return data as T;
}
