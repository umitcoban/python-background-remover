from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont
from io import BytesIO
from rembg import remove
import cv2
import numpy as np

class ImageProcessService:
    def __init__(self, shadow_offset=(15, 15), blur_radius=15, shadow_color=(0, 0, 0, 120)):
        """
        Görüntü işleme servisi başlatılır.
        :param shadow_offset: Gölge kaydırma miktarı (x, y).
        :param blur_radius: Gölge için bulanıklık yarıçapı.
        :param shadow_color: Gölge rengi (RGBA).
        """
        self.shadow_offset = shadow_offset
        self.blur_radius = blur_radius
        self.shadow_color = shadow_color

    def remove_background(self, image_data, width=None, height=None):
        """
        Görüntünün arka planını kaldırır.
        :param image_data: Yüklenen resmin byte verisi.
        :param width: Yeni genişlik.
        :param height: Yeni yükseklik.
        :return: Arka planı kaldırılmış resmin byte verisi.
        """
        # Yüklenen dosyayı oku
        input_image = Image.open(BytesIO(image_data))

        # Oranları koruyarak resmi yeniden boyutlandır
        if width and height:
            input_image.thumbnail((width, height))

        # Arka planı kaldır
        output_image = remove(input_image)

        # Sonucu byte dizisine kaydet
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def add_shadow(self, image_data):
        """
        Resme uygun sanal bir gölge ekler.
        :param image_data: Yüklenen resmin byte verisi.
        :return: Gölgelendirilmiş resmin byte verisi.
        """
        # Orijinal resmi aç
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        width, height = image.size

        # Gölge için boş bir resim oluştur
        shadow = Image.new("RGBA", (width + abs(self.shadow_offset[0]) * 2, height + abs(self.shadow_offset[1]) * 2), (0, 0, 0, 0))
        
        # Resmin alfa kanalını kullanarak gölge oluştur
        alpha = image.split()[3]  # PNG'nin transparan kanalı
        shadow_layer = Image.new("RGBA", image.size, self.shadow_color)
        shadow_layer.putalpha(alpha)

        # Gölgeyi boş resme yapıştır
        shadow.paste(shadow_layer, (self.shadow_offset[0], self.shadow_offset[1]), shadow_layer)

        # Gaussian Blur ile gölgeyi yumuşat
        shadow = shadow.filter(ImageFilter.GaussianBlur(self.blur_radius))

        # Orijinal resmi gölgenin üstüne yerleştir
        shadow.paste(image, (abs(self.shadow_offset[0]), abs(self.shadow_offset[1])), image)

        # Sonucu byte formatına çevir
        output_buffer = BytesIO()
        shadow.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def apply_filter(self, image_data, filter_type="grayscale"):
        """
        Resme çeşitli filtreler uygular.
        :param image_data: Yüklenen resmin byte verisi.
        :param filter_type: Uygulanacak filtre (grayscale, sepia, negative).
        :return: Filtrelenmiş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGB")

        if filter_type == "grayscale":
            image = ImageOps.grayscale(image)
        elif filter_type == "sepia":
            sepia_filter = Image.new("RGB", image.size)
            pixels = image.load()
            for i in range(image.width):
                for j in range(image.height):
                    r, g, b = pixels[i, j]
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    pixels[i, j] = (min(tr, 255), min(tg, 255), min(tb, 255))
        elif filter_type == "negative":
            image = ImageOps.invert(image)

        output_buffer = BytesIO()
        image.save(output_buffer, format="PNG")
        output_buffer.seek(0)
        
        return output_buffer

    def resize_image(self, image_data, width, height):
        """
        Resmi belirtilen genişlik ve yükseklik ile yeniden boyutlandırır.
        :param image_data: Yüklenen resmin byte verisi.
        :param width: Yeni genişlik.
        :param height: Yeni yükseklik.
        :return: Boyutlandırılmış resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data))
        image = image.resize((width, height))

        output_buffer = BytesIO()
        image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def rotate_image(self, image_data, angle):
        """
        Resmi belirli bir derece döndürür.
        :param image_data: Yüklenen resmin byte verisi.
        :param angle: Döndürme açısı (derece cinsinden).
        :return: Döndürülmüş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data))
        rotated_image = image.rotate(angle, expand=True)

        output_buffer = BytesIO()
        rotated_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def add_text(self, image_data, text="Test", position=(10, 10), font_size=30):
        """
        Resmin üzerine yazı ekler.
        :param image_data: Yüklenen resmin byte verisi.
        :param text: Eklenecek metin.
        :param position: Metnin konumu (x, y).
        :param font_size: Font boyutu.
        :return: Üzerine metin eklenmiş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        draw = ImageDraw.Draw(image)

        # Font belirleme (Default font kullanılıyor, harici font ekleyebilirsin)
        font = ImageFont.load_default()

        # Yazıyı çizme
        draw.text(position, text, fill="white", font=font)

        output_buffer = BytesIO()
        image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def sketch_effect(self, image_data):
        """
        Resmi çizim efektine çevirir.
        :param image_data: Yüklenen resmin byte verisi.
        :return: Sketch efekti uygulanmış resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_cv = np.array(image)

        gray = cv2.cvtColor(image_cv, cv2.COLOR_RGB2GRAY)
        inverted = cv2.bitwise_not(gray)
        blurred = cv2.GaussianBlur(inverted, (21, 21), sigmaX=0, sigmaY=0)
        sketch = cv2.divide(gray, 255 - blurred, scale=256)

        sketch_image = Image.fromarray(sketch)
        output_buffer = BytesIO()
        sketch_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def crop_image(self, image_data, left, top, right, bottom):
        """
        Resmi belirli bir alan üzerinden kırpar.
        :param image_data: Yüklenen resmin byte verisi.
        :param left: Sol koordinat.
        :param top: Üst koordinat.
        :param right: Sağ koordinat.
        :param bottom: Alt koordinat.
        :return: Kırpılmış resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data))
        cropped_image = image.crop((left, top, right, bottom))

        output_buffer = BytesIO()
        cropped_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def sharpen_image(self, image_data):
        """
        Resmi keskinleştirir.
        :param image_data: Yüklenen resmin byte verisi.
        :return: Keskinleştirilmiş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data))
        sharpened_image = image.filter(ImageFilter.SHARPEN)

        output_buffer = BytesIO()
        sharpened_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def edge_detection(self, image_data):
        """
        Resimde kenar algılama işlemi yapar.
        :param image_data: Yüklenen resmin byte verisi.
        :return: Kenar algılanmış resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("L")  # Gri tonlamaya çevir
        edges = image.filter(ImageFilter.FIND_EDGES)

        output_buffer = BytesIO()
        edges.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer


    def pixelate_image(self, image_data, pixel_size=10):
        """
        Resme mozaik (pixelate) efekti uygular.
        :param image_data: Yüklenen resmin byte verisi.
        :param pixel_size: Mozaik boyutu (default: 10).
        :return: Mozaik efekti uygulanmış resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data))
        image = image.resize((image.width // pixel_size, image.height // pixel_size), Image.NEAREST)
        pixelated_image = image.resize((image.width * pixel_size, image.height * pixel_size), Image.NEAREST)

        output_buffer = BytesIO()
        pixelated_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def apply_basic_shadow(self, image_data, shadow_opacity=120, blur_radius=10, offset=(20, 20)):
        """
        Resmin altına sabit bir gölge ekler.
        
        :param image_data: Yüklenen resmin byte verisi.
        :param shadow_opacity: Gölge saydamlığı (0-255).
        :param blur_radius: Gölge yumuşatma miktarı.
        :param offset: Gölgenin kayma miktarı (x, y).
        :return: Gölge eklenmiş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        width, height = image.size

        # 🎭 Alfa kanalını alarak nesnenin dış hatlarını belirle
        alpha = image.split()[3]

        # 🖤 Siyah renkte gölge oluştur
        shadow = Image.new("RGBA", (width + offset[0], height + offset[1]), (0, 0, 0, 0))
        shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, shadow_opacity))
        shadow_layer.putalpha(alpha)

        # 📦 Gölgeyi arka plana yapıştır ve offset uygula
        shadow.paste(shadow_layer, offset, shadow_layer)

        # 🌫 Gaussian Blur ile gölgeyi yumuşat
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        # 🎨 Orijinal resmi gölgenin üstüne yapıştır
        combined = Image.new("RGBA", (width + offset[0], height + offset[1]), (0, 0, 0, 0))
        combined.paste(shadow, (0, 0), shadow)
        combined.paste(image, (0, 0), image)

        # 🔄 Sonucu byte formatına çevir
        output_buffer = BytesIO()
        combined.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def apply_realistic_shadow(self, image_data, light_angle=45, shadow_opacity=120, blur_radius=15, shadow_length=1.0):
        """
        Gerçekçi bir açıya göre gölge uygular ve gölge resim boyutlarını aşmaz.
        
        :param image_data: Yüklenen resmin byte verisi.
        :param light_angle: Işık açısı (derece).
        :param shadow_opacity: Gölge opaklığı (0-255).
        :param blur_radius: Gölgenin yumuşatma miktarı.
        :param shadow_length: Gölgenin uzama oranı.
        :return: Gerçekçi gölge eklenmiş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        width, height = image.size

        # 🎭 Alfa kanalını alarak nesnenin dış hatlarını belirle
        alpha = image.split()[3]

        # 🖤 Siyah gölge katmanı oluştur
        shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, shadow_opacity))
        shadow_layer.putalpha(alpha)

        # 🎯 Gölgenin yönünü ve uzamasını belirle
        angle_radians = np.radians(light_angle)
        x_offset = int(np.cos(angle_radians) * shadow_length * width)  # X ekseninde gölge uzaması
        y_offset = int(np.sin(angle_radians) * shadow_length * height)  # Y ekseninde gölge uzaması

        # 📐 Gölge matris dönüşümü uygula
        shadow = shadow_layer.transform(
            (width, height),  # Boyutlar orijinal resim boyutlarıyla sınırlandırılır
            Image.AFFINE,
            (
                1, np.tan(angle_radians), 0,  # X: ölçek, kaydırma
                0, 1, 0                       # Y: ölçek
            ),
            resample=Image.BICUBIC,
        )

        # 🌫 Gaussian Blur ile gölgeyi yumuşat
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        # 🎨 Resim ve gölgeyi aynı boyutta bir arka plana yerleştir
        combined = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        combined.paste(shadow, (0, 0), shadow)
        combined.paste(image, (0, 0), image)

        # 🔄 Sonucu byte formatına çevir
        output_buffer = BytesIO()
        combined.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer


    def standardize_aspect_ratio(self, image_data, target_width=500, target_height=500, background_color=(255, 255, 255)):
        """
        Resmin oranını standartlaştırır ve hedef boyutlara göre beyaz arka plan ekler.
        
        :param image_data: Yüklenen resmin byte verisi.
        :param target_width: Hedef genişlik.
        :param target_height: Hedef yükseklik.
        :param background_color: Arka plan rengi.
        :return: Standart oranlı resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        original_width, original_height = image.size

        # Yeni boyutları hesapla
        scale = min(target_width / original_width, target_height / original_height)
        new_width = int(original_width * scale)
        new_height = int(original_height * scale)
        resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # ANTIALIAS yerine LANCZOS

        # Hedef boyutta beyaz bir arka plan oluştur
        background = Image.new("RGBA", (target_width, target_height), background_color + (255,))
        paste_x = (target_width - new_width) // 2
        paste_y = (target_height - new_height) // 2
        background.paste(resized_image, (paste_x, paste_y), resized_image)

        # Sonucu döndür
        output_buffer = BytesIO()
        background.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer


    def remove_background_and_add_shadow(self, image_data, shadow_opacity=120, blur_radius=15, shadow_offset=(15, 15)):
        """
        Arka planı kaldırır ve ürüne gölge ekler.
        
        :param image_data: Yüklenen resmin byte verisi.
        :param shadow_opacity: Gölge saydamlığı.
        :param blur_radius: Gölge yumuşatma miktarı.
        :param shadow_offset: Gölgenin kayma miktarı.
        :return: Arka planı kaldırılmış ve gölge eklenmiş resmin byte verisi.
        """
        # 1️⃣ Arka planı kaldır
        no_bg_image = self.remove_background(image_data)

        # 2️⃣ Gölge ekle
        shadow_image = self.add_shadow(no_bg_image.getvalue())

        return shadow_image

    def generate_social_media_profile(self, image_data, background_color=(255, 255, 255)):
        """
        Yuvarlak sosyal medya profil fotoğrafı hazırlar.
        
        :param image_data: Yüklenen resmin byte verisi.
        :param background_color: Arka plan rengi.
        :return: Yuvarlak formatlı profil fotoğrafının byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        width, height = image.size
        size = min(width, height)

        # Kare format oluştur
        cropped_image = image.crop(((width - size) // 2, (height - size) // 2, (width + size) // 2, (height + size) // 2))

        # Yuvarlak maske oluştur
        mask = Image.new("L", (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)

        # Yuvarlak resmi beyaz arka planla birleştir
        output_image = Image.new("RGBA", (size, size), background_color + (255,))
        output_image.paste(cropped_image, (0, 0), mask)

        # Sonucu döndür
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer

    def remove_text(self, image_data):
        """
        OpenCV kullanarak metin alanlarını siler.
        
        :param image_data: Yüklenen resmin byte verisi.
        :return: Metinleri silinmiş resmin byte verisi.
        """
        # 1️⃣ Resmi yükle ve NumPy dizisine dönüştür
        image = Image.open(BytesIO(image_data)).convert("RGB")
        image_np = np.array(image)

        # 2️⃣ Gri tonlama ve kenar tespiti
        gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
        edges = cv2.Canny(gray, 50, 150)

        # 3️⃣ Metin bölgelerinin maskesini oluştur (kontur tespiti)
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mask = np.zeros_like(gray)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = w / h
            if 0.2 < aspect_ratio < 10:  # Uygun genişlik/yükseklik oranı
                cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        # 4️⃣ Orijinal görüntüde maskelenen alanları doldur
        inpainted = cv2.inpaint(image_np, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)

        # 5️⃣ Sonucu byte formatına çevir
        output_image = Image.fromarray(inpainted)
        output_buffer = BytesIO()
        output_image.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer