import { apiFetch } from "@/lib/api";
import { AuthResponse } from "@/types";

export async function signUp(email: string, password: string): Promise<AuthResponse> {
  const res = await apiFetch<AuthResponse>("/auth/signup", {
    method: "POST",
    body: JSON.stringify({ email, password }),
    skipAuth: true,
  });
  if (typeof window !== "undefined") {
    localStorage.setItem("user_id", res.user.id);
    localStorage.setItem("user_email", res.user.email);
  }
  return res;
}

export async function signIn(email: string, password: string): Promise<AuthResponse> {
  const res = await apiFetch<AuthResponse>("/auth/signin", {
    method: "POST",
    body: JSON.stringify({ email, password }),
    skipAuth: true,
  });
  if (typeof window !== "undefined") {
    localStorage.setItem("user_id", res.user.id);
    localStorage.setItem("user_email", res.user.email);
  }
  return res;
}

export async function signOut(): Promise<void> {
  await apiFetch("/auth/signout", { method: "POST" });
  if (typeof window !== "undefined") {
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
  }
}
