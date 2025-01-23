import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ["lucide-react"],
  },
  define: {
    __APP_VERSION__: JSON.stringify(process.env.npm_package_version),
  },
  envDir: "./..env",
  envPrefix: "INNALYZE_",
  server: {
    host: "0.0.0.0",
    port: parseInt(process.env.INNALYZE_FRONT_PORT ?? "") || undefined,
    proxy: {
      "/api": {
        ws: true,
        changeOrigin: true,
        target: process.env.INNALYZE_SERVER_URL,
        secure: false,
      },
    },
    cors: {
      credentials: true,
    },
  },
  preview: {
    host: "0.0.0.0",
    port: parseInt(process.env.INNALYZE_FRONT_PORT ?? "") || undefined,
  },
});
