<script setup lang="ts">
import { FloatButton, App as AntApp } from "ant-design-vue";
import {
  FilePdfOutlined,
  FolderOutlined,
  SettingOutlined,
} from "@ant-design/icons-vue";
// import { VuePDF, usePDF } from "@tato30/vue-pdf";
// // import PDF from "pdf-vue3";
// import { useWebSocket } from "@vueuse/core";

// const { status, data, send, open, close } = useWebSocket(
//   "ws://localhost:8000/control/ws",
//   {
//     autoReconnect: {
//       delay: 3000,
//     },
//     onMessage(ws, event) {
//       console.log(event.data);
//       if (event.data === "page:next") {
//         // page.value += 1;
//         if (page.value < pages.value) {
//           page.value += 1;
//         }
//       }
//       if (event.data === "page:prev") {
//         if (page.value > 1) {
//           page.value -= 1;
//         }
//       }
//       if (event.data === "scale:up") {
//         // scale.value += 0.1;
//         if (scale.value < 2) {
//           scale.value += 0.1;
//         }
//       }
//       if (event.data === "scale:down") {
//         // scale.value -= 0.1;
//         if (scale.value > 0.1) {
//           scale.value -= 0.1;
//         }
//       }
//     },
//   }
// );
// const { pdf, pages } = usePDF("/test.pdf");
// const page = ref(1);
// const scale = ref(1);
</script>

<template>
  <AntApp>
    <div class="app-main">
      <NuxtPage />

      <FloatButton.Group shape="square">
        <FloatButton @click="navigateTo('/')">
          <template #icon>
            <FilePdfOutlined />
          </template>
        </FloatButton>
        <FloatButton @click="navigateTo('/file')">
          <template #icon>
            <FolderOutlined />
          </template>
        </FloatButton>
        <FloatButton @click="navigateTo('/config')">
          <template #icon>
            <SettingOutlined />
          </template>
        </FloatButton>
      </FloatButton.Group>
    </div>
  </AntApp>
</template>

<style>
.app-main {
  width: 100vw;
  height: 100vh;
  overflow: hidden;
  box-sizing: border-box;
}
</style>
