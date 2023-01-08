# importamos modulos
from tkinter import *
from tkinter import ttk

# Importar modulos para deteccion de Errores
from tkinter import messagebox
import re

# Importar modulos para bases de Datos
import sqlite3
from sqlite3 import Error
import datetime
from plyer import notification


ventana = Tk()
ventana.geometry("800x600")
ventana.title("NOMINA DEL PERSONAL")
ventana.configure(background="#4BD4DE")

##################################

var_numeroDelEmpleado = StringVar()
var_nombreyApellido = StringVar()
var_puesto = StringVar()
var_sueldo = StringVar()
nroRegistro = 0
# Archivos
archivo = open("ProyectoEugenia\Borrados2.txt", "w")
# FUNCIONES PARA BASE DE DATOS
def actualizarDB(con, numero, numEmpleado, nombreyApellido, puesto, sueldo):
    numEmp = int(numEmpleado)
    suel = int(sueldo)
    cursor = con.cursor()
    data = (numEmp, nombreyApellido, puesto, suel, numero)
    sql = "UPDATE tablaRegistros SET numeroDelEmpleado=?, nombreyApellido=?, puesto=?, sueldo=? WHERE nroRegistro=?;"
    cursor.execute(sql, data)
    con.commit()


def fventanaModificar():
    def aceptar():
        var_numeroDelEmpleado = textBox_numeroDelEmpleado2
        var_nombreyApellido = textBox_nombreyApellido2
        var_puesto = textBox_puesto2
        var_sueldo = textBox_sueldo2
        actualizarDB(
            con,
            nroRegistro_Aux,
            var_numeroDelEmpleado.get(),
            var_nombreyApellido.get(),
            var_puesto.get(),
            var_sueldo.get(),
        )
        tree.item(
            item=item,
            text=str(nroRegistro_Aux),
            values=(
                var_numeroDelEmpleado.get(),
                var_nombreyApellido.get(),
                var_puesto.get(),
                var_sueldo.get(),
            ),
        )
        textBox_numeroDelEmpleado2.delete(0, "end")
        textBox_nombreyApellido2.delete(0, "end")
        textBox_puesto2.delete(0, "end")
        textBox_sueldo2.delete(0, "end")
        ventana2.destroy()

    ventana2 = Tk()
    ventana2.geometry("400x150")
    ventana2.title("MODIFICAR")
    ventana2.configure(background="#777777")
    item = tree.focus()
    nroRegistro_Aux = int(tree.item(item)["text"])
    lista_auxiliar = tree.item(item)["values"]
    print(lista_auxiliar)
    label_numeroDelEmpleado2 = Label(
        ventana2, text="Numero de empleado", bg="#777777", font="Arial 15"
    )
    label_nombreyApellido2 = Label(
        ventana2, text="Nombre y Apellido", bg="#777777", font="Arial 15"
    )
    label_puesto2 = Label(ventana2, text="Puesto", bg="#777777", font="Arial 15")
    label_sueldo2 = Label(ventana2, text="Sueldo", bg="#777777", font="Arial 15")

    label_numeroDelEmpleado2.grid(row=0, column=0, sticky=E)
    label_nombreyApellido2.grid(row=1, column=0, sticky=E)
    label_puesto2.grid(row=2, column=0, sticky=E)
    label_sueldo2.grid(row=3, column=0, sticky=E)
    # Creacion de Entrys para cada ingreso de informacion
    textBox_numeroDelEmpleado2 = Entry(
        ventana2, font="Arial 15", textvariable=var_numeroDelEmpleado
    )
    textBox_nombreyApellido2 = Entry(
        ventana2, font="Arial 15", textvariable=var_nombreyApellido
    )
    textBox_puesto2 = Entry(ventana2, font="Arial 15", textvariable=var_puesto)
    textBox_sueldo2 = Entry(ventana2, font="Arial 15", textvariable=var_sueldo)

    # Colocacion de Entrys para cada ingreso de informacion
    textBox_numeroDelEmpleado2.grid(row=0, column=1)
    textBox_nombreyApellido2.grid(row=1, column=1)
    textBox_puesto2.grid(row=2, column=1)
    textBox_sueldo2.grid(row=3, column=1)

    textBox_numeroDelEmpleado2.insert(0, lista_auxiliar[0])
    textBox_nombreyApellido2.insert(0, lista_auxiliar[1])
    textBox_puesto2.insert(0, lista_auxiliar[2])
    textBox_sueldo2.insert(0, lista_auxiliar[3])

    boton_Aceptar = Button(
        ventana2, text="ACEPTAR", font="Arial 15", width=20, command=aceptar
    )
    boton_Aceptar.grid(row=4, column=1, sticky=W)

    ventana2.mainloop()


def crear_base():
    global nroRegistro
    con = sqlite3.connect("ProyectoEugenia\BaseDatos2.db")
    cursor = con.cursor()
    # Verificar si la tabla 'tablaRegistros' existe en la base de datos
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='tablaRegistros'"
    )
    if cursor.fetchone() is not None:
        query = "SELECT * FROM tablaRegistros"
        cursor.execute(query)
        results = cursor.fetchall()
        for result in results:
            tree.insert(
                "",
                "end",
                text=str(result[0]),
                values=(result[1], result[2], result[3], result[4]),
            )
        nroRegistro = result[0]
    return con


def crear_tabla(con):

    cursor = con.cursor()  # permite agregar info a la base de daotos
    sql = "CREATE TABLE IF NOT EXISTS tablaRegistros(nroRegistro integer PRIMARY KEY,numeroDelEmpleado integer NOT NULL, nombreyApellido text NOT NULL, puesto text,sueldo integer NOT NULL)"
    cursor.execute(sql)
    con.commit()


def insertarBD(con, numEmpleado, nombreyApellido, puesto, sueldo):
    global nroRegistro
    numEmp = int(numEmpleado)
    suel = int(sueldo)
    cursor = con.cursor()
    data = (nroRegistro, numEmp, nombreyApellido, puesto, suel)
    sql = "INSERT INTO tablaRegistros(nroRegistro, numeroDelEmpleado,nombreyApellido,puesto,sueldo) VALUES(?, ?, ?, ?, ?)"
    cursor.execute(sql, data)
    con.commit()


def borrarDB(con, numero):
    cursor = con.cursor()
    data = (numero,)
    sql = "DELETE from tablaRegistros where nroRegistro = ?;"
    cursor.execute(sql, data)
    con.commit()


# FUNCIONES PARA TKINTER
def agregarTk():
    seleccionarTk(con)
    Error = False
    # Verificamos si el contenido de var_numeroDelEmpleado contiene algún carácter no válido
    if (not re.fullmatch("[0-9]*", var_numeroDelEmpleado.get())) or (
        not re.fullmatch("[0-9]*", var_sueldo.get())
    ):
        messagebox.showerror("Error", "Ha ocurrido un error al agregar el registro.")
        Error = True
    if (not re.fullmatch("[a-zA-ZñÑáéíóúÁÉÍÓÚ \s]*", var_puesto.get())) or (
        not re.fullmatch("[a-zA-ZñÑáéíóúÁÉÍÓÚ \s]*", var_nombreyApellido.get())
    ):
        messagebox.showerror("Error", "Ha ocurrido un error al agregar el registro.")
        Error = True
    if (
        not var_numeroDelEmpleado.get()
        or not var_nombreyApellido.get()
        or not var_puesto.get()
        or not var_sueldo.get()
    ):
        messagebox.showerror("Error", "Ha ocurrido un error al agregar el registro.")
        Error = True
    if Error == False:
        global nroRegistro
        nroRegistro += 1
        insertarBD(
            con,
            var_numeroDelEmpleado.get(),
            var_nombreyApellido.get(),
            var_puesto.get(),
            var_sueldo.get(),
        )
        tree.insert(
            "",
            "end",
            text=str(nroRegistro),
            values=(
                var_numeroDelEmpleado.get(),
                var_nombreyApellido.get(),
                var_puesto.get(),
                var_sueldo.get(),
            ),
        )
        notification.notify(
            title="Elemento agregado.",
            message="La tarea ha sido completada con éxito",
            app_name="Mi aplicación",
            timeout=10,
        )
        # se elimina el contenido de los textBox
        textBox_numeroDelEmpleado.delete(0, "end")
        textBox_nombreyApellido.delete(0, "end")
        textBox_puesto.delete(0, "end")
        textBox_sueldo.delete(0, "end")


def borrarTk():
    global nroRegistro
    if not tree.focus():
        messagebox.showerror("Error", "Debe seleccionar un item.")
    item = tree.focus()
    partes = item.split("I")
    numero = int(partes[1])
    contenido = tree.item(item, "values")
    ahora = datetime.datetime.now()
    archivo.write(
        "Elemento borrado en fecha: "
        + ahora.strftime("%Y-%m-%d")
        + ". A las  "
        + ahora.strftime("%H:%M")
        + " es:"
        + str(contenido)
    )
    borrarDB(con, numero)
    tree.delete(item)
    notification.notify(
        title="Eliminacion Exitosa",
        message="La tarea ha sido completada con éxito",
        app_name="Mi aplicación",
        timeout=10,
    )
    nroRegistro -= 1


def modificarTk():
    fventanaModificar()


def seleccionarTk(con):
    global nroRegistro
    cursor = con.cursor()
    data = (nroRegistro,)
    sql = "SELECT * FROM tablaRegistros WHERE nroRegistro =?;"
    cursor.execute(sql, data)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


# Creacion de labels superiores: titulo y 3 espacios
titulo = Label(
    ventana, text="Nomina del personal", bg="#4BD4DE", fg="#000000", font="Helvetica 25"
)
vacio1 = Label(ventana, text="", bg="#4BD4DE", fg="#000000", font="Helvetica 20")
vacio2 = Label(ventana, text="", bg="#4BD4DE", fg="#000000", font="Helvetica 20")
vacio3 = Label(ventana, text="", bg="#4BD4DE", fg="#000000", font="Helvetica 20")

# Colocacion de labels superiores: titulo y 2 espacios
titulo.grid(row=0, column=1, columnspan=2)
vacio1.grid(row=1, column=2)
vacio2.grid(row=2, column=2)
vacio3.grid(row=7, column=2)

# Creacion de labels costado izquierdo
label_numeroDelEmpleado = Label(
    ventana, text="Numero de empleado", bg="#4BD4DE", font="Arial 15"
)
label_nombreyApellido = Label(
    ventana, text="Nombre y Apellido", bg="#4BD4DE", font="Arial 15"
)
label_puesto = Label(ventana, text="Puesto", bg="#4BD4DE", font="Arial 15")
label_sueldo = Label(ventana, text="Sueldo", bg="#4BD4DE", font="Arial 15")

# Colocacion de labels en la grilla
label_numeroDelEmpleado.grid(row=3, column=0, sticky=E)
label_nombreyApellido.grid(row=4, column=0, sticky=E)
label_puesto.grid(row=5, column=0, sticky=E)
label_sueldo.grid(row=6, column=0, sticky=E)

# Creacion de Entrys para cada ingreso de informacion
textBox_numeroDelEmpleado = Entry(
    ventana, font="Arial 15", textvariable=var_numeroDelEmpleado
)
textBox_nombreyApellido = Entry(
    ventana, font="Arial 15", textvariable=var_nombreyApellido
)
textBox_puesto = Entry(ventana, font="Arial 15", textvariable=var_puesto)
textBox_sueldo = Entry(ventana, font="Arial 15", textvariable=var_sueldo)

# Colocacion de Entrys para cada ingreso de informacion
textBox_numeroDelEmpleado.grid(row=3, column=1)
textBox_nombreyApellido.grid(row=4, column=1)
textBox_puesto.grid(row=5, column=1)
textBox_sueldo.grid(row=6, column=1)

# Creacion de botones ABM
boton_Alta = Button(ventana, text="Alta", font="Arial 15", width=20, command=agregarTk)
boton_Baja = Button(ventana, text="Baja", font="Arial 15", width=20, command=borrarTk)
boton_Modificacion = Button(
    ventana, text="Modificacion", font="Arial 15", width=20, command=modificarTk
)

# Colocacion de botones ABM
boton_Alta.grid(row=3, column=3, sticky=W)
boton_Baja.grid(row=4, column=3, sticky=W)
boton_Modificacion.grid(row=5, column=3, sticky=W)

# Creacion de tree para mostrar datos
tree = ttk.Treeview(ventana)

tree["columns"] = ("col1", "col2", "col3", "col4")

tree.column("#0", width=90, minwidth=90)
tree.column("col1", width=190, minwidth=190)
tree.column("col2", width=190, minwidth=190)
tree.column("col3", width=190, minwidth=190)
tree.column("col4", width=150, minwidth=150)

tree.heading("#0", text="Nº de Registro")
tree.heading("col1", text="Numero de Empleado")
tree.heading("col2", text="Nombre y Apellido")
tree.heading("col3", text="Puesto")
tree.heading("col4", text="Salario")

tree.grid(column=0, row=8, columnspan=4)

#


con = crear_base()
crear_tabla(con)
#################################
ventana.mainloop()
