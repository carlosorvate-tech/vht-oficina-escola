# 📋 Documento de Auditoria Técnica e Revisão de Arquitetura — v2.0 Didática

**Projeto:** Calculadora de Valor da Hora Técnica (VHT) — Plataforma Educacional & Comercial (v2.0 Didática)  
**Propriedade Intelectual:** INFINITUS SISTEMAS INTELIGENTES  
**Patrocinador Master:** Auto Mecânica República  
**Repositório Remoto:** [https://github.com/carlosorvate-tech/vht-oficina-escola](https://github.com/carlosorvate-tech/vht-oficina-escola)  
**Data da Auditoria:** 13/08/2026  
**Auditor Responsável:** IDE AntiGravity (Agente Autônomo de Codificação e Implantação)

---

## 1. 🎯 Novidades da Versão 2.0 Didática

1. **Disambiguação Clara das Entradas da Barra Lateral:**
   - Adicionada rotulagem explícita informando que o campo `Custo Mensal INDIVIDUAL` exige o custo de **UM ÚNICO MECÂNICO** (Salário + Encargos + Benefícios).
   - O motor de cálculo multiplica automaticamente o valor individual pela quantidade de profissionais.

2. **Aba 2: Guia Didático de Formação do Custo:**
   - Explicitação matemática interativa via `st.expander` detalhando:
     - Diferença entre custo individual e custo total da equipe.
     - Horas contratadas vs. horas faturáveis com fator de eficiência.
     - Diluição progressiva dos custos fixos à medida que a equipe aumenta.
     - A fórmula do Markup (Divisor) com expressões LaTeX renderizadas.

3. **Aba 3: Emissor de Orçamentos com Impressão Estilizada:**
   - Inclusão de regras CSS de mídia `@media print` ocultando a interface do Streamlit ao imprimir.
   - Pré-visualização formatada em cartão de Orçamento de Serviço com marcas institucionais.
   - Botão em JavaScript acionando `window.print()` nativo do navegador para salvar em PDF ou imprimir.

---

## 2. 📜 Rastreabilidade dos Commits no GitHub

| Commit Hash | Autor | Mensagem do Commit | Estado |
| :--- | :--- | :--- | :---: |
| `4a35793` | carlosorvate-tech | `feat: implantacao autônoma vht calculator - infinitus / republica` | 🟢 PUSHED |
| `e76c245` | carlosorvate-tech | `feat: add Windows one-click launcher script run_app.bat` | 🟢 PUSHED |
| `7f960df` | carlosorvate-tech | `docs: add AUDIT_REVIEW.md technical audit and architecture report` | 🟢 PUSHED |
| `5a725db` | carlosorvate-tech | `feat: add streamlit_app.py entrypoint alias for Streamlit Community Cloud default path` | 🟢 PUSHED |
| `707bc02` | carlosorvate-tech | `feat: v2.0 didatica com impressao de orcamento e entradas explicativas` | 🟢 PUSHED |

---

> **Certificação de Validação v2.0:** Código compilado sem avisos ou erros de sintaxe, testado localmente e sincronizado no GitHub.
