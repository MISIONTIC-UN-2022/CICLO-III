import os
from flask import Flask, render_template
from formulario import Contactenos

app = Flask( __name__ )
app.secret_key = os.urandom( 24 )

@app.route( '/' )
def hello_world():
    form = Contactenos()
    return render_template( 'contacto.html', titulo='Contactenos', form=form )

if __name__ == '__main__':
    app.run()
