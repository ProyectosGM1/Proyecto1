import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
import time
import re


def conexionChatGpt():
    try:
        #config# Configurar Chrome en modo headless
        options = uc.ChromeOptions()
        #options.add_argument("--headless=new")  # Para que no se abra la ventana
        #options.add_argument("--disable-gpu")
        #options.add_argument("--no-sandbox")
        #options.add_argument("--disable-dev-shm-usage")

        #Abre chrome
        driver = uc.Chrome(options=options)
        url = "https://chatgpt.com/?model=auto"
    # 1. Abrir Google con url
        driver.get(url)
        time.sleep(2)  # Esperar a que cargue la página
        if driver.title:  # Si el título no está vacío, significa que cargó la página
            print(f"✅ Conexión exitosa a {url}")
            print(f"🔹 Título de la página: {driver.title}")
        else:
            print(f"❌ No se pudo cargar {url}")


        # Comprobar si la página tiene contenido
        if len(driver.page_source) > 100:
            print("✅ La página cargó correctamente (contiene contenido)")
        else:
            print("❌ La página parece vacía")

    except Exception as e:
        print(f"❌ Error al conectar con la página: {e}")
    finally:
        return driver

def mandarMensaje(driver, texto):
    search_box = driver.find_element(By.CLASS_NAME,"ProseMirror")    
    search_box.send_keys(texto)

def click(driver):
    boton = driver.find_element(By.XPATH, "//button[@aria-label='Enviar mensaje']")
    boton.click()

def leerMensaje():
    divs = driver.find_elements(By.XPATH, '//div[contains(@class, "markdown") and contains(@class, "dark:prose-invert") and contains(@class, "break-words")]')
    #   markdown prose dark:prose-invert w-full break-words light markdown-new-styling
    respuestas = [div.text for div in divs]
    return(respuestas)

#SALIR y cerrar driver
def salir ():
    driver.quit()