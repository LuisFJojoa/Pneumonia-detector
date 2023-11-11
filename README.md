## Curso - Desarrollo de proyectos de IA

Entrega preliminar a cargo de Luis Fernando Jojoa Quintero

## Hola! Bienvenido a la herramienta para la detección rápida de neumonía

Deep Learning aplicado en el procesamiento de imágenes radiográficas de tórax en formato DICOM con el fin de clasificarlas en 3 categorías diferentes:

1. Neumonía Bacteriana

2. Neumonía Viral

3. Sin Neumonía

Aplicación de una técnica de explicación llamada Grad-CAM para resaltar con un mapa de calor las regiones relevantes de la imagen de entrada.

---

## Arquitectura de archivos propuesta.

### main.py

Es la entrada principal del proyecto, se encarga de inicializar todas las instancias necesarias para el correcto funcionamiento de la aplicación. Es aquí donde se lee el archivo binario del modelo de red neuronal convolucional previamente entrenado llamado 'conv_MLP_84.h5'.

### app.py

Contiene la lógica de la aplicación. Se encarga de correr el modelo de predicción y crear los archivos CSV y PDF correspondientes a la predicción realizada.

### gui.py

Contiene el diseño de la interfaz gráfica utilizando Tkinter. Los botones llaman métodos contenidos en otros scripts.

### image.py

Se tiene la clase ImageLoader que permite cargar la imagen desde el ordenador, identificar que formato tiene dicha imagen y con base en ello realiza un proceso de lectura acorde al formato. Adicionalmente, permite validar si un formato de imagen es valido o no y realizar el pre-procesamiento de la imagen que se utilizará para el modelo de predicción. Para esto último se tienen encuenta los siguientes pasos:

- Resize a 512x512
- conversión a escala de grises
- ecualización del histograma con CLAHE
- normalización de la imagen entre 0 y 1
- conversión del arreglo de imagen a formato de batch (tensor)

### grad_cam.py

Script que recibe la imagen y la procesa.

### ia_model.py

Script que aplicando el modelo gradCAM obtiene la predicción y la capa convolucional de interés para obtener las características relevantes de la imagen
como la etiqueta, el heatmap y la probabilidad.

### utils.py

Script que contiene métodos utilizados dentro de la aplicación y se separan de la GUI con el fin de reducir el acople e incrementar cohesión. Dichos métodos sirven para crear o editar el archivo CSV con los nuevos datos y generar un archivo PDF con la evidencia encontrada después de realizar la predicción.

---

## Uso de la herramienta:

A continuación le explicaremos cómo empezar a utilizarla.

Requerimientos necesarios para el funcionamiento:

### Funcionamiento local para Mac/Linux/Windows:

- Instale Anaconda siguiendo las siguientes instrucciones (Seleccione su sistema operativo):
  https://docs.anaconda.com/anaconda/install/

- Si tiene windows abra Anaconda Prompt (En macOS o Linux lo puede hacer directamente en la terminar) y ejecute las siguientes instrucciones:

  cd ruta/proyecto/local por ejemplo cd C:\Users\user\\Desktop\Neumonia_proyecto\pneumonia_detector\pneumonia_detector

  ````conda create -n tf tensorflow
  conda activate tf
  pip install -r requirements.txt```

  ````

- Para realizar las pruebas unitarias ejecute la siguiente instrucción:

  `pytest test/nombre_de_test (cambie el 'nombre_de_test' por cualquiera de los tres test que se encuentran dentro de la carpeta)`

- Para levantar la aplicación y desplegar la interfaz ejecute la siguiente instrucción:

  `python main.py`

Uso de la Interfaz Gráfica:

- Ingrese la cédula del paciente en el campo "Personal ID"
- Presione el botón 'Load X Ray Image', seleccione la imagen del explorador de archivos del computador (Las imágenes de prueba están dentro de este proyecto en la carpeta volumes)
- Presione el botón 'Predict' y espere unos segundos hasta que observe los resultados.
- Presione el botón 'Save CSV File' para almacenar la información del paciente en un archivo excel con extensión .csv
- Presione el botón 'Download Pdf' para descargar un archivo PDF con la información desplegada en la interfaz
- Presión el botón 'Clear data' para limpiar la interfaz y cargar una nueva imagen

---

### Funcionamiento para contenedor haciendo uso de Docker:

- Instale la aplicación xming (Para windows) o xquartz (Para macOS), cualquiera de estos es un servicio de aplicaciones gráficas. Permite ejecutar gráficamente cualquier aplicación desde un ordenador con Windows accediendo de forma remota a un sistema Linux, por ejemplo a través de un cliente SSH. Esto permite que se conecte con docker para usarse como pantalla y visualizar el contenido que requiera de esta.
- Descargue Docker-desktop en [mac](https://docs.docker.com/docker-for-mac/install/#download-docker-for-mac) o [windows](https://docs.docker.com/docker-for-windows/install/#download-docker-for-windows)
- Abra la aplicación Docker Desktop
- Abra la aplicación xming o xquartz
- dirijase a la ruta del proyecto cd ruta/proyecto/local y asegurese de que está en la ruta donde se encuentra el archido Dockerfile
- Ejecute el siguiente comando `docker build -t pneumonia_detector .`
- Una vez termine el proceso, en Docker Desktop en la pestaña images encontrará la imagen creada con el nombre _pneumonia_detector_
- Ejecute el siguiente comando `docker run -it --rm -e DISPLAY=host.docker.internal:0.0 -v "%cd%"/volumes:/home/volumes pneumonia_detector`
- Dirigite nuevamente a Docker Desktop y abre el contenedor que se acaba de levantar
- Clic en la pestaña Terminal
- Entra a la carpeta `cd pneumonia_detector`
- Ejecuta el siguiente comando para realizar los test `pytest test/nombre/de/test.py/`
- Ejecuta el siguiente comando para levantar la aplicación en el contenedor `python main.py`

## Acerca del Modelo

La red neuronal convolucional implementada (CNN) es basada en el modelo implementado por F. Pasa, V.Golkov, F. Pfeifer, D. Cremers & D. Pfeifer en su artículo Efcient Deep Network Architectures for Fast Chest X-Ray Tuberculosis Screening and Visualization.

Está compuesta por 5 bloques convolucionales, cada uno contiene 3 convoluciones; dos secuenciales y una conexión 'skip' que evita el desvanecimiento del gradiente a medida que se avanza en profundidad.
Con 16, 32, 48, 64 y 80 filtros de 3x3 para cada bloque respectivamente.

Después de cada bloque convolucional se encuentra una capa de max pooling y después de la última una capa de Average Pooling seguida por tres capas fully-connected (Dense) de 1024, 1024 y 3 neuronas respectivamente.

Para regularizar el modelo utilizamos 3 capas de Dropout al 20%; dos en los bloques 4 y 5 conv y otra después de la 1ra capa Dense.

## Acerca de Grad-CAM

Es una técnica utilizada para resaltar las regiones de una imagen que son importantes para la clasificación. Un mapeo de activaciones de clase para una categoría en particular indica las regiones de imagen relevantes utilizadas por la CNN para identificar esa categoría.

Grad-CAM realiza el cálculo del gradiente de la salida correspondiente a la clase a visualizar con respecto a las neuronas de una cierta capa de la CNN. Esto permite tener información de la importancia de cada neurona en el proceso de decisión de esa clase en particular. Una vez obtenidos estos pesos, se realiza una combinación lineal entre el mapa de activaciones de la capa y los pesos, de esta manera, se captura la importancia del mapa de activaciones para la clase en particular y se ve reflejado en la imagen de entrada como un mapa de calor con intensidades más altas en aquellas regiones relevantes para la red con las que clasificó la imagen en cierta categoría.

## Proyecto original realizado por:

Isabella Torres Revelo - https://github.com/isa-tr
Nicolas Diaz Salazar - https://github.com/nicolasdiazsalazar
