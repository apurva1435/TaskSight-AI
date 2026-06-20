from fastapi import APIRouter, UploadFile, File, Form

from utils.file_handler import save_uploaded_file

from services.blip_vqa import generate_answer
from services.blip_caption import generate_caption

router = APIRouter()


@router.post("/analyze")
async def analyze_image(
    file: UploadFile = File(...),
    question: str = Form(None),
    model_name: str = Form(...)
):

    # Read uploaded image
    image_bytes = await file.read()

    # Save uploaded file
    file_path, unique_filename = save_uploaded_file(
        file,
        image_bytes
    )

    # BLIP VQA
    if model_name == "blip_vqa":

        answer = generate_answer(
            file_path,
            question
        )

        return {
            "model": "BLIP VQA",
            "question": question,
            "answer": answer,
            "saved_filename": unique_filename
        }

    # BLIP Captioning
    elif model_name == "blip_caption":

        caption = generate_caption(file_path)

        return {
            "model": "BLIP Captioning",
            "caption": caption,
            "saved_filename": unique_filename
        }

    # Invalid model
    return {
        "error": "Invalid model selected"
    }