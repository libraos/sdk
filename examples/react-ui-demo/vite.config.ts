import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
// @libraos/react-ui is linked with file:, so it resolves react from clients/react-ui/node_modules;
// dedupe makes the kit and the app share one React (two copies throw "reading 'useRef'" at runtime).
export default defineConfig({ plugins: [react()], resolve: { dedupe: ["react", "react-dom"] } });
