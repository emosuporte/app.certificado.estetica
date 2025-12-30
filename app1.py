import io
import tempfile
from datetime import datetime

import streamlit as st
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas


def generate_certificate(nome_aluno, nome_curso, background_path=None):
    pdf_title = "Certificado de Conclusão de Curso Estética"
    buffer = io.BytesIO()

    c = canvas.Canvas(buffer, pagesize=letter)
    c.setTitle(pdf_title)

    if background_path:
        c.drawImage(background_path, 0, 0, width=8.5 * inch, height=11 * inch)

    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(4.25 * inch, 5.5 * inch, nome_aluno)

    c.setFont("Helvetica", 16)
    c.drawCentredString(4.25 * inch, 4 * inch, nome_curso)

    data_atual = datetime.now().strftime("%d/%m/%Y")
    c.setFont("Helvetica", 12)
    c.drawCentredString(4.25 * inch, 3 * inch, f"Data: {data_atual}")

    c.save()
    buffer.seek(0)
    return buffer.getvalue()


st.set_page_config(page_title="Certificado Estética", page_icon="🎓", layout="centered")

st.markdown(
    """
    <style>
    .app-header {
        text-align: center;
        padding: 1rem 0 0.5rem;
    }
    .app-header h1 {
        font-size: 2.4rem;
        margin-bottom: 0.2rem;
    }
    .app-header p {
        color: #6c757d;
        margin-top: 0;
    }
    .card {
        background: #ffffff;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 12px 30px rgba(16, 24, 40, 0.08);
    }
    .stButton > button {
        width: 100%;
        border-radius: 999px;
        font-weight: 600;
        padding: 0.75rem 1rem;
    }
    .info-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #f2f4f7;
        padding: 0.4rem 0.75rem;
        border-radius: 999px;
        font-size: 0.85rem;
        color: #475467;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-header">
        <div class="info-pill">✨ Certificados rápidos e elegantes</div>
        <h1>Sistema para Certificado Estética</h1>
        <p>Preencha os dados abaixo e gere o PDF pronto para impressão.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    with st.form("certificado_form"):
        nome_aluno = st.text_input("Nome do aluno", placeholder="Ex: Maria Silva")
        nome_curso = st.text_input("Nome do curso", placeholder="Ex: Estética Avançada")
        background_file = st.file_uploader(
            "Imagem de fundo (opcional)", type=["png", "jpg", "jpeg"]
        )
        submitted = st.form_submit_button("Gerar certificado")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("Prévia")
    st.caption("Veja as informações que vão aparecer no certificado.")
    st.write("**Aluno:**", nome_aluno or "—")
    st.write("**Curso:**", nome_curso or "—")
    st.write("**Data:**", datetime.now().strftime("%d/%m/%Y"))
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if nome_aluno.strip() and nome_curso.strip():
        background_path = None
        if background_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(background_file.read())
                background_path = temp_file.name

        pdf_bytes = generate_certificate(nome_aluno, nome_curso, background_path)

        st.success("Certificado gerado com sucesso!")
        st.download_button(
            "Baixar certificado",
            data=pdf_bytes,
            file_name=f"Certificado_{nome_aluno}.pdf",
            mime="application/pdf",
        )
    else:
        st.warning("Por favor, preencha o nome do aluno e o nome do curso.")
