from fastapi import FastAPI, File, UploadFile, Query
from fastapi.responses import StreamingResponse
from service import ImageProcessService

app = FastAPI(root_path="/")

# Servis sınıfını başlat
service = ImageProcessService()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...), width: int = None, height: int = None):
    """
    Yüklenen resmin arka planını kaldırır.
    """
    image_data = await file.read()
    output_buffer = service.remove_background(image_data, width, height)
    return StreamingResponse(output_buffer, media_type="image/png")

@app.post("/add-shadow/")
async def add_shadow(file: UploadFile = File(...)):
    """
    Yüklenen resme gölge ekler.
    """
    image_data = await file.read()
    shadow_buffer = service.add_shadow(image_data)
    return StreamingResponse(shadow_buffer, media_type="image/png")

@app.post("/apply-filter/")
async def apply_filter(file: UploadFile = File(...), filter_type: str = "grayscale"):
    """
    Resme sepia, grayscale veya negatif filtre uygular.
    """
    image_data = await file.read()
    filtered_image = service.apply_filter(image_data, filter_type)
    return StreamingResponse(filtered_image, media_type="image/png")

@app.post("/resize-image/")
async def resize_image(file: UploadFile = File(...), width: int = Query(...), height: int = Query(...)):
    """
    Resmi belirtilen genişlik ve yükseklik değerine göre yeniden boyutlandırır.
    """
    image_data = await file.read()
    resized_image = service.resize_image(image_data, width, height)
    return StreamingResponse(resized_image, media_type="image/png")

@app.post("/rotate-image/")
async def rotate_image(file: UploadFile = File(...), angle: float = Query(...)):
    """
    Resmi belirli bir açıya göre döndürür.
    """
    image_data = await file.read()
    rotated_image = service.rotate_image(image_data, angle)
    return StreamingResponse(rotated_image, media_type="image/png")

@app.post("/add-text/")
async def add_text(
    file: UploadFile = File(...),
    text: str = "Test",
    x: int = 10,
    y: int = 10,
    font_size: int = 30
):
    """
    Resmin üzerine metin ekler.
    """
    image_data = await file.read()
    text_image = service.add_text(image_data, text, (x, y), font_size)
    return StreamingResponse(text_image, media_type="image/png")

@app.post("/sketch-effect/")
async def sketch_effect(file: UploadFile = File(...)):
    """
    Resmi çizim efektine çevirir.
    """
    image_data = await file.read()
    sketch_image = service.sketch_effect(image_data)
    return StreamingResponse(sketch_image, media_type="image/png")

@app.post("/crop/")
async def crop_image(
    file: UploadFile = File(...),
    left: int = 0,
    top: int = 0,
    right: int = 100,
    bottom: int = 100
):
    """
    Resmi belirtilen koordinatlar üzerinden kırpar.
    """
    image_data = await file.read()
    cropped_image = service.crop_image(image_data, left, top, right, bottom)
    return StreamingResponse(cropped_image, media_type="image/png")

@app.post("/sharpen/")
async def sharpen_image(file: UploadFile = File(...)):
    """
    Resmi keskinleştirir.
    """
    image_data = await file.read()
    sharpened_image = service.sharpen_image(image_data)
    return StreamingResponse(sharpened_image, media_type="image/png")

@app.post("/edge-detection/")
async def edge_detection(file: UploadFile = File(...)):
    """
    Resimde kenar algılama işlemi yapar.
    """
    image_data = await file.read()
    edge_detected_image = service.edge_detection(image_data)
    return StreamingResponse(edge_detected_image, media_type="image/png")

@app.post("/pixelate/")
async def pixelate_image(file: UploadFile = File(...), pixel_size: int = 10):
    """
    Resme mozaik (pixelate) efekti uygular.
    """
    image_data = await file.read()
    pixelated_image = service.pixelate_image(image_data, pixel_size)
    return StreamingResponse(pixelated_image, media_type="image/png")

@app.post("/basic-shadow/")
async def basic_shadow(
    file: UploadFile = File(...),
    shadow_opacity: int = 120,
    blur_radius: int = 10,
    offset_x: int = 20,
    offset_y: int = 20,
):
    """
    Temel gölge efekti ekler.
    """
    image_data = await file.read()
    shadowed_image = service.apply_basic_shadow(
        image_data, shadow_opacity, blur_radius, (offset_x, offset_y)
    )
    return StreamingResponse(shadowed_image, media_type="image/png")

@app.post("/realistic-shadow/")
async def realistic_shadow(
    file: UploadFile = File(...),
    light_angle: int = 45,
    shadow_opacity: int = 120,
    blur_radius: int = 15,
    shadow_length: float = 1.0,
):
    """
    Işığın geldiği açıya göre gerçekçi gölge ekler.
    """
    image_data = await file.read()
    shadowed_image = service.apply_realistic_shadow(
        image_data, light_angle, shadow_opacity, blur_radius, shadow_length
    )
    return StreamingResponse(shadowed_image, media_type="image/png")

@app.post("/standardize-aspect-ratio/")
async def standardize_aspect_ratio(
    file: UploadFile = File(...),
    target_width: int = 500,
    target_height: int = 500
):
    """
    Resmin oranını standart hale getirip, hedef boyutlarda arka plan ekler.
    """
    image_data = await file.read()
    result = service.standardize_aspect_ratio(image_data, target_width, target_height)
    return StreamingResponse(result, media_type="image/png")

@app.post("/remove-bg-and-add-shadow/")
async def remove_bg_and_add_shadow(file: UploadFile = File(...)):
    """
    Arka planı kaldırır ve gölge ekler.
    """
    image_data = await file.read()
    result = service.remove_background_and_add_shadow(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/generate-social-profile/")
async def generate_social_profile(file: UploadFile = File(...)):
    """
    Yuvarlak sosyal medya profil fotoğrafı oluşturur.
    """
    image_data = await file.read()
    result = service.generate_social_media_profile(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/generate-social-media-profile/")
async def generate_social_media_profile(file: UploadFile = File(...)):
    """
    Yuvarlak sosyal medya profil fotoğrafı oluşturur.
    """
    image_data = await file.read()
    result = service.generate_social_media_profile(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/remove-text/")
async def remove_text(file: UploadFile = File(...)):
    """
    Resimdeki metin alanlarını siler.
    """
    image_data = await file.read()
    result = service.remove_text(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/cartoon-effect/")
async def cartoon_effect(file: UploadFile = File(...)):
    """
    Resmi çizgi film tarzına dönüştürür.
    """
    image_data = await file.read()
    result = service.apply_cartoon_effect(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/glitch-effect/")
async def glitch_effect(
    file: UploadFile = File(...),
    intensity: float = Query(0.1, ge=0, le=1)
):
    """
    Resme glitch (bozulma) efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_glitch_effect(image_data, intensity)
    return StreamingResponse(result, media_type="image/png")

@app.post("/neon-effect/")
async def neon_effect(
    file: UploadFile = File(...),
    glow_amount: float = Query(2.5, ge=0, le=5)
):
    """
    Resme neon efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_neon_effect(image_data, glow_amount)
    return StreamingResponse(result, media_type="image/png")

@app.post("/vintage-effect/")
async def vintage_effect(file: UploadFile = File(...)):
    """
    Resme vintage/eski fotoğraf efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_vintage_effect(image_data)
    return StreamingResponse(result, media_type="image/png")
