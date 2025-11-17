import tkinter as tk
from tkinter import messagebox, ttk
import numpy as py
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show, legend, xlabel, ylabel, grid
 
class Tri:
    def __init__(self):
        self.main=tk.Toplevel()
        self.main.title('Funciones Trigonometrica')
        self.main.geometry('330x270+670+200')
        self.main.config(bg='Black')
        self.main.resizable(False, False)
        self.razon='Sen(x)'
        self.ejex=[]
        self.ejey=[]
        estilos=ttk.Style(); estilos.theme_use('default')
        estilos.configure('Treeview.Heading', background='#00736E', font=('Helvetica', 12))
        frame=tk.Frame(self.main, width=215, height=250)
        self.tabla=ttk.Treeview(frame, height=18, columns=1); self.tabla.heading('#0', text='x'); self.tabla.heading('#1', text='f(x)')
        self.tabla.column('#0', anchor='c', width=100); self.tabla.column('1', anchor='c', width=100)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        self.tabla.config(yscrollcommand=barra.set)
        boton_imprimir=tk.Button(self.main, text='Imprimir', bg='#00736E', fg='Black', font=('Helvetica', 12), width=7, command=self.imprimir)
        self.boton_graficar=tk.Button(self.main, text='Graficar', bg='#00736E', font=('Helvetica', 12), width=7, command=self.graficar)
        self.boton_cambio=tk.Button(self.main, text='Cos(x)', bg='#093D80', fg='Black', font=('Helvetica', 12), width=7, command=self.cambio)
        boton_cerrar=tk.Button(self.main, text='Cerrar', bg='#870707', font=('Helvetica', 12), width=7, command=self.cerrar)
        frame.place(x=110, y=10)
        self.tabla.place(x=0, y=0)
        barra.place(x=200, y=0, height=270)
        boton_imprimir.place(x=10, y=10)
        self.boton_graficar.place(x=10, y=50)
        self.boton_cambio.place(x=10, y=90)
        boton_cerrar.place(x=10, y=130)
    def imprimir(self):
        self.ejex.clear()
        self.ejey.clear()
        self.limpiar()
        self.tabla.tag_configure('par', font=('Helvetica', 12))
        self.tabla.tag_configure('inpar', background='#42827C', font=('Helvetica', 12))
        for i in range(0, 1000):
            sen=py.sin(py.radians(i))
            cos=py.cos(py.radians(i))
            if i%2==0 and self.razon=='Sen(x)':
                self.tabla.insert('', 'end', text=f'{i:.1f}', value=f'{sen:.3f}', tags='par')
            elif i%2!=0 and self.razon=='Sen(x)':
                self.tabla.insert('', 'end', text=f'{i:.1f}', value=f'{sen:.3f}', tags='inpar')
            elif i%2==0 and self.razon=='Cos(x)':
                self.tabla.insert('', 'end', text=f'{i:.1f}', value=f'{cos:.3f}', tags='par')
            elif i%2!=0 and self.razon=='Cos(x)':
                self.tabla.insert('', 'end', text=f'{i:.1f}', value=f'{cos:.3f}', tags='inpar')
    def limpiar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        plt.close()
    def cambio(self):
        if not self.tabla.get_children():
            self.mensaje()
        else:
            if self.razon=='Sen(x)':
                self.boton_cambio.config(text='Sen(x)')
                self.razon='Cos(x)'
                self.imprimir()
                self.graficar()
            else:
                self.boton_cambio.config(text='Cos(x)')
                self.razon='Sen(x)'
                self.imprimir()
                self.graficar()
    def graficar(self):
        if not self.tabla.get_children():
            self.mensaje()
        else:
            plt.clf()
            self.boton_graficar.config(text='Limpiar', command=self.limpiar)
            for item in self.tabla.get_children():
                self.ejex.append(float(self.tabla.item(item, 'text')))
                self.ejey.append(float(self.tabla.item(item, 'values')[0]))
            plt.title('Funciones Trigonometricas')
            plot(self.ejex, self.ejey, color='#00736E', label=f'{self.razon}')
            plt.yticks([-1,0, 1])
            xlabel('x')
            ylabel('f(X)')
            legend()
            grid(True)
            grid(color='black')
            plt.get_current_fig_manager().window.wm_geometry('+1200+200')
            plt.show()
    def cerrar(self):
        self.main.destroy()
        plt.close()
    def mensaje(self):
        messagebox.showinfo('Vacio', 'La tabla esta vacio...')
