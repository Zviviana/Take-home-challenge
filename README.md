# Automatización de pruebas de Mercado Libre

Este proyecto automatiza la búsqueda de "PlayStation 5" en Mercado Libre México, aplica filtros, ordena los resultados y recupera los primeros 5 nombres de productos y precios.

## Requisitos

- Python 3.8+
- Google Chrome y ChromeDriver
- Selenium

## Configuración

1. Clona el repositorio o copia los archivos de código.
2. Instala las dependencias:
```bash
pip install selenium
```
3. Asegúrate de que `chromedriver` esté instalado y agregado a tu PATH.

## Ejecución

Ejecuta el script:
```bash
python main.py
```

## Salida

- La consola mostrará los nombres y precios de los primeros 5 productos.
- Las capturas de pantalla de cada paso se guardan en el directorio `screenshots/`.
