# Deployment

## Local

```bash
python scripts/generate_sample_data.py
python -m src.models.train
uvicorn src.api.main:app --reload
```

Verificacoes:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/ready
curl http://127.0.0.1:8000/model-info
```

## Docker

```bash
docker compose up --build
```

## Producao

Recomendacoes para transformar em servico real:

- executar atras de API gateway;
- habilitar HTTPS;
- configurar autenticacao;
- usar registry de modelos;
- armazenar logs e metricas em stack observavel;
- monitorar drift de dados e performance;
- criar pipeline CI/CD com testes e scanning de dependencias;
- separar ambiente de treinamento e inferencia;
- aprovar uso com governanca clinica e juridica.
- publicar artefatos em model registry com hash, aprovador e rollback.

## Variaveis de Ambiente

Consulte `.env.example`. Em producao, use secret manager e nunca commit de `.env`.

## CI

O workflow `.github/workflows/ci.yml` instala dependencias, gera dados sinteticos, treina o modelo e executa os testes. Isso garante que o repositorio continue reproduzivel para avaliadores no GitHub.
