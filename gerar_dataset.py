"""
Script para geração de dataset realista de agendamentos odontológicos.
Simula regras de negócio, especialidades, impacto financeiro e comportamentos
reais de pacientes (faltas, confirmações, tempo de antecedência e tipo de pagamento).
"""

import random
import pandas as pd
import numpy as np

# Semente para reprodutibilidade dos resultados
np.random.seed(42)
random.seed(42)

N = 1200

# Especialidades e procedimentos típicos de odontologia com duração e valores médios
especialidades_dados = {
    "Ortodontia": {
        "procedimentos": ["Manutenção Ortodôntica"],
        "duracao": [30],
        "valores": [150, 180, 200, 220],
        "peso": 0.28
    },
    "Clínica Geral": {
        "procedimentos": ["Restauração em Resina", "Profilaxia e Raspagem Supragengival", "Avaliação Inicial"],
        "duracao": [30, 45, 60],
        "valores": [100, 160, 220, 280],
        "peso": 0.26
    },
    "Endodontia": {
        "procedimentos": ["Tratamento de Canal (Molar)", "Tratamento de Canal (Pré-Molar/Anterior)", "Retratamento Endodôntico"],
        "duracao": [60, 90, 120],
        "valores": [650, 850, 1100, 1400],
        "peso": 0.16
    },
    "Implantodontia / Cirurgia": {
        "procedimentos": ["Instalação de Implante", "Exodontia de Terceiro Molar (Siso)", "Enxerto Ósseo"],
        "duracao": [60, 90, 120],
        "valores": [450, 900, 1500, 2200],
        "peso": 0.12
    },
    "Odontopediatria": {
        "procedimentos": ["Condicionamento e Profilaxia", "Restauração Decíduo", "Aplicação de Flúor/Selante"],
        "duracao": [30, 45],
        "valores": [140, 190, 250],
        "peso": 0.10
    },
    "Periodontia": {
        "procedimentos": ["Raspagem e Aplainamento Radicular", "Cirurgia Periodontal a Retalho"],
        "duracao": [45, 60],
        "valores": [250, 380, 550],
        "peso": 0.08
    }
}

especialidades = list(especialidades_dados.keys())
pesos_esp = [especialidades_dados[e]["peso"] for e in especialidades]

dias_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado"]
pesos_dias = [0.18, 0.20, 0.20, 0.19, 0.15, 0.08]

periodos = ["Manhã", "Tarde", "Noite"]
pesos_periodos = [0.40, 0.45, 0.15]

registros = []

for i in range(1, N + 1):
    id_agendamento = f"AGD-{1000 + i}"
    id_paciente = f"PAC-{random.randint(100, 550):04d}"  # Alguns pacientes repetem (recorrência)
    
    # Especialidade e procedimento
    esp = np.random.choice(especialidades, p=pesos_esp)
    info_esp = especialidades_dados[esp]
    procedimento = random.choice(info_esp["procedimentos"])
    duracao = random.choice(info_esp["duracao"])
    valor = random.choice(info_esp["valores"])
    
    # Idade baseada na especialidade
    if esp == "Odontopediatria":
        idade = random.randint(3, 12)
    elif esp == "Ortodontia":
        idade = random.randint(12, 38)
    else:
        idade = int(np.clip(np.random.normal(38, 14), 18, 75))
        
    genero = np.random.choice(["Feminino", "Masculino"], p=[0.58, 0.42])
    
    dia = np.random.choice(dias_semana, p=pesos_dias)
    periodo = np.random.choice(periodos, p=pesos_periodos)
    
    # Tipo de pagamento
    tipo_pagamento = np.random.choice(["Particular", "Convênio"], p=[0.55, 0.45])
    
    # Antecedência do agendamento (dias entre marcar e a data da consulta)
    antecedencia = int(np.clip(np.random.exponential(scale=8), 0, 45))
    
    # Histórico de faltas anteriores do paciente (0 a 3+)
    hist_faltas = np.random.choice([0, 1, 2, 3], p=[0.68, 0.20, 0.08, 0.04])
    
    # Confirmação de WhatsApp (quem marca muito antes tende a confirmar menos)
    prob_confirma = 0.88 if antecedencia <= 5 else (0.75 if antecedencia <= 15 else 0.55)
    confirmou_wpp = np.random.choice(["Sim", "Não"], p=[prob_confirma, 1 - prob_confirma])
    
    # CÁLCULO DA PROBABILIDADE DE NO-SHOW (Regras com lógica clínica e de comportamento)
    # Probabilidade base de falta no mercado odontológico: ~15%
    prob_falta = 0.12
    
    # Fator 1: Confirmação por WhatsApp (o mais determinante)
    if confirmou_wpp == "Não":
        prob_falta += 0.35
    else:
        prob_falta -= 0.05
        
    # Fator 2: Dias de antecedência
    if antecedencia > 20:
        prob_falta += 0.15
    elif antecedencia <= 2:
        prob_falta -= 0.04
        
    # Fator 3: Histórico prévio de faltas
    if hist_faltas >= 2:
        prob_falta += 0.22
    elif hist_faltas == 1:
        prob_falta += 0.08
        
    # Fator 4: Tipo de pagamento (convênio tende a faltar mais que particular com sinal)
    if tipo_pagamento == "Convênio":
        prob_falta += 0.08
    else:
        prob_falta -= 0.03
        
    # Fator 5: Procedimentos de alto valor/dor urgente (ex: canal agudo) têm menor falta
    if esp in ["Endodontia", "Implantodontia / Cirurgia"]:
        prob_falta -= 0.06
    elif esp == "Clínica Geral" and procedimento == "Avaliação Inicial":
        prob_falta += 0.10  # Primeira consulta gratuita/avaliação tem alto no-show
        
    # Fator 6: Dias específicos (Sábado e Sexta Noite têm mais desistência)
    if dia == "Sábado" or (dia == "Sexta" and periodo == "Noite"):
        prob_falta += 0.10
        
    # Limitar entre 2% e 90%
    prob_falta = np.clip(prob_falta, 0.02, 0.90)
    
    # Determinar status final
    status = "Faltou" if np.random.rand() < prob_falta else "Compareceu"
    
    registros.append({
        "id_agendamento": id_agendamento,
        "id_paciente": id_paciente,
        "idade": idade,
        "genero": genero,
        "especialidade": esp,
        "procedimento": procedimento,
        "duracao_minutos": duracao,
        "valor_procedimento": valor,
        "tipo_pagamento": tipo_pagamento,
        "dias_antecedencia": antecedencia,
        "dia_semana": dia,
        "periodo": periodo,
        "confirmou_whatsapp": confirmou_wpp,
        "historico_faltas": hist_faltas,
        "status": status
    })

df = pd.DataFrame(registros)
caminho_csv = "projeto_1_noshow/data/agendamentos_odontologia.csv"
df.to_csv(caminho_csv, index=False, encoding="utf-8-sig")

print(f"Dataset gerado com sucesso em: {caminho_csv}")
print(f"Total de registros: {len(df)}")
print(f"Distribuição do status:\n{df['status'].value_counts(normalize=True).round(3) * 100}%")
