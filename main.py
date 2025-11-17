import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import Trigonometricas as tri
import suavisado as su
import ordenar as orde
import regresion_lineal as rl 
import MC as mc

class Main:
    def __init__(self):
        self.main=tk.Tk()
        self.main.title('Analisis de Datos')
        self.main.geometry('550x390+50+200')
        self.main.config(background='#000000')
        self.constructores()
        self.main.mainloop()
    def constructores(self):
        letra='Serif Bold'
        portada=tk.Label(text='INSTITUTO POLITECNICO NACIONAL', font=(letra, 18), bg='#000000', fg='#FFFFFF')
        unidad=tk.Label(text='ESIME UNIDAD ZACATENCO', font=(letra, 18), bg='#000000', fg='#FFFFFF')
        carrera=tk.Label(text='ING. COMUNICACIONES Y ELECTRONICA', font=(letra, 18), bg='#000000', fg='#FFFFFF')
        materia=tk.Label(text='ANALISIS DE DATOS', font=(letra, 18), bg='#000000', fg='#FFFFFF')
        nombre=tk.Label(text='JUAN CRUZ OSORIO', font=(letra, 18), bg='#000000', fg='#FFFFFF')
        menu_principal=tk.Menu()
        self.main.config(menu=menu_principal)
        submenu=tk.Menu(menu_principal, tearoff=0)
        menu_principal.add_cascade(label='Menu', menu=submenu)
        submenu.add_command(label='Funciones Trigonometricas', command=tri.Tri)
        submenu.add_command(label='Suavisado', command=su.Suavisado)
        submenu.add_command(label='Ordenar', command=orde.Ordenar)
        submenu.add_command(label='Regresion Lineal', command=rl.Rl)
        submenu.add_command(label='Metodo Minimos Cuadrados', command=mc.Minimos)
        submenu.add_command(label='', command=self.mensaje)
        boton_cerrar=tk.Button(text='Cerrar', font=(letra, 12), bg='red', command=self.cerrar)

        #   Zona de acomodo
        portada.place(x=55, y=50)
        unidad.place(x=100, y=100)
        carrera.place(x=30, y=150)
        materia.place(x=145, y=200)
        nombre.place(x=145, y=250)
        boton_cerrar.place(x=10, y=350)
    def mensaje(self):
        messagebox.showinfo('Mensaje', 'XD')
    def cerrar(self):
        self.main.destroy()
        plt.close()

if __name__=='__main__':
    Main()
