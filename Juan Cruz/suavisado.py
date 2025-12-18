import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot, show, xlabel, ylabel, grid, legend

class Suavisado:
    def __init__(self):
        self.ventana=tk.Toplevel() 
        self.ventana.title('Suavisado')
        self.ventana.geometry('400x250+700+200')
        self.ventana.config(bg='Black')
        self.x=[]
        self.y=[]
        self.valores=[]
        self.constructores()
        self.ventana.mainloop()
    def generar(self):
        self.limpiar()
        self.max=int(self.maximo.get())
        if self.max<=200:
            for i in range(self.max):
                datos=round(2.8+(3.3-2.8)*(random.random()), 3)
                self.x.append(i+1)
                self.y.append(datos)
                self.tabla.insert('', 'end', values=(self.x[i], self.y[i],''))
        else:
            messagebox.showinfo('MAXIMO DE DATOS', 'El maximo de datos de de 1-200...')
    def suavisar(self):
        self.ord=int(self.orden.get())
        if not (2<=self.ord<=10):
            messagebox.showinfo('MAXIMO ORDEN', 'El orden maximo es de 2-10...')
        else:
            if not len(self.tabla.get_children()):
                self.mensaje()
            else:
                self.valores.clear()
                for i in self.tabla.get_children():
                    self.tabla.delete(i)
                for i in range(self.max):
                    filtro=self.valores[-(self.ord-1):]+[0]*(self.ord-1)
                    auxiliar=(self.y[i]+sum(filtro))/self.ord
                    self.valores.append(auxiliar)
                    self.tabla.insert('', 'end', values=(self.x[i], self.y[i], f'{self.valores[i]:.2f}'))
    def graficar(self):
        if not len(self.tabla.get_children()):
            self.mensaje()
        else:
            plt.clf()
            orden=self.orden.get()
            plt.close('all')
            plt.figure(figsize=(8,5))
            plt.title(f'Grafica de orden {orden}')
            plt.get_current_fig_manager().window.wm_geometry('+1100+200')
            plot(self.x, self.y, color='#780606')
            plot(self.x, self.valores, color='#064654')
            xlabel('x')
            ylabel('y')
            grid(color='black')
            plt.show()
    def cerrar(self):
        self.ventana.destroy()
        plt.close()
    def limpiar(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        self.x.clear()
        self.y.clear()
        plt.close()
    def mensaje(self):
        messagebox.showinfo('Vacio', 'La tabla esta vacia')
    def constructores(self):
        frame=ttk.Frame(self.ventana, width=260, height=200)
        self.tabla=ttk.Treeview(frame, columns=('i', 'Signal', 'Suavisado'), show='headings')
        self.tabla.heading('i', text='i'); self.tabla.column('i', anchor='center', width=50)
        self.tabla.heading('Signal', text='Signal'); self.tabla.column('Signal' , anchor='center', width=100)
        self.tabla.heading('Suavisado', text='Suavisado'); self.tabla.column('Suavisado', anchor='center', width=100)
        lorden=tk.Label(self.ventana, text='Orden: ', font=(12))
        self.orden=ttk.Combobox(self.ventana, value=[2,3,4,5], width=5, font=(12)); self.orden.set(2)
        lmaximo=tk.Label(self.ventana, text='Maximo:', font=(12))
        self.maximo=ttk.Combobox(self.ventana, value=[10, 20, 100], width=5, font=(12)); self.maximo.set(100)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        boton_generar=tk.Button(self.ventana, text='Generar', font=(12), background='Blue', command=self.generar, width=7)
        boton_suavisar=tk.Button(self.ventana, text='Suavisar', font=(12), background='Blue', command=self.suavisar, width=7)
        boton_graficar=tk.Button(self.ventana, text='Graficar', font=(12), background='blue', command=self.graficar, width=7)
        boton_limpiar=tk.Button(self.ventana, text='Limpiar', font=(12), background='Blue', command=self.limpiar, width=7)
        boton_cerrar=tk.Button(self.ventana, text='Cerrar', font=(12), background='#780606', command=self.cerrar, width=7)
        frame.place(x=120, y=10)
        self.tabla.place(x=0, y=0, height=200)
        barra.place(x=380, y=10, height=200)
        lorden.place(x=180, y=220)
        self.orden.place(x=240, y=220)
        lmaximo.place(x=10, y=220)
        self.maximo.place(x=80, y=220)
        boton_generar.place(x=10, y=10)
        boton_suavisar.place(x=10, y=50)
        boton_graficar.place(x=10, y=90)
        boton_limpiar.place(x=10, y=130)
        boton_cerrar.place(x=10, y=170) 
