import sqlite3


class Library:
    def __init__(self):
        self.profile = None

    def student_profile(self, id):
        try:
            with sqlite3.connect("library.db") as connection:
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM individualData WHERE Id = ?", (id,))
                self.profile = cursor.fetchone()
        except sqlite3.Error as error:
            print(f"An error occurred: {error}")
        return self.profile
