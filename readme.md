

# **Librarian** #
## recomendador de libros ##

Librarian es un recomendador de libros **basado en los libros que has leidoy la nota** 
que le pondrias(1 la mas baja, 5 la mas alta)


---

### **Instalacion** ###

	`pip install requeriments.txt`

### **Getting Started** ###

Preparar los datos necesarios para que funcione.
ejecutaremos el jupyter-notebook que hay en la carpeta preprocess 
y ejecutaremos las celdas por debajo del titulo  *Fast instalation*:

	`jupyter-notebook preprocess/data_clean.ipynb`

Despues procedemos  arrancar el servidor flask:

	`python main.py`

y poor ultimo arrancaremos el servidor  streamlit:

	`streamlit run streamlit.py`


---
### **Uso** ###

La herramienta esta basada en el modelo de maching learning *K means* 
en el cual se recogen las  reviews de 1M de usuarios,  a una lista  de 10K libros
y basandose en sus opiniones, es capaz de generar una clasificacion de los mismo segun sus gustos.

A continuacion vemos una representacion de de los usuarios diferenciados por el grupo en el cual la herramienta los ha  clasificado:

![clusters](/src/images/clusters.png "Clusters")

Con esto podemos predecir a que grupo pertenecera un usuario si conocemos los libros que ha leido y la calificacion que les pondria, gracias al modelo, y asi poder  realizar una recomendacion basada en libros que gutaron a usuarios 
similares del mismo grupo

Se  da la opcion de elegir entre 3 tipos de modelo:

    General: Menos restrictivo, crea grupos mas generales y grandes.

    Equilibrado (Optimo): Toma en cuenta  el numero ooptimoo  de grupos en  funcion de la cantitadad de usuarios  con los que  ha entrenado  el modelo

    Especifico: Crea grupos mas especificos definiendo mucho mas la diferencia entre grupos


**A continuación capturas de la herramienta**:

![cap1](/src/images/cap1.png "Capture 1")

- - - - - 

![cap2](/src/images/cap2.png "Capture 2")



<h3 align="left">Languages and Tools:</h3>
<p align="left"> <a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a> <a href="https://flask.palletsprojects.com/" target="_blank"> <img src="https://www.vectorlogo.zone/logos/pocoo_flask/pocoo_flask-icon.svg" alt="flask" width="40" height="40"/> </a> <a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a> <a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a> <a href="https://redis.io" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/redis/redis-original-wordmark.svg" alt="redis" width="40" height="40"/> </a> </p>