import functools
import os

from OpenSSL.crypto import FILETYPE_PEM
from flask import Flask, render_template, flash, request, redirect, url_for, session, send_file, \
    g, make_response
from werkzeug.security import generate_password_hash, check_password_hash

import utils
from db import get_db
from formulario import Contactenos

app = Flask( __name__ )
app.secret_key = os.urandom( 24 )


@app.route( '/' )
def index():
    if g.user:
        return redirect( url_for( 'send' ) )
    return render_template( 'login.html' )


@app.route( '/register', methods=('GET', 'POST') )
def register():
    if g.user:
        return redirect( url_for( 'send' ) )
    try:
        if request.method == 'POST':
            name= request.form['nombre']
            username = request.form['username']
            password = request.form['password']
            email = request.form['correo']
            error = None
            db = get_db()

            if not utils.isUsernameValid( username ):
                error = "El usuario debe ser alfanumerico o incluir solo '.','_','-'"
                flash( error )
                return render_template( 'register.html' )

            if not utils.isPasswordValid( password ):
                error = 'La contraseña debe contenir al menos una minúscula, una mayúscula, un número y 8 caracteres'
                flash( error )
                return render_template( 'register.html' )

            if not utils.isEmailValid( email ):
                error = 'Correo invalido'
                flash( error )
                return render_template( 'register.html' )

            if db.execute( 'SELECT id FROM usuario WHERE correo = ?', (email,) ).fetchone() is not None:
                error = 'El correo ya existe'.format( email )
                flash( error )
                return render_template( 'register.html' )

            hashContraseña = generate_password_hash( password )
            db.execute(
                'INSERT INTO usuario (nombre, usuario, correo, contraseña) VALUES (?,?,?,?)',
                (name, username, email, hashContraseña)
            )
            db.commit()

            # yag = yagmail.SMTP('micuenta@gmail.com', 'clave') #modificar con tu informacion personal
            # yag.send(to=email, subject='Activa tu cuenta',
            #        contents='Bienvenido, usa este link para activar tu cuenta ')
            flash( 'Revisa tu correo para activar tu cuenta' )
            return render_template( 'login.html' )
        return render_template( 'register.html' )
    except:
        return render_template( 'register.html' )


@app.route( '/login', methods=('GET', 'POST') )
def login():
    try:
        if g.user:
            return redirect( url_for( 'send' ) )
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
                'SELECT * FROM usuario WHERE usuario = ?', (username,)
            ).fetchone()

            if user is None:
                error = 'Usuario o contraseña inválidos'
            else:
                #Otra manera de validar hash password (o sol CP 14)
                if check_password_hash( user['contraseña'], password ):
                    session.clear()
                    session['user_id'] = user[0]
                    resp = make_response( redirect( url_for( 'send' ) ) )
                    resp.set_cookie( 'username', username )
                    return resp
                    # return redirect( url_for( 'send' ) )
                else:
                    error = 'Usuario o contraseña inválidos'
            flash( error )
        return render_template( 'login.html' )
    except:
        print( "Error " )
        return render_template( 'login.html' )


@app.route( '/contacto', methods=('GET', 'POST') )
def contacto():
    form = Contactenos()
    return render_template( 'contacto.html', titulo='Contactenos', form=form )


def login_required(view):
    @functools.wraps( view )
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect( url_for( 'login' ) )

        return view( **kwargs )

    return wrapped_view


@app.route( '/downloadpdf', methods=('GET', 'POST') )
@login_required
def downloadpdf():
    return send_file( "resources/doc.pdf", as_attachment=True )


@app.route( '/downloadimage', methods=('GET', 'POST') )
@login_required
def downloadimage():
    return send_file( "resources/image.png", as_attachment=True )


@app.route( '/send', methods=('GET', 'POST') )
@login_required
def send():
    if request.method == 'POST':
        from_id = g.user['id']
        to_username = request.form['para']
        subject = request.form['asunto']
        body = request.form['mensaje']
        db = get_db()
        username = request.cookies.get( 'username' )
        if not to_username:
            flash( username + ': Para es un campo requerido' );
            return render_template( 'send.html' )

        if not subject:
            flash( username + ': Asunto es un campo requerido' );
            return render_template( 'send.html' )

        if not body:
            flash( username + ': Mensaje es un campo requerido' );
            return render_template( 'send.html' )

        error = None
        userto = None

        userto = db.execute(
            'SELECT * FROM usuario WHERE usuario = ?', (to_username,)
        ).fetchone()

        if userto is None:
            error = username + ': usuario digitado en el campo Para no existe'

        if error is not None:
            flash( error )

        else:
            db = get_db()
            db.execute(
                'INSERT INTO mensajes (from_id, to_id, asunto, mensaje)'
                ' VALUES (?, ?, ?, ?)',
                (g.user['id'], userto['id'], subject, body)
            )
            db.commit()
            flash( "Mensaje Enviado" )

    return render_template( 'send.html' )


@app.before_request
def load_logged_in_user():
    user_id = session.get( 'user_id' )

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM usuario WHERE id = ?', (user_id,)
        ).fetchone()


@app.route( '/logout' )
def logout():
    session.clear()
    return redirect( url_for( 'login' ) )


if __name__ == '__main__':
    app.run( host='127.0.0.1', port =443, ssl_context=('micertificado.pem', 'llaveprivada.pem')  )
