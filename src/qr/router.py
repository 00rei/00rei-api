from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from io import BytesIO
import qrcode
from typing import Annotated

from src.qr.schemas import QRData

router = APIRouter(
    prefix="/qr"
)


@router.post("/")
async def create_qr(data: Annotated[QRData, Body()]):
    print(data)
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data.url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    img_bytes_io = BytesIO()
    img.save(img_bytes_io, format="PNG")
    img_bytes_io.seek(0)

    return StreamingResponse(img_bytes_io, media_type="image/png")
