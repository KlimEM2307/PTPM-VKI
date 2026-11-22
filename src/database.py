import sqlite3


class TriangleDatabase:
    """Класс работы с БД SQLite."""

    def __init__(self, db_path=":memory:"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS triangles (
                side1 REAL NOT NULL,
                side2 REAL NOT NULL,
                side3 REAL NOT NULL,
                triangle_type TEXT NOT NULL,
                error_message TEXT,
                PRIMARY KEY (side1, side2, side3)
            )
            """
        )
        self.conn.commit()

    def add(self, side1, side2, side3, triangle_type, error_message=None):
        self.conn.execute(
            "INSERT OR REPLACE INTO triangles VALUES (?, ?, ?, ?, ?)",
            (side1, side2, side3, triangle_type, error_message),
        )
        self.conn.commit()

    def get(self, side1, side2, side3):
        cur = self.conn.execute(
            "SELECT triangle_type, error_message FROM triangles "
            "WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (side1, side2, side3),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return {"triangle_type": row[0], "error_message": row[1]}

    def delete(self, side1, side2, side3):
        self.conn.execute(
            "DELETE FROM triangles WHERE side1 = ? AND side2 = ? AND side3 = ?",
            (side1, side2, side3),
        )
        self.conn.commit()

    def close(self):
        self.conn.close()