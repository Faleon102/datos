from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estudiantes.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

class estudiantes(db.Model):
   id = db.Column('estudiante_id', db.Integer, primary_key = True)
   nombre1 = db.Column(db.String(50))
   nombre2 = db.Column(db.String(50))
   apellido = db.Column(db.String(80))
   direccion = db.Column(db.String(100))
   ciudad = db.Column(db.String(10))

   def __init__(self, nombre1, nombre2, apellido, direccion, ciudad):
       self.nombre1 = nombre1
       self.nombre2 = nombre2
       self.apellido = apellido
       self.direccion = direccion
       self.ciudad = ciudad

@app.route('/')
def mostrar():
   return render_template('mostrar.html', estudiantes = estudiantes.query.all() )

@app.route('/nuevo', methods = ['GET', 'POST'])
def nuevo():
   if request.method == 'POST':
      if not request.form['nombre1'] or not request.form['nombre2'] or not request.form['apellido'] or not request.form['direccion']:
         flash('Porfavor ingrese todos los datos', 'error')
      else:
         estudiante = estudiantes(request.form['nombre1'], request.form['nombre2'], request.form['apellido'], request.form['direccion'], request.form['ciudad'])

         db.session.add(estudiante)
         db.session.commit()
         flash('Nuevo registro exitoso')
         return redirect(url_for('mostrar'))
   return render_template('nuevo.html')

@app.route("/actualizar", methods=["POST"])
def actualizar():
    nombre1 = request.form.get("nombrev")
    estudiante = estudiantes.query.filter_by(nombre1=nombre1).first()
    return render_template('actualizar.html', result = estudiante, nombrev = nombre1)

@app.route("/actualizar_record", methods=["POST"])
def actualizar_record():
    nombre1 = request.form.get("nombrev")
    estudiante = estudiantes.query.filter_by(nombre1=nombre1).first()
    estudiante.nombre1 = request.form['nombre1']
    estudiante.nombre2 = request.form['nombre2']
    estudiante.apellido = request.form['apellido']
    estudiante.direccion = request.form['direccion']
    estudiante.ciudad = request.form['ciudad']
    db.session.commit()
    return redirect('/')

@app.route("/delete", methods=["POST"])
def delete():
    nombre1 = request.form.get("nombrev")
    estudiante = estudiantes.query.filter_by(nombre1=nombre1).first()
    db.session.delete(estudiante)
    db.session.commit()
    return redirect("/")

if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)
