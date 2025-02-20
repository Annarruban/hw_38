import pymysql
from pymysql.cursors import DictCursor
from db_queries import QueryHandler
from exceptions import BadTableName, BadSign, BadColumn

dbconfig = {# я удалила конфиги, чтоб загрузить на гит

        }

query_handler = QueryHandler(dbconfig)

def display_compared_table_data(query_handler, table_name, column, value, sign):
    table_name = table_name.strip().capitalize()
    column = column.strip().lower()
    sign = sign.strip()
    if sign not in {">", "<", "="}:
        raise BadSign()
    if column not in query_handler.get_all_columns(table_name):
        raise BadColumn()
    for row in query_handler.row_comparator_by_value(table_name, column, value, sign):
        print(row)

def display_columns(query_handler, table_name: str) -> None:
    table_name = table_name.strip().capitalize()
    for column in query_handler.get_all_columns(table_name):
        print(column)




user_table_name = input("Hello. Please enter a table name to see all it´s columns."
                        "(Role, User, News, Comment) ")
try:
    display_columns(query_handler, user_table_name)
    user_column = input("Choose please one of the displayed columns ")
    user_value = input("Enter a value ")
    user_sign = input("Enter a sign >, < or = ")
    display_compared_table_data(
        query_handler, user_table_name, user_column,
        user_value, user_sign
    )
except BadTableName:
    print(f"Table {user_table_name} does not exist. Please enter correct one.")
except BadSign:
    print("Enter one of the suggested signs please.")
except BadColumn:
    print("Enter one of the suggested columns please.")

