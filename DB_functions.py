import sqlite3
from sqlite3 import Error
import csv
from random import shuffle
from enums4bot import *

def connect_to_DB(DB_file_name):
    connection = None
    try:
        connection = sqlite3.connect(DB_file_name, check_same_thread=False)
        print("Соединение с базой установлено успешно")
    except Error as error_info:
        print(f"Ошибка исполнения запроса: '{error_info}'")

    return connection

def execute_query(query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as error_info:
        print(f"Ошибка исполнения запроса: '{error_info}'")

def execute_read_query(query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as error_info:
        print(f"Ошибка исполнения запроса: '{error_info}'")

def create_full_csv_file():
    with open("full_DB.csv", "w", newline='') as csv_file:
        csvWriter = csv.writer(csv_file, delimiter=';')
        query_result = execute_read_query("SELECT name, nickname, friend FROM users "\
                                          f"WHERE state={States.S_FULL}")
        csvWriter.writerows(query_result)

if __name__ == "__main__":
    connection = connect_to_DB("DB.sqlite")
    execute_query("""
    CREATE TABLE users (
        id int NOT NULL UNIQUE,
        state int NOT NULL,
        role varchar,
        name varchar, 
        nickname varchar,
        friend varchar,
        PRIMARY KEY (id)
    );""")

def get_total_students():
    query_result = execute_read_query(f"SELECT id FROM users "\
                                      f"WHERE state={States.S_FULL}")
    return len(query_result)

def toss_is_able():
    query_result = execute_read_query(f"SELECT friend FROM users "\
                                      f"WHERE state={States.S_FULL}")
    friends = [row[0] for row in query_result]
    return None in friends

def create_toss():
    query_result = execute_read_query(f"SELECT nickname FROM users "\
                                      f"WHERE state={States.S_FULL}")
    nicknames = [row[0] for row in query_result]
    shuffle(nicknames)
    num_of_nicknames = len(nicknames)
    for i in range(0, num_of_nicknames, 2):
        execute_query(f"UPDATE users SET friend='{nicknames[i]}' WHERE nickname='{nicknames[i+1]}'")
        execute_query(f"UPDATE users SET friend='{nicknames[i+1]}' WHERE nickname='{nicknames[i]}'")


def check_user_in_db(user_id):
    query_result = execute_read_query(f"SELECT id FROM users "\
                                      f"WHERE id={user_id}")
    if query_result:
        return True
    return False

def check_nickname_in_db(nickname):
    query_result = execute_read_query(f"SELECT nickname FROM users "\
                                      f"WHERE nickname='{nickname}'")
    if query_result:
        return True
    return False

def check_nickname_is_null(user_id):
    query_result = execute_read_query(f"SELECT nickname FROM users "\
                                      f"WHERE id={user_id}")
    try:
        nickname = query_result[0][0]
        return not nickname
    except:
        return True
    
def check_role_is_null(user_id):
    query_result = execute_read_query(f"SELECT role FROM users "\
                                      f"WHERE id={user_id}")
    try:
        role = query_result[0][0]
        return not role
    except:
        return True
    
def add_user(user_id):
    execute_query(f"INSERT INTO users (id, state) "\
                  f"VALUES ({user_id}, {States.U_START})")

def set_state(user_id, state):
    execute_query(f"UPDATE users SET state={state} WHERE id={user_id}")

def get_state(user_id):
    query_result = execute_read_query(f"SELECT state FROM users WHERE id={user_id}")
    try:
        return query_result[0][0]
    except:
        return 0

def set_role(user_id, role):
    execute_query(f"UPDATE users SET role='{role}' WHERE id={user_id}")

def get_role(user_id):
    query_result = execute_read_query(f"SELECT role FROM users WHERE id={user_id}")
    try:
        role = query_result[0][0]
        return role if role else False
    except:
        return False
    
def set_name(user_id, name):
    execute_query(f"UPDATE users SET name='{name}' WHERE id={user_id}")

def get_name(user_id):
    query_result = execute_read_query(f"SELECT name FROM users WHERE id={user_id}")
    try:
        name = query_result[0][0]
        return name if name else False
    except:
        return False

def set_nickname(user_id, nickname):
    execute_query(f"UPDATE users SET nickname='{nickname}' WHERE id={user_id}")
    
def get_nickname(user_id):
    query_result = execute_read_query(f"SELECT nickname FROM users WHERE id={user_id}")
    try:
        nickname = query_result[0][0]
        return nickname if nickname else False
    except:
        return False
    
def get_friend(user_id):
    query_result = execute_read_query(f"SELECT friend FROM users WHERE id={user_id}")
    try:
        friend = query_result[0][0]
        return friend if friend else False
    except:
        return False
