// Entry point for "The picture that tastes of one ingredient".
// The picture itself is baked into the repository as entry.png, rendered
// locally at build time. At grade time this program simply copies that
// committed image into the output directory the harness provides, using
// only the Node standard library so it runs in a sandbox with no network.
import { copyFileSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL("./entry.png", import.meta.url), join(outDir, "entry.png"));
