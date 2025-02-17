# Python 3.13 minimal imajı
FROM python:3.13-slim

# Çalışma dizinini belirle
WORKDIR /app

# Gerekli sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    libgl1-mesa-glx \
    libglib2.0-0 \
    imagemagick \
    libmagickwand-dev \
    libgomp1 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# ImageMagick politika ayarlarını güncelle (güvenlik kısıtlamalarını kaldır)
RUN if [ -f /etc/ImageMagick-6/policy.xml ]; then \
    sed -i 's/<policy domain="coder" rights="none" pattern="PDF" \/>/<policy domain="coder" rights="read|write" pattern="PDF" \/>/' /etc/ImageMagick-6/policy.xml; \
    fi

# Bağımlılıkları yükle
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Uygulama kodlarını kopyala
COPY . .

# Uvicorn ile FastAPI başlat
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
