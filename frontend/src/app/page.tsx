import { redirect } from "next/navigation";
import { cookies } from "next/headers";

export default async function Home() {
  let hasToken = false;
  try {
    const cookieStore = await cookies();
    const token = cookieStore.get("access_token");
    hasToken = !!token;
  } catch {
    // If cookies() fails, redirect to login
  }

  if (hasToken) {
    redirect("/dashboard");
  } else {
    redirect("/login");
  }
}
