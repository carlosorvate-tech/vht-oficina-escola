import streamlit as st
import pandas as pd
import os
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(
    page_title="Gestão VHT | INFINITUS",
    page_icon="⚙️",
    layout="wide"
)

# ---------------------------------------------------------
# ESTILIZAÇÃO CUSTOMIZADA PREMIUM (DARK SLATE & ALTO CONTRASTE)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Estilo Global Dark Slate */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Top Bar & Header Transparent Dark */
    [data-testid="stHeader"] {
        background-color: rgba(15, 23, 42, 0.95);
    }
    
    /* Sidebar Escura Elegante */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
        border-right: 1px solid #334155;
    }
    
    /* Cartões de Métricas (st.metric) */
    [data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        padding: 16px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
    }
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700 !important;
    }
    [data-testid="stMetricDelta"] {
        color: #34d399 !important;
    }
    
    /* Estilização das Abas (st.tabs) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 8px;
        border-radius: 8px;
        border: 1px solid #334155;
    }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: transparent;
        border-radius: 6px;
        color: #94a3b8;
        font-weight: 600;
        padding: 0px 16px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }
    
    /* Regras de Impressão (Papel / PDF) */
    @media print {
        body * {
            visibility: hidden !important;
        }
        #secao-impressao, #secao-impressao * {
            visibility: visible !important;
            color: #000000 !important;
            background-color: #ffffff !important;
        }
        #secao-impressao {
            position: absolute !important;
            left: 0 !important;
            top: 0 !important;
            width: 100% !important;
            border: 2px solid #000000 !important;
            padding: 20px !important;
        }
        .no-print {
            display: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

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
# SIDEBAR: ENTRADAS DE DADOS DIDÁTICAS
# ---------------------------------------------------------
st.sidebar.header("1. Custos Fixos & Margens")
st.sidebar.markdown("*Despesas estruturais e tributárias da oficina*")

custos_fixos = st.sidebar.number_input(
    "Custos Fixos Mensais TOTAIS (R$)", 
    value=10000.0, step=500.0, 
    help="Soma de TODAS as despesas da estrutura da oficina no mês (Aluguel, IPTU, Água, Luz, Internet, Salário da Recepção/Admin, Contabilidade, Seguros, Softwares gerais e Depreciação de Equipamentos). NÃO inclua o salário dos mecânicos aqui."
)

impostos_pct = st.sidebar.slider(
    "Alíquota de Impostos (%)", 
    0.0, 25.0, 8.0, 0.5,
    help="Porcentagem média de impostos faturados sobre a nota de serviço de mão de obra (Ex: Simples Nacional ~8%)."
) / 100.0

margem_pct = st.sidebar.slider(
    "Margem de Lucro Desejada (%)", 
    0.0, 40.0, 20.0, 1.0,
    help="Porcentagem de lucro líquido pretendida pela oficina sobre a venda da mão de obra."
) / 100.0

st.sidebar.header("2. Equipe Mecânica Geral (Básica)")
st.sidebar.markdown("*Mão de obra de suspensão, freio, motor, óleo e manutenção rotineira*")

qtd_geral = st.sidebar.number_input(
    "Quantidade de Mecânicos Gerais", 
    value=4, min_value=1,
    help="Número total de mecânicos que atuam na equipe de manutenção geral."
)

custo_geral_indiv = st.sidebar.number_input(
    "Custo Mensal INDIVIDUAL por Mecânico Geral (R$)", 
    value=5000.0, step=200.0,
    help="⚠️ VALOR UNITÁRIO POR MECÂNICO: Digite o valor referente a UM ÚNICO MECÂNICO (Salário Base + Encargos FGTS/INSS + Provisão Férias/13º + Benefícios VT/VR). O sistema multiplicará automaticamente pela quantidade de mecânicos informada."
)

horas_geral = st.sidebar.number_input(
    "Horas Contratadas por Mecânico / Mês", 
    value=176,
    help="Horas pagas no contrato de trabalho por funcionário no mês (Padrão CLT: 44h/semana x 4 = 176 horas)."
)

efic_geral = st.sidebar.slider(
    "Eficiência Operacional (%) - Geral", 
    40, 95, 75,
    help="Percentual do tempo pago que é EFETIVAMENTE VENDIDO em ordens de serviço. Desconta tempo gasto com limpeza, busca de peças, testes e reuniões. Média do setor: 70% a 80%."
) / 100.0

st.sidebar.header("3. Diagnóstico / Especialista (Avançada)")
st.sidebar.markdown("*Mão de obra de eletrônica, osciloscópio, injeção e redes de comunicação*")

qtd_esp = st.sidebar.number_input(
    "Quantidade de Especialistas", 
    value=1, min_value=0,
    help="Número total de mecânicos especialistas/diagnostistas na oficina."
)

custo_esp_indiv = st.sidebar.number_input(
    "Custo Mensal INDIVIDUAL por Especialista (R$)", 
    value=8000.0, step=500.0,
    help="⚠️ VALOR UNITÁRIO POR ESPECIALISTA: Custo total de UM ÚNICO ESPECIALISTA (Salário qualificado + Encargos + Benefícios)."
)

custo_tech = st.sidebar.number_input(
    "Custos Tecnológicos Exclusivos / Mês (R$)", 
    value=1500.0, step=100.0,
    help="Mensalidade de softwares de esquemas elétricos, atualização do scanner e depreciação de equipamentos avançados (osciloscópios)."
)

horas_esp = st.sidebar.number_input(
    "Horas Contratadas por Especialista / Mês", 
    value=176,
    help="Carga horária mensal contratada por especialista."
)

efic_esp = st.sidebar.slider(
    "Eficiência Operacional (%) - Diagnóstico", 
    30, 90, 55,
    help="A eficiência do especialista é naturalmente menor (~50% a 60%), pois ele consome mais tempo estudando diagramas elétricos e fazendo medições de bancada antes de faturar a hora."
) / 100.0

# ---------------------------------------------------------
# MOTOR DE CÁLCULO DETERMINÍSTICO
# ---------------------------------------------------------
c_dir_geral_total = qtd_geral * custo_geral_indiv
c_dir_esp_total = (qtd_esp * custo_esp_indiv) + custo_tech
custo_total_folha_e_tech = c_dir_geral_total + c_dir_esp_total

h_cont_geral = qtd_geral * horas_geral
h_cont_esp = qtd_esp * horas_esp

h_fat_geral = h_cont_geral * efic_geral
h_fat_esp = h_cont_esp * efic_esp
h_fat_total = h_fat_geral + h_fat_esp

rateio_fixo_h = custos_fixos / h_fat_total if h_fat_total > 0 else 0

c_dir_geral_h = c_dir_geral_total / h_fat_geral if h_fat_geral > 0 else 0
c_base_geral = rateio_fixo_h + c_dir_geral_h

c_dir_esp_h = c_dir_esp_total / h_fat_esp if h_fat_esp > 0 else 0
c_base_esp = rateio_fixo_h + c_dir_esp_h

divisor = 1.0 - (impostos_pct + margem_pct)
vht_geral = c_base_geral / divisor if divisor > 0 else 0
vht_esp = c_base_esp / divisor if divisor > 0 else 0

custo_total_mensal = custos_fixos + custo_total_folha_e_tech
custo_minuto_parado = custo_total_mensal / (h_fat_total * 60) if h_fat_total > 0 else 0

vht_medio_liquido = ((vht_geral * (h_fat_geral/h_fat_total) if h_fat_total>0 else 0) + 
                     (vht_esp * (h_fat_esp/h_fat_total) if h_fat_total>0 else 0)) * (1 - impostos_pct)
horas_break_even = custo_total_mensal / vht_medio_liquido if vht_medio_liquido > 0 else 0

# ---------------------------------------------------------
# INTERFACE PRINCIPAL EM ABAS
# ---------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "🧮 Precificação & Painel VHT", 
    "📘 Guia Didático de Formação do Custo", 
    "📝 Emissor de Orçamentos com Impressão",
    "🤝 Parceiros & Patrocínio"
])

# --- ABA 1: PRECIFICAÇÃO ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("VHT - Mecânica Geral", f"R$ {vht_geral:.2f} / h", f"Custo Base: R$ {c_base_geral:.2f}")
    col2.metric("VHT - Diagnóstico", f"R$ {vht_esp:.2f} / h", f"Custo Base: R$ {c_base_esp:.2f}")
    col3.metric("Minuto Parado", f"R$ {custo_minuto_parado:.2f} / min", "Custo da Ociosidade")
    col4.metric("Ponto de Equilíbrio", f"{horas_break_even:.1f} hrs/mês", f"{(horas_break_even/h_fat_total)*100:.1f}% da capacidade" if h_fat_total > 0 else "0%")

    st.subheader("📋 Resumo da Formação dos Custos por Categoria")
    df_resumo = pd.DataFrame({
        "Categoria de Serviço": ["Mecânica Geral (Básica)", "Diagnóstico Eletrônico (Avançado)"],
        "Nº Profissionais": [f"{qtd_geral} mecânicos", f"{qtd_esp} especialista(s)"],
        "Folha + Tech Total (R$)": [f"R$ {c_dir_geral_total:,.2f}", f"R$ {c_dir_esp_total:,.2f}"],
        "Capacidade Faturável": [f"{h_fat_geral:.1f} hrs/mês", f"{h_fat_esp:.1f} hrs/mês"],
        "Rateio Custo Fixo / h": [f"R$ {rateio_fixo_h:.2f}", f"R$ {rateio_fixo_h:.2f}"],
        "Custo Direto / h": [f"R$ {c_dir_geral_h:.2f}", f"R$ {c_dir_esp_h:.2f}"],
        "Custo Base Total / h": [f"R$ {c_base_geral:.2f}", f"R$ {c_base_esp:.2f}"],
        "Markup (Imp + Lucro)": [f"{(impostos_pct+margem_pct)*100:.1f}%", f"{(impostos_pct+margem_pct)*100:.1f}%"],
        "VALOR DA HORA TÉCNICA (VHT)": [f"R$ {vht_geral:.2f}", f"R$ {vht_esp:.2f}"]
    })
    st.dataframe(df_resumo, use_container_width=True)

# --- ABA 2: GUIA DIDÁTICO DE FORMAÇÃO DO CUSTO ---
with tab2:
    st.subheader("📘 Como cada Real é calculado (Guia Didático da Formação do Preço)")
    st.markdown("""
    Esta seção explica a lógica por trás de cada etapa da precificação. O cálculo de uma oficina mecânica não é arbitrário, ele segue a **Engenharia de Custos da Mão de Obra**.
    """)
    
    with st.expander("1️⃣ Esclarecimento sobre o Custo dos Mecânicos (Individual vs. Equipe)", expanded=True):
        st.write(f"""
        * **Valor Informado:** O input na barra lateral (`R$ {custo_geral_indiv:,.2f}`) representa o custo de **1 ÚNICO MECÂNICO** (Salário + Encargos FGTS/INSS + Benefícios).
        * **Custo Total da Equipe Geral ({qtd_geral} mecânicos):** {qtd_geral} x R$ {custo_geral_indiv:,.2f} = **R$ {c_dir_geral_total:,.2f}/mês**.
        * **Por que calcular assim?** Permite à oficina avaliar com precisão o impacto de admitir ou demitir um profissional sem distorcer o custo fixo da estrutura.
        """)

    with st.expander("2️⃣ Horas Faturáveis vs. Horas Contratadas (Eficiência Operacional)"):
        st.write(f"""
        * **Horas Contratadas ({qtd_geral} mecânicos):** {qtd_geral} x {horas_geral}h = **{h_cont_geral} horas/mês**.
        * **Eficiência ({efic_geral*100:.0f}%):** Nenhum profissional produz 100% do tempo. Parte da jornada é consumida com deslocamento do veículo, organização de ferramentas, reuniões, testes de rodagem e atrasos na entrega de peças.
        * **Capacidade Real Vendível:** {h_cont_geral}h x {efic_geral*100:.0f}% = **{h_fat_geral:.1f} horas faturáveis/mês**.
        """)

    with st.expander("3️⃣ A Diluição Mágica do Custo Fixo"):
        st.write(f"""
        * **Custo Fixo Total da Oficina:** R$ {custos_fixos:,.2f}/mês (Aluguel, Luz, Recepção, Contabilidade, etc.).
        * **Capacidade Total da Oficina:** {h_fat_geral:.1f}h (Geral) + {h_fat_esp:.1f}h (Diagnóstico) = **{h_fat_total:.1f} horas faturáveis**.
        * **Rateio de Custo Fixo por Hora:** R$ {custos_fixos:,.2f} / {h_fat_total:.1f}h = **R$ {rateio_fixo_h:.2f} por cada hora vendida**.
        > **Aviso Importante:** Quanto mais mecânicos produzindo na oficina, mais horas faturáveis existem para dividir o mesmo aluguel. Por isso, aumentar a equipe **BARATEIA** o custo fixo de cada hora técnica individual!
        """)

    with st.expander("4️⃣ A Fórmula do Markup (Margem de Lucro e Impostos)"):
        st.write(f"""
        O Preço Final (VHT) não é calculated apenas somando a porcentagem ao custo. Ele utiliza o **Divisor de Markup** para garantir que a margem e os impostos incidam sobre o **faturamento bruto final**:
        
        $$\\text{{VHT}} = \\frac{{\\text{{Custo Base por Hora}}}}{{1 - (\\text{{Impostos \\%}} + \\text{{Margem \\%}})}} = \\frac{{\\text{{R\\$ {c_base_geral:.2f}}}}}{{1 - ({impostos_pct:.2f} + {margem_pct:.2f})}} = \\mathbf{{\\text{{R\\$ {vht_geral:.2f}/h}}}}$$
        """)

# --- ABA 3: ORÇAMENTO COM IMPRESSÃO ---
with tab3:
    st.subheader("📝 Simulador de Orçamento e Emissão de O.S.")
    
    col_inputs, col_preview = st.columns([1, 1])
    
    with col_inputs:
        cliente_nome = st.text_input("Nome do Cliente", value="João da Silva")
        veiculo_nome = st.text_input("Veículo / Placa", value="VW Gol 1.0 - Placa ABC-1234")
        h_basica_os = st.number_input("Horas de Serviço Básico (Mecânica Geral)", value=2.5, step=0.5)
        h_diag_os = st.number_input("Horas de Diagnóstico Eletrônico", value=1.0, step=0.5)
        valor_pecas = st.number_input("Valor Total das Peças (R$)", value=350.0, step=50.0)
        obs_os = st.text_area("Observações Técnicas", value="Troca de correia dentada, tensores e diagnóstico de falha de ignição no cilindro 2.")
    
    total_mo_basica = h_basica_os * vht_geral
    total_mo_diag = h_diag_os * vht_esp
    total_mo_geral = total_mo_basica + total_mo_diag
    total_orcamento = total_mo_geral + valor_pecas
    
    with col_preview:
        st.markdown("### 👁️ Pré-visualização da Ordem de Serviço")
        
        st.markdown(f"""
        <div id="secao-impressao" style="border: 2px solid #0284c7; padding: 20px; border-radius: 8px; background-color: #1e293b; color: #f8fafc;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #0284c7; padding-bottom: 10px;">
                <div>
                    <h2 style="margin:0; color: #38bdf8;">AUTO MECÂNICA REPÚBLICA</h2>
                    <p style="margin:0; font-size: 0.9em; color: #94a3b8;">Apoio Educacional Oficial & Oficina Referência</p>
                </div>
                <div style="text-align: right;">
                    <h4 style="margin:0; color: #38bdf8;">ORÇAMENTO DE SERVIÇOS</h4>
                    <p style="margin:0; font-size: 0.85em; color: #94a3b8;">Tecnologia INFINITUS</p>
                </div>
            </div>
            
            <div style="margin-top: 15px; font-size: 0.95em;">
                <p><strong>Cliente:</strong> {cliente_nome} | <strong>Veículo:</strong> {veiculo_nome}</p>
                <p><strong>Observações:</strong> {obs_os}</p>
            </div>
            
            <hr style="border-color: #334155;">
            
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9em;">
                <thead>
                    <tr style="background-color: #334155; text-align: left; color: #38bdf8;">
                        <th style="padding: 8px;">Descrição do Item</th>
                        <th style="padding: 8px; text-align: center;">Qtd/Horas</th>
                        <th style="padding: 8px; text-align: right;">Valor Unit.</th>
                        <th style="padding: 8px; text-align: right;">Total</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #334155;">Mão de Obra Básica (Mecânica Geral)</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: center;">{h_basica_os:.1f} h</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: right;">R$ {vht_geral:.2f}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: right;">R$ {total_mo_basica:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #334155;">Mão de Obra Especializada (Diagnóstico)</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: center;">{h_diag_os:.1f} h</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: right;">R$ {vht_esp:.2f}</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: right;">R$ {total_mo_diag:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px; border-bottom: 1px solid #334155;">Peças e Componentes Aplicados</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: center;">--</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: right;">--</td>
                        <td style="padding: 8px; border-bottom: 1px solid #334155; text-align: right;">R$ {valor_pecas:.2f}</td>
                    </tr>
                </tbody>
            </table>
            
            <div style="margin-top: 20px; text-align: right; font-size: 1.1em;">
                <p style="margin: 3px 0;"><strong>Subtotal Mão de Obra:</strong> R$ {total_mo_geral:.2f}</p>
                <p style="margin: 3px 0;"><strong>Subtotal Peças:</strong> R$ {valor_pecas:.2f}</p>
                <h3 style="margin: 10px 0 0 0; color: #38bdf8;">TOTAL GERAL: R$ {total_orcamento:.2f}</h3>
            </div>
            
            <div style="margin-top: 25px; border-top: 1px solid #334155; padding-top: 10px; font-size: 0.75em; color: #94a3b8; text-align: center;">
                <p>Plataforma de Cálculo VHT • Propriedade Intelectual INFINITUS SISTEMAS INTELIGENTES • Patrocínio Auto Mecânica República</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        components.html(
            """
            <button onclick="window.print()" style="
                background-color: #0284c7; 
                color: white; 
                padding: 12px 24px; 
                border: none; 
                border-radius: 6px; 
                font-weight: bold; 
                cursor: pointer;
                width: 100%;
                font-size: 16px;
            ">🖨️ Imprimir Orçamento / Salvar em PDF</button>
            """,
            height=60
        )

# --- ABA 4: PARCEIROS ---
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
    "<div style='text-align: center; color: #94a3b8; font-size: 0.85em;'>"
    "<b>INFINITUS SISTEMAS INTELIGENTES</b> © Todos os direitos reservados • "
    "Patrocínio Oficial: <b>Auto Mecânica República</b>"
    "</div>", 
    unsafe_allow_html=True
)
