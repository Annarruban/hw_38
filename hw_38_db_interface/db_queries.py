from db_connection import DBConnector
from exceptions import BadTableName

class QueryHandler(DBConnector):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)

    def get_all_roles(self):
        cursor = self.get_cursor()
        cursor.execute("select * from Role")
        records = cursor.fetchall()
        return records

    def get_role_id_by_name(self, name_role: str):
        cursor = self.get_cursor()
        cursor.execute("select id from Role where name = %s", (name_role,))
        records = cursor.fetchone()
        if records:
            return records
        return None

    def get_all_columns(self, table_name: str) -> set[str]:
        cursor = self.get_cursor()
        cursor.execute("""SELECT DISTINCT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
          WHERE TABLE_NAME = %s AND TABLE_SCHEMA = %s""", (table_name, self._dbconfig["database"]))
        records = cursor.fetchall()
        if not records:
            raise BadTableName()
        columns = {column.get('COLUMN_NAME') for column in records}
        return columns

    def row_comparator_by_value(self, table_name, column, value, sign):
        cursor = self.get_cursor()
        cursor.execute(f"""SELECT {column} FROM {table_name}
         WHERE {column} {sign} %s""", (value, ))
        records = cursor.fetchall()
        return records