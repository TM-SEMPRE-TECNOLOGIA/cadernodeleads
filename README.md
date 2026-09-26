# Telegram Affiliate Bot

Este é um bot do Telegram feito em Python para interceptar links de produtos (ex: Amazon, Shopee) e gerar automaticamente o seu próprio link de afiliado. Ideal para quem deseja ganhar comissão com auto-compras ou facilitar a distribuição de links.

## 🚀 Como Executar Localmente

### 1. Pré-requisitos
- Ter o [Python 3.9+](https://www.python.org/downloads/) instalado.
- Ter uma conta no Telegram.

### 2. Instalar as Dependências
Abra o terminal na pasta do projeto e rode o comando:
```bash
pip install -r requirements.txt
```

### 3. Configurar as Variáveis de Ambiente
Crie um arquivo chamado `.env` na raiz do projeto (mesmo local de `bot.py`). O conteúdo deve seguir o padrão:
```env
TELEGRAM_BOT_TOKEN=seu_token_aqui
AMAZON_AFFILIATE_TAG=seu_codigo_amazon-20
SHOPEE_APP_ID=seu_shopee_app_id
SHOPEE_APP_SECRET=seu_shopee_app_secret
```

#### Onde conseguir essas credenciais?
*   **TELEGRAM_BOT_TOKEN:** No Telegram, procure o usuário `@BotFather`. Digite `/newbot`, siga os passos para dar um nome ao seu bot e, no final, ele te dará o Token de Acesso da API HTTP.
*   **AMAZON_AFFILIATE_TAG:** No painel do Amazon Associados, é o seu "ID de rastreamento" (ex: `seu-nome-20`).
*   **SHOPEE_APP_ID / SECRET:** Requer aprovação na plataforma Shopee Open API para afiliados. 

### 4. Rodar o Bot
Execute o comando abaixo:
```bash
python bot.py
```
Se tudo der certo, você verá a mensagem `Iniciando o bot...`. Agora, vá no Telegram, procure pelo seu bot e mande um link da Amazon para ele testar!

## 📦 Hospedagem / Deploy
Para deixar o bot rodando 24 horas por dia (sem precisar deixar seu computador ligado), você pode hospedar este código gratuitamente (ou com custos muito baixos) em plataformas como:
*   [Railway.app](https://railway.app/)
*   [Render.com](https://render.com/)
*   [Heroku](https://heroku.com/)

Basta conectar o seu repositório do GitHub nessas plataformas e configurar as Variáveis de Ambiente lá nos painéis de controle delas.
