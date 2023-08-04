# TODO app

Es una pequeña aplicación con GUI de tareas pendientes, creada con Python, Tkinter y MySQL Connector/Python.  

La aplicación utiliza un servidor local MySQL para almacenar los datos, y necesita en su archivo de configuración las credenciales de un usuario existente y con permisos.  

## Funcionalidades

* La aplicación almacena tareas, las cuales tiene una descripción, un estado (completado) y una fecha de creacion.
* Las tareas se muestran en una grilla o tabla ordenadas por fecha de creación. Se puede ver su descripción y si está completada o no. También permite mostrar solo las tareas pendientes o solo las completadas.  
* Permite crear tareas nuevas.  
* Permite cambiar el estado de una tarea a completada. No permite volver al estado pendiente.  
* Permite eliminar una tarea (este completada o no).  
* Permite modificar la descripción de una tarea.  

Se divide en 4 archivos:

* `main.py`: es el entry point de la aplicación. Se asegura de que exista la base de datos y crea la ventana principal.  
* `ui.py`: contiene 2 clases para las ventanas principal y de tarea.  
* `datos.py`: contiene funciones para el acceso a datos.  
* `config.py`: contiene una variable con la ruta de acceso del icono y una variable con el diccionario de las credenciales de acceso a la base de datos. Es recomendable no modificar el nombre de la base de datos, solo el usuario y contraseña.

Finalmente, el proyecto contiene una carpeta `img` en donde se almacena el icono de la aplicación.