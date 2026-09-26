# Melhorias do Caderno de Leads — Avaliação & Plano

**Referência avaliada:** `leadsperhour.com` (6 snapshots no Downloads/Melhorias do caderno)
**Objetivo:** transformar o Caderno de Leads (Sales CRM & Cockpit) usando o que há de bom nessa referência — sem virar um SaaS B2B, mantendo o escopo leve (PWA de arquivo único + `server.py` + `leads.json`).

---

## 1. O que é a referência (leadsperhour.com)

> *"Infra de agentes de IA para vendas B2B — antes, durante e depois de cada call."*

Produto orientado a *times* de vendas B2B brasileiros, com **3 agentes num flywheel fechado**:

| Agente | O que faz |
|---|---|
| **LPH Prospect** | 8 agentes rodando 24/7 em e-mail, LinkedIn, WhatsApp e telefone — do ICP até a reunião agendada. |
| **LPH Meet** | Co-piloto de IA **durante** a call: briefing pré-reunião (90s), deteção de objeção em ~0,8s, battle card, scorecard de 10 competências, "Game Tapes". |
| **LPH Roleplay** | Treino com buyer personas calibradas nas suas calls reais; scoring de 10 competências, dificuldade adaptativa; lançamento 10/05/2026. |

**Posicionamento-chave que vale roubar:**
- **O moat é o DURANTE.** Gong/Fireflies analisam depois; o Meet age enquanto o deal está vivo.
- **Flywheel:** dado da reunião → treino do Roleplay → resultado alimenta playbook do Meet → realimenta targeting do Prospect.
- **Anti-hype:** "humano × IA, não humano + IA". IA cuida do mecânico; humano julga, conecta e fecha.
- **Metrics com fonte/ano:** RAIN Group (+41% close), Forrester (+45% win), Gartner (87% esquecido em 120 dias), 11x.ai (−80% custo prospecção), Datagrid (11h/semana).
- **Preços/funil** (Starter R$2.990 / Growth R$4.990 / Scale R$9.990) — relevante só se você vender esse produto.

---

## 2. O que o Caderno de Leads já tem

De `caderno-de-leads.html`:
- 5 pilares: **Prospecção → Qualificação → Negociação → Fechamento → Pós-Venda** (+ Lixeira/Arquivo).
- **Sales Cockpit BR/US** (teleprompter, roteiro em 4 passos, matriz de objeções, cronômetro, gravação de áudio .webm), pipeline CRM, sticky notes, metas de contato/propostas.
- **Hermes AI copilot**: qualificação, enriquecimento de dossiê, objeções, "2 indicações", simular call.
- `leads.json` + cache local; PWA com service worker; exportar/imprimir.

**Conclusão:** a fundação (CRM + cockpits + copiloto IA) já é forte. O gap está em **"vivência de coaching"** (briefing/battle card/scorecard), **prospecção multicanal com cadência**, **roleplay/simulação estruturada** e **métricas com fontes**.

---

## 3. Mapa Referência → Caderno (o que falta)

| Conceito LPH | Onde entra no Caderno | Status |
|---|---|---|
| Briefing pré-call (90s) | Abrir o Cockpit já com resumo: dor, ticket, objeções prováveis, próximo passo | **Falta** (hoje é manual) |
| Battle card / objeção→réplica instantânea | Matriz de Objeções do Cockpit, com pré-carregada por nicho | Tem base, **melhorar** |
| Scorecard pós-call (10 competências) | Checklist pós-call no Cockpit (discovery, valor, objeção, fechamento…) | **Falta** |
| "Game Tapes" (melhores momentos) | Marcar trechos-chave da gravação .webm + nota do que funcionou | **Falta** |
| Prospecção multicanal + cadência | Pilar 1 (Buscar Maps & Insta): adicionar templates de abordagem por canal (LinkedIn/WhatsApp/e-mail) + follow-ups agendados | **Melhorar** |
| ICP + score de qualificação | Pilar 2 (Auditar dor & ticket): adicionar fit/score do lead | **Melhorar** |
| Roleplay com personas + dificuldade adaptativa | "Simular Call" do copiloto: personas por nicho + níveis e scoring | **Melhorar** |
| Flywheel fechado visual | Conectar Negociação→Roleplay→Prospecção com uma visão de loop | **Falta** |
| Metrics com fontes | Metas (targets) + painel com números reais e benchmark citado | **Melhorar** |
| Anti-hype humano+IA | Já é human-in-the-loop — reforçar no tom do copiloto | **Manter** |

---

## 4. Plano priorizado

### Fase 1 — Alto impacto, baixo esforço (1–2 sessões)
1. **Briefing pré-call automático** no Cockpit: gerar com o Hermes um cartão de 4 linhas (dor / ticket / objeção provável / próximo passo) antes de cada ligação.
2. **Matriz de Objeções por nicho** (estética, gastronomia, arquitetura…) com réplica pronta, e seletor durante o cockpit.
3. **Scorecard pós-call** (10 competências, simplificadas para o funil): caixa de checkmarks + 1 campo de "o que melhorar", salvo no lead.
4. **Metas/métricas com benchmark citado**: no painel de targets, linkar a fonte (RAIN/Forrester/11x/Datagrid).
5. **Correção já feita como pré-requisito:** `leads.json` válido, `server.py` com `Cache-Control: no-store`, `sw.js` sem cachear `/api/`.

### Fase 2 — Alcance (2–3 sessões)
6. **Cadência de prospecção**: por lead, sequência de follow-up (D1/D3/D7) por canal, com lembrete na Fila de Ligações.
7. **Score de qualificação (ICP)**: campos de dor/ticket/bio-segurança/orçamento → pontuação 0–10 que classifica prioridade automaticamente.
8. **Personas de roleplay**: 3–4 personas por nicho que o "Simular Call" usa (cético, técnico, o que pede desconto), com dificuldade fácil→média→difícil.

### Fase 3 — Diferenciação (opcional, conforme necessidade)
9. **Game Tapes**: permitir marcar "momentos" na gravação do cockpit (objeção/pricing/fechamento) e reproduzir destes trechos.
10. **Visão de flywheel**: dashboard que mostra o loop Prospecção→Call→Treino→Retorno.
11. **Exportar playbook do time** (o que funcionou por nicho) como artefato reutilizável.

---

## 5. O que NÃO fazer (e por quê)
- **Automação multicanal 24/7 estilo Prospect** (e-mail/LinkedIn/WhatsApp em massa): o Caderno é uma ferramenta de uso pessoal/comercial de nicho, não um SDR de time. O Hermes já faz a parte de redação; automação de envio em escala exige integrações (RD/HubSpot/Salesforce) que hoje não existem e não cabem no arquivo único.
- **Análise de áudio em tempo real (detecta objeção em ~0,8s):** **JÁ IMPLEMENTADO client-side** via `webkitSpeechRecognition` do navegador + motor de detecção de objeções em PT-BR (réplica instantânea, ~1s, offline). A versão "cerebral" com LLM/ASR backend é opcional e paga latência/custo — hoje o teleprompter + matriz cobrem o caso de uso (ver seção de análise em tempo real).
- **Pricing em planos:** a menos que você passe a vender o próprio Caderno como SaaS. Hoje é ferramenta interna.

---

## 6. Efeito esperado
- Menos tempo por call (briefing pronto → entra na ligação em <1 min).
- Mais consistência: scorecard e matriz transformam "memória do vendedor" em padrão.
- Melhor aprendizado: roleplay + game tapes aceleram rampagem (a referência cita −50% no ramp-up).
- Prova social nas vendas: métricas com fontes reforçam o pitch dos cockpits BR/US.

---

*Avaliação concluída. Próximo passo sugerido: aprovar a Fase 1 e eu começar a implementar no `caderno-de-leads.html`.*
