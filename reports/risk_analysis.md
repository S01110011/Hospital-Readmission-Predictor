# Analise de Riscos

## Riscos Clinicos

- Falso negativo: paciente em risco classificado como baixo risco.
- Falso positivo: paciente sem readmissao provavel recebe alerta desnecessario.
- Overreliance: equipe confiar demais no modelo.

## Riscos Tecnicos

- Drift de dados.
- Mudanca de protocolo hospitalar.
- Dados faltantes ou categorias novas.
- Modelo treinado em dados nao representativos.

## Riscos de Privacidade

- Reidentificacao por combinacao de atributos.
- Exposicao de dados em logs.
- Vazamento de arquivos CSV ou notebooks.

## Controles Recomendados

- Validacao periodica.
- Monitoramento por subgrupo.
- Threshold definido com equipe clinica.
- Revisao humana obrigatoria.
- Auditoria de acesso.
- Criptografia e mascaramento de logs.
