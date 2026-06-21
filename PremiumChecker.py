# -*- coding: utf-8 -*-

import os
import re
import time
import requests

from urllib.parse import urlparse
from datetime import datetime

BASE = "/storage/emulated/0/༺𝐡𝐚𝐬𝐬𝐢𝐞𝐥𝐥𝟐𝟎𝟐𝟑༻"

ONLINE_CODES = [200, 301, 302, 403, 405]

# ==========================
# CREAR CARPETAS
# ==========================

def crear_carpetas():

    carpetas = [
        BASE,
        BASE + "/hits",
        BASE + "/logs",
        BASE + "/config"
    ]

    for c in carpetas:
        os.makedirs(c, exist_ok=True)

# ==========================
# BANNER
# ==========================

def banner():

    os.system("cls" if os.name == "nt" else "clear")

    print("""
█▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█
█      ༺𝐡𝐚𝐬𝐬𝐢𝐞𝐥𝐥𝟐𝟎𝟐𝟑༻       █
█       PREMIUM CHECKER       █
█▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█
""")

# ==========================
# CONFIG
# ==========================

def obtener_nick():

    nick = input("👤 Nick: ").strip()

    if not nick:
        nick = "Unknown"

    return nick

# ==========================
# EXTRAER URLS
# ==========================

def extraer_urls(texto):

    patron = r'https?://[^\s]+'

    urls = re.findall(patron, texto)

    return list(dict.fromkeys(urls))

# ==========================
# HOST / PORT
# ==========================

def obtener_info(url):

    u = urlparse(url)

    host = u.hostname

    if u.port:
        puerto = u.port
    elif u.scheme == "https":
        puerto = 443
    else:
        puerto = 80

    return host, puerto, u.scheme.upper()

# ==========================
# CHECK URL
# ==========================

def verificar(url):

    inicio = time.time()

    try:

        r = requests.get(
            url,
            timeout=10,
            allow_redirects=False,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        tiempo = round(time.time() - inicio, 2)

        if r.status_code in ONLINE_CODES:
            estado = "ONLINE"
        else:
            estado = "OFFLINE"

        return estado, tiempo

    except:

        return "OFFLINE", 0

# ==========================
# GUARDAR
# ==========================

def guardar_resultado(texto, estado):

    fecha = datetime.now().strftime("%Y%m%d")

    if estado == "ONLINE":
        archivo = f"{BASE}/hits/ONLINE_{fecha}.txt"
    else:
        archivo = f"{BASE}/hits/OFFLINE_{fecha}.txt"

    with open(
        archivo,
        "a",
        encoding="utf-8"
    ) as f:

        f.write(texto + "\n\n")

# ==========================
# MOSTRAR
# ==========================

def mostrar(nick, host, puerto,
            estado, tiempo, url):

    resultado = f"""
╭───✦ 彡★ Scan By Hassiell2023 彡★
├● 🌐 HOST : {host}
├● 🔌 PORT : {puerto}
├● ✅ STATUS : {estado}
├● ⏱ RESPONSE : {tiempo}s
├● 📄 URL : {url}
╰───✦ 👤 HIT BY : {nick}
"""

    print(resultado)

    guardar_resultado(
    resultado,
    estado
)

# ==========================
# PROGRESO
# ==========================

def progreso(actual, total):

    porcentaje = int((actual / total) * 100)

    llenos = porcentaje // 5

    barra = "█" * llenos

    barra += "░" * (20 - llenos)

    print(
        f"\r[{barra}] {porcentaje}% ({actual}/{total})",
        end=""
    )

# ==========================
# CARGAR TXT
# ==========================

def cargar_txt():

    ruta = input(
        "\n📂 Ruta TXT: "
    ).strip()

    if not os.path.isfile(ruta):

        print("❌ Archivo no encontrado")

        return []

    with open(
        ruta,
        "r",
        encoding="utf-8",
        errors="ignore"
    ) as f:

        contenido = f.read()

    return extraer_urls(contenido)

# ==========================
# MANUAL
# ==========================

def cargar_manual():

    urls = []

    print(
        "\nPega URLs (ENTER vacío para terminar)\n"
    )

    while True:

        linea = input("> ").strip()

        if not linea:
            break

        urls.append(linea)

    return list(dict.fromkeys(urls))

# ==========================
# MENU
# ==========================

def menu():

    print("""
╔══════════════════════════════╗
║       MENÚ PRINCIPAL         ║
╠══════════════════════════════╣
║ [1] 🌐 Cargar TXT           ║
║ [2] ✍️ Entrada Manual       ║
║ [0] 🚪 Salir               ║
╚══════════════════════════════╝
""")

# ==========================
# MAIN
# ==========================

def main():

    crear_carpetas()

    banner()

    nick = obtener_nick()

    while True:

        banner()

        print(f"👤 Nick : {nick}")

        menu()

        opcion = input(
            "\n👉 Opción: "
        ).strip()

        if opcion == "0":
            break

        elif opcion == "1":

            urls = cargar_txt()

        elif opcion == "2":

            urls = cargar_manual()

        else:
            continue

        total = len(urls)

        if total == 0:

            print("\n❌ No se encontraron URLs")

            input("\nENTER para continuar...")

            continue

        online = 0
        offline = 0

        try:

            for i, url in enumerate(urls, 1):

                host, puerto, _ = obtener_info(url)

                estado, tiempo = verificar(url)

                if estado == "ONLINE":
                    online += 1
                else:
                    offline += 1

                mostrar(
                    nick,
                    host,
                    puerto,
                    estado,
                    tiempo,
                    url
                )

                progreso(i, total)

        except KeyboardInterrupt:

            print("\n")
            print("⛔ Escaneo detenido por el usuario")

        print("\n")

        print("━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🌐 TOTAL   : {total}")
        print(f"✅ ONLINE  : {online}")
        print(f"❌ OFFLINE : {offline}")
        print("━━━━━━━━━━━━━━━━━━━━━━━━━━")

        input("\nENTER para continuar...")


if __name__ == "__main__":
    main()