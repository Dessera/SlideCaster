<script lang="ts" setup>
import { UploadOutlined } from "@ant-design/icons-vue";
import {
  Card,
  Space,
  Flex,
  Switch,
  App,
  Upload,
  Button as AButton,
} from "ant-design-vue";
import type { UploadRequestOption } from "ant-design-vue/es/vc-upload/interface";
import { getErrResponse } from "~/api";

import {
  useClientStatus,
  useClientStart,
  useClientStop,
  useUploadMap,
  useUploadModel,
} from "~/api/control";

const { message } = App.useApp();

const clientStatusLoading = ref(false);

const clientStatusEnabled = computed(() => !clientStatusLoading.value);

const { data: clientStatus, isError } = useClientStatus(clientStatusEnabled);

const { mutateAsync: startClient } = useClientStart();
const { mutateAsync: stopClient } = useClientStop();

const { mutateAsync: uploadMap } = useUploadMap();
const { mutateAsync: uploadModel } = useUploadModel();

const handleClientStatusChange = async (checked: boolean) => {
  clientStatusLoading.value = true;
  console.log(checked);
  try {
    if (checked) {
      await startClient();
      message.success("服务启动成功");
    } else {
      await stopClient();
      message.success("服务停止成功");
    }
  } catch (error) {
    const detail = getErrResponse(error);
    message.error(`服务操作失败：${detail}`);
  } finally {
    clientStatusLoading.value = false;
  }
};

const handleMapUploadRequest = async (options: UploadRequestOption) => {
  const { onError, onSuccess } = options;

  const file = options.file as File;

  try {
    await uploadMap(file);
    onSuccess?.("ok");
    message.success(`上传映射文件 ${file.name} 成功`);
  } catch (error) {
    const detail = getErrResponse(error);
    onError?.(new Error(detail));
    message.error(`上传映射文件 ${file.name} 失败：${detail}`);
  }
};

const handleModelUploadRequest = async (options: UploadRequestOption) => {
  const { onError, onSuccess } = options;

  const file = options.file as File;

  try {
    await uploadModel(file);
    onSuccess?.("ok");
    message.success(`上传模型文件 ${file.name} 成功`);
  } catch (error) {
    const detail = getErrResponse(error);
    onError?.(new Error(detail));
    message.error(`上传模型文件 ${file.name} 失败：${detail}`);
  }
};
</script>

<template>
  <div class="w-full h-full overflow-hidden p-3">
    <Card title="服务配置">
      <Space class="w-full" direction="vertical" size="large">
        <Flex justify="space-between">
          <span>服务状态</span>
          <Switch
            :checked="clientStatus"
            :loading="clientStatusLoading"
            :disabled="isError"
            @update:checked="handleClientStatusChange as any"
          />
        </Flex>
        <Flex justify="space-between">
          <span>映射文件</span>
          <Upload :custom-request="handleMapUploadRequest">
            <AButton>
              <UploadOutlined />
              点击上传
            </AButton>
            <template #itemRender> </template>
          </Upload>
        </Flex>
        <Flex justify="space-between">
          <span>模型文件</span>
          <Upload :custom-request="handleModelUploadRequest">
            <AButton>
              <UploadOutlined />
              点击上传
            </AButton>
            <template #itemRender> </template>
          </Upload>
        </Flex>
      </Space>
    </Card>
  </div>
</template>
