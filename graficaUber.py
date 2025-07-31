import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
from matplotlib.backends.backend_pdf import PdfPages

# Configurar página
st.set_page_config(page_title="Gráficos de Documentos", layout="centered")
st.title("📊 Comparación de Documentos y Hojas")

# --- Datos generales actualizados ---
df_general = pd.DataFrame({
    "Categoría": [
        "Documentos",
        "Documentos a procesar",
        "Documentos procesados",
        "Documentos categorizados (batch)",
        "Diferencia (Hojas blancas)"
    ],
    "Documentos": [1496, 0, 1496, 10773, 0],
    "Hojas": [90397, 0, 90397, 52074, 38323]
})

# df_tipo = pd.DataFrame({
#     "Tipo de Documento": [
#         "Auxiliar de Mayor",
#         "Otros",
#         "Polizas de Diario",
#         "Polizas de Egreso",
#         "Polizas de Ingreso",
#         "Polizas de Banorte",
#         "Poliza Tarjeta Amex",
#         "Poliza de AMEX",
#         "Polizas de Nomina",
#         "Polizas de Transferencias"
#     ],
#     "Documentos": [129, 377, 1932, 56, 562, 396, 8, 57, 4, 6846],
#     "Hojas": [884, 6270, 6177, 595, 1130, 2260, 1230, 1173, 47, 17452]
# })



# --- Función para crear gráficos ---l
def crear_graficos():
    figs = []

    color_documentos = '#87CEEB'
    color_hojas = '#F08080'

     # Tabla 1: df_general como figura
    fig3, ax3 = plt.subplots(figsize=(10, 2))
    ax3.axis('off')
    tabla1 = ax3.table(cellText=df_general.values, colLabels=df_general.columns, loc='center', cellLoc='center')
    tabla1.scale(1, 1.5)
    tabla1.auto_set_font_size(False)
    tabla1.set_fontsize(10)
    fig3.suptitle("Tabla: Resumen General", fontsize=12)
    figs.append(fig3)

    # Gráfico 1: General
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    x = np.arange(len(df_general))
    ancho = 0.35
    doc_bars = ax1.bar(x - ancho/2, df_general['Documentos'], width=ancho, label='Documentos', color=color_documentos)
    hoja_bars = ax1.bar(x + ancho/2, df_general['Hojas'], width=ancho, label='Hojas', color=color_hojas)
    ax1.set_title("Resumen general de documentos y hojas")
    ax1.set_xticks(x)
    ax1.set_xticklabels(df_general['Categoría'], rotation=45, ha='right')
    ax1.set_ylabel("Cantidad")
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    ax1.bar_label(doc_bars, padding=3)
    ax1.bar_label(hoja_bars, padding=3)
    figs.append(fig1)

    # Tabla 2: df_tipo como figura
    # fig4, ax4 = plt.subplots(figsize=(10, 4))
    # ax4.axis('off')
    # tabla2 = ax4.table(cellText=df_tipo.values, colLabels=df_tipo.columns, loc='center', cellLoc='center')
    # tabla2.scale(1, 1.5)
    # tabla2.auto_set_font_size(False)
    # tabla2.set_fontsize(10)
    # fig4.suptitle("Tabla: Documentos por Tipo \n", fontsize=12)
    # figs.append(fig4)

    # # Gráfico 2: Por tipo
    # fig2, ax2 = plt.subplots(figsize=(10, 5))
    # x2 = np.arange(len(df_tipo))
    # doc_bars2 = ax2.bar(x2 - ancho/2, df_tipo['Documentos'], width=ancho, label='Documentos', color=color_documentos)
    # hoja_bars2 = ax2.bar(x2 + ancho/2, df_tipo['Hojas'], width=ancho, label='Hojas', color=color_hojas)
    # ax2.set_title("Documentos y hojas por tipo de documento")
    # ax2.set_xticks(x2)
    # ax2.set_xticklabels(df_tipo['Tipo de Documento'], rotation=45, ha='right')
    # ax2.set_ylabel("Cantidad")
    # ax2.legend()
    # ax2.grid(axis='y', linestyle='--', alpha=0.7)
    # ax2.bar_label(doc_bars2, padding=3)
    # ax2.bar_label(hoja_bars2, padding=3)
    # figs.append(fig2)

   

    return figs

# --- Mostrar gráficos en pantalla ---
st.subheader("📈 Gráficos de Comparación")
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
    file_name="graficos_documentos.pdf",
    mime="application/pdf"
)
