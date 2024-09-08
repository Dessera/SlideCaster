<script setup lang="ts">
// import { VuePDF, usePDF } from "@tato30/vue-pdf";
import PDF from "pdf-vue3";
import { useWebSocket } from "@vueuse/core";

const { status, data, send, open, close } = useWebSocket(
  "ws://localhost:8000/control/ws",
  {
    autoReconnect: {
      delay: 1000,
    },
    onMessage(ws, event) {
      console.log(event.data);
      if (event.data === "page_up") {
        page.value += 1;
      }
    },
  }
);

const page = ref(1);
</script>

<template>
  <div class="app-main">
    <!-- <VuePDF :pdf="pdf" fit-parent /> -->
    <PDF
      src="https://mozilla.github.io/pdf.js/web/compressed.tracemonkey-pldi-09.pdf"
      :page="page"
    />
  </div>
</template>

<style scoped>
/* .app-main {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  box-sizing: border-box;
} */
</style>
