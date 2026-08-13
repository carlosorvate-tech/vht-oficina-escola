import streamlit as st
import pandas as pd
import os
from PIL import Image

# ---------------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# ---------------------------------------------------------
st.set_page_config(
    page_title="Gestão VHT | INFINITUS",
    page_icon="⚙️",
    layout="wide"
)

# ---------------------------------------------------------
# CABEÇALHO DE MARCAS E PATROCÍNIO
# ---------------------------------------------------------
col_logo_left, col_title, col_logo_right = st.columns([2.5, 5, 2.5])

with col_logo_left:
    st.caption("💡 PROPRIEDADE INTELECTUAL")
    if os.path.exists("Nova Infinitus.jpg"):
        st.image("Nova Infinitus.jpg", use_container_width=True)
    else:
        st.info("⚡ **INFINITUS**\n\nSistemas Inteligentes")

with col_title:
    st.title("⚙️ Calculadora VHT")
    st.markdown("**Plataforma Educacional de Precificação & Gestão de Oficinas Mecânicas**")

with col_logo_right:
    st.caption("🏆 PATROCINADOR MASTER")
    if os.path.exists("logo oficina republica.jpeg"):
        st.image("logo oficina republica.jpeg", use_container_width=True)
    else:
        st.success("🔧 **AUTO MECÂNICA REPÚBLICA**\n\nApoio Educacional Oficial")

st.divider()

# ---------------------------------------------------------
# SIDEBAR: ENTRADAS DE DADOS
# ---------------------------------------------------------
st.sidebar.header("1. Custos Fixos & Impostos")
custos_fixos = st.sidebar.number_input(
    "Custos Fixos Mensais (R$)", 
    value=10000.0, step=500.0, 
    help="Aluguel, água, luz, internet, recepção, contabilidade, seguros, etc."
)
impostos_pct = st.sidebar.slider("Alíquota Impostos (%)", 0.0, 25.0, 8.0, 0.5) / 100.0
margem_pct = st.sidebar.slider("Margem Lucro Desejada (%)", 0.0, 40.0, 20.0, 1.0) / 100.0

st.sidebar.header("2. Equipe Mecânica Geral")
qtd_geral = st.sidebar.number_input("Nº de Mecânicos Gerais", value=4, min_value=1)
custo_geral = st.sidebar.number_input("Custo Mensal / Mecânico Geral (R$)", value=5000.0, step=200.0)
horas_geral = st.sidebar.number_input("Horas Contratadas / Mês (Geral)", value=176)
efic_geral = st.sidebar.slider("Eficiência Geral (%)", 40, 95, 75) / 100.0

st.sidebar.header("3. Diagnóstico / Especialista")
qtd_esp = st.sidebar.number_input("Nº de Especialistas", value=1, min_value=0)
custo_esp = st.sidebar.number_input("Custo Mensal / Especialista (R$)", value=8000.0, step=500.0)
custo_tech = st.sidebar.number_input("Softwares e Ferramentas / Mês (R$)", value=1500.0, step=100.0)
horas_esp = st.sidebar.number_input("Horas Contratadas / Mês (Especialista)", value=176)
efic_esp = st.sidebar.slider("Eficiência Especialista (%)", 30, 90, 55) / 100.0

# ---------------------------------------------------------
# MOTOR DE CÁLCULO
# ---------------------------------------------------------
h_cont_geral = qtd_geral * horas_geral
h_cont_esp = qtd_esp * horas_esp
h_fat_geral = h_cont_geral * efic_geral
h_fat_esp = h_cont_esp * efic_esp
h_fat_total = h_fat_geral + h_fat_esp

rateio_fixo_h = custos_fixos / h_fat_total if h_fat_total > 0 else 0

c_dir_geral_total = qtd_geral * custo_geral
c_dir_geral_h = c_dir_geral_total / h_fat_geral if h_fat_geral > 0 else 0
c_base_geral = rateio_fixo_h + c_dir_geral_h

c_dir_esp_total = (qtd_esp * custo_esp) + custo_tech
c_dir_esp_h = c_dir_esp_total / h_fat_esp if h_fat_esp > 0 else 0
c_base_esp = rateio_fixo_h + c_dir_esp_h

divisor = 1 - (impostos_pct + margem_pct)
vht_geral = c_base_geral / divisor if divisor > 0 else 0
vht_esp = c_base_esp / divisor if divisor > 0 else 0

custo_total_mensal = custos_fixos + c_dir_geral_total + c_dir_esp_total
custo_minuto_parado = custo_total_mensal / (h_fat_total * 60) if h_fat_total > 0 else 0

vht_medio_liquido = ((vht_geral * (h_fat_geral/h_fat_total) if h_fat_total>0 else 0) + 
                     (vht_esp * (h_fat_esp/h_fat_total) if h_fat_total>0 else 0)) * (1 - impostos_pct)
horas_break_even = custo_total_mensal / vht_medio_liquido if vht_medio_liquido > 0 else 0

# ---------------------------------------------------------
# INTERFACE PRINCIPAL EM ABAS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🧮 Precificação & Painel VHT", 
    "📊 DRE & Indicadores de Gestão", 
    "📝 Emissor de Orçamentos Prático",
    "🤝 Parceiros & Patrocínio"
])

# --- ABA 1: PRECIFICAÇÃO & PAINEL VHT ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("VHT - Mecânica Geral", f"R$ {vht_geral:.2f} / h", f"Custo Base: R$ {c_base_geral:.2f}")
    col2.metric("VHT - Diagnóstico", f"R$ {vht_esp:.2f} / h", f"Custo Base: R$ {c_base_esp:.2f}")
    col3.metric("Minuto Parado", f"R$ {custo_minuto_parado:.2f} / min", "Prejuízo da ociosidade")
    col4.metric("Ponto de Equilíbrio", f"{horas_break_even:.1f} hrs/mês", f"{(horas_break_even/h_fat_total)*100:.1f}% da capacidade" if h_fat_total > 0 else "0%")

    st.subheader("📋 Resumo da Estrutura de Custos por Hora Vendida")
    df_resumo = pd.DataFrame({
        "Categoria de Serviço": ["Mecânica Geral (Básica)", "Diagnóstico Eletrônico (Avançado)"],
        "Horas Faturáveis/Mês": [f"{h_fat_geral:.1f} h", f"{h_fat_esp:.1f} h"],
        "Rateio Custo Fixo / h": [f"R$ {rateio_fixo_h:.2f}", f"R$ {rateio_fixo_h:.2f}"],
        "Custo Direto / h": [f"R$ {c_dir_geral_h:.2f}", f"R$ {c_dir_esp_h:.2f}"],
        "Custo Base Total / h": [f"R$ {c_base_geral:.2f}", f"R$ {c_base_esp:.2f}"],
        "Impostos + Margem": [f"{(impostos_pct+margem_pct)*100:.1f}%", f"{(impostos_pct+margem_pct)*100:.1f}%"],
        "Valor da Hora Técnica (VHT)": [f"R$ {vht_geral:.2f}", f"R$ {vht_esp:.2f}"]
    })
    st.dataframe(df_resumo, use_container_width=True)

# --- ABA 2: DRE & INDICADORES ---
with tab2:
    st.subheader("📊 DRE Operacional Simulado")
    fat_potencial = (h_fat_geral * vht_geral) + (h_fat_esp * vht_esp)
    imp_total = fat_potencial * impostos_pct
    rec_liquida = fat_potencial - imp_total
    lucro_operacional = rec_liquida - custo_total_mensal
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Faturamento Máximo Potencial", f"R$ {fat_potencial:,.2f}")
    col_b.metric("Custo Total da Operação", f"R$ {custo_total_mensal:,.2f}")
    col_c.metric("Lucro Líquido Projetado", f"R$ {lucro_operacional:,.2f}", f"Margem Real: {(lucro_operacional/fat_potencial)*100:.1f}%" if fat_potencial > 0 else "0%")

# --- ABA 3: EMISSOR DE ORÇAMENTOS ---
with tab3:
    st.subheader("📝 Simulador de Orçamento para Clientes")
    col_x, col_y = st.columns([1, 1])
    with col_x:
        desc_servico = st.text_input("Descrição do Veículo / Cliente", value="VW Gol 1.0 - Cliente João")
        h_basica_os = st.number_input("Horas de Serviço Básico (Mecânica Geral)", value=2.5, step=0.5)
        h_diag_os = st.number_input("Horas de Diagnóstico Eletrônico", value=1.0, step=0.5)
        valor_pecas = st.number_input("Valor Total de Peças Aplicadas (R$)", value=350.0, step=50.0)
    
    total_mo_basica = h_basica_os * vht_geral
    total_mo_diag = h_diag_os * vht_esp
    total_mo_geral = total_mo_basica + total_mo_diag
    total_orcamento = total_mo_geral + valor_pecas
    
    with col_y:
        st.markdown(f"### 📄 Orçamento Estimado: {desc_servico}")
        st.markdown(f"* **Mão de Obra Geral:** {h_basica_os}h × R$ {vht_geral:.2f} = **R$ {total_mo_basica:.2f}**")
        st.markdown(f"* **Diagnóstico Eletrônico:** {h_diag_os}h × R$ {vht_esp:.2f} = **R$ {total_mo_diag:.2f}**")
        st.markdown(f"* **Subtotal Mão de Obra:** **R$ {total_mo_geral:.2f}**")
        st.markdown(f"* **Subtotal Peças:** **R$ {valor_pecas:.2f}**")
        st.divider()
        st.markdown(f"## **Total Geral: R$ {total_orcamento:.2f}**")
        st.caption("🔒 *Orçamento gerado via Plataforma VHT • Tecnologia INFINITUS SISTEMAS INTELIGENTES • Patrocínio: Auto Mecânica República*")

# --- ABA 4: PARCEIROS E PATROCÍNIO ---
with tab4:
    st.subheader("🤝 Patrocinadores e Fomento Educacional")
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.success("### 🔧 Auto Mecânica República\n**Patrocinador Master & Oficina Referência**")
        st.write("Apoio oficial para a formação de novos gestores automotivos e incentivo à valorização da hora técnica.")
    with col_p2:
        st.info("### 💡 INFINITUS Sistemas Inteligentes\n**Propriedade Intelectual & Tecnologia**")
        st.write("Desenvolvimento de soluções analíticas e plataformas inteligentes para o setor automotivo e acadêmico.")

# ---------------------------------------------------------
# RODAPÉ FIXO
# ---------------------------------------------------------
st.divider()
st.markdown(
    "<div style='text-align: center; color: #666; font-size: 0.85em;'>"
    "<b>INFINITUS SISTEMAS INTELIGENTES</b> © Todos os direitos reservados • "
    "Patrocínio Oficial: <b>Auto Mecânica República</b>"
    "</div>", 
    unsafe_allow_html=True
)
