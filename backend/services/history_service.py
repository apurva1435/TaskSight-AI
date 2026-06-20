from database import cursor


def get_all_experiments():

    cursor.execute("""

    SELECT
        id,
        image_name,
        question,
        caption_result,
        vqa_answer,
        attention_map

    FROM experiments

    ORDER BY id DESC

    """)

    rows = cursor.fetchall()

    experiments = []

    for row in rows:

        experiments.append({

            "id": row[0],

            "image_name": row[1],

            "question": row[2],

            "caption_result": row[3],

            "vqa_answer": row[4],

            "attention_map": row[5]
        })

    return experiments

from database import conn


def delete_experiment(experiment_id):

    cursor.execute(
        """
        DELETE FROM experiments
        WHERE id = ?
        """,
        (experiment_id,)
    )

    conn.commit()