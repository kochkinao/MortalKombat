import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.connection_cursor = self.connection.cursor()
        self.cursor = self.connection_cursor

    async def add_plus(self,):
        with self.connection:
            count_plus = self.cursor.execute("SELECT plus FROM statistics WHERE id = 1").fetchall()[0][0]
            count_plus = int(count_plus) + 1
            self.cursor.execute("UPDATE statistics SET plus = ? WHERE id = 1", (count_plus, ))

    async def add_minus(self,):
        with self.connection:
            count_minus = self.cursor.execute("SELECT minus FROM statistics WHERE id = 1").fetchall()[0][0]
            count_minus = int(count_minus) + 1
            self.cursor.execute("UPDATE statistics SET minus = ? WHERE id = 1", (count_minus, ))

    async def get_plus(self):
        with self.connection:
            return self.cursor.execute("SELECT plus FROM statistics").fetchall()[0][0]

    async def get_minus(self):
        with self.connection:
            return self.cursor.execute("SELECT minus FROM statistics").fetchall()[0][0]

    async def add_plus_zb(self,):
        with self.connection:
            count_plus = self.cursor.execute("SELECT plus_zb FROM statistics WHERE id = 1").fetchall()[0][0]
            count_plus = int(count_plus) + 1
            self.cursor.execute("UPDATE statistics SET plus_zb = ? WHERE id = 1", (count_plus, ))

    async def add_minus_zb(self,):
        with self.connection:
            count_minus = self.cursor.execute("SELECT minus_zb FROM statistics WHERE id = 1").fetchall()[0][0]
            count_minus = int(count_minus) + 1
            self.cursor.execute("UPDATE statistics SET minus_zb = ? WHERE id = 1", (count_minus, ))

    async def get_plus_zb(self):
        with self.connection:
            return self.cursor.execute("SELECT plus_zb FROM statistics").fetchall()[0][0]

    async def get_minus_zb(self):
        with self.connection:
            return self.cursor.execute("SELECT minus_zb FROM statistics").fetchall()[0][0]

    async def get_balance(self):
        with self.connection:
            return self.cursor.execute("SELECT balance FROM statistics").fetchall()[0][0]

    async def set_balance(self, money):
        with self.connection:
            balance = self.cursor.execute("SELECT balance FROM statistics").fetchall()[0][0]
            balance += money
            self.cursor.execute("UPDATE statistics SET balance = ? WHERE id = 1", (balance,))

    async def clear(self):
        with self.connection:
            self.cursor.execute("UPDATE statistics SET plus = 0 WHERE id = 1")
            self.cursor.execute("UPDATE statistics SET minus = 0 WHERE id = 1")
            self.cursor.execute("UPDATE statistics SET plus_zb = 0 WHERE id = 1")
            self.cursor.execute("UPDATE statistics SET minus_zb = 0 WHERE id = 1")
            self.cursor.execute("UPDATE statistics SET balance = 10000 WHERE id = 1")