# primera funcion para traducir audio a teto 
import requests

# direcctioAudioFile = "C:\\Users\\Luis Leo\\Pictures\\Camera Roll\\audio.m4a" 

def translateudioFile(direcctioAudioFile):

    # en esta parte es donde se puede modificar las variables de deepgram como modelo, lenguaje,etc.
    url = "https://api.deepgram.com/v1/listen?model=nova-3-general&detect_language=true"

    #encabezados para la peticion a la api
    headers = {
        "Authorization": "Token abd4694b9ca963040d3cdfe33454ab0b5f85d2c8",
        "Content-Type": "audio/m4a"
    }

    #abrir direccion archivo , guardar en variable y realizar peticion pasando header, url y archivo audio
    #mejorar codigo por si no encuentra archivo, no se puede realzar la peticio----TODO --------
    with open(direcctioAudioFile, "rb") as audio_file:
        response = requests.post(url, headers=headers, data=audio_file)

    #filtrar transcripcion
    try:
        respuestaJson=response.json()
        transcripcion= respuestaJson["results"]["channels"][0]["alternatives"][0]["transcript"]
        print(transcripcion)
        return transcripcion
    except (KeyError,IndexError,TypeError):
        print("no se logro encontrar transcripcion, revisar posicion en json")

    #comentario extra

def saveText(transcripcion): # regresar direccion o texto, opcional
    with open("output.txt", "w") as file:
        print(transcripcion, file=file)