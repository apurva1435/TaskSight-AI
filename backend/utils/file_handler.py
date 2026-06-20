import uuid


def save_uploaded_file(file, image_bytes):

    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    # Create upload path
    file_path = f"../uploads/{unique_filename}"

    # Save image
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    return file_path, unique_filename