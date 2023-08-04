import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno

import datos

class Principal(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.ventana = parent
        self.salir = lambda: parent.destroy()

        self.columnconfigure(0, weight=1)   # descripcion
        self.columnconfigure(1, weight=1)   # check
        self.columnconfigure(2, weight=1)   # check
        self.columnconfigure(3, weight=0)   # scrollbar

        # self.columnconfigure(3, weight=0)   # scrollbar
        self.rowconfigure(0, weight=1)  # titulo
        self.rowconfigure(1, weight=1)  # tipos
        self.rowconfigure(2, weight=1)  # tareas
        self.rowconfigure(3, weight=1)  # acciones
        self.rowconfigure(4, weight=1)  # salir

        ttk.Label(self, text="TODO app").grid(row=0, column=0, columnspan=4)
        self.set_botonera1()
        self.set_botonera2()
        self.set_tabla()
        btn_salir = ttk.Button(self, text="Salir", command=self.salir)
        btn_salir.grid(row=4, column=1, columnspan=2, sticky=tk.E)

        self.cargar_tabla()
    
    def cargar_tabla(self, tipo="all"):
        """Cargar la tabla con las tareas segun el tipo.
        
        Tipo es 'all' (todas), 'done' (completadas) o 'pending' (pendientes)
        """
        self.vaciar_tabla()
        registros = datos.get_tareas(tipo)
        for id_tarea, tarea, completada in registros:
            self.tabla.insert('', tk.END,
                              values=(id_tarea, tarea, "Si" if completada else "No"))
        
        # ¡Aca escondemos la primera columna 'ID' con los ids de cada tarea!
        self.tabla["displaycolumns"] = ('tarea', 'completada')
        
    def vaciar_tabla(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

    def set_tabla(self):
        """Crear la tabla con tres columnas, id, tarea y completada.
        
        La columna ID se va a ocultar para que el usuario no la vea,
        ya que no le interesa cual es el id de cada tarea.
        De todas formas podemos obeneter el id de cada tarea despues.
        """
        columnas = ('id', 'tarea', 'completada')
        self.tabla = ttk.Treeview(self, columns=columnas,show='headings',
                                  selectmode="browse") # sin multi-seleccion
        self.tabla.grid(row=2, column=0, columnspan=3, sticky=(tk.NSEW))
        scroll = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.tabla.yview)
        scroll.grid(row=2, column=3, sticky=tk.NS)
        self.tabla.configure(yscroll=scroll.set)
        self.tabla.heading('id', text='ID')
        self.tabla.heading('tarea', text='Descripcion')
        self.tabla.heading('completada', text='Completada')

    def set_botonera1(self):
        """crear la botonera para mostrar tareas en la tabla"""
        botonera1 = ttk.Frame(self)
        botonera1.grid(row=1, column=0, columnspan=4)
        botonera1.columnconfigure(0, weight=1)
        botonera1.columnconfigure(1, weight=1)
        botonera1.columnconfigure(2, weight=1)
        btn_pendientes = ttk.Button(botonera1, text="Mostrar solo pendientes",
                                    command=lambda:self.cargar_tabla("pending"))
        btn_pendientes.grid(row=0, column=0, padx=3, pady=3)
        btn_completadas = ttk.Button(botonera1, text="Mostrar solo completadas",
                                     command=lambda:self.cargar_tabla("done"))
        btn_completadas.grid(row=0, column=1, padx=3, pady=3)
        btn_todo = ttk.Button(botonera1, text="Mostrar todo",
                              command=lambda:self.cargar_tabla("all"))
        btn_todo.grid(row=0, column=2, padx=3, pady=3)
    
    def set_botonera2(self):
        """crear botonera de abm de tareas"""
        botonera2 = ttk.Frame(self)
        botonera2.grid(row=3, column=0, columnspan=4)
        botonera2.columnconfigure(0, weight=1)
        botonera2.columnconfigure(1, weight=1)
        botonera2.columnconfigure(2, weight=1)
        btn_completar = ttk.Button(botonera2, text="Completar", command=self.completar)
        btn_completar.grid(row=0, column=0, padx=3, pady=3)
        
        btn_editar = ttk.Button(botonera2, text="Editar", command=self.modificar)
        btn_editar.grid(row=0, column=1, padx=3, pady=3)

        btn_eliminar = ttk.Button(botonera2, text="Eliminar", command=self.eliminar)
        btn_eliminar.grid(row=0, column=2, padx=3, pady=3)
        
        btn_nueva = ttk.Button(botonera2, text="Nueva", command=self.agregar)
        btn_nueva.grid(row=0, column=3, padx=3, pady=3)

    def agregar(self):
        """Abrir ventana para crear nueva tarea."""
        ventana_tarea = tk.Toplevel(self.ventana)
        Tarea(ventana_tarea, self.cargar_tabla).grid(row=0, column=0, sticky=tk.NSEW)

    def modificar(self):
        """Abrir ventana para modificar una tarea."""
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            id_tarea = item['values'][0] # id de la tarea obtenida del treeview
            tarea = item['values'][1]
            ventana_tarea = tk.Toplevel(self.ventana)
            frame = Tarea(ventana_tarea, self.cargar_tabla,
                          id_tarea=id_tarea, texto_tarea=tarea)
            frame.grid(row=0, column=0, sticky=tk.NSEW)
        else:
            messagebox.showinfo(message="Debe seleccionar una tarea primero")

    def completar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            id_tarea = item['values'][0] # id de la tarea obtenida del treeview
            completada = item['values'][2]
            if completada == "Si":
                messagebox.showinfo(message="La tarea ya estaba completada   ¬¬")
                return
            datos.completar_tarea(id_tarea)
            messagebox.showinfo(message="Tarea completada :)")
            self.cargar_tabla()
        else:
            messagebox.showinfo(message="Debe seleccionar una tarea primero")

    def eliminar(self):
        seleccion = self.tabla.selection()
        if seleccion:
            item = self.tabla.item(seleccion[0])
            id_tarea = item['values'][0] # id de la tarea obtenida del treeview
            tarea = item['values'][1]
            mensaje = f"Esta a punto de eliminar la tarea: {tarea}.\n¿Desea continuar?"
            if askyesno(title="Eliminar tarea", message=mensaje):
                datos.eliminar_tarea(id_tarea)
                messagebox.showinfo(message="Tarea eliminada.")
                self.cargar_tabla()
        else:
            messagebox.showinfo(message="Debe seleccionar una tarea primero")

class Tarea(ttk.Frame):
    """
    Frame para la ventana que muestra una tarea para modificacion
    o el formulario para crear una nueva."""
    def __init__(self, parent, actualizar_tareas, id_tarea=None, texto_tarea=None):
        super().__init__(parent, padding=10)
        parent.focus()
        parent.grab_set()
        self.cerrar_ventana = lambda:parent.destroy()
        self.actualizar_tareas = actualizar_tareas
        self.id_tarea = id_tarea

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # label
        ttk.Label(self, text="Tarea").grid(row=0, column=0)
        # entry + var
        self.tarea_text = tk.StringVar()
        tarea_entry = ttk.Entry(self, textvariable=self.tarea_text, width=60)
        tarea_entry.grid(row=0, column=1, padx=3, pady=3)
        tarea_entry.focus_set()
        # botonera
        botonera = ttk.Frame(self)
        botonera.grid(row=1, column=0, columnspan=2, sticky=tk.E)
        # boton cancelar
        btn_cancelar = ttk.Button(botonera, text="Cancelar", command=self.cerrar_ventana)
        btn_cancelar.grid(row=0, column=0, padx=3, pady=3, sticky=tk.E)
        btn_guardar = ttk.Button(botonera, text="Agregar", command=self.guardar)
        btn_guardar.grid(row=0, column=1, padx=3, pady=3, sticky=tk.E)

        if id_tarea is not None:
            # modificar la tarea
            self.tarea_text.set(texto_tarea)
            btn_guardar.configure(text="Modificar")
        
        parent.bind('<Return>', lambda e: btn_guardar.invoke())

    def guardar(self):
        tarea = self.tarea_text.get()
        if self.id_tarea is not None:
            datos.actualizar_tarea(self.id_tarea, tarea)
        else:
            datos.nueva_tarea(tarea)
        # actualizar tabla
        self.actualizar_tareas()
        # cerrar ventana
        self.cerrar_ventana()