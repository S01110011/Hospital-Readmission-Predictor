# Model Card

## Modelo

Hospital Readmission Predictor, versao local.

## Uso Pretendido

Estimar risco de readmissao hospitalar em 30 dias para demonstracao de ciencia de dados em saude. Pode apoiar priorizacao de follow-up em um cenario simulado.

## Uso Nao Pretendido

- Diagnostico clinico.
- Decisao automatizada sem revisao humana.
- Substituicao de protocolos assistenciais.
- Uso regulado sem validacao clinica.

## Dados

Dados sinteticos gerados por regras probabilisticas. Nao contem PHI ou dados pessoais reais.

## Metricas

O pipeline calcula accuracy, precision, recall, F1-score, ROC-AUC e matriz de confusao. Recall e priorizado por reduzir falsos negativos em pacientes sob risco de readmissao.

## Rastreabilidade

Cada treino salva `model_summary.json` com timestamp UTC, tamanho do dataset, taxa positiva, regra de selecao, features e hash SHA-256 do artefato `model.joblib`.

## Riscos

- Baixa validade externa por dados sinteticos.
- Possivel vies se adaptado para dados reais sem auditoria.
- Interpretacao indevida de correlacoes como causalidade.

## Mitigacoes

- Disclaimer clinico.
- Validacao de entrada.
- Documentacao de privacidade.
- Recomendacao de monitoramento, calibracao e validacao prospectiva.
- Endpoint `/model-info` para revisao operacional de metadados nao sensiveis.
