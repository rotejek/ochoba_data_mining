import psycopg2


class DataBaseWrapper:
    def __init__(self, config):
        self.conn = psycopg2.connect(host=config["host"],
                                     port=config["port"],
                                     database=config["database"],
                                     user=config["user"],
                                     password=config["password"])
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def commit(self):
        self.conn.commit()

    def execute_insert(self, query, values):
        self.cursor.execute(query, values)

    def execute_select(self, query, values):
        self.cursor.execute(query, values)
        return self.cursor.fetchall()

    def execute_update(self, query, values):
        self.cursor.execute(query, values)