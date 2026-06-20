from database import conn, cursor


def save_experiment(
    image_name,
    question,
    caption_result,
    vqa_answer,
    attention_map
):

    cursor.execute("""

    INSERT INTO experiments (
        image_name,
        question,
        caption_result,
        vqa_answer,
        attention_map
    )

    VALUES (?, ?, ?, ?, ?)

    """, (

        image_name,
        question,
        caption_result,
        vqa_answer,
        attention_map
    ))

    conn.commit()

    return cursor.lastrowid


def save_human_attention(
    experiment_id,
    x,
    y,
    width,
    height
):

    cursor.execute("""

    INSERT INTO human_attention (

        experiment_id,
        x,
        y,
        width,
        height

    )

    VALUES (?, ?, ?, ?, ?)

    """, (

        experiment_id,
        x,
        y,
        width,
        height
    ))

    conn.commit()
    return cursor.lastrowid