import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import solidJs from "@astrojs/solid-js";

import vue from "@astrojs/vue";

// https://astro.build/config
export default defineConfig({
  output: 'server',
  server: { port: import.meta.env.PUBLIC_YARN_PORT, host: true },
  integrations: [tailwind(), solidJs(), vue()]
});
