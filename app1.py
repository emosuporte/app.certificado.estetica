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


st.set_page_config(page_title="Certificado Estética", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    .app-shell {
        max-width: 1100px;
        margin: 0 auto;
        padding: 1.5rem 1rem 3rem;
    }
    .hero {
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        margin-bottom: 2rem;
    }
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: #eef2ff;
        color: #4338ca;
        padding: 0.35rem 0.75rem;
        border-radius: 999px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    .hero h1 {
        font-size: 2.6rem;
        margin: 0;
    }
    .hero p {
        margin: 0;
        color: #475467;
        font-size: 1.05rem;
        max-width: 680px;
    }
    .card {
        background: #ffffff;
        border: 1px solid #e4e7ec;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 20px 40px rgba(15, 23, 42, 0.08);
    }
    .card-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.35rem;
    }
    .card-subtitle {
        color: #667085;
        font-size: 0.95rem;
        margin-bottom: 1.25rem;
    }
    .preview-label {
        color: #98a2b3;
        font-size: 0.85rem;
        margin-bottom: 0.2rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }
    .preview-value {
        font-size: 1.1rem;
        font-weight: 600;
    }
    .steps {
        display: grid;
        gap: 0.75rem;
        margin-top: 1.5rem;
    }
    .step {
        display: flex;
        gap: 0.75rem;
        align-items: flex-start;
        background: #f9fafb;
        border-radius: 14px;
        padding: 0.85rem 1rem;
    }
    .step span {
        background: #e0e7ff;
        color: #4338ca;
        font-weight: 700;
        border-radius: 10px;
        padding: 0.3rem 0.6rem;
        font-size: 0.85rem;
    }
    .step p {
        margin: 0;
        color: #344054;
        font-size: 0.95rem;
    }
    .stButton > button {
        width: 100%;
        border-radius: 999px;
        font-weight: 600;
        padding: 0.85rem 1rem;
        background: #111827;
        color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='app-shell'>", unsafe_allow_html=True)

st.markdown(
    """
    <section class="hero">
        <div class="badge">v0 • Certificados inteligentes</div>
        <h1>Certificados para Estética com acabamento profissional</h1>
        <p>Personalize os dados do aluno, faça upload do fundo do certificado e gere um PDF pronto para imprimir ou enviar.</p>
    </section>
    """,
    unsafe_allow_html=True,
)

col_left, col_right = st.columns([1.1, 0.9], gap="large")

if "pdf_bytes" not in st.session_state:
    st.session_state.pdf_bytes = None
    st.session_state.file_name = None

with col_left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Dados do certificado</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card-subtitle'>Preencha os campos e faça o download do PDF imediatamente.</div>",
        unsafe_allow_html=True,
    )
    with st.form("certificado_form"):
        nome_aluno = st.text_input("Nome do aluno", placeholder="Ex: Maria da Silva")
        nome_curso = st.text_input("Nome do curso", placeholder="Ex: Estética Facial Avançada")
        background_file = st.file_uploader(
            "Imagem de fundo (opcional)", type=["png", "jpg", "jpeg"]
        )
        submitted = st.form_submit_button("Gerar certificado")
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("<div class='card-title'>Prévia rápida</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='card-subtitle'>Confirme os dados antes de gerar o certificado.</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='preview-label'>Aluno</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='preview-value'>{nome_aluno or '—'}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='preview-label'>Curso</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='preview-value'>{nome_curso or '—'}</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='preview-label'>Data</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div class='preview-value'>{datetime.now().strftime('%d/%m/%Y')}</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="steps">
            <div class="step"><span>1</span><p>Preencha o nome do aluno e o curso.</p></div>
            <div class="step"><span>2</span><p>Envie o fundo do certificado, se desejar.</p></div>
            <div class="step"><span>3</span><p>Baixe o PDF pronto para impressão.</p></div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

if submitted:
    if nome_aluno.strip() and nome_curso.strip():
        background_path = None
        if background_file is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
                temp_file.write(background_file.read())
                background_path = temp_file.name

        st.session_state.pdf_bytes = generate_certificate(
            nome_aluno, nome_curso, background_path
        )
        st.session_state.file_name = f"Certificado_{nome_aluno}.pdf"
    else:
        st.warning("Por favor, preencha o nome do aluno e o nome do curso.")

if st.session_state.pdf_bytes:
    st.success("Certificado gerado com sucesso!")
    st.download_button(
        "Baixar certificado",
        data=st.session_state.pdf_bytes,
        file_name=st.session_state.file_name,
        mime="application/pdf",
    )

st.markdown("</div>", unsafe_allow_html=True)
