import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

declare global {
  var CSS_STYLES: string;
  var CSS_ALIASES: string;
}

const __dirname = dirname(fileURLToPath(import.meta.url));

globalThis.CSS_STYLES = readFileSync(join(__dirname, "src/styles.css"), "utf-8");
globalThis.CSS_ALIASES = readFileSync(join(__dirname, "src/aliases.css"), "utf-8");
