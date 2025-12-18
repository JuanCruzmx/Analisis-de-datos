import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox, ttk
import random
import numpy as np

class Rl:
    def __init__(self):
        self.rl=tk.Toplevel()
        self.rl.title('Regresión Lineal')
        self.rl.geometry('350x260+700+200')
        self.rl.config(background='black')
        self.x=[]
        self.y=[]
        self.yp=[]
        self.r=0
        self.constructores()
    def constructores(self):
        label=tk.Label(self.rl, text='Tamaño:', font=(11), width=7, background='blue')
        self.entry=tk.Entry(self.rl, width=7, font=(11))
        boton_cerrar=tk.Button(self.rl, text='Cerrar', command=self.cerrar, font=(11), background='Red', width=7)
        boton_generar=tk.Button(self.rl, text='Generar', command=self.generar, font=(11), background='Blue', width=7)
        boton_promedio=tk.Button(self.rl, text='Promedio', command=self.promedio, font=(11), background='Blue', width=7)
        boton_graficar=tk.Button(self.rl, text='Graficar', command=self.graficar, font=(11), background='Blue', width=7)
        boton_limpiar=tk.Button(self.rl, text='Limpiar', command=self.limpiar, font=(11), background='Blue', width=7)
        frame=tk.Frame(self.rl, width=220, height=210, background='black')
        self.tabla=ttk.Treeview(frame, columns=('x', 'y'), show='headings')
        self.tabla.heading('x', text='x'); self.tabla.column('x', anchor='center', width=100)
        self.tabla.heading('y', text='y'); self.tabla.column('y', anchor='center', width=100)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        boton_generar.place(x=10, y=10)
        boton_promedio.place(x=10, y=50)
        boton_graficar.place(x=10, y=90)
        boton_limpiar.place(x=10, y=130)
        boton_cerrar.place(x=10, y=170)
        label.place(x=120, y=10)
        self.entry.place(x=200, y=10)
        frame.place(x=120, y=40)
        self.tabla.place(x=0, y=0, height=210)
        barra.place(x=200, y=0, height=210)
        self.tabla.configure(yscrollcommand=barra.set)
    def mensaje(self):
        messagebox.showinfo('VACIO', 'La tabla esta vacia...')
    def cerrar(self):
        self.rl.destroy()
        plt.close('all')
    def limpiar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        self.x.clear()
        self.y.clear()
        self.yp.clear()
        self.r=0
        plt.close('all')
    def generar(self):
        self.x.clear()
        self.y.clear()
        try:
            self.mi, ma=map(int, self.entry.get().split('-'))
            for i in range(50):
                self.x.append(round(random.uniform(self.mi, ma), 1))
                self.y.append(round(random.uniform(-10, 10)+self.x[i], 1))
                self.tabla.insert('', 'end', values=(self.x[i], self.y[i]))
        except:
            messagebox.showerror('ERROR', 'Ingresa el tamaño\nFormato (min - max)')
    def promedio(self):
        self.yp.clear()
        if not self.x:
            self.mensaje()
            return
        px=sum(self.x)/len(self.x)
        py=sum(self.y)/len(self.y)
        desv_x=sum((xi-px)**2 for xi in self.x)
        desv_y=sum((yi-py)**2 for yi in self.y)
        n=sum((xi-px)*(yi-py) for xi,yi in zip(self.x,self.y))
        d=np.sqrt(desv_x)*np.sqrt(desv_y)
        self.r=round(n/d, 2)
        a=round(n/desv_x, 3)
        self.b=round(py-a*px, 3)
        for xi in self.x:
            self.yp.append(a*xi+self.b)
        messagebox.showinfo('SE CALCULO LOS PROMEDIOS', 'Promedios calculados...')
    def graficar(self):
        if not self.tabla.get_children():
            self.mensaje()
        else:
            plt.clf()
            plt.scatter(self.x, self.y, color='blue', label='Datos')
            plt.plot(self.x, self.yp, color='black', label=f'r={self.r}')
            plt.get_current_fig_manager().window.wm_geometry('+1100+200')
            plt.title('Regresión Lineal')
            plt.xlim(left=self.mi)
            plt.ylim(bottom=0)
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.show() 
