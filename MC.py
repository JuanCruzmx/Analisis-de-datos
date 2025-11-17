import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np
import csv

class Minimos:
    def __init__(self):
        self.main=tk.Toplevel()
        self.main.title('Metodo de Minimos Cuadrados')
        self.main.geometry('400x220+700+250')
        self.main.config(background='black')
        self.x=[]
        self.y=[]
        self.yp=[]
        self.constructores()
        self.main.mainloop()
    def constructores(self):
        boton_cerrar=tk.Button(self.main, text='Cerrar', command=self.cerrar, font=(12), background='Red', width=7)
        boton_generar=tk.Button(self.main, text='Generar', command=self.generar, font=(12), background='Blue', width=7)
        boton_promedio=tk.Button(self.main, text='Promedio', command=self.promedio, font=(12), background='Blue', width=7)
        boton_graficar=tk.Button(self.main, text='Graficar', command=self.graficar, font=(12), background='Blue', width=7)
        boton_limpiar=tk.Button(self.main, text='Limpiar', command=self.limpiar, font=(12), background='Blue', width=7)
        frame=tk.Frame(self.main, width=270, height=200, background='')
        self.tabla=ttk.Treeview(frame, columns=('n', 'x', 'y'), show='headings', height=10)
        self.tabla.heading('n', text='n'); self.tabla.column('n', anchor='center', width=50)
        self.tabla.heading('x', text='x'); self.tabla.column('x', anchor='center', width=100)
        self.tabla.heading('y', text='y'); self.tabla.column('y', anchor='center', width=100)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        boton_generar.place(x=10, y=10)
        boton_promedio.place(x=10, y=50)
        boton_graficar.place(x=10, y=90)
        boton_limpiar.place(x=10, y=130)
        boton_cerrar.place(x=10, y=170)
        frame.place(x=120, y=10)
        self.tabla.place(x=0, y=0)
        barra.place(x=250, y=0, height=200)
    def cerrar(self):
        self.main.destroy()
        plt.close()
    def limpiar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        plt.close('all')
        r=0
        self.x.clear()
        self.y.clear()
        self.yp.clear()
    def generar(self):
        ruta=filedialog.askopenfilename(title='Seleccionar archivo CSV:', filetypes=[('ArchivoS csv', '*.csv')])
        if not ruta:
            return
        with open(ruta, 'r', newline='') as archivo:
            f=archivo.readlines()
            for linea in f[1:]:
                linea=linea.strip()
                x,y=linea.split(',')
                self.x.append(int(x))
                self.y.append(int(y))
            for i in range(len(self.x)):
                self.tabla.insert('', 'end', values=(i+1, self.x[i], self.y[i]))
    def promedio(self):
        self.yp.clear()
        if not self.x:
            messagebox.showinfo('VACIA', 'La tabla esta vacia')
            return
        px=sum(self.x)/len(self.x)
        py=sum(self.y)/len(self.y)
        desv_x=sum((xi-px)**2 for xi in self.x)
        desv_y=sum((yi-py)**2 for yi in self.y)
        n=sum((xi-px)*(yi-py) for xi,yi in zip(self.x,self.y))
        d=np.sqrt(desv_x)*np.sqrt(desv_y)
        self.r=round(n/d,2)
        a=round(n/desv_x, 2)
        b=round(py-a*px, 2)
        for xi in self.x:
            self.yp.append(a*xi+b)
    def graficar(self):
        plt.clf()
        if not self.x:
            messagebox.showinfo('Vacia', ' La tabla esta vacia...')
        else:
            plt.scatter(self.x, self.y, color='blue', label='Datos')
            plt.plot(self.x, self.y, color='black', label=f'Recta') 
            plt.plot(self.x, self.yp, color='blue', label=f'r={self.r}')
            plt.get_current_fig_manager().window.wm_geometry('+1200+200')
            plt.title('MC')
            plt.ylim(bottom=9)
            plt.xticks(self.x)
            plt.yticks(range(self.y[0], self.y[-1], 1000))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.show()
