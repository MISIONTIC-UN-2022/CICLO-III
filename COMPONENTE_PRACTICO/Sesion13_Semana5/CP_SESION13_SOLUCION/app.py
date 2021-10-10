import os

import yagmail as yagmail
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
import utils
from db import get_db
from formulario import Contactenos
from message import mensajes

app = Flask( __name__ )
app.secret_key = os.urandom( 24 )


@app.route( '/' )
def index():
    return render_template( 'register.html' )

@app.route( '/register', methods=('GET', 'POST') )
def register():
    try:
        if request.method == 'POST':
            name= request.form['nombre']
            username = request.form['username']
            password = request.form['password']
            email = request.form['correo']
            error = None
            db = get_db()
            db.executescript(
                "INSERT INTO usuario (nombre, usuario, correo, contraseña) VALUES ('%s','%s','%s','%s')" % (name, username, email, password)
                #"; UPDATE usuario set correo='hack';"
            )
            #db.execute(
            #    'INSERT INTO usuario (usuario, correo, contraseña) VALUES ('%s','%s','%s')' %
            #    (username, email, password)
            #)
            db.commit()
            print( "P2" )
            return render_template( 'login.html' )
        return render_template( 'register.html' )
    except:
        return render_template( 'register.html' )


@app.route( '/login', methods=('GET', 'POST') )
def login():
    try:
        if request.method == 'POST':
            db = get_db()
            error = None
            username = request.form['username']
            password = request.form['password']

            if not username:
                error = 'Debes ingresar el usuario'
                flash( error )
                return render_template( 'login.html' )

            if not password:
                error = 'Contraseña requerida'
                flash( error )
                return render_template( 'login.html' )

            user = db.execute(
                'SELECT * FROM usuario WHERE usuario = ? AND contraseña = ? ', (username, password)
            ).fetchone()

            # print('USER ')
            # print(user)

            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                return redirect( 'message' )
            flash( error )
        return render_template( 'login.html' )
    except:
        return render_template( 'login.html' )


@app.route( '/contacto', methods=('GET', 'POST') )
def contacto():
    form = Contactenos()
    return render_template( 'contacto.html', titulo='Contactenos', form=form )


@app.route( '/message', methods=('GET', 'POST') )
def message():
    print( "Retrieving info" )
    return jsonify( {'mensajes': mensajes} )


if __name__ == '__main__':
    app.run()
