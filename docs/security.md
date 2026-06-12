# Seguranca, Privacidade e Governanca

## Principios

- Minimizar dados coletados.
- Nao versionar dados sensiveis.
- Separar configuracoes e segredos por variaveis de ambiente.
- Validar todas as entradas externas.
- Registrar eventos operacionais sem expor informacoes pessoais.
- Usar o modelo somente como apoio a decisao clinica.
- Publicar apenas metadados nao sensiveis sobre modelos.

## LGPD

Em um caso real, dados de saude sao dados pessoais sensiveis. O tratamento exigiria base legal adequada, finalidade explicita, necessidade, transparencia, controles de acesso, retencao definida e governanca. Tambem seriam recomendados relatorio de impacto, avaliacao de risco e registro das operacoes de tratamento.

## HIPAA

Para ambientes sujeitos a HIPAA, o sistema deveria proteger PHI com controles administrativos, fisicos e tecnicos. Exemplos: criptografia em transito e repouso, auditoria, controle de acesso por minimo privilegio, Business Associate Agreements quando aplicavel e politicas de resposta a incidentes.

## Anonimizacao e Minimizacao

Este repositorio usa dados sinteticos, sem identificadores diretos. Em dados reais:

- remover identificadores diretos;
- generalizar datas e localidades quando possivel;
- aplicar pseudonimizacao com chaves protegidas;
- evitar colunas sem valor analitico claro;
- controlar reidentificacao por combinacoes raras.

## Segredos

Credenciais nunca devem ser colocadas em codigo, notebooks ou CSV. Use `.env` local e secret manager em producao. O arquivo `.env.example` mostra apenas nomes de variaveis, sem valores sensiveis.

## API

A API usa Pydantic para validar ranges e categorias. Em producao, acrescente:

- autenticacao e autorizacao;
- rate limiting;
- HTTPS obrigatorio;
- logs estruturados com mascaramento;
- monitoramento de erros;
- WAF ou gateway de API.

Controles ja presentes neste repositorio:

- CORS desabilitado por padrao quando nenhuma origem e configurada.
- Cabecalhos `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy` e `Cache-Control`.
- Endpoint `/ready` para readiness sem executar predicoes falsas.
- Endpoint `/model-info` com hash SHA-256 do artefato e metadados de treino.
- Imagem Docker executando com usuario nao-root.

## Disclaimer Clinico

O modelo e somente uma ferramenta de apoio. Ele nao diagnostica, nao prescreve condutas e nao substitui profissionais de saude, protocolos institucionais ou avaliacao individual do paciente.
