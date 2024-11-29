<script setup lang="ts">
import {
  Flex,
  Result,
  FloatButtonGroup,
  FloatButton,
  Spin,
  App,
} from "ant-design-vue";
import {
  UpOutlined,
  DownOutlined,
  FullscreenOutlined,
  FullscreenExitOutlined,
  DoubleLeftOutlined,
  DoubleRightOutlined,
} from "@ant-design/icons-vue";
import { useFileList, useGetFileURL } from "~/api/file";
import { useControlWebsocket } from "~/api/control";
import { usePDF, VuePDF } from "@tato30/vue-pdf";

const { message } = App.useApp();

const getFileURL = useGetFileURL();

const { data: files, isError, isFetching } = useFileList();
const currentIndex = ref(0);
const currentFile = computed(() => {
  if (files.value && files.value.length > 0) {
    if (currentIndex.value < 0 || currentIndex.value >= files.value.length) {
      return null;
    }
    const file = files.value[currentIndex.value];
    return getFileURL(file);
  }
  return null;
});

const currentPage = ref(1);
const currentScale = ref(1);

const { pdf, pages } = usePDF(currentFile);

// lazy implementation, but it works :)
// I don't want to refactor this because it's just for display

const handleNextPage = () => {
  // cycle next page
  currentPage.value = (currentPage.value % pages.value) + 1;
};

const handlePrevPage = () => {
  // cycle prev page
  currentPage.value = currentPage.value - 1 || pages.value;
};

const handleZoomIn = () => {
  currentScale.value = currentScale.value + 0.1;
};

const handleZoomOut = () => {
  currentScale.value = currentScale.value - 0.1;
};

const handleNextFile = () => {
  if (!files.value) return;
  currentIndex.value = (currentIndex.value + 1) % files.value.length;
};

const handlePrevFile = () => {
  if (!files.value) return;
  if (currentIndex.value === 0) {
    currentIndex.value = files.value.length - 1;
  } else {
    currentIndex.value -= 1;
  }
};

const handleReset = () => {
  currentPage.value = 1;
  currentScale.value = 1;
};

const handleWsMessage = (ws: WebSocket, ev: MessageEvent) => {
  const cmd = ev.data as string;
  if (cmd === "page:next") {
    handleNextPage();
  } else if (cmd === "page:prev") {
    handlePrevPage();
  } else if (cmd === "scale:up") {
    handleZoomIn();
  } else if (cmd === "scale:down") {
    handleZoomOut();
  } else if (cmd === "file:next") {
    handleNextFile();
  } else if (cmd === "file:prev") {
    handlePrevFile();
  } else if (cmd === "settings:reset") {
    handleReset();
  } else {
    console.warn("Unknown command:", cmd);
  }
};

const cws = useControlWebsocket(
  handleWsMessage,
  (ws, ev) => message.error("WebSocket 连接失败，请检查日志"),
  (ws) => message.info("WebSocket 连接成功"),
  (ws) => message.info("WebSocket 连接已关闭")
);
</script>

<template>
  <div class="w-full h-full overflow-hidden p-3">
    <Flex class="w-full h-full" justify="center" align="center">
      <Spin :spinning="isFetching">
        <VuePDF
          v-if="pdf"
          :pdf="pdf"
          :page="currentPage"
          :scale="currentScale"
        />
        <Result
          v-else-if="!isFetching"
          title="资源加载失败，请检查日志"
          :status="404"
        />
      </Spin>
    </Flex>

    <FloatButtonGroup class="right-20" shape="square">
      <FloatButton @click="handlePrevPage">
        <template #icon>
          <UpOutlined />
        </template>
      </FloatButton>

      <FloatButton @click="handleNextPage">
        <template #icon>
          <DownOutlined />
        </template>
      </FloatButton>

      <FloatButton @click="handleZoomIn">
        <template #icon>
          <FullscreenOutlined />
        </template>
      </FloatButton>

      <FloatButton @click="handleZoomOut">
        <template #icon>
          <FullscreenExitOutlined />
        </template>
      </FloatButton>

      <FloatButton @click="handlePrevFile">
        <template #icon>
          <DoubleLeftOutlined />
        </template>
      </FloatButton>

      <FloatButton @click="handleNextFile">
        <template #icon>
          <DoubleRightOutlined />
        </template>
      </FloatButton>
    </FloatButtonGroup>
  </div>
</template>
