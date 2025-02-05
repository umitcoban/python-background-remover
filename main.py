from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image
from io import BytesIO
from rembg import remove

app = FastAPI()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...), width: int = None, height: int = None):
    # Yüklenen dosyayı oku
    input_image = Image.open(BytesIO(await file.read()))

    # Oranları koruyarak resmi yeniden boyutlandır
    if width and height:
        input_image.thumbnail((width, height))

    # Arka planı kaldır
    output_image = remove(input_image)

    # Sonucu byte dizisine kaydet
    output_buffer = BytesIO()
    output_image.save(output_buffer, format="PNG")
    output_buffer.seek(0)

    return StreamingResponse(output_buffer, media_type="image/png")
