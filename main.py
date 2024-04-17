<<<<<<< HEAD
import pandas as pd
from fastapi import FastAPI
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


app = FastAPI()

@app.get('/developer')

def developer(desarrollador):

    df_items_developer = pd.read_parquet('arch_parquet/df_items_developer.parquet')
    # Filtra el dataframe por desarrollador de interés
    data_filtrada = df_items_developer[df_items_developer['developer'] == desarrollador]
    # Calcula la cantidad de items por año
    cantidad_por_año = data_filtrada.groupby('año_lanzamiento')['item_id'].count()
    # Calcula la cantidad de elementos gratis por año
    cantidad_gratis_por_año = data_filtrada[data_filtrada['price'] == 0.0].groupby('año_lanzamiento')['item_id'].count()
    # Calcula el porcentaje de elementos gratis por año
    porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

    result_dict = {
        'cantidad_items_por_año': cantidad_por_año.to_dict(),
        'porcentaje_gratis_por_año': porcentaje_gratis_por_año.to_dict()
    }
    
    return result_dict

@app.get('/userdata')

def userdata(user_id):
   
    df_reviews = pd.read_parquet('arch_parquet/df_reviews.parquet')
    df_gastos_items = pd.read_parquet('arch_parquet/gastos_items.parquet')
    # Filtra por el usuario de interés
    usuario = df_reviews[df_reviews['user_id'] == user_id]
    # Calcula la cantidad de dinero gastado para el usuario de interés
    cantidad_dinero = df_gastos_items[df_gastos_items['user_id']== user_id]['price'].iloc[0]
    # Busca el count_item para el usuario de interés    
    count_items = df_gastos_items[df_gastos_items['user_id']== user_id]['items_count'].iloc[0]
    
    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = usuario['reviews_recommend'].sum()
    # Calcula el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews['user_id'].unique())
    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

    return {
        'Dinero Gastado': str(int(cantidad_dinero)) + ' USD',
        '% de recomendación': str(round(float(porcentaje_recomendaciones), 2)*100) +' %',
        'Cantidad de items': int(count_items)
    }


@app.get('/UserForGenre')

def UserForGenre(genero: str):
    try:
        df_año_horas = pd.read_parquet('arch_parquet/df_anio_horas.parquet')
        df_año_horas = df_año_horas[['genres','user_id', 'año_lanzamiento','playtime_horas']]
        df_filtrado = df_año_horas[df_año_horas['genres'] == genero]
        playtime_sum = df_filtrado.groupby(['user_id', 'año_lanzamiento'])['playtime_horas'].sum() 
        user_max_playtime = playtime_sum.groupby('user_id').sum().idxmax()
        playtime_by_year = playtime_sum.loc[user_max_playtime].to_dict()
        del df_año_horas, df_filtrado, playtime_sum
        return {"Usuario con más horas jugadas para el género: " + genero : user_max_playtime, "Horas jugadas": playtime_by_year}
    except Exception as e:
        return {"error": str(e)}
    
@app.get('/best_developer_year')

def get_best_developer(año: int):
    review_games = pd.read_parquet('arch_parquet\df_reviews.parquet')
    review_games = review_games[['developer','año_lanzamiento','reviews_recommend', 'sentiment_analysis']]
    df_filtered = review_games[(review_games['año_lanzamiento'] == año) & (review_games['reviews_recommend'] == True) & (review_games['sentiment_analysis'] >= 1)]
    positive_reviws_count = df_filtered['developer'].value_counts()
    top_3_best_developers = positive_reviws_count.nlargest(3).index.tolist()
    del review_games, df_filtered, positive_reviws_count
    return [{"Puesto 1" : top_3_best_developers[0]}, {"Puesto 2" : top_3_best_developers[1]}, {"Puesto 3" : top_3_best_developers[2]}]

@app.get('/developer_reviews_analysis')

def developer_reviews_analysis(developer:str):
    """
    Esta funcion calcula para un desarrolador la cantidad de usuarios con reviews positivas y negativas.
    params:
    developer_rec:str : Desarrolador
    """
    # Carga los datos de los juegos de steam
    df_games = pd.read_csv('Datasets_limpio/steam_games.csv')
    # Tomo solo un 10% de mi df:
    df_games= df_games.sample(frac=0.1,random_state=42)
    # Carga las revisiones de los usuarios
    df_reviews = pd.read_csv('Datasets_limpio/df_reviews.csv')
    # Tomo solo un 10% de mi df:
    #df_reviews= df_reviews.sample(frac=0.1,random_state=42)
    df_games['id'] = df_games['id'].astype(int)
    df_reviews['reviews_item_id'] = df_reviews['reviews_item_id'].astype(int)
    # Merging los dos datasets, con una combinación interna en sus respectivos 'id'
    func_5 = pd.merge(df_reviews,df_games,left_on='reviews_item_id',right_on='id',how='inner')
    # Convertir todos los nombres de los desarrolladores en letras minúsculas para evitar la duplicación de datos debido a las diferencias de mayúsculas y minúsculas
    func_5['developer_x'] = func_5['developer_x'].str.lower()
    # Convertir el nombre del desarrollador proporcionado en letras minúsculas
    developer2 = developer.lower()
    # Filtrar por desarrollador
    func_5 = func_5[func_5['developer_x'] == developer2]
    # Verificar si se encuentra los juegos del desarrollador en el dataset
    if func_5.empty:
        # En caso de que no se encuentre, se muestra mensaje indicando que no hay comentarios para este desarrollador
        return 'No se encontraron reviews para ese desarrollador'
    # En caso contrario, contar los sentimientos de análisis de comentarios
    # Cuenta los comentarios positivos
    true_value = func_5[func_5['sentiment_analysis']==2]['sentiment_analysis'].count()
    # Cuenta los comentarios negativos
    false_value = func_5[func_5['sentiment_analysis']==0]['sentiment_analysis'].count()
    # Devolver conteos en un diccionario
    return {developer2:[f'Negative = {int(false_value)}',f'Positive = {int(true_value)}']}

@app.get('/recomendacion_usuario')

def recomendacion_usuario(user_id:str):

    df_games = pd.read_csv('Datasets_limpio\\steam_games.csv', encoding='utf-8')
    df_ml = pd.read_csv('Datasets_limpio\\df_ml_sa.csv', encoding='utf-8')
    df_comparacion = pd.read_csv('Datasets_limpio\\df_comparacion.csv', encoding='utf-8')

    n_clusters = 2
    features = df_ml[['genres','item_id','title','recommend','sentiment_analysis']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
    kmeans.fit(scaled_features)
    df_ml['cluster'] = kmeans.labels_

    kmeans.fit(df_ml)

    cluster_labels = kmeans.labels_
    df_ml['cluster'] = cluster_labels
 
    if user_id not in df_comparacion['user_id_comp'].values:
        return f"El usuario {user_id} no se encuentra."

    user_id2 = df_comparacion[df_comparacion['user_id_comp'] == user_id]['user_id'].values[0]

    user_cluster = df_ml[df_ml['user_id'] == user_id2]['cluster'].values[0]

    users_mismo_cluster = df_ml[df_ml['cluster'] == user_cluster]

    juegos_recomendados = users_mismo_cluster.groupby('item_id')['recommend'].sum()
    
    top_5 = juegos_recomendados.sort_values(ascending=False).head(5)
    

    recomendaciones = []
    for i, game_id in enumerate(top_5.index):
        game_name = df_games.loc[df_games['id'] == game_id, 'title'].values
        recomendaciones.append(f"Recomendación {i+1}: {game_name[0]}")
    respuesta = {"Recomendaciones para el usuario": user_id, "recomendaciones": recomendaciones}
    return respuesta
=======
import pandas as pd
from fastapi import FastAPI
import pyarrow as pa
import pyarrow.parquet as pq
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans


app = FastAPI()

@app.get('/developer')

def developer(desarrollador):

    df_items_developer = pd.read_parquet('arch_parquet/df_items_developer.parquet')
    # Filtra el dataframe por desarrollador de interés
    data_filtrada = df_items_developer[df_items_developer['developer'] == desarrollador]
    # Calcula la cantidad de items por año
    cantidad_por_año = data_filtrada.groupby('año_lanzamiento')['item_id'].count()
    # Calcula la cantidad de elementos gratis por año
    cantidad_gratis_por_año = data_filtrada[data_filtrada['price'] == 0.0].groupby('año_lanzamiento')['item_id'].count()
    # Calcula el porcentaje de elementos gratis por año
    porcentaje_gratis_por_año = (cantidad_gratis_por_año / cantidad_por_año * 100).fillna(0).astype(int)

    result_dict = {
        'cantidad_items_por_año': cantidad_por_año.to_dict(),
        'porcentaje_gratis_por_año': porcentaje_gratis_por_año.to_dict()
    }
    
    return result_dict

@app.get('/userdata')

def userdata(user_id):
   
    df_reviews = pd.read_parquet('arch_parquet/df_reviews.parquet')
    df_gastos_items = pd.read_parquet('arch_parquet/gastos_items.parquet')
    # Filtra por el usuario de interés
    usuario = df_reviews[df_reviews['user_id'] == user_id]
    # Calcula la cantidad de dinero gastado para el usuario de interés
    cantidad_dinero = df_gastos_items[df_gastos_items['user_id']== user_id]['price'].iloc[0]
    # Busca el count_item para el usuario de interés    
    count_items = df_gastos_items[df_gastos_items['user_id']== user_id]['items_count'].iloc[0]
    
    # Calcula el total de recomendaciones realizadas por el usuario de interés
    total_recomendaciones = usuario['reviews_recommend'].sum()
    # Calcula el total de reviews realizada por todos los usuarios
    total_reviews = len(df_reviews['user_id'].unique())
    # Calcula el porcentaje de recomendaciones realizadas por el usuario de interés
    porcentaje_recomendaciones = (total_recomendaciones / total_reviews) * 100

    return {
        'Dinero Gastado': str(int(cantidad_dinero)) + ' USD',
        '% de recomendación': str(round(float(porcentaje_recomendaciones), 2)*100) +' %',
        'Cantidad de items': int(count_items)
    }


@app.get('/UserForGenre')

def UserForGenre(genero: str):
    try:
        df_año_horas = pd.read_parquet('arch_parquet/df_anio_horas.parquet')
        df_año_horas = df_año_horas[['genres','user_id', 'año_lanzamiento','playtime_horas']]
        df_filtrado = df_año_horas[df_año_horas['genres'] == genero]
        playtime_sum = df_filtrado.groupby(['user_id', 'año_lanzamiento'])['playtime_horas'].sum() 
        user_max_playtime = playtime_sum.groupby('user_id').sum().idxmax()
        playtime_by_year = playtime_sum.loc[user_max_playtime].to_dict()
        del df_año_horas, df_filtrado, playtime_sum
        return {"Usuario con más horas jugadas para el género: " + genero : user_max_playtime, "Horas jugadas": playtime_by_year}
    except Exception as e:
        return {"error": str(e)}
    
@app.get('/best_developer_year')

def get_best_developer(año: int):
    review_games = pd.read_parquet('arch_parquet/df_reviews.parquet')
    review_games = review_games[['developer','año_lanzamiento','reviews_recommend', 'sentiment_analysis']]
    df_filtered = review_games[(review_games['año_lanzamiento'] == año) & (review_games['reviews_recommend'] == True) & (review_games['sentiment_analysis'] >= 1)]
    positive_reviws_count = df_filtered['developer'].value_counts()
    top_3_best_developers = positive_reviws_count.nlargest(3).index.tolist()
    del review_games, df_filtered, positive_reviws_count
    return [{"Puesto 1" : top_3_best_developers[0]}, {"Puesto 2" : top_3_best_developers[1]}, {"Puesto 3" : top_3_best_developers[2]}]

@app.get('/developer_reviews_analysis')

def developer_reviews_analysis(developer:str):
    """
    Esta funcion calcula para un desarrolador la cantidad de usuarios con reviews positivas y negativas.
    params:
    developer_rec:str : Desarrolador
    """
    # Carga los datos de los juegos de steam
    df_games = pd.read_csv('Datasets_limpio/steam_games.csv')
    # Tomo solo un 10% de mi df:
    df_games= df_games.sample(frac=0.1,random_state=42)
    # Carga las revisiones de los usuarios
    df_reviews = pd.read_csv('Datasets_limpio/df_reviews.csv')
    # Tomo solo un 10% de mi df:
    #df_reviews= df_reviews.sample(frac=0.1,random_state=42)
    df_games['id'] = df_games['id'].astype(int)
    df_reviews['reviews_item_id'] = df_reviews['reviews_item_id'].astype(int)
    # Merging los dos datasets, con una combinación interna en sus respectivos 'id'
    func_5 = pd.merge(df_reviews,df_games,left_on='reviews_item_id',right_on='id',how='inner')
    # Convertir todos los nombres de los desarrolladores en letras minúsculas para evitar la duplicación de datos debido a las diferencias de mayúsculas y minúsculas
    func_5['developer_x'] = func_5['developer_x'].str.lower()
    # Convertir el nombre del desarrollador proporcionado en letras minúsculas
    developer2 = developer.lower()
    # Filtrar por desarrollador
    func_5 = func_5[func_5['developer_x'] == developer2]
    # Verificar si se encuentra los juegos del desarrollador en el dataset
    if func_5.empty:
        # En caso de que no se encuentre, se muestra mensaje indicando que no hay comentarios para este desarrollador
        return 'No se encontraron reviews para ese desarrollador'
    # En caso contrario, contar los sentimientos de análisis de comentarios
    # Cuenta los comentarios positivos
    true_value = func_5[func_5['sentiment_analysis']==2]['sentiment_analysis'].count()
    # Cuenta los comentarios negativos
    false_value = func_5[func_5['sentiment_analysis']==0]['sentiment_analysis'].count()
    # Devolver conteos en un diccionario
    return {developer2:[f'Negative = {int(false_value)}',f'Positive = {int(true_value)}']}

@app.get('/recomendacion_usuario')

def recomendacion_usuario(user_id:str):

    df_games = pd.read_csv('Datasets_limpio/steam_games.csv', encoding='utf-8')
    df_ml = pd.read_csv('Datasets_limpio/df_ml_sa.csv', encoding='utf-8')
    df_comparacion = pd.read_csv('Datasets_limpio/df_comparacion.csv', encoding='utf-8')

    n_clusters = 2
    features = df_ml[['genres','item_id','title','recommend','sentiment_analysis']]
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)
    kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init=10)
    kmeans.fit(scaled_features)
    df_ml['cluster'] = kmeans.labels_

    kmeans.fit(df_ml)

    cluster_labels = kmeans.labels_
    df_ml['cluster'] = cluster_labels
 
    if user_id not in df_comparacion['user_id_comp'].values:
        return f"El usuario {user_id} no se encuentra."

    user_id2 = df_comparacion[df_comparacion['user_id_comp'] == user_id]['user_id'].values[0]

    user_cluster = df_ml[df_ml['user_id'] == user_id2]['cluster'].values[0]

    users_mismo_cluster = df_ml[df_ml['cluster'] == user_cluster]

    juegos_recomendados = users_mismo_cluster.groupby('item_id')['recommend'].sum()
    
    top_5 = juegos_recomendados.sort_values(ascending=False).head(5)
    

    recomendaciones = []
    for i, game_id in enumerate(top_5.index):
        game_name = df_games.loc[df_games['id'] == game_id, 'title'].values
        recomendaciones.append(f"Recomendación {i+1}: {game_name[0]}")
    respuesta = {"Recomendaciones para el usuario": user_id, "recomendaciones": recomendaciones}
    return respuesta
>>>>>>> a6c25998b5b544783130af59b9c2e210d2af3273
