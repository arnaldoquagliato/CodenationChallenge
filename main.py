import requests
import json
import string
import hashlib
import requests


def requestFromApi():    
    request = requests.get('https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=ae41dc89f8af4c35eeb29f3dbb67228bfea111c8')
    return request.json()

#Receber o arquivo Json da API
objeto_json = requestFromApi()

#Utilizado para saber as letras do alfabeto
letras = list(string.ascii_lowercase)

#nessa função onde será feito a decodificação de acordo com as casas
def decifrador(letra):
    valorIndex = letras.index(letra) 
    if valorIndex < 4:
        valorIndex = valorIndex + 21
        return letras[valorIndex]
    else:
        return letras[valorIndex-5]


#Onde será decifrado 
def decifrandoAPI():
    for letra in objeto_json['cifrado']:
        if letra == '.' or letra == ',' or letra == ')' or letra == '(' or letra == ';' or letra.isdigit() or letra == "'" or letra == ' ':
            objeto_json['decifrado'] = objeto_json['decifrado'] + letra
        else:         
            objeto_json['decifrado'] = objeto_json['decifrado'] + decifrador(letra)
    return objeto_json['decifrado']

objeto_json['decifrado'] = decifrandoAPI()

#Onde será feito o resumoCriptografico  
def resumoCriptograficoAPI():
    resumoCriptografico = hashlib.sha1(str(objeto_json).encode('utf-8'))
    resumoCriptografico = resumoCriptografico.hexdigest()
    return resumoCriptografico

objeto_json['resumo_criptografico'] = resumoCriptograficoAPI()

def arquivoJson(objeto_json):
    info = open('answer.json', 'w')
    info.write(str(objeto_json))
    info.close

#arquivoJson(objeto_json)
def enviandoMetodoPost():
    url = 'https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=ae41dc89f8af4c35eeb29f3dbb67228bfea111c8'

    files = [
        ('answer', ('answer.json', open('answer.json', 'rb'), 'json')),
        ('answer', ('answer.json', open('answer.json', 'rb'), 'json')),
    ]

    r = requests.post(url, files=files)
    print(r.status_code)
    print(r.text)
