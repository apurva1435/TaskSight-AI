def get_task_prompt(task_type):

    prompts = {

        "scene_understanding":
        "Describe the complete scene in the image.",

        "object_counting":
        "How many important objects or animals are visible?",

        "risk_detection":
        "Are there any dangerous or risky elements in the image?",

        "spatial_reasoning":
        "Describe the spatial arrangement of important objects."
    }

    return prompts.get(
        task_type,
        "Describe the image."
    )