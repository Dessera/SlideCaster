from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path

router = APIRouter(tags=["resource"])


@router.get("/pdf/{name}")
def get_pdf_file(name: str):
    path = Path(f"/mnt/resource_media/{name}")
    if not path.exists():
        raise HTTPException(status_code=403, detail="请求资源不存在")
    else:
        return FileResponse(str(path))


@router.get("/pdf")
def get_pdf_list():
    path = Path("/mnt/resource_media")
    if not path.exists():
        raise HTTPException(status_code=403, detail="未识别到外部存储设备")
    else:
        items = []
        for item in path.iterdir():
            if item.is_file() and item.match("*.pdf"):
                items.append(item)
        return items
