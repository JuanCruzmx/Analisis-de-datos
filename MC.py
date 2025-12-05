import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
import numpy as np
import csv

class Minimos:
    def __init__(self):
        self.main=tk.Toplevel()
        self.main.title('Metodo de Minimos Cuadrados')
        self.main.geometry('400x350+700+250')
        self.main.config(background='black')
        self.punto=None
        self.lx=None
        self.ly=None
        self.x=[]
        self.y=[]
        self.yp=[]
        self.constructores()
        self.main.mainloop()
    def constructores(self):
        boton_cerrar=tk.Button(self.main, text='Cerrar', command=self.cerrar, font=(12), background='Red', width=7)
        boton_generar=tk.Button(self.main, text='Generar', command=self.generar, font=(12), background='Blue', width=7)
        boton_graficar=tk.Button(self.main, text='Graficar', command=self.graficar, font=(12), background='Blue', width=7)
        boton_limpiar=tk.Button(self.main, text='Limpiar', command=self.limpiar, font=(12), background='Blue', width=7)
        frame=tk.Frame(self.main, width=270, height=200, background='')
        self.tabla=ttk.Treeview(frame, columns=('n', 'x', 'y'), show='headings', height=10)
        self.tabla.heading('n', text='n'); self.tabla.column('n', anchor='center', width=50)
        self.tabla.heading('x', text='x'); self.tabla.column('x', anchor='center', width=100)
        self.tabla.heading('y', text='y'); self.tabla.column('y', anchor='center', width=100)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        self.entry=tk.Entry(self.main, font=(12), width=7)
        entrada=tk.Button(self.main, text='Ver', font=(12), background='Blue', width=7, command=self.error)
        self.label=tk.Label(self.main, text='', background='black', foreground='white', font=(12))
        self.label2=tk.Label(self.main, text='', font=(12), background='black', foreground='white')
        self.label3=tk.Label(self.main, text='', font=(12), background='black', foreground='white')
        self.label4=tk.Label(self.main, text='', font=(12), background='black', foreground='white')
        boton_generar.place(x=10, y=10)
        boton_graficar.place(x=10, y=50)
        boton_limpiar.place(x=10, y=90)
        boton_cerrar.place(x=10, y=130)
        self.entry.place(x=10, y=220)
        entrada.place(x=100, y=220)
        self.label.place(x=10, y=260)
        self.label2.place(x=10, y=300)
        self.label3.place(x=180, y=300)
        self.label4.place(x=200, y=260)
        frame.place(x=120, y=10)
        self.tabla.place(x=0, y=0)
        barra.place(x=250, y=0, height=200)
    def cerrar(self):
        self.main.destroy()
        plt.close()
    def limpiar(self):
        self.entry.delete('0',tk.END)
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        plt.close('all')
        r=0
        self.x.clear()
        self.y.clear()
        self.yp.clear()
        self.label.config(text='')
        self.label2.config(text='')
        self.label3.config(text='')
        self.label4.config(text='')
    def generar(self):
        ruta=filedialog.askopenfilename(title='Seleccionar archivo CSV:', filetypes=[('ArchivoS csv', '*.csv')])
        if not ruta:
            return
        with open(ruta, 'r', newline='') as archivo:
            f=archivo.readlines()
            for linea in f[1:]:
                x, y=[j.strip() for j in linea.split(',')[:2]]
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
        self.a=round(n/desv_x, 2)
        self.b=round(py-self.a*px, 2)
        for xi in self.x:
            self.yp.append(self.a*xi+self.b)
    def graficar(self):
        plt.clf()
        if not self.x:
            messagebox.showinfo('Vacia', ' La tabla esta vacia...')
        else: 
            self.promedio()
            plt.scatter(self.x, self.y, color='blue', label='Datos')
            plt.plot(self.x, self.y, color='black') 
            plt.plot(self.x, self.yp, color='blue', label=f'r={self.r}')
            plt.get_current_fig_manager().window.wm_geometry('+1200+200')
            plt.title('MC')
            plt.ylim(bottom=9)
            plt.xticks(range(min(self.x), max(self.x)+1, 10))
            plt.yticks(range(min(self.y), max(self.y)+1, 10))
            plt.xlabel('x')
            plt.ylabel('y')
            plt.legend()
            plt.grid(True)
            plt.show()
    def error(self):
        n=self.x.index(int(self.entry.get()))
        e_a=abs(n-self.r)
        if self.punto is not None:
            self.punto.remove()
            self.lx.remove()
            self.ly.remove()
        self.punto, =plt.plot(int(self.entry.get()), self.y[n], 'ro', label=f'Punto {int(self.entry.get())}')
        plt.legend()
        self.lx=plt.axvline(int(self.entry.get()), linestyle='--')
        self.ly=plt.axhline(self.y[n], linestyle='--')
        plt.draw()
        self.label.config(text=f'Error Absoluto={round(e_a,2)}')
        self.label4.config(text=f'Error Relativo={round((e_a/int(self.entry.get()))*100, 2)}')
        self.label2.config(text=f'F(x)={round(self.a*int(self.entry.get())+self.b, 2)}')
        self.label3.config(text=f'y={self.a}x+{self.b}')
