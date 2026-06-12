# Metodologia

## Dados

O dataset sintetico simula fatores associados a readmissao em ate 30 dias, incluindo idade, comorbidades, historico de utilizacao, tempo de permanencia, volume de medicamentos, exames, diagnostico principal e agendamento de follow-up.

## Pre-processamento

- Numericos: imputacao por mediana e padronizacao.
- Categoricos: imputacao por moda e one-hot encoding.
- Booleanos: imputacao por moda.

## Engenharia de Atributos

- `medications_per_day`: complexidade terapeutica relativa ao tempo de internacao.
- `high_utilization`: proxy de uso frequente ou internacao prolongada.
- `complex_chronic_condition`: combinacao de CKD, diabetes e hipertensao.

## Modelos

Sao comparados:

- Logistic Regression;
- Random Forest;
- Gradient Boosting.

A selecao usa recall como criterio principal e ROC-AUC como desempate. Em readmissao, falsos negativos podem atrasar intervencoes pos-alta; por isso, recall e uma metrica clinicamente relevante.

O artefato final inclui metadados de treinamento, taxa positiva, regra de selecao, metricas do melhor modelo, versao e hash SHA-256 para rastreabilidade.

## Validacao

O dataset e dividido com `train_test_split` estratificado. A avaliacao inclui accuracy, precision, recall, F1-score, ROC-AUC, matriz de confusao, curva ROC e Precision-Recall.

## Explicabilidade

O projeto inclui suporte documental para SHAP e relatorios de importancia. Em uso real, a explicabilidade deve ser analisada com especialistas clinicos para evitar conclusoes causais indevidas.

## Threshold

O threshold padrao e `0.50`, configuravel por variavel de ambiente. Em ambiente real, ele deveria ser ajustado conforme capacidade operacional, custo de falso negativo, volume de alertas e validacao clinica.
