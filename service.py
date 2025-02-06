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

    def apply_advanced_perspective_shadow(self, image_data, shadow_angle=45, shadow_opacity=100, blur_radius=25, shadow_scale=1.5):
        """
        3D açısal perspektif gölgesi ekler.
        :param image_data: Yüklenen resmin byte verisi.
        :param shadow_angle: Gölgenin açısı (derece cinsinden).
        :param shadow_opacity: Gölge saydamlığı (0-255).
        :param blur_radius: Gölgenin yumuşatma yarıçapı.
        :param shadow_scale: Gölgenin uzama oranı.
        :return: Perspektif gölge eklenmiş resmin byte verisi.
        """
        image = Image.open(BytesIO(image_data)).convert("RGBA")
        width, height = image.size

        # 🎭 Alfa kanalını alarak nesnenin dış hatlarını belirle
        alpha = image.split()[3]

        # 🖤 Siyah gölge katmanı oluştur
        shadow_layer = Image.new("RGBA", image.size, (0, 0, 0, shadow_opacity))
        shadow_layer.putalpha(alpha)

        # 📏 Perspektif matris dönüşümüyle gölgeyi uzat
        shadow = shadow_layer.transform(
            (int(width * shadow_scale), int(height * shadow_scale)),
            Image.AFFINE,
            (
                1, np.tan(np.radians(shadow_angle)), 0,
                0, 1, height * 0.5  # Daha geniş bir taban için
            ),
            resample=Image.BICUBIC,
        )

        # 🌫 Gaussian Blur ile gölgeyi yumuşat
        shadow = shadow.filter(ImageFilter.GaussianBlur(blur_radius))

        # 🖼 Gölgeyi arka plana yerleştir
        shadow_background = Image.new("RGBA", (int(width * shadow_scale), int(height * shadow_scale)), (0, 0, 0, 0))
        shadow_background.paste(shadow, (0, int(height * 0.3)), shadow)

        # 🎨 Orijinal resmi gölgenin üstüne yerleştir
        shadow_background.paste(image, (0, 0), image)

        # 🔄 Sonucu byte formatına çevir
        output_buffer = BytesIO()
        shadow_background.save(output_buffer, format="PNG")
        output_buffer.seek(0)

        return output_buffer
