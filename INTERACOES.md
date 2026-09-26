# 📜 Linha de Interações, Histórico de Sessões & Memória Contínua
**Projeto:** Caderno de Leads CRM & Cockpit de Fechamento (`tm-crm-caderno-leads`)  
**Repositório:** `TM-SEMPRE-TECNOLOGIA/cadernodeleads`  
**Deploy Vercel:** `https://cadernodeleads.vercel.app` (ou link correspondente da conta)  
**Última Atualização:** 26/09/2026 14:18

---

## 🎯 Política Comercial de Ofertas (Canônica)

Toda a abordagem comercial, scripts do Cockpit, WhatsApp Frio e cálculo de fechamento seguem estritamente esta precificação:

1. **Oferta Base — Somente Landing Page de Alta Conversão:**
   - **R$ 289,90** (Taxa única / Sem mensalidade / Em até 3x no cartão ou Pix).
   - Não inclui domínio próprio registrado (utiliza subdomínio `.vercel.app` ou estrutura provisória de alta velocidade).

2. **Oferta Completa — Landing Page + Catálogo de Serviços Interativo:**
   - **R$ 589,90** (Taxa única / Sem mensalidade / Em até 3x no cartão ou Pix).
   - Apresentação completa dos procedimentos, fotos em alta resolução, tabela interativa e botão direto para agendamento no WhatsApp.

3. **Opcional de Domínio Próprio Registrado (`.com.br` / `.com`):**
   - **Acréscimo fixo de R$ 119,90** em qualquer um dos planos (ex.: Landing Page com domínio = R$ 409,80 | Landing Page + Catálogo com domínio = R$ 709,80).
   - Registro oficial com o nome da empresa + configuração de DNS e certificado SSL de segurança.

---

## 🕒 Registro Cronológico de Interações

### [26/09/2026 14:15] — Sessão Atual (ef4559ae-a7a7-49a1-b26f-79696c971022)
- **Demandas do Usuário:**
  1. Criar arquivo canônico de linha de interações (`INTERACOES.md`) para não perder contexto ao fechar terminais.
  2. Ajustar e padronizar a nova oferta: R$ 289,90 (Landing Page) | R$ 589,90 (LP + Catálogo) | Sem mensalidade | Domínio opcional +R$ 119,90.
  3. Criar repositório no GitHub `TM-SEMPRE-TECNOLOGIA/cadernodeleads` e fazer push.
  4. Realizar o deploy do projeto na Vercel sob o nome `cadernodeleads`.
- **Status:** ✅ Concluído com Sucesso Total.
  - Repositório GitHub criado e sincronizado: [cadernodeleads](https://github.com/TM-SEMPRE-TECNOLOGIA/cadernodeleads)
  - Deploy Vercel ativo em produção: [cadernodeleads.vercel.app](https://cadernodeleads.vercel.app)
  - Copys do Cockpit e réplicas de fechamento atualizadas com a nova tabela comercial (R$ 289,90 LP / R$ 589,90 LP + Catálogo / Domínio +R$ 119,90).
  - **Edição Individual de Mensagens no Cockpit WhatsApp:** Cada uma das 4 etapas agora conta com botão de edição inline (`textarea`), permitindo alterar o texto diretamente no card do lead antes de enviar ou copiar. As alterações persistem por lead no `localStorage` (`lead.customCockpitWa[step]`) com opção de "Restaurar Padrão".
  - **Formatação WhatsApp Humanizada com Emojis:** Quebras de linhas limpas em tópicos e emojis equilibrados (✨, 🗓️, 🙏, ⭐, 📲, 🤝, ⚡, 🚀, 1️⃣, 2️⃣, 📌) sem blocos de texto maçantes.
  - **Correção no Botão Sales Cockpit:** Identificado e corrigido `ReferenceError: escapeHtml is not defined` que impedia o modal de abrir ao clicar em "Sales Cockpit & Ligar". Função sanitizadora declarada, testada via Chromium DevTools e com deploy imediato na Vercel.

---

### [25/09/2026 22:40 - 26/09/2026 02:11] — Madrugada (Sessão a76b98c8-49a7-46b4-8988-10604844a3f3)
- **Demandas & Execuções:**
  1. **Conexão Real com a Evolution API no Railway:**
     - URL: `https://evolution-api-production-64484.up.railway.app`
     - Instância conectada: `Vendas 1` (WhatsApp Baileys do Thiago, nº `5562996046458`).
     - Ativado escudo anti-ban: presença *composing* (digitando...) de 3.5s antes do envio, delays dinâmicos (45s base + jitter randômico de 5 a 15s) e pausa preventiva de 2min a cada 10 envios.
     - Botão de Disparo Teste adicionado para envio instantâneo no número pessoal.
  2. **Refinamento Humanizado das Copys (WhatsApp Frio):**
     - Remoção de textos robóticos/agressivos; introdução de fluxo conversacional em 4 passos.
     - Passo 1: Sondagem simples de atendimento no bairro.
     - Passo 2: Elogio da nota 5.0 no Google + validação da dor de responder tudo no dedo.
     - Passo 3: Solução sem atrito e sem esforço técnico para ela.
     - Passo 4: Fechamento com âncora de taxa única e retorno em 1 cliente.
  3. **Correção de UI / Transição de Status:**
     - Corrigido travamento visual ao mover cards entre abas filtradas do Kanban/Notebook (adicionado `renderAll()` imediato e Toast informativo).
  4. **Preparação Vercel:**
     - Criado `vercel.json` e rotas serverless em `api/data.js` e `api/leads.js` para persistência em nuvem híbrida (Upstash KV / fallback local).

---

### [08/09/2026] — Implementação do CRM Cockpit v2
- **Commits:** `165578e`, `372d78c`, `fdab87b`.
- Implementação inicial do Cockpit HUD, visualização em Bento Grid, modo Stealth pré-ligação e restauração dos badges de Instagram em cada card de lead.
