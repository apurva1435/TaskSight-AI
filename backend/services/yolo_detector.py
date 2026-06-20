from ultralytics import YOLO

# Load model once
model = YOLO("yolov8n.pt")


def detect_objects(image_path):

    results = model(image_path)

    detected_objects = []

    for result in results:

        for box in result.boxes:

            class_id = int(box.cls[0])

            class_name = model.names[class_id]

            confidence = float(box.conf[0])

            x1, y1, x2, y2 = box.xyxy[0].tolist()

            detected_objects.append({

                "label": class_name,

                "confidence": round(confidence, 2),

                "x1": int(x1),

                "y1": int(y1),

                "x2": int(x2),

                "y2": int(y2)

            })

    return detected_objects