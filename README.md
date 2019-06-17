# Eventex

Sistema de eventos da Morena.

## Como desenvolver?

1. clone o repositório
2. crie um virtualenv
3. ative o virtualenv
4. instale as dependências
5. configure a instância com `.env`
6. execute os testes

```bash
git clone git@github.com:amenezes/wttd
cd wttd
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```

## Como fazer o deploy?

