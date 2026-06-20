from transformers import (
    BlipProcessor,
    BlipForConditionalGeneration
)

from PIL import Image

# Load processor and model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)


def generate_caption(image_path):

    # Open image
    image = Image.open(image_path).convert("RGB")

    # Process image
    inputs = processor(
        image,
        return_tensors="pt"
    )

    # Generate output
    output = model.generate(**inputs)

    # Decode caption
    caption = processor.decode(
        output[0],
        skip_special_tokens=True
    )

    return caption