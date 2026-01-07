# API REST - Gestao de Tarefas

Objetivo: API de gerenciamento de tarefas com autenticação JWT, preparada para avaliação técnica.
Stack: Django 6, Django REST Framework, SimpleJWT, PostgreSQL (obrigatório), decouple, drf-spectacular.

## 1) Requisitos
1. Python 3.14
2. Virtualenv ativa (`.venv`)
3. PostgreSQL (DB local ou remoto)

## 2) Configurar variaveis
1. Copie `env.example` para `.env`
2. Preencha: `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `ALLOWED_HOSTS`
3. Para producao, crie um `.env` (ou `.env.production` local) a partir do `env.example`, ajustando DEBUG=False, ativando HTTPS/HSTS e preenchendo apenas nos ambientes de deploy
4. Nunca comite credenciais reais; mantenha `.env*` fora do versionamento e entregue os valores sensíveis por canal seguro

## 3) Instalar dependencias
1. `python -m pip install -r requirements.txt`

## 4) Banco e migracoes
1. `python manage.py migrate`

## 5) Criar superusuario
1. `python manage.py createsuperuser`

## 6) Rodar servidor
1. `python manage.py runserver`
2. API: `http://localhost:8000`
3. Swagger: `http://localhost:8000/api/docs/`
4. Admin: `http://localhost:8000/admin/`

## 7) Testes
1. `python manage.py test`

## 8) Paginacao
1. Padrao DRF `PageNumberPagination`
2. `PAGE_SIZE=50`

## 9) Produção (ajuste antes de subir)
1. `DEBUG=False`
2. `ALLOWED_HOSTS` com dominio ou IP publico
3. HTTPS ativo: `SECURE_SSL_REDIRECT=True`, `SESSION_COOKIE_SECURE=True`, `CSRF_COOKIE_SECURE=True`, `SECURE_HSTS_SECONDS>0` (HSTS inclui subdomínios/preload quando o tempo for maior que 0)
4. Tokens JWT: access 1h, refresh 7d, rotacao com blacklist

## 10) Notas rapidas
1. Pin `setuptools<81` evita warning do `simplejwt`; remova quando o pacote abandonar `pkg_resources`
2. Banco: somente PostgreSQL (configure `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`)
3. Endpoints principais: `/auth/register/`, `/auth/login/`, `/tasks/`
