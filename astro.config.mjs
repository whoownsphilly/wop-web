import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import solidJs from "@astrojs/solid-js";
import vue from "@astrojs/vue";

import vercel from "@astrojs/vercel/serverless";

// https://astro.build/config
export default defineConfig({
  output: 'server',
  server: {
    port: Number(import.meta.env.WEB_PORT||4321),
    host: true
  },
  adapter: vercel(),
  integrations: [tailwind(), solidJs(), vue()]
});
