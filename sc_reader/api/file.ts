import axios from "axios";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";

import { useApiURL } from ".";

export function useFileList() {
  const apiURL = useApiURL("/file");
  return useQuery({
    queryKey: ["file"],
    queryFn: async () => {
      const { data } = await axios.get(apiURL);
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
  const apiURL = useApiURL("/file");
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      await axios.post(apiURL, formData);
    },
    onSuccess: () => {
      // Invalidate the file list query
      queryClient.invalidateQueries({ queryKey: ["file"] });
    },
  });
}

export function useGetFileURL() {
  const apiURL = useApiURL("/file");
  return (filename: string) => `${apiURL}/${encodeURIComponent(filename)}`;
}
