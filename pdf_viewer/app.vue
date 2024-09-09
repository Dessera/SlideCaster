<script setup lang="ts">
import { VuePDF, usePDF } from "@tato30/vue-pdf";
// import PDF from "pdf-vue3";
import { useWebSocket } from "@vueuse/core";

const { status, data, send, open, close } = useWebSocket(
  "ws://localhost:8000/control/ws",
  {
    autoReconnect: {
      delay: 3000,
    },
    onMessage(ws, event) {
      console.log(event.data);
      if (event.data === "page:next") {
        // page.value += 1;
        if (page.value < pages.value) {
          page.value += 1;
        }
      }
      if (event.data === "page:prev") {
        if (page.value > 1) {
          page.value -= 1;
        }
      }
      if (event.data === "scale:up") {
        // scale.value += 0.1;
        if (scale.value < 2) {
          scale.value += 0.1;
        }
      }
      if (event.data === "scale:down") {
        // scale.value -= 0.1;
        if (scale.value > 0.1) {
          scale.value -= 0.1;
        }
      }
    },
  }
);
const { pdf, pages } = usePDF(
  "https://mozilla.github.io/pdf.js/web/compressed.tracemonkey-pldi-09.pdf"
);

const page = ref(1);
const scale = ref(1);
</script>

<template>
  <div class="app-main">
    <VuePDF :pdf :page :scale />
  </div>
</template>
