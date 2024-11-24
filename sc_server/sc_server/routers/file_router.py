from fastapi import APIRouter, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..services import file_service

router = APIRouter(tags=["file"], prefix="/file")


@router.get("")
async def get_files():
    return file_service.get_files()


@router.get("/{file_name}")
async def get_file(file_name: str):
    file_path = file_service.get_file(file_name)
    if file_path is None:
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@router.post("")
async def upload_file(file: UploadFile):
    content = await file.read()
    return file_service.save_file(content, file.filename)


@router.delete("/{file_name}")
async def delete_file(file_name: str):
    if not file_service.delete_file(file_name):
        raise HTTPException(status_code=404, detail="File not found")
    return {"message": "File deleted"}
