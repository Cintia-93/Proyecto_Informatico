from api import app
from flask import request, jsonify
from api.db.db import mysql
from api.models.client import Usuario
import jwt
import datetime

@app.route('/login', methods = ['POST'])
def login():
    auth = request.authorization
    print(auth)

    """ Control: existen valores para la autenticacion? """
    if not auth or not auth.username or not auth.password:
        return jsonify({"message": "No autorizado"}), 401       
            
    """ Control: existe y coincide el usuario en la BD? """
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM usuario WHERE nombre_us = %s AND contrasena_us = %s', (auth.username, auth.password))
    row = cur.fetchone()

    if not row:
       return jsonify({"message": "No autorizado"}), 401  
    
    """ El usuario existe en la BD y coincide su contraseña """
    token = jwt.encode({'id': row[0],
                        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=100)}, app.config['SECRET_KEY'])

    return jsonify({"token": token, "username": auth.username , "id": row[0]})

@app.route('/registro', methods = ['POST'])
def Registro_usuario():
    name = request.get_json()["name"]
    surname = request.get_json()["surname"]
    age = request.get_json()["age"]
    dni = request.get_json()["dni"]
    password = request.get_json()["password"]
    
    cur = mysql.connection.cursor()
    """ Control si existe el usuario indicado """
    cur.execute('SELECT * FROM usuario WHERE nombre_us = %s', (name,))
    row = cur.fetchone()

    if row:
        return jsonify({"message": "usuario ya registrado"})

    """ acceso a BD -> INSERT INTO """    
    cur.execute('INSERT INTO usuario (nombre_us, apellidos_us, edad, dni_us, contrasena_us, us_tipo) VALUES (%s, %s, %s, %s, %s, %s)', (name, surname, age, dni, password, 3))
    mysql.connection.commit()

    """ obtener el id del registro creado """
    cur.execute('SELECT LAST_INSERT_ID()')
    row = cur.fetchone()
    print(row[0])
    id = row[0]
    return jsonify({"name": name, "surname": surname, "age": age, "dni": dni, "password": password, "id": id})