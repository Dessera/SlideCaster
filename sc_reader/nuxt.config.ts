// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: "2024-04-03",
  modules: ["@nuxtjs/tailwindcss"],
  devtools: { enabled: true },
  ssr: false,

  runtimeConfig: {
    public: {
      appBaseURL: "http://127.0.0.1:8000",
    },
  },
});
