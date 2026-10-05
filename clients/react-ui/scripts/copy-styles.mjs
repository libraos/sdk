import { copyFileSync } from "node:fs";
copyFileSync("src/styles.css", "dist/styles.css");
copyFileSync("src/aliases.css", "dist/aliases.css");
