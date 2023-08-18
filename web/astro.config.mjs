import { defineConfig } from 'astro/config';
import tailwind from "@astrojs/tailwind";
import solidJs from "@astrojs/solid-js";

import vue from "@astrojs/vue";

// https://astro.build/config
export default defineConfig({
  output: 'server',
  integrations: [tailwind(), solidJs(), vue()]
});