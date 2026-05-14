import streamlit as st
import pdfplumber
import re
import io
import zipfile

def extrair_placa(pdf_bytes):
    try:
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            texto = pdf.pages[0].extract_text()
            if texto:
                # Busca Placa Mercosul ou Antiga
                padrao_placa = r'[A-Z]{3}-?\d[A-Z0-9]\d{2}'
                resultado = re.search(padrao_placa, texto)
                if resultado:
                    # Limpa e padroniza a placa encontrada
                    return resultado.group(0).replace("-", "").upper().strip()
    except:
        return None
    return None

st.set_page_config(page_title="Renomeador CRLV-e", page_icon="📄")

st.title("Renomear CRLV - e")
st.markdown("""
1. Arraste todos os arquivos de uma vez.
2. O sistema vai extrair a placa e renomear como: **CRLV - e - PLACA - 2026**
""")

uploaded_files = st.file_uploader("Selecione os PDFs", type="pdf", accept_multiple_files=True)

if uploaded_files:
    if st.button(f"Renomear {len(uploaded_files)} arquivos agora"):
        zip_buffer = io.BytesIO()
        arquivos_processados = 0
        erros = []

        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
            barra_progresso = st.progress(0)
            
            for i, uploaded_file in enumerate(uploaded_files):
                bytes_data = uploaded_file.read()
                placa = extrair_placa(bytes_data)
                
                if placa:
                    # Ajuste exato do nome conforme solicitado
                    novo_nome = f"CRLV-e - {placa} - 2026.pdf"
                    zip_file.writestr(novo_nome, bytes_data)
                    arquivos_processados += 1
                else:
                    erros.append(uploaded_file.name)
                
                barra_progresso.progress((i + 1) / len(uploaded_files))

        if arquivos_processados > 0:
            st.success(f"✅ Concluído! {arquivos_processados} arquivos renomeados com sucesso.")
            st.download_button(
                label="📥 Baixar Arquivos Renomeados (.ZIP)",
                data=zip_buffer.getvalue(),
                file_name="CRLV_Renomeados_2026.zip",
                mime="application/zip"
            )
        
        if erros:
            with st.expander("⚠️ Arquivos onde a placa não foi encontrada"):
                for e in erros:
                    st.write(e)