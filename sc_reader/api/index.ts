import pathLib from "path-browserify-esm";

export function useApiBaseURL() {
  return useRuntimeConfig().public.apiBaseURL;
}

export function useGetApiURL(scope: string[] = []) {
  const base = useApiBaseURL();
  return (path: string = "") => {
    const baseUrl = new URL(base);
    const oldPath = baseUrl.pathname;
    const newPath = pathLib.join(oldPath, ...scope, path);
    return new URL(newPath, base).toString();
  };
}

export function useGetWebsocketURL(scope: string[] = []) {
  const getApiURL = useGetApiURL(scope);

  return (path: string = "") => {
    const url = getApiURL(path);
    return url.replace("http", "ws");
  };
}

export function getErrResponse(err: any) {
  // FastAPI error response
  if (err.response && err.response.data && err.response.data.detail) {
    return err.response.data.detail as string;
  }
  return "未知错误";
}
