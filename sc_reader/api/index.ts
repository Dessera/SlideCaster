import pathLib from "path-browserify-esm";

export function useApiBaseURL() {
  const base = useRuntimeConfig().public.apiBaseURL;
  return new URL(base);
}

export function useGetApiURL(scope: string[] = []) {
  const base = useApiBaseURL();
  return (path: string = "") => {
    const oldPath = base.pathname;
    const newPath = pathLib.join(oldPath, ...scope, path);
    return new URL(newPath, base).toString();
  };
}

export function getErrResponse(err: any) {
  // FastAPI error response
  if (err.response && err.response.data && err.response.data.detail) {
    return err.response.data.detail as string;
  }
  return "未知错误";
}
