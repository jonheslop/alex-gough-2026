// @ts-check
import { defineConfig } from "astro/config";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import react from "@astrojs/react";
import tinaDirective from "./astro-tina-directive/register";

import cloudflare from "@astrojs/cloudflare";

// https://astro.build/config
export default defineConfig({
  site: process.env.SITE_URL,
  integrations: [mdx(), sitemap(), react(), tinaDirective()],
  adapter: cloudflare(),
});