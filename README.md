#         Data-Science-Project-1

Proyecto individual 1 - Henry


Este proyecto consiste en crear tu primer modelo de ML que soluciona un problema de negocio: Steam pide que te encargues de crear un sistema de recomendación de videojuegos para usuarios. 

## ETL y Engineering
De los archivos que se encuentran en Datasets, uno (steam_games.json.gz) estaba bien estructurado y los otros dos no, por lo que se usaron funciones para la extraccion de datos distintas.
Se realizó también la columna 'sentiment_analysis' realizando una funcion con la libreria Nltk
Se realizo un analisis de los datos, completando faltantes, eliminando nulos, anulando columnas que no sirven para las funciones solicitadas.


## EDA
En el EDA se vio cual la cantidad de juegos por genero, la cantidad de juegos segun año de lanzamiento, hago una comparativa de las recomendaciones segun el sentimiento de los usuarios, calculo la distribucion de horas jugadas por la cantidad de juegos y la cantidad de items comprados por juegos, y finalmente veo cuales son los juegos mas jugados.

## Desarrollo de la API
Se solicita crear 5 funciones utilizando FASTAPI: def PlayTimeGenre, def UserForGenre, def UsersRecommend, def UsersNotRecommend y def Sentiment_Analysis.

## Modelo de ML
Se solicita entrenar un modelo de Machine Learning que nos devuelva un sistema de recomendación de juegos para el usuario:
-def recomendacion_usuario

## Deployment
Se solicita hacer un deploy de las API en Render. 

# Enlaces
- Video: (https://drive.google.com/file/d/1HKgcLCLG_mrHqCnkdRinTAw5KQr4Ivkh/view?usp=sharing)
- GitHub: (https://github.com/Alejo260894/Data-Science-Project-1.git)
- Deploy: (https://data-science-project-1.onrender.com/docs)
