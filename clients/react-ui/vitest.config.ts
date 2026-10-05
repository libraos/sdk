import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["src/**/*.test.tsx"],
    css: true,
    setupFiles: ["./src/test-setup.ts"],
  },
});
