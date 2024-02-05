from typing import Annotated

from fastapi import APIRouter, Body, UploadFile, File
from fastapi.responses import StreamingResponse

from src.ascii.service import get_ascii_art

router = APIRouter(
    prefix="/ascii"
)


@router.post("/")
async def process_image(font_size: Annotated[int, Body()], file: UploadFile = File(...)):
    result = await get_ascii_art(font_size, file)
    return StreamingResponse(result, media_type="image/png")
