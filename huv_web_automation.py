# huv_web_automation.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from dataclasses import dataclass
from typing import Callable, Optional
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://huvpatologia.qhorte.com/index.php"

@dataclass
class Credenciales:
    usuario: str
    clave: str

# Mapa de criterios → data-valor del menú (según markup dado)
CRITERIOS = {
    "Fecha de Ingreso": "1",
    "Fecha de Finalizacion": "2",
    "Rango de Peticion": "3",
    "Datos del Paciente": "4",
}

def _log(msg: str, cb: Optional[Callable[[str], None]] = None):
    (cb or print)(msg)

def automatizar_entrega_resultados(
    fecha_inicial_ddmmaa: str,
    fecha_final_ddmmaa: str,
    cred: Credenciales,
    criterio: str = "Fecha de Ingreso",
    headless: bool = False,
    log_cb: Optional[Callable[[str], None]] = None,
):
    """
    Orquesta: login → SEGUIMIENTO → Entrega de resultados → set criterio → set fechas → Consultar.
    Fechas en formato DD/MM/YYYY.
    """
    _log("Iniciando automatización de Entrega de resultados…", log_cb)

    # --- Chrome ---
    chrome_opts = Options()
    if headless:
        chrome_opts.add_argument("--headless=new")
    chrome_opts.add_argument("--start-maximized")
    chrome_opts.add_argument("--disable-gpu")
    chrome_opts.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_opts)
    wait = WebDriverWait(driver, 20)

    try:
        # 1) Login
        driver.get(URL)
        _log("Cargando página de login…", log_cb)

        user = wait.until(EC.presence_of_element_located((By.ID, "inputUser")))
        pwd  = wait.until(EC.presence_of_element_located((By.ID, "inputPassword")))
        user.clear(); user.send_keys(cred.usuario)
        pwd.clear();  pwd.send_keys(cred.clave)

        _log("Enviando credenciales…", log_cb)
        wait.until(EC.element_to_be_clickable((By.ID, "button1"))).click()

        # 2) Ir a SEGUIMIENTO → Entrega de resultados
        _log("Navegando a SEGUIMIENTO → Entrega de resultados…", log_cb)
        seg = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class,'dropdown-toggle')][contains(normalize-space(.),'SEGUIMIENTO')]")))
        seg.click()

        entrega = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick,'form_entrega_resultado.php')]")))
        entrega.click()

        # 3) Seleccionar criterio
        _log(f"Seleccionando criterio: {criterio}", log_cb)
        valor = CRITERIOS.get(criterio, "1")

        wait.until(EC.element_to_be_clickable((By.ID, "CriterioSelect"))).click()
        # Intento por data-valor; si falla, por texto visible
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//ul[@id='divCriterioFiltro']//a[@class='CriterioFiltro' and @data-valor='{valor}']"))).click()
        except Exception:
            wait.until(EC.element_to_be_clickable((By.XPATH, f"//ul[@id='divCriterioFiltro']//a[contains(normalize-space(.),'{criterio}')]"))).click()

        # 4) Fechas
        _log(f"Seteando fechas: {fecha_inicial_ddmmaa} → {fecha_final_ddmmaa}", log_cb)
        fi = wait.until(EC.presence_of_element_located((By.ID, "fecha_inicial")))
        ff = wait.until(EC.presence_of_element_located((By.ID, "fecha_final")))
        fi.clear(); fi.send_keys(fecha_inicial_ddmmaa)
        ff.clear(); ff.send_keys(fecha_final_ddmmaa)

        # 5) Consultar (varios fallbacks)
        _log("Ejecutando consulta…", log_cb)
        posibles = [
            (By.XPATH, "//button[contains(translate(., 'CONSULTAR', 'consultar'),'consultar')]"),
            (By.XPATH, "//input[@type='submit' and contains(translate(@value,'CONSULTAR','consultar'),'consultar')]"),
            (By.XPATH, "//button[contains(.,'Buscar') or contains(.,'buscar')]"),
            (By.CSS_SELECTOR, "button#btnConsultar, input#btnConsultar, button[name='btnConsultar']")
        ]
        clicked = False
        for by, sel in posibles:
            try:
                btn = wait.until(EC.element_to_be_clickable((by, sel)))
                btn.click()
                clicked = True
                break
            except Exception:
                continue
        if not clicked:
            raise RuntimeError("No se encontró el botón de 'Consultar'.")

        # 6) Esperar resultados visibles (heurística simple: una tabla o un contenedor resultante)
        _log("Esperando resultados…", log_cb)
        try:
            wait.until(EC.any_of(
                EC.presence_of_element_located((By.CSS_SELECTOR, "table, .table, .dataTable")),
                EC.presence_of_element_located((By.XPATH, "//*[contains(.,'No se encontraron resultados') or contains(.,'Resultados')]"))
            ))
        except Exception:
            pass

        _log("Consulta completada. Resultados listos en la página.", log_cb)

        # (Opcional) Aquí podrías parsear una tabla y retornarla como DataFrame.
        # from pandas import read_html
        # tablas = read_html(driver.page_source)
        # return tablas[0] if tablas else None

        return True

    finally:
        # Dale un respiro por si el usuario quiere ver la página; ajusta si usas headless
        time.sleep(1.0 if headless else 0.5)
        driver.quit()
