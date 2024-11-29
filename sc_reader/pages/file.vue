<script lang="ts" setup>
import {
  Card,
  UploadDragger,
  List,
  ListItem,
  Button as AButton,
  ListItemMeta,
  Result,
  App,
} from "ant-design-vue";
import { FilePdfOutlined, InboxOutlined } from "@ant-design/icons-vue";
import type { UploadRequestOption } from "ant-design-vue/es/vc-upload/interface";

import {
  useFileList,
  useDeleteFile,
  useUploadFile,
  useGetFileURL,
} from "~/api/file";
import { getErrResponse } from "~/api";

const { modal, message } = App.useApp();

const { data, isError } = useFileList();
const { mutateAsync: deleteFile } = useDeleteFile();
const { mutateAsync: uploadFile } = useUploadFile();
const getFileURL = useGetFileURL();

const handleDelete = (name: string) => {
  modal.confirm({
    title: "删除文件",
    content: `确定删除文件 ${name} 吗？`,
    onOk: async () => {
      try {
        await deleteFile(name);
        message.success(`删除文件 ${name} 成功`);
      } catch (error) {
        const detail = getErrResponse(error);
        message.error(`删除文件 ${name} 失败：${detail}`);
      }
    },
  });
};

const handleUploadRequest = async (options: UploadRequestOption) => {
  const { onError, onSuccess } = options;

  const file = options.file as File;

  try {
    await uploadFile(file);
    onSuccess?.("ok");
    message.success(`上传文件 ${file.name} 成功`);
  } catch (error) {
    const detail = getErrResponse(error);
    onError?.(new Error(detail));
    message.error(`上传文件 ${file.name} 失败：${detail}`);
  }
};
</script>

<template>
  <div class="w-full h-full overflow-hidden p-3">
    <Card title="资源查看">
      <Result v-if="isError" title="资源加载失败，请检查日志" />
      <List v-else>
        <ListItem v-for="item in data">
          <template #actions>
            <AButton type="link" :href="getFileURL(item)">查看</AButton>
            <AButton type="link" danger @click="handleDelete(item)">
              删除
            </AButton>
          </template>
          <ListItemMeta>
            <template #avatar>
              <FilePdfOutlined />
            </template>
            <template #title>{{ item }}</template>
          </ListItemMeta>
        </ListItem>
      </List>
      <UploadDragger accept=".pdf" :custom-request="handleUploadRequest">
        <p class="ant-upload-drag-icon">
          <InboxOutlined />
        </p>
        <p class="ant-upload-text">点击上传PDF文件，或将文件拖拽至此</p>
      </UploadDragger>
    </Card>
  </div>
</template>
