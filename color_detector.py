from pathlib import Path

import cv2
import numpy as np


def load_image(image_path: str) -> np.ndarray:
    """Load an image from disk."""
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(f"Image not found: {image_path}")

    return image


def create_color_mask(
    image: np.ndarray,
    lower_hsv: tuple[int, int, int],
    upper_hsv: tuple[int, int, int],
) -> np.ndarray:
    """Create a binary mask for pixels inside an HSV range."""
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower_bound = np.array(lower_hsv, dtype=np.uint8)
    upper_bound = np.array(upper_hsv, dtype=np.uint8)

    return cv2.inRange(
        hsv_image,
        lower_bound,
        upper_bound,
    )


def clean_mask(
    mask: np.ndarray,
    kernel_size: int = 5,
) -> np.ndarray:
    """Remove small noise and fill gaps in a binary mask."""
    kernel = np.ones(
        (kernel_size, kernel_size),
        dtype=np.uint8,
    )

    opened_mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel,
    )

    return cv2.morphologyEx(
        opened_mask,
        cv2.MORPH_CLOSE,
        kernel,
    )


def isolate_color(
    image: np.ndarray,
    mask: np.ndarray,
) -> np.ndarray:
    """Keep only the image pixels selected by the mask."""
    return cv2.bitwise_and(
        image,
        image,
        mask=mask,
    )


def draw_bounding_boxes(
    image: np.ndarray,
    mask: np.ndarray,
    minimum_area: float = 500,
) -> tuple[np.ndarray, int]:
    """Draw bounding boxes around detected color regions."""
    annotated_image = image.copy()

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )

    detected_objects = 0

    for contour in contours:
        area = cv2.contourArea(contour)

        if area < minimum_area:
            continue

        x, y, width, height = cv2.boundingRect(contour)

        cv2.rectangle(
            annotated_image,
            (x, y),
            (x + width, y + height),
            (0, 255, 0),
            3,
        )

        cv2.putText(
            annotated_image,
            f"Green object: {area:.0f}px",
            (x, max(y - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        detected_objects += 1

    return annotated_image, detected_objects


def save_image(image: np.ndarray, output_path: Path) -> None:
    """Save an image, creating the output directory if needed."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if not cv2.imwrite(str(output_path), image):
        raise OSError(f"Could not save image: {output_path}")