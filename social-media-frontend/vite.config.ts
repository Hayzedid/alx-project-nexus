import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true,
  },
  optimizeDeps: {
    noDiscovery: true, // Disable dependency discovery to save disk space
    include: [], // Don't pre-bundle any dependencies
  },
  build: {
    minify: false, // Disable minification to save disk space
  },
});
