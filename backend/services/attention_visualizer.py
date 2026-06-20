import cv2
import numpy as np
import uuid


def generate_attention_map(image_path):

    # Read image
    image = cv2.imread(image_path)

    # Resize image
    image = cv2.resize(image, (500, 500))

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Create heatmap
    heatmap = cv2.applyColorMap(
        gray,
        cv2.COLORMAP_JET
    )

    # Blend original image + heatmap
    blended = cv2.addWeighted(
        image,
        0.6,
        heatmap,
        0.4,
        0
    )

    # Unique output filename
    output_filename = f"{uuid.uuid4()}_attention.jpg"

    output_path = f"../outputs/{output_filename}"

    # Save output image
    cv2.imwrite(output_path, blended)

    return output_filename