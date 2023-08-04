import mysql.connector

import config


class Conector:
    def __init__(self):
        self._is_connected = False
        try:
            self.conn = mysql.connector.connect(
                host=config.credenciales['host'],
                user=config.credenciales['user'],
                password=config.credenciales['password'],
                port=config.credenciales['port'],
                database=config.credenciales['database']
            )
            self._cursor = self.conn.cursor()
            self._is_connected = True
        except mysql.connector.Error as err:
            print(f"ERROR AL CONECTAR: {err}")

    def is_connected(self):
        return self._is_connected

    def run_query(self, query='', data=None):
        if self.is_connected():
            self._cursor.execute(query, data)
            if query.upper().startswith('SELECT'):
                data = self._cursor.fetchall()
            elif 'CREATE TABLE' in query.upper():
                pass
            else:
                self.conn.commit()
                data = self._cursor.lastrowid
        return data

    def close(self):
        if self.is_connected():
            self._cursor.close()
            self.conn.close()
            self._is_connected = False

    def __del__(self):
        self.close()


if __name__ == "__main__":
    conn = Conector()
    if conn.is_connected():
        print('CONECTADO')
        conn._cursor.execute("SHOW DATABASES")
        for db in conn._cursor:
            print(db)
        conn.close()

    if not conn.is_connected():
        print("CERRADA")
