import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image

def main():
    st.title("Mediciones de alteraciones en colas de ratón")

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

        # 🔧 CAMBIO 1: Aislamos cada imagen en un st.expander
        with st.expander(f"📸 Imagen: {fname}", expanded=True):  
            img = Image.open(uploaded_file).convert("RGB")
            ancho = img.width  # ancho para normalización

            # 🔧 CAMBIO 2: Inicializar estado si no existe
            if f"estado_{fname}" not in st.session_state:
                st.session_state[f"estado_{fname}"] = 0

            estado = st.session_state[f"estado_{fname}"]

            # Mostrar instrucciones según el estado actual
            if estado == 0:
                st.write("➡️ Haz click para **Inicio de la cola**")
            elif estado == 1:
                st.write("➡️ Haz click para **Fin de la cola**")
            elif estado == 2:
                st.write("➡️ Haz click para **Límite de la trombosis**")
            else:
                st.success("✅ Todos los puntos ya fueron seleccionados para esta imagen.")

            # 🔧 CAMBIO 3: Coordinadas interactivas (con key único por imagen)
            coords = streamlit_image_coordinates(img, key=f"coords_{fname}")

            # 🔧 CAMBIO 4: Mostrar coordenadas para debug
            if coords:
                st.write("🖱 Coordenadas detectadas:", coords)
                x = coords["x"]
                x_norm = x / ancho  # valor normalizado entre 0 y 1

                # Guardar la coordenada según el estado actual
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

            # 🔧 CAMBIO 5: Calcular y mostrar resultados si ya están los 3 puntos
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
                st.markdown("### 📊 Resultados normalizados:")
                st.write(f"- Inicio: `{inicio:.4f}`")
                st.write(f"- Fin: `{fin:.4f}`")
                st.write(f"- Límite de trombosis: `{trombosis:.4f}`")
                st.write(f"- Largo total de la cola: `{largo_total:.4f}`")
                st.write(f"- Largo de la trombosis: `{largo_trombosis:.4f}`")
                if ratio is not None:
                    st.write(f"- Ratio trombosis / total: `{ratio:.4f}`")
                else:
                    st.write("- Ratio trombosis / total: ❌ No definido")

                resultados[fname] = {
                    "inicio": inicio,
                    "fin": fin,
                    "trombosis": trombosis,
                    "largo_total": largo_total,
                    "largo_trombosis": largo_trombosis,
                    "ratio": ratio,
                }

    # 🔧 CAMBIO 6: Mostrar resumen final si hay datos
    if resultados:
        st.markdown("## 📋 Resumen de resultados")
        st.table({
            fname: {
                "ratio": f"{res['ratio']:.4f}" if res["ratio"] is not None else "N/A",
                "largo_total": f"{res['largo_total']:.4f}",
                "largo_trombosis": f"{res['largo_trombosis']:.4f}"
            }
            for fname, res in resultados.items()
        })

if __name__ == "__main__":
    main()
