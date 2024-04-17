Proyecto individual 1 - Henry Desarrollado bajo el rol de MLOps Engineer.

Este proyecto consiste en desarrollar un sistema de recomendación de juegos para la plataforma Steams, basado en los datos provistos de años anteriores.

ETL
Se suministraron tres archivos JSON comprimidos en GZip: steam_games.json.gz, user_reviews.json.gz y users_item.json.gz Se requirió utilizar funciones para la extracción de los datos. Estos archivos contenian datos anidados, nulos, duplicados y en algunos casos se requirió modificar el formato. Se realizó también la columna 'sentiment_analysis' realizando una funcion con la libreria TextBlob. Luego de desanidar y limpiar los datasets, hice un pequeño analisis de las funciones y los datos que iba a necesitar para cada una. Agrupé columnas y generé nuevos datasets especificos para que cumplan con los requerimientos de cada función. Esto también contribuyó a que los datasets sean más pequeños y se utilicen menos recursos. Los datasets fueron exportados a .csv y quedaron finalmente en uso: -df_usersrecommend.csv -df_playtimegenre.csv -df_ml.csv -df_ml_names.csv

EDA
En el analisis exploratorio de datos, pude identificar los géneros de los juegos, los juegos recomendados por cada año y un recuento del sentiment_analysis. Pero considero que mi analisis de los datos fue realizando el ETL y seleccionando qué columnas iba a requerir en base a las funciones.

Desarrollo de la API
Se solicita crear 5 funciones utilizando FASTAPI: def PlayTimeGenre, def UserForGenre, def UsersRecommend, def UsersNotRecommend y def Sentiment_Analysis. El desarrollo de los endpoints se encuentra en el archivo Endpoints.ipynb, en el que fui probando resultados. Luego los pasé al archivo main.py que consumirá la API con los decoradores requeridos.

Modelo de ML
Se solicita entrenar un modelo de Machine Learning que nos devuelva un sistema de recomendación de juegos para el usuario: -def recomendacion_usuario Este modelo deriva en un POST de FASTAPI

Deployment
Se solicita hacer un deploy de las API en Render.

Enlaces
Video: (https://drive.google.com/file/d/123QZAwVmISsUQ6GUmJbZUvQ97jTgm7cl/view?usp=sharing)
GitHub: (https://github.com/rebbc/PI_ML_OPS_1)
Deploy: (https://pi-ml-ops-1-vildosola.onrender.com/docs)
