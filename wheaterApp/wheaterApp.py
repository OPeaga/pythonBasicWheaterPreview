import requests
import urllib.request as url
from json import loads
import pprint
from datetime import datetime

# Programa basicao de prévia de temperatura feito por Pedro Henrique 

apiKeyAccuwheater = 'MUoQjTkI3vbFtr3PLz1qqemgnJM3N5hy'

semana = ['Segunda','Terça','Quarta','Quinta','Sexta','Sábado','Domingo']
dadosPrevisao = []

def getCoordinates():
  # Fazendo a request
  r = requests.get('http://www.geoplugin.net/json.gp')
  
  if (r.status_code != 200):
    print("Não foi possível obter localização. Provavelmente o número de Requisições já foi ultrapassado por hoje :( ")
  else:
    # print(r.text)
    
    # Transformando em Json
    localizacao = loads(r.text)
    # print(pprint.pprint(localizacao))
    
    # Capturando Valores
    latitude = localizacao['geoplugin_latitude']
    longitude = localizacao['geoplugin_longitude']
    
    # Imprimindo
    # print(f'latitude: {latitude}')
    # print(f'longitude: {longitude}')
    
    dados = (latitude,longitude)
    
    return dados

def getLocationDetails(dados):
  locationApiUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/search?apikey=' + apiKeyAccuwheater + '&q=' + dados[0] + '%2C' + dados[1] + '&language=pt-br'
  
  r = requests.get(locationApiUrl)
  
  if (r.status_code != 200):
    print('Nao foi possível tirar o código do local\n')
    print(r.status_code)
  else:
    # pprint.pprint(loads(r.text))
    locationResponse = loads(r.text)
    nomeLocal = locationResponse['AdministrativeArea']['LocalizedName'] + " , "  + locationResponse['Country']['LocalizedName']
    
    codigoLocal = locationResponse['Key']
    
    print("Local: " + nomeLocal + "\n")
  return getClimateDetails(codigoLocal)

def getClimateDetails(key):
  apiConditionsUrl = ["http://dataservice.accuweather.com/currentconditions/v1/", "KEY" , "?apikey=" + apiKeyAccuwheater + "&language=pt-br"]
  apiConditionsUrl[1] = str(key)
  v = "".join(apiConditionsUrl)
  r = requests.get(v)
  
  if(r.status_code != 200):
    print("Erro na solicitação de Clima")
  else:
    # pprint.pprint(loads(r3.text))
    climateResponse = loads(r.text)
    temperaturaValorC = climateResponse[0]['Temperature']['Metric']['Value']
    temperaturaStatus = climateResponse[0]['WeatherText']
    temperaturaValorF = climateResponse[0]['Temperature']['Imperial']['Value']
    print(f"Condições de Hoje\nTemperatura em Celsius: {temperaturaValorC} ºC\nTemperatura em Fahrenheit = {temperaturaValorF} F\nStatus: {temperaturaStatus}\n")
    getWheaterPreview(key)

def getWheaterPreview(key):
  # Pegar dados dos próximos 5 dias
  forecastApiUrl = ["http://dataservice.accuweather.com/forecasts/v1/daily/5day/" + key + "?apikey=" + apiKeyAccuwheater + "&language=pt-br&metric=true"]
  
  v = "".join(forecastApiUrl)
  
  response = url.urlopen(v).read().decode('utf8')
  dados = loads(response)
  # pprint.pprint(dados)
  print("Previsão dos próximos 4 dias:\n")

  for i in range(5):
    
    localWeekday = datetime.now().weekday()
    
    temperaturaMax = dados['DailyForecasts'][i]['Temperature']['Maximum']['Value']
    temperaturaMin = dados['DailyForecasts'][i]['Temperature']['Minimum']['Value']
    status = dados['DailyForecasts'][i]['Day']['IconPhrase']
    datastring = dados['DailyForecasts'][i]['Date']
    
    data = datetime.strptime(datastring,"%Y-%m-%dT%H:%M:%S%z")
    
    if (i + localWeekday) <= 6:
      diaSemana = semana[i+localWeekday]
    else:
      diaSemana = semana[i+localWeekday-7]
      
    dia = {"tempMax": temperaturaMax, "tempMin":temperaturaMin, "diaSemana":diaSemana, "status" : status, "data": data.strftime("%d/%m/%Y")}
    dadosPrevisao.append(dia)
    
    printInfo()
  
def printInfo():
  for item in dadosPrevisao:
    print("\n---------------------------------------------------------------------------------\n")
    print(f"Dia da Semana:{item['diaSemana']}\nTemperatura Máxima:{item['tempMax']}ºC\nTemperatura Mínima:{item['tempMin']}ºC\n{item['status']}\nData: {item['data']}\n")
  dadosPrevisao.clear()
  
def main():
  dados = getCoordinates()
  getLocationDetails(dados)
  
main()