// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import react from "@astrojs/react";
import tinaDirective from "./astro-tina-directive/register";

import cloudflare from "@astrojs/cloudflare";

// https://astro.build/config
export default defineConfig({
  site: process.env.SITE_URL || "https://alex-gough-2026.albion-dev.workers.dev",
  integrations: [mdx(), sitemap(), react(), tinaDirective()],
  adapter: cloudflare({
    imageService: "passthrough",
  }),
  session: false,
  // Astro 7 defaults to "jsx", which drops whitespace between lines of inline
  // content (e.g. "© 2026Alex Gough" in the footer). Keep the v5 behaviour.
  compressHTML: true,
});
