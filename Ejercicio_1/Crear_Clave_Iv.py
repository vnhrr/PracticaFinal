import base64

from Crypto.Random import get_random_bytes

def generar_y_guardar_clave_iv(nombre_archivo):
    # Generar clave y IV
    clave = get_random_bytes(16)  # 16 bytes para AES-128
    iv = get_random_bytes(16)  # 16 bytes para el vector de inicialización

    # Codificar clave y IV en Base64 para guardar en texto legible
    clave_b64 = base64.b64encode(clave).decode('utf-8')
    iv_b64 = base64.b64encode(iv).decode('utf-8')

    # Guardar clave e IV en un archivo
    with open(nombre_archivo, "w") as archivo:
        archivo.write(f"{clave_b64}\n")
        archivo.write(f"{iv_b64}\n")

    print(f"Clave e IV generados y guardados en {nombre_archivo}")

# Llamar a la función para generar el archivo
generar_y_guardar_clave_iv("clave_iv.txt")


