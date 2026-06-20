import sqlite3

conn = sqlite3.connect(
    "tasksight.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS experiments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    image_name TEXT,

    question TEXT,

    caption_result TEXT,

    vqa_answer TEXT,

    attention_map TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS human_attention (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    experiment_id INTEGER,

    x REAL,

    y REAL,

    width REAL,

    height REAL,

    FOREIGN KEY(experiment_id)
    REFERENCES experiments(id)
)
""")

conn.commit()