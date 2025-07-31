import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

# Configurar página
st.set_page_config(page_title="Gráficos de Imágenes", layout="centered")
st.title("🖼️ Comparación de Imágenes")

# --- Datos solo de imágenes ---
df_general = pd.DataFrame({
    "Categoría": [
        "Imagenes Totales",
        "Imagenes procesadss",
        "Imagenes categorizadas (batch)", 
        "Diferencia (Imágenes blancas)"
    ],
    "Imágenes": [90397, 90397, 52074, 38323]
})

# --- Función para crear gráficos ---
def crear_graficos():
    figs = []

    color_hojas = "#80F0CB"

    # Tabla
    fig_tabla, ax_tabla = plt.subplots(figsize=(10, 2))
    ax_tabla.axis('off')
    tabla = ax_tabla.table(
        cellText=df_general.values,
        colLabels=df_general.columns,
        loc='center',
        cellLoc='center'
    )
    tabla.scale(1, 1.5)
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(10)
    fig_tabla.suptitle("Tabla: Resumen de Imágenes", fontsize=12)
    figs.append(fig_tabla)

    # Gráfico de barras solo de imágenes
    fig_bar, ax_bar = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df_general))
    ancho = 0.4
    bars = ax_bar.bar(x, df_general['Imágenes'], width=ancho, label='Imágenes', color=color_hojas)
    ax_bar.set_title("Resumen general de imágenes")
    ax_bar.set_xticks(x)
    ax_bar.set_xticklabels(df_general['Categoría'], rotation=45, ha='right')
    ax_bar.set_ylabel("Cantidad")
    ax_bar.grid(axis='y', linestyle='--', alpha=0.7)
    ax_bar.bar_label(bars, padding=3)
    figs.append(fig_bar)

    return figs

# --- Mostrar gráficos en pantalla ---
st.subheader("📈 Gráficos de Comparación de Imágenes")
figures = crear_graficos()
for fig in figures:
    st.pyplot(fig)

# --- Generar PDF ---
def generar_pdf(figs):
    pdf_buffer = BytesIO()
    with PdfPages(pdf_buffer) as pdf:
        for fig in figs:
            pdf.savefig(fig, bbox_inches='tight')
        plt.close('all')  # Cierra los plots abiertos
    pdf_buffer.seek(0)
    return pdf_buffer

# --- Botón para descargar PDF ---
st.subheader("📥 Descargar gráficos en PDF")
pdf_data = generar_pdf(figures)
st.download_button(
    label="Descargar PDF",
    data=pdf_data,
    file_name="graficos_imagenes.pdf",
    mime="application/pdf"
)
