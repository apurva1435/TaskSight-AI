import cv2
import uuid


def generate_overlay_visualization(

    image_path,

    human_x,
    human_y,

    human_width,
    human_height,

    selected_object

):

    image = cv2.imread(image_path)
    print("IMAGE SHAPE:", image.shape)

    hx1 = int(human_x)
    hy1 = int(human_y)

    hx2 = int(human_x + human_width)
    hy2 = int(human_y + human_height)
    print("HUMAN BOX")

    print(hx1, hy1)
    print(hx2, hy2)

    if selected_object:

        ax1 = int(selected_object["x1"])
        ay1 = int(selected_object["y1"])

        ax2 = int(selected_object["x2"])
        ay2 = int(selected_object["y2"])

        print("AI BOX")

        print(ax1, ay1)
        print(ax2, ay2)

    cv2.rectangle(
        image,
        (hx1, hy1),
        (hx2, hy2),
        (0, 0, 255),
        3
    )

    cv2.putText(
        image,
        "HUMAN",
        (hx1, max(20, hy1 - 10)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 0, 255),
        2
    )

    if selected_object:

        ax1 = int(selected_object["x1"])
        ay1 = int(selected_object["y1"])

        ax2 = int(selected_object["x2"])
        ay2 = int(selected_object["y2"])

        cv2.rectangle(
            image,
            (ax1, ay1),
            (ax2, ay2),
            (0, 255, 0),
            3
        )

        cv2.putText(
            image,
            "AI",
            (ax1, max(20, ay1 - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )

    output_filename = (
        f"{uuid.uuid4()}_overlay.jpg"
    )

    output_path = (
        f"../outputs/{output_filename}"
    )

    cv2.imwrite(
        output_path,
        image
    )

    return output_filename