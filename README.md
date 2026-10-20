# 🦷 Case de Negócios: Análise de No-Show e Otimização de Cadeira em Clínica Odontológica

> **Stack:** Python 3 (`pandas`, `numpy`, `matplotlib`, `seaborn`)  
> **Tema:** Otimização de Produtividade Clínica, Redução de Absenteísmo e Impacto Financeiro  
> **Autor:** Transição Odontologia ➔ Análise de Dados em Saúde

---

## 📌 1. O Problema de Negócio

Na rotina odontológica, a **cadeira vazia é o maior gerador de custo ocioso**. Diferente de um comércio que pode estocar produtos, **a hora clínica não utilizada não se recupera**.

Quando um paciente falta sem aviso prévio (*no-show*):
1. O custo fixo do consultório (aluguel, equipe auxiliar, energia, depreciação) continua correndo.
2. O dentista e a ASB/TSB ficam com tempo ocioso improdutivo.
3. Outro paciente com dor ou necessidade de urgência deixa de ser atendido.

### Objetivo do Projeto
Analisar uma base de **1.200 agendamentos** para:
- Mapear a **taxa global de faltas (*no-show*)** e quantificar o **prejuízo financeiro direto**.
- Identificar os principais **fatores de risco de falta** (antecedência, especialidade, confirmação por WhatsApp, histórico).
- Propor um **plano de ação orientado a dados** para recuperar faturamento e horas clínicas perdidas.

---

## 📊 2. Principais Indicadores Encontrados (KPIs)

* **Volume Analisado:** 1.200 consultas agendadas.
* **Taxa Geral de No-Show:** **21,5%** (258 consultas perdidas).
* **Prejuízo Financeiro Bruto:** **R$ 104.610,00** em procedimentos não realizados.
* **Horas Clínicas Desperdiçadas:** **217,8 horas** de cadeira ociosa.
* **Ticket Médio da Falta:** **R$ 405,47**.

---

## 🔍 3. Principais Descobertas Clínicas & Comportamentais

### 1. O Efeito Crítico da Confirmação por WhatsApp
* Pacientes que **confirmaram via WhatsApp**: apenas **12,8%** de falta.
* Pacientes que **NÃO confirmaram**: taxa de falta salta para **58,0%** (mais de 4,5x maior).
* **Insight:** Das 258 faltas, mais da metade (134) estavam no grupo de não confirmados, representando **R$ 60.320,00** do prejuízo total.

### 2. O Paradoxo da Endodontia e Cirurgia (Volume vs. Impacto Financeiro)
* Em **porcentagem**, Clínica Geral (26,6%) e Ortodontia (24,0%) têm mais faltas.
* Porém, em **impacto financeiro em Reais**, **Endodontia** lidera as perdas com **R$ 33.050,00** perdidos, seguida por **Implantodontia / Cirurgia** com **R$ 27.900,00**.
* **Explicação Clínica:** Procedimentos de Endodontia e Implante ocupam blocos longos de agenda (60 a 120 minutos) e possuem alto valor agregado. Uma única falta de canal molar custa o equivalente a 6 manutenções ortodônticas.

### 3. A Curva de Antecedência do Agendamento
* Consultas agendadas com **até 3 dias de antecedência**: apenas **15,1%** de no-show.
* Consultas agendadas com **mais de 15 dias de antecedência**: **31,6%** de no-show.
* **Insight:** Quanto mais distante a data marcada, maior o esquecimento e o descompromisso do paciente.

---

## 📈 4. Visualizações Geradas

Os gráficos gerados pela análise encontram-se na pasta [`graficos/`](graficos/):

1. **`01_noshow_por_especialidade.png`**: Ranking percentual de faltas comparado com a média geral da clínica.
2. **`02_antecedencia_e_whatsapp.png`**: Comparativo cruzado demonstrando como a confirmação reduz o absenteísmo mesmo em agendamentos de longo prazo.
3. **`03_perda_financeira_por_especialidade.png`**: Demonstração de que o maior prejuízo financeiro vem de especialidades de alto ticket (Endodontia e Cirurgia).

---

## 💡 5. Plano de Ação Estratégico & Simulação Financeira

Com base nos dados, desenhamos 3 intervenções práticas para a equipe de recepção e gestão:

1. **Régua de Confirmação Automatizada 48h / 24h:**
   - Agendamentos com mais de 7 dias recebem disparo automático via WhatsApp 48 horas antes.
   - Em caso de ausência de confirmação até 24 horas antes, o horário é liberado para lista de espera ou encaixe ativo.
2. **Política de Pré-pagamento / Sinal para Procedimentos Longos:**
   - Para sessões de Endodontia, Cirurgia e Prótese (> R$ 500 ou > 60 min), instituir sinal de 20% a 30% na reserva do horário.
3. **Gestão de Recidivistas:**
   - Pacientes com histórico de $\ge 2$ faltas só podem agendar em horários de menor demanda (meio da tarde) ou com encaixe no próprio dia.

### 💰 Retorno Estimado (ROI da Decisão)
* Reduzindo pela metade o absenteísmo do grupo que não confirma WhatsApp, a clínica recupera **R$ 30.160,00** e preserva aproximadamente **58 horas clínicas úteis**.

---

## 🚀 6. Como Executar Este Projeto

### Pré-requisitos
Ter o Python 3 instalado com as bibliotecas:
```bash
py -m pip install pandas numpy matplotlib seaborn
```

### Passo a passo
1. Clonar este repositório ou abrir na pasta do projeto:
```bash
cd projeto_1_noshow
```

2. Gerar o dataset de agendamentos:
```bash
py gerar_dataset.py
```

3. Rodar a análise completa e gerar os gráficos:
```bash
py analise_noshow.py
```
Os relatórios e números serão exibidos no terminal e os gráficos salvos automaticamente em `graficos/`.
