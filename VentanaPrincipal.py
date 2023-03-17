from tkinter import ttk
from tkinter import *
import tkinter as tk
import os
from os import *
from tkinter.messagebox import askokcancel, showinfo
from MostrarReceta import MostrarReceta
from Receta import Receta
from PIL import Image,ImageTk 
from PIL import *
from VentanaAgregar import VentanaAgregar
from VentanaEditar import VentanaEditar

class App(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.parent=parent
        width=1000
        height=600
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        parent.geometry(alignstr) 
        self.frame=tk.Frame(parent)
        self.frame.pack(expand=1)
        
        self.btn_agregar=ttk.Button(self.frame,text='Agregar Receta',command=self.ventana_agregar)
        self.btn_agregar.grid(row=1,column=0)
        
        self.btn_editar=ttk.Button(self.frame,text='Editar Receta',command=self.ventana_editar)
        self.btn_editar.grid(row=1,column=1)
        
        self.btn_eliminar=ttk.Button(self.frame,text='Eliminar Receta',command=self.eliminar_receta)
        self.btn_eliminar.grid(row=1,column=2)
        
        self.btn_mostrar=ttk.Button(self.frame,text='Ver Receta',command=self.ver_receta)
        self.btn_mostrar.grid(row=1,column=3)
        
        frame_lista=ttk.Frame(self.frame, borderwidth=2, relief="groove") 
        frame_lista=LabelFrame(self.frame,text='Recetas')
        frame_lista.grid(row=2, column=0,columnspan=5) 
        cabecera=('Nombre','Tiempo de Preparación','Tiempo de Cocción')
        
        # configuracion del alto de las filas rowheight
        arbol=ttk.Style()
        arbol.configure('my_style.Treeview', rowheight=80)
        tree_scroll=ttk.Scrollbar(frame_lista)
        tree_scroll.pack(side='right',fill='y')
        self.tabla=ttk.Treeview(frame_lista,columns=tuple(cabecera),style='my_style.Treeview',yscrollcommand=tree_scroll.set,selectmode='browse',show='tree',height=5)
        self.tabla.pack(padx=20,pady=20)
        
        tree_scroll.config(command=self.tabla.yview)
            
        carpeta_principal=os.path.dirname(__file__)
        self.carpeta_img=os.path.join(carpeta_principal,'media')
        if not os.path.exists(self.carpeta_img):
            os.makedirs(self.carpeta_img) 
        #parent.iconbitmap(os.path.join(carpeta_img,'emp.jpg'))
        
        self.tabla.column('#0',width=120,anchor='center')
        self.tabla.column('Nombre',width=150,anchor='center')
        self.tabla.column('Tiempo de Preparación',width=120,anchor='center')
        self.tabla.column('Tiempo de Cocción',width=120,anchor='center')

        for r in Receta.lista_recetas():
            imagen=Image.open(os.path.join(self.carpeta_img,r['Imagen']))
            self.img=ImageTk.PhotoImage(imagen)
            imagen_red=imagen.resize((120,80),Image.LANCZOS)
            self.img_red=ImageTk.PhotoImage(imagen_red)
            self.tabla.insert("","end",image=self.img_red,values=(r['Nombre'],'Tiempo Preparación:\n'+str(r['Tiempo_preparacion'])+' Minutos','Tiempo de Cocción:\n'+str(r['Tiempo_coccion'])+' Minutos'))        
        
    def ventana_agregar(self):
        toplevel=tk.Toplevel(self.parent)
        VentanaAgregar(toplevel)
        
    def ventana_editar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            fila = item['values'][0]
            receta=Receta.buscar_receta_nombre(fila)
            toplevel=tk.Toplevel(self.parent)
            VentanaEditar(toplevel,receta.get('Nombre'),receta.get('Ingredientes'),receta.get('Tiempo_preparacion'),
                        receta.get('Tiempo_coccion'),receta.get('Preparacion'),receta.get('Etiquetas'),receta.get('Imagen'),receta.get('favorita'))
        else:
            showinfo(message="Debe seleccionar una elemento primero")   
        
    def eliminar_receta(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            fila = item['values'][0] 
            for item in seleccion:
                res = askokcancel(title="Eliminar fila",
                    message=("Eliminar receta?"
                    "\n" + "".join(fila)))
                if res:
                    self.tabla.delete(item)
                    Receta.eliminar_receta(fila)
        else:
            showinfo(message="Debe seleccionar una elemento primero")         
    
    def ver_receta(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion)
            fila = item['values'][0]
            receta=Receta.buscar_receta_nombre(fila)
            toplevel=tk.Toplevel(self.parent)
            MostrarReceta(toplevel,receta.get('Nombre'),receta.get('Etiquetas'),receta.get('Tiempo_preparacion'),
                        receta.get('Tiempo_coccion'),receta.get('Ingredientes'),receta.get('Imagen'),receta.get('Preparacion'))
        else:
            showinfo(message="Debe seleccionar una elemento primero") 
            
root=tk.Tk()        
App(root).mainloop()
            