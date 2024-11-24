import axios from "axios";
import { useMutation, useQuery, useQueryClient } from "@tanstack/vue-query";

import { useGetApiURL } from ".";

export function useClientStatus(enabled: boolean | Ref<boolean> = true) {
  const getApiURL = useGetApiURL(["control"]);
  return useQuery({
    queryKey: ["control"],
    refetchInterval: 1000,
    enabled,
    queryFn: async () => {
      const { data } = await axios.get(getApiURL("status"));
      return data as boolean;
    },
  });
}

export function useClientStart() {
  const getApiURL = useGetApiURL(["control"]);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      await axios.post(getApiURL("start"));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["control"] });
    },
  });
}

export function useClientStop() {
  const getApiURL = useGetApiURL(["control"]);
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      await axios.post(getApiURL("stop"));
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["control"] });
    },
  });
}

export function useUploadModel() {
  const getApiURL = useGetApiURL(["control"]);
  // const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      await axios.post(getApiURL("model"), formData);
    },
    // onSuccess: () => {
    //   queryClient.invalidateQueries({ queryKey: ["control"] });
    // },
  });
}

export function useUploadMap() {
  const getApiURL = useGetApiURL(["control"]);
  // const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      await axios.post(getApiURL("map"), formData);
    },
    // onSuccess: () => {
    //   queryClient.invalidateQueries({ queryKey: ["control"] });
    // },
  });
}
