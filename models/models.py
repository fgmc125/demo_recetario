from conector import Conector


class Model:
    def __init__(self):
        self.conexion = None
        self.__ejecutar_script_sql()

    def __ejecutar_script_sql(self):
        self.conexion = Conector()
        try:
            with open('script_database.sql', 'r') as sql_file:
                script = sql_file.read()

            queries = script.split(';')

            for query in queries:
                query = query.strip()
                if query:
                    self.conexion.run_query(query)

            print("¡Script SQL ejecutado exitosamente!")
        except FileNotFoundError:
            print("ERROR: No se encontró el archivo 'script_database.sql'")
        except Exception as e:
            print(f"ERROR AL EJECUTAR EL SCRIPT SQL: {e}")
        finally:
            self.conexion = None

    def nueva_receta(self,
                     nombre_receta,
                     tiempo_coccion,
                     tiempo_preparacion):
        self.conexion = Conector()
        sql = "INSERT INTO recetas (nombre_receta, tiempo_coccion, tiempo_preparacion, creacion) " \
              "VALUES (%s, %s, %s, NOW())"
        data = (nombre_receta, tiempo_coccion, tiempo_preparacion)
        id_receta = self.conexion.run_query(sql, data)

        self.conexion.close()
        return id_receta

    def obtener_todas_recetas(self):
        self.conexion = Conector()
        sql = "SELECT * FROM recetas"
        recetas = self.conexion.run_query(sql)

        self.conexion.close()
        return recetas

if __name__ == "__main__":
    model = Model()
    pollo = model.nueva_receta("pollito", "5", "55")
    data = model.obtener_todas_recetas()
    print(pollo)
    print(data)
