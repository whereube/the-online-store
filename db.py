from flask import redirect, render_template, flash, session
import psycopg2 
import psycopg2.extras
import uuid
from datetime import date

def open_db():
    try:
        connection = psycopg2.connect(
            user = 'am3070',
            password = 'u50odo96', 
            host = 'pgserver.mau.se',
            port = '5432',
            database = 'am3070'
            )
        return connection
    except: 
        print("Databasen finns inte!")

def close_db(connection):
    connection.close()

def user_in_db(user_email, user_password):
    connection = open_db()
    cursor = connection.cursor()
    cursor.execute("select id, name, email, password from \"profile\" where email = %s and password = %s", (user_email, user_password))
    records = cursor.fetchall()

    if records == []:
        close_db(connection)
        return False
    else:   
        close_db(connection) 
        return records

def create_profile_in_db(user_name, user_email, user_password):
    connection = open_db()
    cursor = connection.cursor()
    user_id = str(uuid.uuid4())
    cursor.execute("""insert into profile (id, name, email, password) values (%s, %s, %s, %s)""", (user_id, user_name, user_email, user_password))
    cursor.close()
    connection.commit()
    close_db(connection)

def get_articles_from_db():
    connection = open_db()
    cursor = connection.cursor()
    cursor.execute("""select * from articles""")
    records = cursor.fetchall()
    cursor.close()
    close_db(connection)
    return records

def get_categories_from_db():
    connection = open_db()
    cursor = connection.cursor()
    cursor.execute("""select * from category""")
    records = cursor.fetchall()
    cursor.close()
    close_db(connection)
    return records

