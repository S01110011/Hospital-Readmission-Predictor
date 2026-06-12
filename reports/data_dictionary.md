# Dicionario de Dados

| Campo | Tipo | Descricao |
|---|---|---|
| age | inteiro | Idade do paciente, 18 a 105 anos. |
| gender | categoria | `female`, `male` ou `other`. |
| length_of_stay | inteiro | Dias de internacao. |
| num_prior_admissions | inteiro | Internacoes previas recentes simuladas. |
| num_medications | inteiro | Quantidade de medicamentos. |
| num_lab_procedures | inteiro | Quantidade de exames laboratoriais. |
| comorbidity_score | inteiro | Escore sintetico de comorbidades. |
| discharge_disposition | categoria | Destino de alta. |
| primary_diagnosis | categoria | Diagnostico principal agrupado. |
| has_diabetes | booleano | Indicador de diabetes. |
| has_hypertension | booleano | Indicador de hipertensao. |
| has_ckd | booleano | Indicador de doenca renal cronica. |
| follow_up_scheduled | booleano | Consulta/contato pos-alta agendado. |
| readmitted_30_days | binario | Variavel alvo: readmissao em ate 30 dias. |
| medications_per_day | float | Medicamentos por dia de internacao. |
| high_utilization | booleano | Internacao longa ou uso hospitalar recorrente. |
| complex_chronic_condition | booleano | CKD, diabetes e hipertensao simultaneos. |
