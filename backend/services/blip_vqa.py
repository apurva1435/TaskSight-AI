from transformers import BlipProcessor, BlipForQuestionAnswering
from PIL import Image

# Load processor and model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-vqa-base"
)

model = BlipForQuestionAnswering.from_pretrained(
    "Salesforce/blip-vqa-base"
)


def generate_answer(image_path, question):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Process image + question
    inputs = processor(
        image,
        question,
        return_tensors="pt"
    )

    # Generate output
    output = model.generate(**inputs)

    # Decode answer
    answer = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return answer