#app = Client("bot_session", api_id=7500863, api_hash="9ac6dbcbbcca795f074afdc7fae65894", bot_token=TOKEN)

from pyrogram import Client, filters
import requests
import re

# Token del bot de Telegram
TOKEN = '7077402329:AAH_eOLI9IjhanJ6698CCiWz42ZlH6Ij_vU'
# Código de la carpeta
codigoCarpeta = 0

# Instanciando al bot de Telegram con Pyrogram
bot = Client("my_bot", api_id=7500863, api_hash="9ac6dbcbbcca795f074afdc7fae65894", bot_token=TOKEN)

# Función para subir la imagen al servidor de ImgBB
def imgbb(url_subida):
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": "d76c3f2b896c51ac2052239c9fe78b0f",
        "image": url_subida
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    response = requests.post(url, data=payload, headers=headers)
    data = response.json()
    imagen_url = data["data"]["url"]
    return imagen_url

# Función para subir la imagen al servidor y guardar en la BD
def subir(message):
    global codigoCarpeta
    chat_id = message.chat.id
    # Obtener el ID del archivo de la foto
    file_id = message.reply_to_message.photo.file_id
    
    #Para obtener el enlace de descarga
    pregu = requests.get(f'https://api.telegram.org/bot{TOKEN}/getFile?file_id={file_id}')
    qqq = pregu.json()

    file_path = qqq['result']['file_path']
    file_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_path}"
    nombre = message.text
    imagen = imgbb(file_url)
    url_crear = f'https://filemoonapi.com/api/folder/create?key=54340gjpnv8a0abxcv6s4&name={nombre}'
    response = requests.get(url_crear)
    data = response.json()
    codigo = data['result']['fld_id']
    url_exec = f'https://script.google.com/macros/s/AKfycbweUyIoRlZXsrDL95366BoYbPMmkozy0n6sglQf8lhGI2zIL4Wug3qIHb3Cctu6nSvW/exec?nombre={nombre}&imagen={imagen}&codigo={codigo}'
    response = requests.get(url_exec)
    bot.send_message(chat_id, codigo)
    bot.send_message(chat_id, "Imagen subida con éxito")
    codigoCarpeta = codigo
    carpeta = 'https://filemoon.sx/folder/' + str(codigo)
    bot.send_message(-1002204285060, carpeta)
    print('Imagen Subida')

# Función para subir las URLs a Filemoon
def subirUrl(message):
    global codigoCarpeta
    urls = re.findall(r'https?://(?!.*\/watch\/)\S+', message.text)
    for url in urls:
        url_video = f'https://filemoonapi.com/api/remote/add?key=54340gjpnv8a0abxcv6s4&fld_id={codigoCarpeta}&url={url}'
        response = requests.get(url_video)
        bot.send_message(message.chat.id, "Enlace subido")
    print('Enlace Subido')

# Configurar los handlers de mensajes
@bot.on_message(filters.command('start'))
def handle_start(client, message):
    global codigoCarpeta
    codigoCarpeta = 0
    chat_id = message.chat.id
    print('Comando Start')
    bot.send_message(chat_id, "Bienvenido a FilemoonAdmin Python")

@bot.on_message(filters.reply & filters.private)
def handle_reply(client, message):
    subir(message)

@bot.on_message(filters.text)
def handle_text(client, message):
    subirUrl(message)

print('Bot Iniciado')
# Iniciar el bot
bot.run()


