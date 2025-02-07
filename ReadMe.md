# Image Processing API Documentation

This API is a FastAPI application that provides various endpoints for image processing operations.

## Endpoints

### Background Operations

#### `POST /remove-bg/`
Removes the background from the uploaded image.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `width`: Output width (optional)
  - `height`: Output height (optional)

#### `POST /remove-bg-and-add-shadow/`
Removes the background and adds shadow to the image.
- **Parameters:**
  - `file`: Image file to upload (required)

### Shadow Effects

#### `POST /add-shadow/`
Adds shadow effect to the image.
- **Parameters:**
  - `file`: Image file to upload (required)

#### `POST /basic-shadow/`
Adds basic shadow effect.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `shadow_opacity`: Shadow opacity (default: 120)
  - `blur_radius`: Blur radius (default: 10)
  - `offset_x`: X-axis offset value (default: 20)
  - `offset_y`: Y-axis offset value (default: 20)

#### `POST /realistic-shadow/`
Adds realistic shadow based on light angle.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `light_angle`: Light angle (default: 45)
  - `shadow_opacity`: Shadow opacity (default: 120)
  - `blur_radius`: Blur radius (default: 15)
  - `shadow_length`: Shadow length (default: 1.0)

### Filtering and Effects

#### `POST /apply-filter/`
Applies various filters to the image.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `filter_type`: Filter type (default: "grayscale")
    - Supported filters: sepia, grayscale, negative

#### `POST /sketch-effect/`
Converts the image to a sketch effect.
- **Parameters:**
  - `file`: Image file to upload (required)

#### `POST /pixelate/`
Applies mosaic (pixelate) effect to the image.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `pixel_size`: Pixel size (default: 10)

### Resizing and Rotation

#### `POST /resize-image/`
Resizes the image to specified dimensions.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `width`: Target width (required)
  - `height`: Target height (required)

#### `POST /rotate-image/`
Rotates the image by specified angle.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `angle`: Rotation angle (required)

#### `POST /standardize-aspect-ratio/`
Standardizes the aspect ratio of the image.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `target_width`: Target width (default: 500)
  - `target_height`: Target height (default: 500)

### Cropping and Editing

#### `POST /crop/`
Crops the image from specified coordinates.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `left`: Left edge coordinate (default: 0)
  - `top`: Top edge coordinate (default: 0)
  - `right`: Right edge coordinate (default: 100)
  - `bottom`: Bottom edge coordinate (default: 100)

#### `POST /sharpen/`
Sharpens the image.
- **Parameters:**
  - `file`: Image file to upload (required)

### Text Operations

#### `POST /add-text/`
Adds text to the image.
- **Parameters:**
  - `file`: Image file to upload (required)
  - `text`: Text to add (default: "Test")
  - `x`: X coordinate (default: 10)
  - `y`: Y coordinate (default: 10)
  - `font_size`: Font size (default: 30)

#### `POST /remove-text/`
Detects and removes text areas from the image.
- **Parameters:**
  - `file`: Image file to upload (required)

### Special Operations

#### `POST /edge-detection/`
Performs edge detection on the image.
- **Parameters:**
  - `file`: Image file to upload (required)

#### `POST /generate-social-profile/`
Creates a round social media profile picture.
- **Parameters:**
  - `file`: Image file to upload (required)

## General Notes

- All endpoints use POST method
- Image files should be sent in multipart/form-data format
- All operations return images in PNG format
- Operations are performed asynchronously
- In case of errors, appropriate HTTP status codes are returned with error messages