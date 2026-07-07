import { defineConfig } from "astro/config";
import vercel from "@astrojs/vercel";

// https://astro.build/config
export default defineConfig({
  site: "https://monomail.millosaurs.me",
  compressHTML: true,
  build: {
    assets: "_assets",
  },
  output: "static",
  adapter: vercel({
    webAnalytics: {
      enabled: true,
    },
  }),
});
