from flask import Flask, render_template, redirect, url_for, Response, session, request, sessions
from flask_mysqldb import MySQL, MySQLdb
import mysql.connector
from bd import obtener_conexion, insertar_usuario, log_user, val_char_pass, vali_user_repeat, vali_email_repeat
import tensorflow as tf
import numpy as np

app = Flask(__name__)
app.secret_key = "login_sensillo"
@app.route("/")
def  index():
    return redirect(url_for('login'))

@app.route("/login", methods=['POST', 'GET'])
def login():
    #if "login" in session:
        #return redirect(url_for('userindex'))
    #else:
        if request.method == 'POST' and request.form['usermail'] != None and request.form['userpass'] != None:
            mydb = obtener_conexion()
            if log_user(mydb, request.form['usermail'], request.form['userpass']):
                session["login"] = True
                session["username"] = request.form['usermail']
                return redirect(url_for('userindex'))
            else:
                return render_template('login/login.html', mensaje = "Usuario o contraseña no validos")
        else:
            return render_template('login/login.html')
        
@app.route("/userindex", methods = ['POST', 'GET'])
def userindex():
    if request.method == 'POST':
        val_celsius = request.form['txtcelsius']
        print(val_celsius)
        val_celsius = 80.0
        val = ai_grados(val_celsius)
        return render_template('login/userindex.html', farenheit = val)
    else:
        return render_template('login/userindex.html')

def ai_grados(valcelsius):
    celsius = np.array([-40, -10, 0, 8, 15, 22, 38], dtype = float)
    farenheit = np.array([-40, 14, 32, 46, 59, 72, 100], dtype = float) 
        
    capa = tf.keras.layers.Dense(units=1, input_shape=[1])
    modelo = tf.keras.Sequential([capa])                    
    #COMPILADO
    #prepara el modelo para entrenarlo
    modelo.compile(
    optimizer = tf.keras.optimizers.Adam(0.1), 
    loss='mean_squared_error'
    )

    #ENTRENAMIENTO get_weights()
    historial = modelo.fit(celsius, farenheit, epochs = 500, verbose = False)
    #print("Entrenado")
    #print(historial.history["loss"])
    #analizando grafico
    #plt.plot(celsius, farenheit)
    #plt.plot(historial.history['loss'])
    #plt.show()
    valor_a_predecir = np.array([valcelsius])
    resultado = modelo.predict(valor_a_predecir)
    print(resultado)
    peso = capa.get_weights()
    #print(peso)
    return(resultado)


@app.route("/register", methods = ['POST', 'GET'])
def register():
    if request.method == 'POST'and request.form['username'] != None and request.form['fullname'] != None and request.form['userpass'] != None and request.form['usermail'] != None:
        mydb = obtener_conexion()
        if val_char_pass(len(request.form['userpass'])): #pass mayor a 7 caracteres
            if vali_user_repeat(mydb, request.form['username']): # usuario repetido
                if vali_email_repeat(mydb, request.form['usermail']):
                    insertar_usuario(mydb, request.form['username'], request.form['userpass'], request.form['usermail'], request.form['fullname'])
                    return render_template('login/login.html', init = "Registrado con Exito") 
                else:
                    return render_template('register.html', err_val = "Email ya se encuentra registrado")
            else:
                return render_template('register.html', err_val = "Usuario ya se encuentra registrado")      
        else:
            return render_template('register.html', err_val = "Contraseña debe ser mayor a 6 caracteres") 
    else:
        return render_template('register.html')
       
if __name__ =='__main__':
    app.run(debug = True)