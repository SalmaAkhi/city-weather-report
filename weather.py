import requests
import json
import dicttoxml
from datetime import datetime

def fetch_weather_data(city):
    api_key = 'ed1e72fdfa1f02a27230404b25fad021'  
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        data['source'] = {
            "type": "API",
            "provider": "OpenWeatherMap",
            "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return data
    else:
        print("Erreur lors de la récupération des données.")
        return None

def convert_to_xml(data):
    xml_data = dicttoxml.dicttoxml(data, custom_root='weather_record', attr_type=False)
    return xml_data.decode('utf-8')

def save_data(json_data, xml_data, city):
    with open(f"{city}_weather.json", "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, indent=4, ensure_ascii=False)
    with open(f"{city}_weather.xml", "w", encoding="utf-8") as xf:
        xf.write(xml_data)

def analyze_weather(data):
    print("\n Analyse des données météorologiques :")
    temp = data['main']['temp']
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    wind_speed = data['wind']['speed']
    wind_deg = data['wind']['deg']
    
    print(f" Température       : {temp}°C")
    print(f" Humidité          : {humidity}%")
    print(f" Pression          : {pressure} hPa")
    print(f" Vent              : {wind_speed} m/s, direction {wind_deg}°")
    
    # Alertes simples
    print("\n Alertes météorologiques :")
    alert = False
    if temp >= 35:
        print(" Alerte canicule !")
        alert = True
    if wind_speed >= 15:
        print(" Alerte vent violent !")
        alert = True
    if humidity >= 90:
        print(" Alerte humidité élevée (risque de pluie ou brouillard)")
        alert = True
    if not alert:
        print(" Aucune alerte détectée.")

def main():
    city = "Paris"  # ← tu peux changer la ville ici
    print(f" Collecte des données météo pour : {city}")
    
    data_json = fetch_weather_data(city)
    
    if data_json:
        data_xml = convert_to_xml(data_json)
        save_data(data_json, data_xml, city)
        analyze_weather(data_json)
        print(f"\n Données sauvegardées dans : {city}_weather.json et {city}_weather.xml")
    else:
        print(" Échec de la récupération des données.")

if __name__ == "__main__":
    main()
