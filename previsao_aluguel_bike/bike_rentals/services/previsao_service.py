import requests
import pandas as pd
from datetime import datetime
import joblib
import os
import holidays 

API_KEY = '45b0bba356e0b5a7aa1d229a41c44353'
LAT = 38.8951
LON = -77.0364

def normalizar_dados(temp, atemp, hum, windspeed):
    temp_norm = (temp + 8) / 47
    atemp_norm = (atemp + 16) / 66
    hum_norm = hum / 100
    windspeed_norm = windspeed / 67
    return temp_norm, atemp_norm, hum_norm, windspeed_norm

def mapear_weather(weather_main):
    # Ajustar conforme os dados que usou no treinamento!
    mapping = {
        'Clear': 1,
        'Clouds': 2,
        'Mist': 2,
        'Fog': 2,
        'Rain': 3,
        'Drizzle': 3,
        'Snow': 3,
        'Thunderstorm': 4
    }
    return mapping.get(weather_main, 1)

def prever_alugueis(data_str):
    data = datetime.strptime(data_str, "%Y-%m-%d")

    # ===> Previsão climática
    url = f'http://api.openweathermap.org/data/2.5/forecast?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric'
    resposta = requests.get(url).json()

    previsao = None
    for item in resposta['list']:
        dt_txt = datetime.strptime(item['dt_txt'], "%Y-%m-%d %H:%M:%S")
        if dt_txt.date() == data.date() and dt_txt.hour == 12:
            previsao = item
            break
    if not previsao:
        raise Exception("Sem previsão para essa data.")

    # ===> Dados brutos da API
    temp = previsao['main']['temp']
    atemp = previsao['main']['feels_like']
    hum = previsao['main']['humidity']
    wind = previsao['wind']['speed']
    weather_main = previsao['weather'][0]['main']

    # ===> Normalização
    temp_n, atemp_n, hum_n, wind_n = normalizar_dados(temp, atemp, hum, wind)

    # ===> Feriado / dia útil / estação
    mes = data.month
    dia_semana = (data.weekday() + 1) % 7  # 0=domingo
    us_holidays = holidays.US()
    eh_feriado = 1 if data in us_holidays else 0
    eh_fds = 1 if dia_semana in [0, 6] else 0
    workingday = 0 if eh_feriado or eh_fds else 1

    if mes in [12, 1, 2]:
        season = 1
    elif mes in [3, 4, 5]:
        season = 2
    elif mes in [6, 7, 8]:
        season = 3
    else:
        season = 4

    clima_cod = mapear_weather(weather_main)

    # ===> Monta DataFrame com as 10 features
    df = pd.DataFrame([{
        'season': season,
        'mnth': mes,
        'holiday': eh_feriado,
        'weekday': dia_semana,
        'workingday': workingday,
        'weathersit': clima_cod,
        'temp': temp_n,
        'atemp': atemp_n,
        'hum': hum_n,
        'windspeed': wind_n
    }])

    # Converter colunas categóricas para 'object'
    colunas_categoricas = ['season', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']
    df[colunas_categoricas] = df[colunas_categoricas].astype('object')

    # ===> Carrega modelo
    modelo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'modelo_gboosting.pkl'))
    modelo = joblib.load(modelo_path)

    y_pred = modelo.predict(df)[0]

    RMSE = 19.31 # RMSE do modelo
    media_alugueis = 848 # média do modelo
    erro_relativo = RMSE / media_alugueis

    margem_erro = round(y_pred * erro_relativo)
    

    return y_pred, margem_erro