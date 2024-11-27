import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()


def save_to_history(file_path, datetime, file_name):
    cur.execute(
        "INSERT OR REPLACE INTO history(file_name, datetime, abs_file_path) VALUES(?, ?, ?)",
        (file_name, datetime, file_path),
    )
    con.commit()


def get_history():
    return cur.execute("SELECT * FROM history").fetchall()
