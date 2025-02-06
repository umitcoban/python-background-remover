from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from service import ImageProcessService

app = FastAPI()

# Servis sınıfını başlat
service = ImageProcessService()

@app.post("/remove-bg/")
async def remove_bg(file: UploadFile = File(...), width: int = None, height: int = None):
    """
    Yüklenen resmin arka planını kaldırır.
    """
    image_data = await file.read()

    # Servisi kullanarak arka planı kaldır
    output_buffer = service.remove_background(image_data, width, height)

    return StreamingResponse(output_buffer, media_type="image/png")

@app.post("/add-shadow/")
async def add_shadow(file: UploadFile = File(...)):
    """
    Yüklenen resme gölge ekler.
    """
    image_data = await file.read()

    # Servisi kullanarak gölge ekle
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
async def resize_image(width: int, height: int, file: UploadFile = File(...)):
    """
    Resmi belirli genişlik ve yükseklik değerine göre yeniden boyutlandırır.
    """
    image_data = await file.read()
    resized_image = service.resize_image(image_data, width, height)
    return StreamingResponse(resized_image, media_type="image/png")

@app.post("/resize-image/")
async def resize_image(width: int, height: int, file: UploadFile = File(...)):
    """
    Resmi belirli genişlik ve yükseklik değerine göre yeniden boyutlandırır.
    """
    image_data = await file.read()
    resized_image = service.resize_image(image_data, width, height)
    return StreamingResponse(resized_image, media_type="image/png")

@app.post("/add-text/")
async def add_text(text: str, file: UploadFile = File(...), x: int = 10, y: int = 10, font_size: int = 30):
    """
    Resim üzerine metin ekler.
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
async def crop_image(file: UploadFile = File(...), left: int = 0, top: int = 0, right: int = 100, bottom: int = 100):
    """
    Resmi kırpar.
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
    Resme mozaik efekti (pixelate) uygular.
    """
    image_data = await file.read()
    pixelated_image = service.pixelate_image(image_data, pixel_size)
    return StreamingResponse(pixelated_image, media_type="image/png")

@app.post("/process-mixed/")
async def process_mixed(file: UploadFile = File(...), width: int = None, height: int = None):
    """
    Resim üzerinde arka plan kaldırma, keskinleştirme ve gölge ekleme işlemlerini sırayla uygular.
    """
    # 1️⃣ Resim dosyasını oku
    image_data = await file.read()

    # 2️⃣ Arka planı kaldır
    bg_removed = service.remove_background(image_data, width, height)
    
    # 3️⃣ Keskinleştirme uygula
    sharpened_image = service.sharpen_image(bg_removed.getvalue())
    
    # 4️⃣ Gölge ekle
    final_image = service.add_shadow(sharpened_image.getvalue())

    # 5️⃣ Sonucu döndür
    return StreamingResponse(final_image, media_type="image/png")

@app.post("/basic-shadow/")
async def basic_shadow(
    file: UploadFile = File(...),
    shadow_opacity: int = 120,
    blur_radius: int = 10,
    offset_x: int = 20,
    offset_y: int = 20,
):
    """
    Temel bir gölge efekti uygular.
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
    shadow_length: float = 1.5,
):
    """
    Işığın geldiği açıya göre gerçekçi bir gölge ekler ve koordinatları resimle hizalar.
    """
    image_data = await file.read()
    shadowed_image = service.apply_realistic_shadow(
        image_data, light_angle, shadow_opacity, blur_radius, shadow_length
    )
    return StreamingResponse(shadowed_image, media_type="image/png")

@app.post("/standardize-aspect-ratio/")
async def standardize_aspect_ratio(file: UploadFile = File(...), target_width: int = 500, target_height: int = 500):
    image_data = await file.read()
    result = service.standardize_aspect_ratio(image_data, target_width, target_height)
    return StreamingResponse(result, media_type="image/png")


@app.post("/remove-bg-and-add-shadow/")
async def remove_bg_and_add_shadow(file: UploadFile = File(...)):
    image_data = await file.read()
    result = service.remove_background_and_add_shadow(image_data)
    return StreamingResponse(result, media_type="image/png")


@app.post("/generate-social-profile/")
async def generate_social_profile(file: UploadFile = File(...)):
    image_data = await file.read()
    result = service.generate_social_media_profile(image_data)
    return StreamingResponse(result, media_type="image/png")


@app.post("/enhance-for-listing/")
async def enhance_for_listing(file: UploadFile = File(...)):
    image_data = await file.read()
    result = service.enhance_for_listing(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/remove-text/")
async def remove_text(file: UploadFile = File(...)):
    """
    Resimde bulunan tüm yazıları siler.
    
    :param file: Yüklenen resim dosyası.
    :return: Yazıları silinmiş resmin PNG formatında çıktısı.
    """
    image_data = await file.read()
    result = service.remove_text(image_data)
    return StreamingResponse(result, media_type="image/png")
