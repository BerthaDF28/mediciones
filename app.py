
### app.py

```python
import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

def main():
    st.title("Medición normalizada de trombosis en imágenes")

    uploaded = st.file_uploader(
        "Sube múltiples imágenes (jpg, png, etc.)",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if not uploaded:
        st.info("Por favor sube al menos una imagen para continuar.")
        return

    resultados = {}

    for uploaded_file in uploaded:
        fname = uploaded_file.name
        img = Image.open(uploaded_file).convert("RGB")
        st.subheader(f"Imagen: {fname}")

        # Ancho para normalización
        ancho = img.width

        # Inicializar estado si no existe
        if f"estado_{fname}" not in st.session_state:
            st.session_state[f"estado_{fname}"] = 0

        # Mostrar instrucciones según estado
        estado = st.session_state[f"estado_{fname}"]
        if estado == 0:
            st.write("➡️ Haz click para **Inicio de la cola**")
        elif estado == 1:
            st.write("➡️ Haz click para **Fin de la cola**")
        elif estado == 2:
            st.write("➡️ Haz click para **Límite de la trombosis**")
        else:
            st.write("✅ Todos los puntos ya fueron seleccionados para esta imagen.")

        coords = streamlit_image_coordinates(img, key=f"coords_{fname}")

        if coords:
            x = coords["x"]
            x_norm = x / ancho  # valor entre 0 y 1

            if estado == 0:
                st.session_state[f"inicio_{fname}"] = x_norm
                st.session_state[f"estado_{fname}"] = 1
                st.success(f"Inicio registrado: x = {x} (normalizado = {x_norm:.4f})")
            elif estado == 1:
                st.session_state[f"fin_{fname}"] = x_norm
                st.session_state[f"estado_{fname}"] = 2
                st.success(f"Fin registrado: x = {x} (normalizado = {x_norm:.4f})")
            elif estado == 2:
                st.session_state[f"trombosis_{fname}"] = x_norm
                st.session_state[f"estado_{fname}"] = 3
                st.success(f"Límite de trombosis registrado: x = {x} (normalizado = {x_norm:.4f})")
            # si estado ya >=3 no hacer nada con clicks adicionales

        # Si ya tiene los 3 puntos, calcular resultados
        if st.session_state.get(f"estado_{fname}", 0) >= 3:
            inicio = st.session_state.get(f"inicio_{fname}")
            fin = st.session_state.get(f"fin_{fname}")
            trombosis = st.session_state.get(f"trombosis_{fname}")

            largo_total = abs(fin - inicio)
            largo_trombosis = abs(fin - trombosis)

            if largo_total == 0:
                ratio = None
                st.error("El inicio y el fin de la cola son iguales. Ratio indefinido.")
            else:
                ratio = largo_trombosis / largo_total

            # Mostrar resultados
            st.write("**Resultados normalizados:**")
            st.write(f"- Inicio: {inicio:.4f}")
            st.write(f"- Fin: {fin:.4f}")
            st.write(f"- Límite de trombosis: {trombosis:.4f}")
            st.write(f"- Largo total de la cola (normalizado): {largo_total:.4f}")
            st.write(f"- Largo de la trombosis (normalizado): {largo_trombosis:.4f}")
            if ratio is not None:
                st.write(f"- Ratio trombosis / total: {ratio:.4f}")
            else:
                st.write("- Ratio trombosis / total: No definido")

            # Guardar resultado en el diccionario
            resultados[fname] = {
                "inicio": inicio,
                "fin": fin,
                "trombosis": trombosis,
                "largo_total": largo_total,
                "largo_trombosis": largo_trombosis,
                "ratio": ratio,
            }

    # Mostrar tabla con todos los resultados si ya hay al menos una imagen con todos los puntos
    if resultados:
        st.write("## Resumen de todas las imágenes")
        st.table(
            {
                fname: {
                    "ratio": resultado["ratio"],
                    "largo_total": resultado["largo_total"],
                    "largo_trombosis": resultado["largo_trombosis"]
                }
                for fname, resultado in resultados.items()
            }
        )


if __name__ == "__main__":
    main()
