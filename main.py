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

@app.post("/beautify-face/")
async def beautify_face(file: UploadFile = File(...)):
    """
    Yüz güzelleştirme efekti uygular.
    """
    image_data = await file.read()
    result = service.beautify_face(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/hdr-effect/")
async def hdr_effect(file: UploadFile = File(...)):
    """
    HDR efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_hdr_effect(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/smart-crop/")
async def smart_crop(
    file: UploadFile = File(...),
    target_width: int = Query(500),
    target_height: int = Query(500)
):
    """
    Akıllı kırpma uygular.
    """
    image_data = await file.read()
    result = service.smart_crop(image_data, target_width, target_height)
    return StreamingResponse(result, media_type="image/png")

@app.post("/auto-color-correction/")
async def auto_color_correction(file: UploadFile = File(...)):
    """
    Otomatik renk düzeltme uygular.
    """
    image_data = await file.read()
    result = service.auto_color_correction(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/enhance-portrait/")
async def enhance_portrait(file: UploadFile = File(...)):
    """
    Portre fotoğrafını geliştirir.
    """
    image_data = await file.read()
    result = service.enhance_portrait(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/center-crop/")
async def center_crop(
    file: UploadFile = File(...),
    target_width: int = Query(500),
    target_height: int = Query(500)
):
    """
    Resmi merkezi olarak kırpar.
    """
    image_data = await file.read()
    result = service.center_crop(image_data, target_width, target_height)
    return StreamingResponse(result, media_type="image/png")

@app.post("/auto-enhance/")
async def auto_enhance(file: UploadFile = File(...)):
    """
    Otomatik renk ve kontrast iyileştirmesi yapar.
    """
    image_data = await file.read()
    result = service.auto_enhance(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/dramatic-effect/")
async def dramatic_effect(file: UploadFile = File(...)):
    """
    Dramatik fotoğraf efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_dramatic_effect(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/watercolor/")
async def watercolor(file: UploadFile = File(...)):
    """
    Resme suluboya efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_watercolor_effect(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/reduce-noise/")
async def reduce_noise(
    file: UploadFile = File(...),
    strength: float = Query(0.1, ge=0, le=1)
):
    """
    Görüntüdeki gürültüyü azaltır.
    """
    image_data = await file.read()
    result = service.reduce_noise(image_data, strength)
    return StreamingResponse(result, media_type="image/png")

@app.post("/texture/")
async def add_texture(
    file: UploadFile = File(...),
    texture_type: str = Query("canvas", regex="^(canvas|paper|concrete)$")
):
    """
    Resme doku efekti ekler.
    """
    image_data = await file.read()
    result = service.apply_texture(image_data, texture_type)
    return StreamingResponse(result, media_type="image/png")

@app.post("/enhance-details/")
async def enhance_details(file: UploadFile = File(...)):
    """
    Görüntüdeki detayları geliştirir.
    """
    image_data = await file.read()
    result = service.enhance_details(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/pencil-sketch/")
async def pencil_sketch(
    file: UploadFile = File(...),
    pencil_type: str = Query("soft", regex="^(soft|hard)$")
):
    """
    Resmi karakalem çizimine dönüştürür.
    """
    image_data = await file.read()
    result = service.apply_pencil_sketch(image_data, pencil_type)
    return StreamingResponse(result, media_type="image/png")

@app.post("/oil-painting/")
async def oil_painting(
    file: UploadFile = File(...),
    brush_size: int = Query(5, ge=1, le=10)
):
    """
    Resme yağlı boya efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_oil_painting(image_data, brush_size)
    return StreamingResponse(result, media_type="image/png")

@app.post("/polaroid/")
async def polaroid_effect(file: UploadFile = File(...)):
    """
    Resme polaroid fotoğraf efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_polaroid_effect(image_data)
    return StreamingResponse(result, media_type="image/png")

@app.post("/double-exposure/")
async def double_exposure(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    """
    İki resmi birleştirerek double exposure efekti uygular.
    """
    image_data1 = await file1.read()
    image_data2 = await file2.read()
    result = service.apply_double_exposure(image_data1, image_data2)
    return StreamingResponse(result, media_type="image/png")

@app.post("/duotone/")
async def duotone(
    file: UploadFile = File(...),
    color1: str = Query("blue", regex="^[a-zA-Z]+$"),
    color2: str = Query("pink", regex="^[a-zA-Z]+$")
):
    """
    Resme duotone efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_duotone(image_data, color1, color2)
    return StreamingResponse(result, media_type="image/png")

@app.post("/tilt-shift/")
async def tilt_shift(
    file: UploadFile = File(...),
    blur_factor: int = Query(5, ge=1, le=10)
):
    """
    Resme minyatür (tilt-shift) efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_tilt_shift(image_data, blur_factor)
    return StreamingResponse(result, media_type="image/png")

@app.post("/color-splash/")
async def color_splash(
    file: UploadFile = File(...),
    color_to_keep: str = Query("red", regex="^(red|green|blue|yellow)$")
):
    """
    Seçilen renk dışındaki tüm renkleri siyah-beyaz yapar.
    """
    image_data = await file.read()
    result = service.apply_color_splash(image_data, color_to_keep)
    return StreamingResponse(result, media_type="image/png")

@app.post("/mirror/")
async def mirror_effect(
    file: UploadFile = File(...),
    direction: str = Query("horizontal", regex="^(horizontal|vertical)$")
):
    """
    Resme ayna efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_mirror_effect(image_data, direction)
    return StreamingResponse(result, media_type="image/png")

@app.post("/kaleidoscope/")
async def kaleidoscope(
    file: UploadFile = File(...),
    segments: int = Query(8, ge=3, le=12)
):
    """
    Resme kaleydoskop efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_kaleidoscope(image_data, segments)
    return StreamingResponse(result, media_type="image/png")

@app.post("/wave/")
async def wave_distortion(
    file: UploadFile = File(...),
    amplitude: int = Query(5, ge=1, le=10),
    wavelength: int = Query(10, ge=5, le=20)
):
    """
    Resme dalga distorsiyonu efekti uygular.
    """
    image_data = await file.read()
    result = service.apply_wave_distortion(image_data, amplitude, wavelength)
    return StreamingResponse(result, media_type="image/png")
