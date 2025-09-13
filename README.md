Esta aplicación permite:

- Subir múltiples imágenes.
- Hacer clic en tres puntos distintos en cada imagen: **inicio de la cola**, **fin de la cola**, **límite de la trombosis**.
- Capturar la coordenada X de esos puntos.
- Normalizar esas coordenadas como porcentaje del ancho de la imagen.
- Calcular:
  - Largo total de la cola (|fin - inicio|)
  - Largo de la trombosis (|fin - límite de trombosis|)
  - Ratio: trombosis / total

Muestra los resultados por cada imagen.

---

## Uso

1. Instalar dependencias:

   ```bash
   pip install -r requirements.txt

2. Ejecutar:

streamlit run app.py

3. Interactuar con cada imagen haciendo clic en los tres puntos pedidos, siguiendo las instrucciones que aparecen.
