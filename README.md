# OpenCV Color Object Detector

A beginner-friendly computer vision project that detects objects based on their color using Python, OpenCV, and HSV segmentation.

The application creates a color mask, cleans it with morphological operations, isolates matching objects, and draws bounding boxes around detected regions.

## Features

- Load an image from disk
- Convert an image from BGR to HSV
- Select pixels within a specified HSV color range
- Generate a binary color mask
- Remove small noise using morphological opening
- Fill small gaps using morphological closing
- Isolate matching colored objects
- Find object contours
- Ignore regions below a minimum area
- Draw bounding boxes and labels
- Count detected objects
- Display each processing stage
- Save processed images

## Processing Pipeline

```text
Original image
      ↓
Convert BGR to HSV
      ↓
Apply lower and upper HSV limits
      ↓
Create binary color mask
      ↓
Morphological opening and closing
      ↓
      ├── Isolate matching colors
      └── Find contours
               ↓
        Filter by contour area
               ↓
     Draw labels and bounding boxes
```

## Project Structure

```text
opencv-color-object-detector/
├── images/
│   └── colored_objects.jpg
├── output/
│   └── .gitkeep
├── .gitignore
├── color_detector.py
├── main.py
├── README.md
└── requirements.txt
```

- `color_detector.py` contains reusable detection functions.
- `main.py` runs the complete detection pipeline.
- `images/` contains input images.
- `output/` contains generated results and is ignored by Git.

## How HSV Color Detection Works

HSV represents colors using three components:

| Channel | OpenCV range | Meaning |
|---|---:|---|
| Hue | `0–179` | The basic color |
| Saturation | `0–255` | The intensity or purity of the color |
| Value | `0–255` | The brightness of the color |

HSV is generally more convenient for color segmentation than BGR because the color information is primarily represented by the Hue channel.

The detector uses `cv2.inRange()` to select pixels between lower and upper HSV boundaries:

```python
mask = cv2.inRange(
    hsv_image,
    lower_bound,
    upper_bound,
)
```

Pixels inside the specified range become white in the mask. All other pixels become black.

## Default Green Range

The initial version detects green objects using:

```python
lower_green = (35, 50, 50)
upper_green = (85, 255, 255)
```

These values are approximate. The ideal range depends on:

- The object's exact shade
- Lighting conditions
- Shadows
- Camera exposure
- Background colors

## Requirements

- Python 3.9 or later
- OpenCV
- NumPy
- Matplotlib

## Installation

Clone the repository:

```bash
git clone https://github.com/bhumikapandey05/opencv-color-object-detector.git
cd opencv-color-object-detector
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it on macOS or Linux:

```bash
source .venv/bin/activate
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Add an image containing a green object to the `images/` directory and name it:

```text
colored_objects.jpg
```

Run the detector:

```bash
python3 main.py
```

The application displays:

1. Original image
2. Cleaned color mask
3. Isolated colored objects
4. Image with bounding boxes and labels

Generated images are saved inside the `output/` directory.

## Example

```python
from color_detector import (
    clean_mask,
    create_color_mask,
    draw_bounding_boxes,
    isolate_color,
    load_image,
)

image = load_image("images/colored_objects.jpg")

mask = create_color_mask(
    image,
    lower_hsv=(35, 50, 50),
    upper_hsv=(85, 255, 255),
)

cleaned_mask = clean_mask(mask, kernel_size=5)
isolated = isolate_color(image, cleaned_mask)

annotated, object_count = draw_bounding_boxes(
    image,
    cleaned_mask,
    minimum_area=500,
)

print(f"Detected objects: {object_count}")
```

## Example HSV Ranges

These ranges are useful starting points and may require adjustment.

### Blue

```python
lower_blue = (90, 50, 50)
upper_blue = (130, 255, 255)
```

### Green

```python
lower_green = (35, 50, 50)
upper_green = (85, 255, 255)
```

### Yellow

```python
lower_yellow = (20, 100, 100)
upper_yellow = (35, 255, 255)
```

## Detecting Red

Red appears at both ends of OpenCV's Hue range, so detecting it normally requires two masks:

```python
lower_red_1 = (0, 100, 100)
upper_red_1 = (10, 255, 255)

lower_red_2 = (170, 100, 100)
upper_red_2 = (179, 255, 255)
```

Create and combine the masks:

```python
mask_1 = create_color_mask(
    image,
    lower_red_1,
    upper_red_1,
)

mask_2 = create_color_mask(
    image,
    lower_red_2,
    upper_red_2,
)

red_mask = cv2.bitwise_or(mask_1, mask_2)
```

## Morphological Cleanup

The raw mask may contain isolated pixels or small gaps.

### Opening

Opening applies erosion followed by dilation. It removes small white regions that are likely noise.

### Closing

Closing applies dilation followed by erosion. It fills small black gaps inside detected objects.

The project applies both operations:

```python
cleaned_mask = clean_mask(
    raw_mask,
    kernel_size=5,
)
```

## Minimum Object Area

Small detected regions are ignored using:

```python
minimum_area=500
```

Increasing this value ignores more small regions:

```python
annotated, count = draw_bounding_boxes(
    image,
    mask,
    minimum_area=1000,
)
```

Decreasing it allows smaller objects to be detected.

## Output Files

The program generates:

```text
output/
├── mask.jpg
├── isolated.jpg
└── detected.jpg
```

These generated images are excluded from Git through `.gitignore`.

## Limitations

Color-based detection can be affected by:

- Uneven lighting
- Strong shadows
- Reflections
- Similar background colors
- Low color saturation
- Objects containing multiple shades
- Incorrect HSV boundaries

Color detection identifies matching pixels; it does not understand the object's identity. For example, it can find green regions but cannot determine whether the region is a bottle, ball, or plant.

## What I Learned

This project demonstrates:

- The difference between BGR and HSV color spaces
- How HSV ranges describe colors
- How to create a binary color mask
- How morphological operations clean masks
- How to isolate image regions using bitwise operations
- How contours identify separate regions
- How contour area filters small detections
- How to calculate and draw bounding boxes
- How lighting affects color segmentation

## Planned Improvements

- Add interactive HSV trackbars
- Allow users to select a target color
- Support red using two Hue ranges
- Add webcam and video input
- Display object coordinates
- Track objects between frames
- Save HSV presets
- Add command-line image selection
- Add automated tests
- Build a graphical user interface

## License

This project is intended for educational and portfolio purposes.