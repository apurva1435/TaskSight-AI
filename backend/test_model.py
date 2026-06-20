from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load processor and model
processor = BlipProcessor.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

model = BlipForConditionalGeneration.from_pretrained(
    "Salesforce/blip-image-captioning-base"
)

# Load local image
raw_image = Image.open("../images/test.jpg").convert("RGB")

# Process image
inputs = processor(raw_image, return_tensors="pt")

# Generate caption
out = model.generate(**inputs)

# Decode output
caption = processor.decode(out[0], skip_special_tokens=True)

print("\nAI Caption:")
print(caption)