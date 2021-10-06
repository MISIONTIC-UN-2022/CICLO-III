import os

import yagmail as yagmail
from flask import Flask, render_template, flash, request, redirect, url_for, jsonify
import utils
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
            username = request.form['username']
            password = request.form['password']
            email = request.form['correo']
            error = None

            if not utils.isUsernameValid( username ):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash( error )
                return render_template( 'register.html' )

            if not utils.isPasswordValid( password ):
                error = 'La contraseña debe contener al menos una minúscula, una mayúscula, un número y 8 caracteres'
                flash( error )
                return render_template( 'register.html' )

            if not utils.isEmailValid( email ):
                error = 'Correo invalido'
                flash( error )
                return render_template( 'register.html' )

            # yag = yagmail.SMTP('micuenta@gmail.com', 'clave') #modificar con tu informacion personal
            # yag.send(to=email, subject='Activa tu cuenta',
            #        contents='Bienvenido, usa este link para activar tu cuenta ')
            flash( 'Revisa tu correo para activar tu cuenta' )
            return redirect( 'login' )
        return render_template( 'register.html' )
    except:
        return render_template( 'register.html' )


@app.route( '/login', methods=('GET', 'POST') )
def login():
    try:
        if request.method == 'POST':            
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

            print("Usuario "+username + "Clave "+ password)
            if username == 'Prueba' and password == 'Prueba1234':
                return redirect('mensaje')
            else:
                error = 'Usuario o contraseña inválidos. Intenta nuevamente '
                flash( error )
                return render_template( 'login.html' )
        return render_template( 'login.html' )
    except:
        return render_template( 'login.html' )

@app.route( '/contactUs' )
def contactUs():
    form = Contactenos()
    return render_template( 'contacto.html', titulo='Contactenos', form=form )

@app.route( '/mensaje' )
def Message():
    return jsonify( {'usuario': mensajes, 'mensaje': "Mensajes"} )


if __name__ == '__main__':
    app.run()
