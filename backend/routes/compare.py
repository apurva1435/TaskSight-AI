from fastapi import APIRouter, UploadFile, File, Form , Request

from utils.file_handler import save_uploaded_file

from services.blip_caption import generate_caption
from services.attention_visualizer import generate_attention_map

from services.experiment_logger import (
    save_experiment,
    save_human_attention
)

from services.task_runner import run_all_tasks

from services.yolo_detector import detect_objects

from services.yolo_visualizer import (
    generate_yolo_visualization
)

from services.overlay_visualizer import (
    generate_overlay_visualization
)

router = APIRouter()


def find_human_selected_object(
    human_x,
    human_y,
    human_width,
    human_height,
    detected_objects
):

    human_center_x = (
        human_x + human_width / 2
    )

    human_center_y = (
        human_y + human_height / 2
    )

    for obj in detected_objects:

        if (

            human_center_x >= obj["x1"]
            and human_center_x <= obj["x2"]

            and

            human_center_y >= obj["y1"]
            and human_center_y <= obj["y2"]

        ):

            return obj

    return None


def calculate_iou(

    human_x,
    human_y,
    human_width,
    human_height,

    object_box

):

    if not object_box:
        return 0

    hx1 = human_x
    hy1 = human_y

    hx2 = human_x + human_width
    hy2 = human_y + human_height

    ox1 = object_box["x1"]
    oy1 = object_box["y1"]

    ox2 = object_box["x2"]
    oy2 = object_box["y2"]

    inter_x1 = max(hx1, ox1)
    inter_y1 = max(hy1, oy1)

    inter_x2 = min(hx2, ox2)
    inter_y2 = min(hy2, oy2)

    intersection_width = max(
        0,
        inter_x2 - inter_x1
    )

    intersection_height = max(
        0,
        inter_y2 - inter_y1
    )

    intersection_area = (
        intersection_width *
        intersection_height
    )

    human_area = (
        human_width *
        human_height
    )

    object_area = (
        (ox2 - ox1) *
        (oy2 - oy1)
    )

    union_area = (

        human_area +

        object_area -

        intersection_area
    )

    if union_area == 0:
        return 0

    iou = intersection_area / union_area

    return round(
        iou * 100,
        2
    )


@router.post("/compare")
async def compare_models(

    request: Request,

    file: UploadFile = File(...),

    human_x: float = Form(0),
    human_y: float = Form(0),

    human_width: float = Form(0),
    human_height: float = Form(0),

    display_width: float = Form(0),
    display_height: float = Form(0)

):
    print("COMPARE ROUTE HIT")

    form = await request.form()

    print("RAW FORM DATA")
    print(form)
    print("END RAW FORM DATA")

    print("\n========== HUMAN BOX ==========")

    print("X:", human_x)
    print("Y:", human_y)

    print("WIDTH:", human_width)
    print("HEIGHT:", human_height)

    print("===============================\n")

    image_bytes = await file.read()

    file_path, unique_filename = save_uploaded_file(
        file,
        image_bytes
    )

    import cv2

    image = cv2.imread(file_path)

    actual_height, actual_width = image.shape[:2]

    print("ACTUAL WIDTH:", actual_width)
    print("ACTUAL HEIGHT:", actual_height)

    print("DISPLAY WIDTH:", display_width)
    print("DISPLAY HEIGHT:", display_height)

    caption_result = generate_caption(
        file_path
    )

    task_results = run_all_tasks(
        file_path
    )

    detected_objects = detect_objects(
        file_path
    )

    selected_object = find_human_selected_object(

        human_x,
        human_y,

        human_width,
        human_height,

        detected_objects
    )

    attention_output = generate_attention_map(
        file_path
    )

    yolo_output = generate_yolo_visualization(

        file_path,

        selected_object["label"]

        if selected_object

        else None
    )
    print("\nOVERLAY VALUES")

    print(human_x)
    print(human_y)

    print(human_width)
    print(human_height)

    print(selected_object)

    print("END OVERLAY\n")

    overlay_output = generate_overlay_visualization(

        file_path,

        human_x,
        human_y,

        human_width,
        human_height,

        selected_object
    )

    agreement_score = calculate_iou(

        human_x,
        human_y,

        human_width,
        human_height,

        selected_object
    )
    print("AGREEMENT SCORE =", agreement_score)

    experiment_id = save_experiment(

        image_name=unique_filename,

        question="Full Multi-Task Experiment",

        caption_result=caption_result,

        vqa_answer="Multiple Tasks Executed",

        attention_map=attention_output
    )

    save_human_attention(

        experiment_id=experiment_id,

        x=human_x,
        y=human_y,

        width=human_width,
        height=human_height
    )

    return {

        "experiment_id": experiment_id,

        "saved_filename": unique_filename,

        "attention_map": attention_output,

        "yolo_visualization": yolo_output,

        "overlay_visualization": overlay_output,

        "agreement_score": agreement_score,

        "caption": caption_result,

        "task_results": task_results,

        "human_attention": {

            "x": human_x,
            "y": human_y,

            "width": human_width,
            "height": human_height
        },

        "human_selected_object":

            selected_object["label"]

            if selected_object

            else "No Match",

        "detected_objects": detected_objects
    }