/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // The browser/SSR base URL for the Hermes API (see config/.env.example).
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000",
  },
};

export default nextConfig;
