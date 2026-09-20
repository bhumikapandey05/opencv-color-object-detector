from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import numpy as np

from color_detector import (
    clean_mask,
    create_color_mask,
    draw_bounding_boxes,
    isolate_color,
    load_image,
    save_image,
)


def prepare_for_display(image: np.ndarray) -> np.ndarray:
    """Convert BGR images to RGB for Matplotlib."""
    if image.ndim == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    return image


def display_results(
    images: list[np.ndarray],
    titles: list[str],
) -> None:
    """Display detection stages together."""
    _, axes = plt.subplots(2, 2, figsize=(12, 9))

    for axis, image, title in zip(axes.flat, images, titles):
        axis.imshow(prepare_for_display(image), cmap="gray")
        axis.set_title(title)
        axis.axis("off")

    plt.tight_layout()
    plt.show()


def main() -> None:
    image_path = Path("images/colored_objects.jpg")
    output_directory = Path("output")

    # Approximate HSV range for green.
    lower_green = (35, 50, 50)
    upper_green = (85, 255, 255)

    original = load_image(str(image_path))

    raw_mask = create_color_mask(
        original,
        lower_green,
        upper_green,
    )

    cleaned_mask = clean_mask(
        raw_mask,
        kernel_size=5,
    )

    isolated = isolate_color(
        original,
        cleaned_mask,
    )

    annotated, object_count = draw_bounding_boxes(
        original,
        cleaned_mask,
        minimum_area=500,
    )

    display_results(
        [original, cleaned_mask, isolated, annotated],
        [
            "Original",
            "Green Mask",
            "Isolated Green Objects",
            f"Detected Objects: {object_count}",
        ],
    )

    results = {
        "mask.jpg": cleaned_mask,
        "isolated.jpg": isolated,
        "detected.jpg": annotated,
    }

    for filename, image in results.items():
        save_image(image, output_directory / filename)

    print(f"Detected green objects: {object_count}")
    print(f"Results saved in: {output_directory}")


if __name__ == "__main__":
    main()