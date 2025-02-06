# Image Processing API Documentation

This API provides a wide range of image processing services, including background removal, filtering, resizing, text addition, sharpening, cropping, and shadow effects. It is designed for developers and businesses who need to process images dynamically through an API interface.

## Usage
API requests should be made using **multipart form-data** with file uploads. The response will be a processed image in PNG format.

### POST /remove-bg/
Removes the background from an uploaded image, making it transparent.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `width` (int, optional) - The desired output width.
- `height` (int, optional) - The desired output height.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/remove-bg/" -F "file=@image.png"
```

### POST /add-shadow/
Adds a virtual shadow effect to the uploaded image for a more realistic appearance.

**Parameters:**
- `file` (UploadFile) - The image to be processed.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/add-shadow/" -F "file=@image.png"
```

### POST /apply-filter/
Applies different filters such as **grayscale**, **sepia**, or **negative** to an image.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `filter_type` (str) - The filter type to apply (**grayscale**, **sepia**, **negative**).

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/apply-filter/" -F "file=@image.png" -F "filter_type=grayscale"
```

### POST /resize-image/
Resizes an image to specified dimensions while maintaining aspect ratio.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `width` (int) - The target width.
- `height` (int) - The target height.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/resize-image/" -F "file=@image.png" -F "width=500" -F "height=500"
```

### POST /add-text/
Adds custom text to an image with specified positioning and font size.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `text` (str) - The text to be added.
- `x` (int) - X coordinate position.
- `y` (int) - Y coordinate position.
- `font_size` (int) - Font size.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/add-text/" -F "file=@image.png" -F "text=Hello" -F "x=50" -F "y=50" -F "font_size=30"
```

### POST /sharpen/
Enhances the sharpness of an image to improve its clarity.

**Parameters:**
- `file` (UploadFile) - The image to be processed.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/sharpen/" -F "file=@image.png"
```

### POST /remove-text/
Automatically detects and removes text from an image using advanced image processing.

**Parameters:**
- `file` (UploadFile) - The image to be processed.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/remove-text/" -F "file=@image.png"
```

### POST /crop/
Crops an image based on the specified coordinates.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `left` (int) - Left coordinate.
- `top` (int) - Top coordinate.
- `right` (int) - Right coordinate.
- `bottom` (int) - Bottom coordinate.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/crop/" -F "file=@image.png" -F "left=10" -F "top=20" -F "right=100" -F "bottom=200"
```

### POST /pixelate/
Applies a pixelation effect to an image for privacy or artistic purposes.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `pixel_size` (int, optional) - The size of pixels (default: 10).

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/pixelate/" -F "file=@image.png" -F "pixel_size=20"
```

### POST /rotate-image/
Rotates an image by a given angle while preserving its quality.

**Parameters:**
- `file` (UploadFile) - The image to be processed.
- `angle` (int) - Rotation angle in degrees.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/rotate-image/" -F "file=@image.png" -F "angle=90"
```

### POST /enhance-for-listing/
Optimizes an image for product listings by enhancing contrast and removing noise.

**Parameters:**
- `file` (UploadFile) - The image to be processed.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/enhance-for-listing/" -F "file=@image.png"
```

### POST /generate-social-profile/
Creates a round profile picture for social media platforms by cropping and centering the image.

**Parameters:**
- `file` (UploadFile) - The image to be processed.

**Example Usage:**
```sh
curl -X POST "http://127.0.0.1:8000/generate-social-profile/" -F "file=@image.png"
```

This API enables seamless and efficient image processing operations for a wide range of applications, from social media profile picture adjustments to e-commerce product image enhancements.

# 🏪 Enhance for Listing API

This API optimizes an image for product listings by enhancing contrast, removing noise, and improving clarity for better visibility on e-commerce platforms.

## 📌 Endpoint
### `POST /enhance-for-listing/`
Optimizes an image for product listings.

## 🔹 Parameters:
- `file` (UploadFile) - The image to be processed.

## 📤 Example Usage:
```sh
curl -X POST "http://127.0.0.1:8000/enhance-for-listing/" -F "file=@product_image.png"
