import axios from "axios";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";

import { useGetApiURL } from ".";

export function useFileList() {
  const getApiURL = useGetApiURL(["file"]);
  return useQuery({
    queryKey: ["file"],
    queryFn: async () => {
      const { data } = await axios.get(getApiURL());
      return data as string[];
    },
  });
}

export function useDeleteFile() {
  const getFileURL = useGetFileURL();

  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (filename: string) => {
      await axios.delete(getFileURL(filename));
    },
    onSuccess: () => {
      // Invalidate the file list query
      queryClient.invalidateQueries({ queryKey: ["file"] });
    },
  });
}

export function useUploadFile() {
  const getApiURL = useGetApiURL(["file"]);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      await axios.post(getApiURL(), formData);
    },
    onSuccess: () => {
      // Invalidate the file list query
      queryClient.invalidateQueries({ queryKey: ["file"] });
    },
  });
}

export function useGetFileURL() {
  const getApiURL = useGetApiURL(["file"]);
  return (filename: string) => getApiURL(encodeURIComponent(filename));
}
