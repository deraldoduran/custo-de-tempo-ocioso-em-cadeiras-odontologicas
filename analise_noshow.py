"""
PROJETO 1: ANÁLISE DE NO-SHOW E IMPACTO FINANCEIRO EM CLÍNICA ODONTOLÓGICA
Autor: Transição Odontologia -> Análise de Dados
Descrição: Análise de 1.200 agendamentos para mapear fatores determinantes
de faltas (no-show), quantificar o prejuízo financeiro em horas de cadeira
e sugerir um plano de ação orientado a dados.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuração estética dos gráficos
sns.set_theme(style="whitegrid")
plt.rcParams.update({
    "font.size": 11,
    "figure.titlesize": 14,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10
})

os.makedirs("projeto_1_noshow/graficos", exist_ok=True)

# ==============================================================================
# PASSO 1: CARGA E INSPEÇÃO DOS DADOS
# ==============================================================================
print("=" * 70)
print("ETAPA 1: CARREGANDO E EXPLORANDO OS DADOS DA CLÍNICA")
print("=" * 70)

df = pd.read_csv("projeto_1_noshow/data/agendamentos_odontologia.csv")

print(f"Total de agendamentos no período: {len(df)}")
print(f"Colunas disponíveis: {list(df.columns)}")
print("\nPrimeiras 3 linhas do dataset:")
print(df.head(3))

# Criando variável binária: 1 se Faltou, 0 se Compareceu
df["is_noshow"] = (df["status"] == "Faltou").astype(int)

# Faixas de dias de antecedência para facilitar a análise de negócio
df["faixa_antecedencia"] = pd.cut(
    df["dias_antecedencia"],
    bins=[-1, 3, 7, 14, 100],
    labels=["Até 3 dias (Imediato)", "4 a 7 dias (Semana)", "8 a 14 dias (2 semanas)", "15+ dias (Longo prazo)"]
)

# ==============================================================================
# PASSO 2: KPIs GLOBAIS DE NEGÓCIO E PERDA FINANCEIRA
# ==============================================================================
print("\n" + "=" * 70)
print("ETAPA 2: PRINCIPAIS INDICADORES EXECUTIVOS (KPIs)")
print("=" * 70)

total_agendamentos = len(df)
total_faltas = df["is_noshow"].sum()
taxa_noshow_geral = df["is_noshow"].mean() * 100

# Cálculo do prejuízo financeiro
df_faltas = df[df["status"] == "Faltou"]
prejuizo_total = df_faltas["valor_procedimento"].sum()
horas_ociosas_total = df_faltas["duracao_minutos"].sum() / 60
ticket_medio_falta = df_faltas["valor_procedimento"].mean()

print(f"• Taxa Geral de No-Show: {taxa_noshow_geral:.1f}% ({total_faltas} de {total_agendamentos} consultas)")
print(f"• Prejuízo Financeiro Bruto: R$ {prejuizo_total:,.2f}")
print(f"• Total de Horas Clínicas Ociosas: {horas_ociosas_total:.1f} horas de consultório")
print(f"• Ticket Médio por Falta: R$ {ticket_medio_falta:,.2f}")

# ==============================================================================
# PASSO 3: ANÁLISE DETALHADA POR FATORES DETERMINANTES
# ==============================================================================
print("\n" + "=" * 70)
print("ETAPA 3: FATORES DETERMINANTES DE FALTAS")
print("=" * 70)

# 3.1 Impacto do WhatsApp
print("\n--- 3.1 IMPACTO DA CONFIRMAÇÃO POR WHATSAPP ---")
wpp_stats = df.groupby("confirmou_whatsapp").agg(
    total=("id_agendamento", "count"),
    faltas=("is_noshow", "sum"),
    taxa_noshow=("is_noshow", lambda x: x.mean() * 100),
    prejuizo=("valor_procedimento", lambda x: x[df.loc[x.index, "status"] == "Faltou"].sum())
).reset_index()
print(wpp_stats.to_string(index=False))

# 3.2 Taxa por Especialidade
print("\n--- 3.2 TAXA DE NO-SHOW E PREJUÍZO POR ESPECIALIDADE ---")
esp_stats = df.groupby("especialidade").agg(
    total=("id_agendamento", "count"),
    faltas=("is_noshow", "sum"),
    taxa_noshow=("is_noshow", lambda x: x.mean() * 100),
    prejuizo_total=("valor_procedimento", lambda x: x[df.loc[x.index, "status"] == "Faltou"].sum())
).sort_values(by="prejuizo_total", ascending=False).reset_index()
esp_stats["prejuizo_total"] = esp_stats["prejuizo_total"].apply(lambda v: f"R$ {v:,.2f}")
print(esp_stats.to_string(index=False))

# 3.3 Antecedência do Agendamento
print("\n--- 3.3 TAXA DE NO-SHOW POR TEMPO DE ANTECEDÊNCIA ---")
ant_stats = df.groupby("faixa_antecedencia", observed=False).agg(
    total=("id_agendamento", "count"),
    taxa_noshow=("is_noshow", lambda x: x.mean() * 100)
).reset_index()
print(ant_stats.to_string(index=False))

# 3.4 Histórico de Faltas do Paciente
print("\n--- 3.4 HISTÓRICO PRÉVIO DE FALTAS ---")
hist_stats = df.groupby("historico_faltas").agg(
    total=("id_agendamento", "count"),
    taxa_noshow=("is_noshow", lambda x: x.mean() * 100)
).reset_index()
print(hist_stats.to_string(index=False))

# ==============================================================================
# PASSO 4: GERAÇÃO DE VISUALIZAÇÕES PROFISSIONAIS
# ==============================================================================
print("\n" + "=" * 70)
print("ETAPA 4: GERANDO GRÁFICOS PARA O PORTFÓLIO...")
print("=" * 70)

# Gráfico 1: No-Show por Especialidade
plt.figure(figsize=(10, 5))
ordem_esp = df.groupby("especialidade")["is_noshow"].mean().sort_values(ascending=False).index
taxas_esp = df.groupby("especialidade")["is_noshow"].mean().sort_values(ascending=False) * 100

ax1 = sns.barplot(
    x=taxas_esp.values,
    y=ordem_esp,
    hue=ordem_esp,
    palette="Blues_r",
    legend=False
)
plt.axvline(x=taxa_noshow_geral, color="red", linestyle="--", label=f"Média Geral ({taxa_noshow_geral:.1f}%)")
plt.title("Taxa de No-Show (%) por Especialidade Odontológica", pad=15, fontweight="bold")
plt.xlabel("Taxa de Falta (%)")
plt.ylabel("Especialidade")
plt.legend(loc="lower right")

for i, v in enumerate(taxas_esp.values):
    ax1.text(v + 0.6, i, f"{v:.1f}%", va="center", fontweight="semibold")

plt.tight_layout()
plt.savefig("projeto_1_noshow/graficos/01_noshow_por_especialidade.png", dpi=300)
plt.close()
print("[OK] Grafico salvo: 01_noshow_por_especialidade.png")

# Gráfico 2: Antecedência cruzada com WhatsApp
plt.figure(figsize=(11, 5))
pivot_wpp_ant = df.groupby(["faixa_antecedencia", "confirmou_whatsapp"], observed=False)["is_noshow"].mean().unstack() * 100

pivot_wpp_ant.plot(kind="bar", figsize=(10, 5), color=["#d9534f", "#5cb85c"], width=0.7)
plt.title("Efeito da Confirmação por WhatsApp x Tempo de Antecedência no No-Show", pad=15, fontweight="bold")
plt.xlabel("Tempo de Antecedência do Agendamento")
plt.ylabel("Taxa de No-Show (%)")
plt.xticks(rotation=0)
plt.legend(title="Confirmou WhatsApp?", loc="upper left")
plt.tight_layout()
plt.savefig("projeto_1_noshow/graficos/02_antecedencia_e_whatsapp.png", dpi=300)
plt.close()
print("[OK] Grafico salvo: 02_antecedencia_e_whatsapp.png")

# Gráfico 3: Prejuízo Financeiro Acumulado por Especialidade
plt.figure(figsize=(10, 5))
prejuizo_esp = df_faltas.groupby("especialidade")["valor_procedimento"].sum().sort_values(ascending=False)

ax3 = sns.barplot(
    x=prejuizo_esp.values,
    y=prejuizo_esp.index,
    hue=prejuizo_esp.index,
    palette="Reds_r",
    legend=False
)
plt.title("Prejuízo Financeiro Acumulado por Falta (R$) por Especialidade", pad=15, fontweight="bold")
plt.xlabel("Valor Total Perdido em Consultório (R$)")
plt.ylabel("Especialidade")

for i, v in enumerate(prejuizo_esp.values):
    ax3.text(v + 800, i, f"R$ {v:,.0f}", va="center", fontweight="semibold")

plt.tight_layout()
plt.savefig("projeto_1_noshow/graficos/03_perda_financeira_por_especialidade.png", dpi=300)
plt.close()
print("[OK] Grafico salvo: 03_perda_financeira_por_especialidade.png")

# ==============================================================================
# PASSO 5: SIMULAÇÃO DE IMPACTO DE UMA POLÍTICA DE GESTÃO (BUSINESS CASE)
# ==============================================================================
print("\n" + "=" * 70)
print("ETAPA 5: SIMULAÇÃO FINANCEIRA DE PLANO DE AÇÃO")
print("=" * 70)

# Cenário de intervenção:
# 1. Implementar confirmação ativa por WhatsApp 48h e 24h antes para todos os agendamentos > 7 dias.
# 2. Se a taxa de no-show dos não confirmados cair pela metade (de ~50% para ~25%), quanto a clínica recupera?
faltas_sem_wpp = df[(df["confirmou_whatsapp"] == "Não") & (df["status"] == "Faltou")]
prejuizo_sem_wpp = faltas_sem_wpp["valor_procedimento"].sum()
potencial_recuperacao_50pct = prejuizo_sem_wpp * 0.50

print(f"• Prejuízo atual concentrado no grupo SEM confirmação de WhatsApp: R$ {prejuizo_sem_wpp:,.2f}")
print(f"• Recuperação estimada com automação de confirmação e reencaixe ativo: R$ {potencial_recuperacao_50pct:,.2f}")
print(f"• Horas clínicas salvas por mês: ~{(faltas_sem_wpp['duracao_minutos'].sum() * 0.5) / 60:.0f} horas")

print("\n" + "=" * 70)
print("ANÁLISE CONCLUÍDA COM SUCESSO!")
print("Arquivos prontos para o seu portfólio no GitHub!")
print("=" * 70)
