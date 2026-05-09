import requests
from PIL import Image
from io import BytesIO
import os
import json

def obtener_pokemon(nombre):
    url = f"https://pokeapi.co/api/v2/pokemon/{nombre.lower()}"
    respuesta = requests.get(url)

    if respuesta.status_code != 200:
        print("❌ Error: El Pokémon no existe en la Pokédex.")
        return None

    datos = respuesta.json()

    # Extraer información
    nombre = datos["name"].capitalize()
    peso = datos["weight"]
    altura = datos["height"]
    imagen_url = datos["sprites"]["front_default"]

    # Movimientos (máximo 4)
    movimientos = [m["move"]["name"] for m in datos["moves"][:4]]

    # Habilidades
    habilidades = [h["ability"]["name"] for h in datos["abilities"]]

    # Tipos
    tipos = [t["type"]["name"] for t in datos["types"]]

    # Mostrar imagen
    if imagen_url:
        img_respuesta = requests.get(imagen_url)
        img = Image.open(BytesIO(img_respuesta.content))
        img.show()

    # Mostrar estadísticas
    print(f"📖 {nombre}")
    print(f"Peso: {peso/10} kg")
    print(f"Altura: {altura/10} m")
    print(f"Movimientos: {', '.join(movimientos)}")
    print(f"Habilidades: {', '.join(habilidades)}")
    print(f"Tipos: {', '.join(tipos)}")

    # Guardar en JSON
    info_pokemon = {
        "nombre": nombre,
        "peso": peso,
        "altura": altura,
        "movimientos": movimientos,
        "habilidades": habilidades,
        "tipos": tipos,
        "imagen_url": imagen_url
    }

    # Carpeta en el escritorio
    escritorio = os.path.join(os.path.expanduser("~"), "Desktop", "pokedex")
    os.makedirs(escritorio, exist_ok=True)

    archivo = os.path.join(escritorio, f"{nombre}.json")
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(info_pokemon, f, indent=4, ensure_ascii=False)

    print(f"✅ Información guardada en {archivo}")

# Ejemplo de uso
pokemon = input("Introduce el nombre de un Pokémon: ")
obtener_pokemon(pokemon)