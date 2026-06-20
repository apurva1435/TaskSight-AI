from services.yolo_detector import detect_objects

objects = detect_objects("../images/test2.jpg")

print("\nDetected Objects:\n")

for obj in objects:
    print(obj)