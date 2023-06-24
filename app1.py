import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from datetime import datetime

def generate_certificate(nome_aluno, nome_curso):
    # Configurações do PDF
    pdf_title = 'Certificado de Conclusão de Curso Estética'
    pdf_name = f'Certificado_{nome_aluno}.pdf'
    
    # Gerar PDF
    c = canvas.Canvas(pdf_name, pagesize=letter)
    c.setTitle(pdf_title)
    
    # Adicionar imagem de fundo do certificado
    certificado_path = 'caminho/para/fundo_certificado.png'
    c.drawImage(certificado_path, 0, 0, width=8.5*inch, height=11*inch)
    
    # Definir o estilo para o nome do aluno
    style_aluno = ParagraphStyle(name='Center', fontSize=32, alignment=TA_CENTER)
    
    # Desenhar o nome do aluno
    c.setFillColor(colors.black)  # Definir a cor do texto para preto
    c.setFont("Helvetica", 32)  # Definir a fonte e o tamanho do texto
    c.drawString(4.25*inch, 5.5*inch, nome_aluno)  # Posicionar o nome do aluno no centro
    
    # Definir o estilo para o nome do curso
    style_curso = ParagraphStyle(name='Center', fontSize=16, alignment=TA_CENTER)
    
    # Desenhar o nome do curso
    c.setFont("Helvetica", 16)  # Definir a fonte e o tamanho do texto
    c.drawString(4.25*inch, 4*inch, nome_curso)  # Posicionar o nome do curso
    
    # Obter a data atual
    data_atual = datetime.now().strftime("%d/%m/%Y")
    
    # Definir o estilo para a data
    style_data = ParagraphStyle(name='Center', fontSize=12, alignment=TA_CENTER)
    
    # Desenhar a data
    c.setFont("Helvetica", 12)  # Definir a fonte e o tamanho do texto
    c.drawString(4.25*inch, 3*inch, f"Data: {data_atual}")  # Posicionar a data
    
    # Salvar PDF
    c.save()
    
    return pdf_name

# Aplicativo Streamlit
st.title('Sistema para Certificado Estética')

# Entrada de dados
nome_aluno = st.text_input('Digite o nome do aluno:')
nome_curso = st.text_input('Digite o nome do curso:')

# Botão para gerar certificado
if st.button('Gerar Certificado'):
    if nome_aluno.strip() != "" and nome_curso.strip() != "":
        certificado_file = generate_certificate(nome_aluno, nome_curso)
        st.success(f'Certificado gerado com sucesso. Você pode baixá-lo [aqui]({certificado_file}).')
    else:
        st.warning('Por favor, preencha o nome do aluno e o nome do curso.')
