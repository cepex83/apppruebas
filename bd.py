import mysql.connector
from flask import request

def obtener_conexion():
    mydb = mysql.connector.connect (
        host = "localhost",
        user = "root",
        password = "",
        database = "login"
    )
    return (mydb)

def insertar_usuario(mydb, username, password, fullname, usermail):
    mycursor = mydb.cursor()
    sql = "INSERT INTO users (username, userpass, fullname, email) VALUES (%s, %s, %s, %s)"
    val = (username, password ,usermail, fullname)
    mycursor.execute(sql, val)
    mydb.commit()
    return()

#valida que se escribio en la base de datos
def log_user(mydb, usermail, userpass):
    mycursor = mydb.cursor()
    query = "SELECT email, userpass FROM users"
    mycursor.execute(query)
    users = mycursor.fetchone()
    while users is not None:
        print(users)
        if usermail in users:
            if userpass in users:
                validate = True
                print(validate)
                return(validate)
        validate = False
        users = mycursor.fetchone()
    return(validate)

#valida pass mayor a 7
def val_char_pass(password):
    if password > 7:
        password = True
        print(password)
        return(password)
    else:
        password = False
        print(password)
        return(password)

def vali_user_repeat(mydb, username):
    mycursor = mydb.cursor()
    query = "SELECT username FROM users"
    mycursor.execute(query)
    users = mycursor.fetchone()
    while users is not None:
        if username in users:
            validate = False
            print(validate)
            return(validate)
        validate = True
        users = mycursor.fetchone()
    print(validate)
    return(validate)

def vali_email_repeat(mydb, usermail):
    mycursor = mydb.cursor()
    query = "SELECT email FROM users"
    mycursor.execute(query)
    mails = mycursor.fetchone()
    while mails is not None:
        if usermail in mails:
            validate = False
            print(validate)
            return(validate)
        validate = True
        mails = mycursor.fetchone()
    print(validate)
    return(validate)
            
            