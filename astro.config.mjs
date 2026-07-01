import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
  site: "https://monomail.millosaurs.me",
  compressHTML: true,
  build: {
    assets: "_assets",
  },
});
