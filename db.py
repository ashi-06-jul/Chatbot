
import sqlite3


class DB:
    def __init__(self, dbname="details.sqlite"):
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname)

    def setup(self):
        stmt = "CREATE TABLE INFO(city text, pincode integer, standard text, board text, medium text, subjects text, number integer, email text, req text, confirm text)"
        self.conn.execute(stmt)
        self.conn.commit()

    def add_item(self, City, Pincode, Standard, Board, Medium, Subjects, Number, Email, Req, Confirm):
        stmt = "INSERT INTO INFO (city, pincode, standard, board, medium, subjects, number, email, req, confirm) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
        args = (City, Pincode, Standard, Board, Medium, Subjects, Number, Email, Req, Confirm)
        self.conn.execute(stmt, args)
        self.conn.commit()

    def delete_item(self, item_text):
        stmt = "DELETE FROM items WHERE description = (?)"
        args = (item_text, )
        self.conn.execute(stmt, args)
        self.conn.commit()

    def get_items(self):
        stmt = "SELECT * FROM INFO"
        return [x[0] for x in self.conn.execute(stmt)]