from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Simulación de la tabla en memoria (CRUD)
contactos = [
    {"id": 1, "nombre": "Juan Pérez", "correo": "juan@email.com", "celular": "71234567"},
    {"id": 2, "nombre": "Ana Gómez", "correo": "ana@email.com", "celular": "79876543"}
]

def generar_id():
    if not contactos: return 1
    return max(c["id"] for c in contactos) + 1

# READ: Listar todos los contactos
@app.route('/')
def index():
    return render_template('index.html', contactos=contactos)

# CREATE: Crear un nuevo contacto
@app.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'POST':
        nuevo_contacto = {
            "id": generar_id(),
            "nombre": request.form['nombre'],
            "correo": request.form['correo'],
            "celular": request.form['celular']
        }
        contactos.append(nuevo_contacto)
        return redirect(url_for('index'))
    return render_template('formulario.html', contacto=None)

# UPDATE: Editar un contacto existente
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    # Buscar el contacto por ID
    contacto = next((c for c in contactos if c["id"] == id), None)
    if not contacto:
        return redirect(url_for('index'))

    if request.method == 'POST':
        contacto['nombre'] = request.form['nombre']
        contacto['correo'] = request.form['correo']
        contacto['celular'] = request.form['celular']
        return redirect(url_for('index'))

    return render_template('formulario.html', contacto=contacto)

# DELETE: Eliminar un contacto
@app.route('/eliminar/<int:id>')
def eliminar(id):
    global contactos
    contactos = [c for c in contactos if c["id"] != id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
