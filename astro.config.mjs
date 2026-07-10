import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  site: "https://monomail.millosaurs.me",
  integrations: [sitemap()],
  compressHTML: true,
  build: {
    assets: "_assets",
  },
});
