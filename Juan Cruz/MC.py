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
        self.n=[]
        self.x=[]
        self.y=[]
        self.yp=[]
        self.constructores()
        self.main.mainloop()
    def constructores(self):
        boton_cerrar=tk.Button(self.main, text='Cerrar', command=self.cerrar, font=(12), background='Red', width=7)
        boton_generar=tk.Button(self.main, text='Generar', command=self.generar, font=(12), background='Blue', width=7)
        boton_limpiar=tk.Button(self.main, text='Limpiar', command=self.limpiar, font=(12), background='Blue', width=7)
        frame=tk.Frame(self.main, width=270, height=200, background='')
        self.tabla=ttk.Treeview(frame, show='headings', height=9)
        barra=ttk.Scrollbar(frame, orient='vertical', command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        f=tk.Label(self.main, text='X=', font=(12), background='black', foreground='white')
        self.entry=tk.Entry(self.main, font=(12), width=7)
        entrada=tk.Button(self.main, text='Ver', font=(12), background='Blue', width=7, command=self.error)
        self.label=tk.Label(self.main, text='', background='black', foreground='white', font=(12))
        self.label2=tk.Label(self.main, text='', font=(12), background='black', foreground='white')
        self.label3=tk.Label(self.main, text='', font=(12), background='black', foreground='white')
        self.label4=tk.Label(self.main, text='', font=(12), background='black', foreground='white')
        boton_generar.place(x=10, y=10)
        boton_limpiar.place(x=10, y=50)
        boton_cerrar.place(x=10, y=90)
        f.place(x=10, y=220)
        self.entry.place(x=40, y=220)
        entrada.place(x=120, y=220)
        self.label.place(x=10, y=260)
        self.label2.place(x=10, y=300)
        self.label3.place(x=180, y=300)
        self.label4.place(x=200, y=260)
        frame.place(x=120, y=10)
        self.tabla.place(x=0, y=0, width=250, height=200)
        barra.place(x=250,y=0, height=200)
    def cerrar(self):
        self.main.destroy()
        plt.close()
    def limpiarr(self):
        self.label.config(text='')
        self.label2.config(text='')
        self.label3.config(text='')
        self.label4.config(text='')
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
        self.limpiar()
        with open(ruta, newline='', encoding='utf-8') as archivo:
            filas=csv.reader(archivo)
            self.encabezado=next(filas)
            self.tabla['columns']=self.encabezado
            for col in self.encabezado:
                self.tabla.heading(col,text=col)
                if col=='n':
                    self.tabla.column(col,anchor='center',width=50)
                else:
                    self.tabla.column(col, anchor='center',width=80)
            for fila in filas:
                self.tabla.insert('', 'end', values=fila)
                self.n.append(fila[0])
                self.x.append(float(fila[1]))
                self.y.append(float(fila[2]))
        self.promedio()
    def promedio(self):
        self.yp.clear()
        px=sum(self.x)/len(self.x)
        py=sum(self.y)/len(self.y)
        desv_x=sum((xi-px)**2 for xi in self.x)
        desv_y=sum((yi-py)**2 for yi in self.y)
        n=sum((xi-px)*(yi-py) for xi,yi in zip(self.x,self.y))
        d=np.sqrt(desv_x)*np.sqrt(desv_y)
        self.r=round(n/d,2)
        self.a=round(n/desv_x, 2)
        self.b=round(py-self.a*px, 2)
        for x in self.x:
            self.yp.append(self.a*x+self.b)
        self.graficar()
    def graficar(self):
        plt.clf()
        plt.scatter(self.x, self.y, color='blue', label='Datos')
        plt.plot(self.x, self.y, color='black') 
        plt.plot(self.x, self.yp, color='red', label=f'r={self.r}')
        plt.get_current_fig_manager().window.wm_geometry('+1200+200')
        plt.title('MC')
        plt.ylim(bottom=9)
        #plt.xticks(np.arange(min(self.x), max(self.x)+0.5, 0.5))
        #plt.yticks(np.arange(min(self.y), max(self.y)+5, 5))
        plt.xlabel(self.encabezado[1])
        plt.ylabel(self.encabezado[2])
        plt.legend()
        plt.grid(True)
        plt.show()
    def error(self):
        self.label3.config(text=f'y={self.a}x+{self.b}')
        try:
            n=self.x.index(float(self.entry.get()))
            vmedido=self.y[n]
            if self.punto is not None:
                self.punto.remove()
                self.lx.remove()
                self.ly.remove()
            self.punto, =plt.plot(float(self.entry.get()), self.y[n], 'ro', label=f'Punto x={float(self.entry.get())}')
            plt.legend()
            self.lx=plt.axvline(float(self.entry.get()), linestyle='--')
            self.ly=plt.axhline(self.y[n], linestyle='--')
            plt.draw()
            vcalculada=self.a*float(self.entry.get())+self.b
            e_a=abs(vmedido-vcalculada)
            self.label.config(text=f'|e|={round(e_a,2)}')
            self.label4.config(text=f'e_r={round((e_a/self.y[n])*100, 2)}%')
            self.label2.config(text=f'F(x)={round(vcalculada, 2)}')
        except ValueError:
            prediccion=self.a*float(self.entry.get())+self.b
            self.label.config(text='La estimacion es de...')
            self.label2.config(text=f'F(x)={round(prediccion, 2)}')
            messagebox.showinfo('No se encuentra en la lista', f'x={self.entry.get()} la aproxamación es {prediccion}') 
