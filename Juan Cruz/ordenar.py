import tkinter as tk
import random
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import ttk
from matplotlib.pyplot import plot, show, legend, xlabel, ylabel, grid

valores=[]
originales=[]

class Ordenar:
    def __init__(self):
        self.main=tk.Toplevel()
        self.main.title('Ordenar')
        self.main.geometry('370x270+660+200')
        self.main.config(background='Black')
        self.main.resizable(False, False)
        frame=tk.Frame(self.main,width=215, height=250)
        self.tabla=ttk.Treeview(frame, columns=('Datos', 'Ordenado'), show='headings')
        self.tabla.heading('Datos', text='Valores'); self.tabla.column('Datos', width=100, anchor='center')
        self.tabla.heading('Ordenado', text='Ordenado'); self.tabla.column('Ordenado', width=100, anchor='center')
        maximo_label=tk.Label(self.main, text='Maximo:', font=(12))
        self.maximo=ttk.Combobox(self.main, value=[10, 100, 1000], width=5, font=(12)); self.maximo.set(100)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        boton_generar=tk.Button(self.main, text='Generar', font=(12), background='#004478', width=7, command=self.generar)
        boton_a=tk.Button(self.main, text='Acendente', font=(12), background='#004478', width=7, command=self.acendente)
        boton_d=tk.Button(self.main, text='Decendente', font=(12), background='#004478', width=7, command=self.decendente)
        boton_limpiar=tk.Button(self.main, text='Limpiar', font=(12), background='#004478', width=7, command=self.limpiar)
        boton_cerrar=tk.Button(self.main, text='Cerrar', font=(12), background='#780000', width=7, command=self.cerrar)
        frame.place(x=150, y=10)
        self.tabla.place(x=0, y=0, height=250)
        barra.place(x=200, y=0, height=250)
        self.tabla.configure(yscrollcommand=barra.set)
        maximo_label.place(x=10, y=10)
        self.maximo.place(x=80, y=10)
        boton_generar.place(x=10, y=40)
        boton_a.place(x=10, y=80)
        boton_d.place(x=10, y=120)
        boton_limpiar.place(x=10, y=160)
        boton_cerrar.place(x=10, y=200)
    def mensaje(self):
        messagebox.showinfo('Vacio', 'La tabla esta vacia...')
    def limpiar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
    def limpiar(self):
        valores.clear()
        originales.clear()
        for i in self.tabla.get_children():
            self.tabla.delete(i)
    def cerrar(self):
        self.main.destroy()
    def generar(self):
        n=int(self.maximo.get())
        for i in range(n):
            r=random.randint(1, 100)
            valores.append(r)
            originales.append(r)
            self.tabla.insert('', 'end', values=(originales[i], ''))
    def acendente(self):
        if not self.tabla.get_children():
            self.mensaje()
        else:
            n=len(valores)
            self.limpiar_tabla()
            for i in range(n-1):
                for j in range(n-i-1):
                    if valores[j]>valores[j+1]:
                        auxiliar=valores[j]
                        valores[j]=valores[j+1]
                        valores[j+1]=auxiliar
            for j in range(n):
                self.tabla.insert('', 'end', values=(originales[j], valores[j])) 
    def decendente(self):
        if not self.tabla.get_children():
            self.mensaje()
        else:
            self.limpiar_tabla()
            n=len(valores)
            for i in range(n-1):
                for j in range(n-i-1):
                    if valores[j]<valores[j+1]:
                        auxiliar=valores[j]
                        valores[j]=valores[j+1]
                        valores[j+1]=auxiliar
            for j in range(n):
                self.tabla.insert('', 'end', values=(originales[j], valores[j])) 
