from services.task_prompts import get_task_prompt
from services.blip_vqa import generate_answer


def run_all_tasks(image_path):

    tasks = [
        "scene_understanding",
        "object_counting",
        "risk_detection",
        "spatial_reasoning"
    ]

    results = {}

    for task in tasks:

        prompt = get_task_prompt(task)

        answer = generate_answer(
            image_path,
            prompt
        )

        results[task] = {
            "prompt": prompt,
            "answer": answer
        }

    return results