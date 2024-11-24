export function useAppBaseURL() {
  return useRuntimeConfig().public.appBaseURL;
}

export function useApiURL(path: string) {
  const url = new URL(path, useAppBaseURL());
  return url.toString();
}

export function getErrResponse(err: any) {
  // FastAPI error response
  if (err.response && err.response.data && err.response.data.detail) {
    return err.response.data.detail;
  }
  return "未知错误";
}
