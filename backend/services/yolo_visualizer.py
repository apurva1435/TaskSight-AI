import cv2
import uuid

from services.yolo_detector import detect_objects


def generate_yolo_visualization(
    image_path,
    selected_label=None
):

    image = cv2.imread(image_path)

    objects = detect_objects(image_path)

    selected_highlighted = False

    for obj in objects:

        x1 = int(obj["x1"])
        y1 = int(obj["y1"])

        x2 = int(obj["x2"])
        y2 = int(obj["y2"])

        label = obj["label"]

        if (
            selected_label
            and
            label == selected_label
            and
            not selected_highlighted
        ):

            color = (0, 0, 255)

            display_text = (
                f"SELECTED: {label}"
            )

            selected_highlighted = True

        else:

            color = (0, 255, 0)

            display_text = label

        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            color,
            2
        )

        cv2.putText(
            image,
            display_text,
            (x1, max(y1 - 10, 20)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            color,
            2
        )

    output_filename = (
        f"{uuid.uuid4()}_yolo.jpg"
    )

    output_path = (
        f"../outputs/{output_filename}"
    )

    cv2.imwrite(
        output_path,
        image
    )

    return output_filename