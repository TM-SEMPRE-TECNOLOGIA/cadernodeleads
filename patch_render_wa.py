import sys

with open(r'index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_fn = '''    // ==============================================================
    // MODALIDADE 3: WHATSAPP FRIO (ESTEIRA HUMANIZADA ATÉ O FECHAMENTO)
    // ==============================================================
    function renderCockpitWhatsApp() {
      const lead = currentCockpitLead;
      if (!lead) return;
      const decisor = getDecisorFirstName(lead.contact);
      const cleanPhone = getFormattedWaPhone(lead.phone);
      const neighborhood = lead.dossier?.neighborhood || (lead.address ? lead.address.split(',')[0] : 'a região');
      const rating = lead.dossier?.rating || '5.0';
      const offerPrice = lead.dossier?.offerPrice || lead.value || 'R$ 289,90';

      // Identifica o serviço principal do nicho de forma 100% natural
      let targetService = 'procedimentos';
      if (lead.dossier && lead.dossier.anchorServices && lead.dossier.anchorServices.length > 0) {
        targetService = lead.dossier.anchorServices[0].toLowerCase();
      } else if (lead.niche) {
        targetService = lead.niche.split(',')[0].toLowerCase().trim();
      }

      document.getElementById('cp-modal-main-title').innerHTML = '<i class="fa-brands fa-whatsapp text-emerald-600 mr-1.5"></i> WhatsApp Consultivo • Prospecção Fria até o Fechamento';
      document.getElementById('cp-target-badge').innerText = 'Ticket: ' + offerPrice + ' (Sem Demonstração Prévia)';

      const scriptTitleEl = document.getElementById('cp-script-title');
      if (scriptTitleEl) {
        scriptTitleEl.innerHTML = '<i class="fa-brands fa-whatsapp text-emerald-600"></i> Funil de Conversa Natural no WhatsApp (4 Passos)';
      }

      const initials = (lead.name || 'CL').split(' ').slice(0, 2).map(w => w[0]).join('').toUpperCase();
      const nowTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

      // Atualiza cabeçalhos dos 4 passos
      const s1Num = document.getElementById('cp-step1-num');
      const s1Title = document.getElementById('cp-step1-title');
      const s1Sub = document.getElementById('cp-step1-sub');
      if (s1Num) s1Num.className = 'w-4 h-4 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[9px] font-bold';
      if (s1Title) s1Title.innerText = '1. Abertura Fria (Pesquisa / Sondagem de Atendimento)';
      if (s1Sub) s1Sub.innerText = 'Tom curioso, desarmado e humano';

      const s2Num = document.getElementById('cp-step2-num');
      const s2Title = document.getElementById('cp-step2-title');
      const s2Sub = document.getElementById('cp-step2-sub');
      if (s2Num) s2Num.className = 'w-4 h-4 rounded-full bg-sky-600 text-white flex items-center justify-center text-[9px] font-bold';
      if (s2Title) s2Title.innerText = '2. Identificação do Gargalo (Validar se o fluxo é 100% manual e sem site)';
      if (s2Sub) s2Sub.innerText = 'Gera consciência sem ofender';

      const s3Num = document.getElementById('cp-step3-num');
      const s3Title = document.getElementById('cp-step3-title');
      const s3Sub = document.getElementById('cp-step3-sub');
      if (s3Num) s3Num.className = 'w-4 h-4 rounded-full bg-amber-600 text-white flex items-center justify-center text-[9px] font-bold';
      if (s3Title) s3Title.innerText = '3. A Solução Sob Medida (Página Oficial no Google sem travar a rotina)';
      if (s3Sub) s3Sub.innerText = 'Valorização do negócio dela';

      const s4Num = document.getElementById('cp-step4-num');
      const s4Title = document.getElementById('cp-step4-title');
      const s4Sub = document.getElementById('cp-step4-sub');
      if (s4Num) s4Num.className = 'w-4 h-4 rounded-full bg-emerald-600 text-white flex items-center justify-center text-[9px] font-bold';
      if (s4Title) s4Title.innerText = '4. Fechamento & Condição Facilitada (Taxa Única / Pix)';
      if (s4Sub) s4Sub.innerText = 'Irrecusável (sem mensalidade)';

      // PASSO 1: ABERTURA FRIA
      const msg1 = 'Oi, tudo bem? Vocês atendem ' + targetService + ' aí em ' + neighborhood + '? Como funciona pra agendar com vocês?';
      const waUrl1 = cleanPhone ? 'https://wa.me/' + cleanPhone + '?text=' + encodeURIComponent(msg1) : '#';

      document.getElementById('cp-step1-text').innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
          <div class="md:col-span-7 space-y-2">
            <p class="text-xs text-zinc-600 dark:text-zinc-300">
              Inicie com curiosidade genuína. Você <strong>não</strong> está vendendo nada ainda, apenas descobrindo se o número responde rápido e como é o atendimento.
            </p>
            <div class="flex items-center gap-2 flex-wrap pt-0.5">
              ` + (cleanPhone ? `
                <a href="` + waUrl1 + `" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-black text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm flex items-center gap-1.5 transition active:scale-95">
                  <i class="fa-brands fa-whatsapp text-sm"></i>
                  <span>Enviar no WhatsApp</span>
                </a>
              ` : '<span class="text-xs text-zinc-400 italic">Sem telefone</span>') + `
              <button onclick="copyStepWaText(1)" class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-zinc-800 dark:text-zinc-200 bg-white dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 flex items-center gap-1 shadow-xs hover:bg-zinc-100 transition active:scale-95">
                <i class="fa-solid fa-copy text-zinc-500"></i>
                <span>Copiar</span>
              </button>
            </div>
          </div>
          <div class="md:col-span-5">
            <div class="rounded-xl overflow-hidden shadow-md border border-zinc-300 dark:border-zinc-700 bg-[#efeae2] dark:bg-[#0b141a]">
              <div class="bg-[#008069] dark:bg-[#1f2c34] text-white px-2.5 py-1.5 flex items-center justify-between text-[11px]">
                <div class="flex items-center gap-1.5 truncate">
                  <div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center font-bold text-[9px]">` + initials + `</div>
                  <span class="truncate font-semibold">` + (lead.name || 'Lead') + `</span>
                </div>
                <span class="text-[9px] text-emerald-200">online</span>
              </div>
              <div class="p-2.5">
                <div class="bg-[#d9fdd3] dark:bg-[#005c4b] text-zinc-900 dark:text-zinc-100 p-2 rounded-lg text-xs leading-relaxed shadow-xs">
                  <p>` + msg1 + `</p>
                  <div class="flex items-center justify-end gap-1 mt-1 text-[9px] text-zinc-500 dark:text-emerald-200/80 font-mono">
                    <span>` + nowTime + `</span>
                    <i class="fa-solid fa-check-double text-sky-500"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

      // Botões de Resposta da Lead no Passo 1
      document.getElementById('cp-step1-branches').innerHTML = `
        <button onclick="setBranch(1, 'passou_tabela')" id="btn-1-passou_tabela" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-emerald-800 dark:text-emerald-300 font-medium flex items-center gap-1 transition">
          <span>🟢</span> "Mandou tabela / preços"
        </button>
        <button onclick="setBranch(1, 'qual_horario')" id="btn-1-qual_horario" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-sky-50 dark:hover:bg-sky-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sky-800 dark:text-sky-300 font-medium flex items-center gap-1 transition">
          <span>🔵</span> "Qual horário você quer?"
        </button>
        <button onclick="setBranch(1, 'quem_e')" id="btn-1-quem_e" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-amber-50 dark:hover:bg-amber-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-amber-800 dark:text-amber-300 font-medium flex items-center gap-1 transition">
          <span>🟡</span> "Quem gostaria?"
        </button>
      `;

      // PASSO 2: IDENTIFICAÇÃO DO GARGALO
      const msg2 = 'Obrigado pelo retorno rápido! Gostei bastante da atenção de vocês. Na verdade eu perguntei porque vi a avaliação de vocês no Google com nota ' + rating + ' estrelas, achei super conceituado, mas reparei que quando as pessoas procuram no Google não encontram um site oficial com os procedimentos e a opção de agendar direto. O atendimento de vocês é todo manual por aqui pelo WhatsApp mesmo?';
      const waUrl2 = cleanPhone ? 'https://wa.me/' + cleanPhone + '?text=' + encodeURIComponent(msg2) : '#';

      document.getElementById('cp-step2-text').innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
          <div class="md:col-span-7 space-y-2">
            <p class="text-xs text-zinc-600 dark:text-zinc-300">
              Elogie a agilidade, cite as 5 estrelas do Google e aponte o gargalo: <strong>todo mundo cai no WhatsApp e ela perde tempo respondendo tudo no dedo</strong> porque não tem site.
            </p>
            <div class="flex items-center gap-2 flex-wrap pt-0.5">
              ` + (cleanPhone ? `
                <a href="` + waUrl2 + `" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-black text-white bg-sky-600 hover:bg-sky-700 shadow-sm flex items-center gap-1.5 transition active:scale-95">
                  <i class="fa-brands fa-whatsapp text-sm"></i>
                  <span>Enviar Mensagem 2</span>
                </a>
              ` : '') + `
              <button onclick="copyStepWaText(2)" class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-zinc-800 dark:text-zinc-200 bg-white dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 flex items-center gap-1 shadow-xs hover:bg-zinc-100 transition active:scale-95">
                <i class="fa-solid fa-copy text-zinc-500"></i>
                <span>Copiar</span>
              </button>
            </div>
          </div>
          <div class="md:col-span-5">
            <div class="rounded-xl overflow-hidden shadow-md border border-zinc-300 dark:border-zinc-700 bg-[#efeae2] dark:bg-[#0b141a]">
              <div class="bg-[#008069] dark:bg-[#1f2c34] text-white px-2.5 py-1.5 flex items-center justify-between text-[11px]">
                <span class="truncate font-semibold">Mensagem 2 (O Gargalo)</span>
                <span class="text-[9px] text-emerald-200">sondagem</span>
              </div>
              <div class="p-2.5">
                <div class="bg-[#d9fdd3] dark:bg-[#005c4b] text-zinc-900 dark:text-zinc-100 p-2 rounded-lg text-xs leading-relaxed shadow-xs">
                  <p>` + msg2 + `</p>
                  <div class="flex items-center justify-end gap-1 mt-1 text-[9px] text-zinc-500 dark:text-emerald-200/80 font-mono">
                    <span>` + nowTime + `</span>
                    <i class="fa-solid fa-check-double text-sky-500"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

      // Botões de Resposta da Lead no Passo 2
      document.getElementById('cp-step2-branches').innerHTML = `
        <button onclick="setBranch(2, 'sim_manual')" id="btn-2-sim_manual" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-emerald-800 dark:text-emerald-300 font-medium flex items-center gap-1 transition">
          <span>🟢</span> "Sim, é só por aqui mesmo"
        </button>
        <button onclick="setBranch(2, 'tenho_insta')" id="btn-2-tenho_insta" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-amber-50 dark:hover:bg-amber-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-amber-800 dark:text-amber-300 font-medium flex items-center gap-1 transition">
          <span>📱</span> "Uso mais o Instagram"
        </button>
        <button onclick="setBranch(2, 'nao_tenho_tempo')" id="btn-2-nao_tenho_tempo" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-purple-50 dark:hover:bg-purple-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-purple-800 dark:text-purple-300 font-medium flex items-center gap-1 transition">
          <span>⏳</span> "A rotina é uma correria"
        </button>
      `;

      // PASSO 3: A SOLUÇÃO SOB MEDIDA
      const msg3 = 'Faz total sentido! Eu atendo outros profissionais de beleza e estética justamente nisso. O problema de não ter uma página oficial é que a cliente nova que pesquisa no Google acha que o espaço é pequeno ou fica insegura, e você perde um tempão explicando valores um a um no WhatsApp. O que a gente faz é montar uma página leve e elegante pro ' + (lead.name || 'seu espaço') + ', que abre em 1 segundo no celular, com as fotos dos seus trabalhos e botão direto de agendamento. Você não precisa fazer nada nem entender de tecnologia, a gente cuida de tudo.';
      const waUrl3 = cleanPhone ? 'https://wa.me/' + cleanPhone + '?text=' + encodeURIComponent(msg3) : '#';

      document.getElementById('cp-step3-text').innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
          <div class="md:col-span-7 space-y-2">
            <p class="text-xs text-zinc-600 dark:text-zinc-300">
              Apresente a solução tirando o peso das costas dela: ela não precisa entender de computador, você faz tudo sob medida pro espaço dela.
            </p>
            <div class="flex items-center gap-2 flex-wrap pt-0.5">
              ` + (cleanPhone ? `
                <a href="` + waUrl3 + `" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-black text-white bg-amber-600 hover:bg-amber-700 shadow-sm flex items-center gap-1.5 transition active:scale-95">
                  <i class="fa-brands fa-whatsapp text-sm"></i>
                  <span>Enviar Mensagem 3</span>
                </a>
              ` : '') + `
              <button onclick="copyStepWaText(3)" class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-zinc-800 dark:text-zinc-200 bg-white dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 flex items-center gap-1 shadow-xs hover:bg-zinc-100 transition active:scale-95">
                <i class="fa-solid fa-copy text-zinc-500"></i>
                <span>Copiar</span>
              </button>
            </div>
          </div>
          <div class="md:col-span-5">
            <div class="rounded-xl overflow-hidden shadow-md border border-zinc-300 dark:border-zinc-700 bg-[#efeae2] dark:bg-[#0b141a]">
              <div class="bg-[#008069] dark:bg-[#1f2c34] text-white px-2.5 py-1.5 flex items-center justify-between text-[11px]">
                <span class="truncate font-semibold">Mensagem 3 (A Oportunidade)</span>
                <span class="text-[9px] text-emerald-200">sem atrito</span>
              </div>
              <div class="p-2.5">
                <div class="bg-[#d9fdd3] dark:bg-[#005c4b] text-zinc-900 dark:text-zinc-100 p-2 rounded-lg text-xs leading-relaxed shadow-xs">
                  <p>` + msg3 + `</p>
                  <div class="flex items-center justify-end gap-1 mt-1 text-[9px] text-zinc-500 dark:text-emerald-200/80 font-mono">
                    <span>` + nowTime + `</span>
                    <i class="fa-solid fa-check-double text-sky-500"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

      // Botões de Resposta da Lead no Passo 3
      document.getElementById('cp-step3-branches').innerHTML = `
        <button onclick="setBranch(3, 'quanto_custa')" id="btn-3-quanto_custa" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-emerald-800 dark:text-emerald-300 font-medium flex items-center gap-1 transition">
          <span>💸</span> "E quanto fica isso?"
        </button>
        <button onclick="setBranch(3, 'como_funciona')" id="btn-3-como_funciona" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-sky-50 dark:hover:bg-sky-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sky-800 dark:text-sky-300 font-medium flex items-center gap-1 transition">
          <span>🤝</span> "Como funciona pra fazer?"
        </button>
        <button onclick="setBranch(3, 'vou_ver_depois')" id="btn-3-vou_ver_depois" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-amber-50 dark:hover:bg-amber-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-amber-800 dark:text-amber-300 font-medium flex items-center gap-1 transition">
          <span>⏳</span> "Agora não posso investir"
        </button>
      `;

      // PASSO 4: FECHAMENTO & PROPOSTA IRRECUSÁVEL
      const msg4 = 'Como a gente já tem a estrutura validada para ' + targetService + ', a gente não cobra aquelas mensalidades caras nem taxas de agência de R$ 2.000. É uma taxa única de apenas ' + offerPrice + ' (que você pode fazer no Pix ou em até 3x no cartão sem juros), e já inclui o endereço oficial com o nome do ' + (lead.name || 'seu espaço') + ' configurado. Com 1 ou 2 atendimentos que você agendar pelo Google, o projeto já se paga 100%. Quer que eu estruture o de vocês pra colocar no ar ainda esta semana?';
      const waUrl4 = cleanPhone ? 'https://wa.me/' + cleanPhone + '?text=' + encodeURIComponent(msg4) : '#';

      document.getElementById('cp-step4-text').innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-12 gap-3 items-center">
          <div class="md:col-span-7 space-y-2">
            <p class="text-xs text-zinc-600 dark:text-zinc-300">
              Apresente o valor com contraste: sem mensalidade, taxa única, domínio incluso e payback imediato em 1 atendimento.
            </p>
            <div class="flex items-center gap-2 flex-wrap pt-0.5">
              ` + (cleanPhone ? `
                <a href="` + waUrl4 + `" target="_blank" class="px-3 py-1.5 rounded-lg text-xs font-black text-white bg-emerald-600 hover:bg-emerald-700 shadow-sm flex items-center gap-1.5 transition active:scale-95">
                  <i class="fa-brands fa-whatsapp text-sm"></i>
                  <span>Enviar Proposta de Fechamento</span>
                </a>
              ` : '') + `
              <button onclick="copyStepWaText(4)" class="px-2.5 py-1.5 rounded-lg text-xs font-bold text-zinc-800 dark:text-zinc-200 bg-white dark:bg-zinc-800 border border-zinc-300 dark:border-zinc-700 flex items-center gap-1 shadow-xs hover:bg-zinc-100 transition active:scale-95">
                <i class="fa-solid fa-copy text-zinc-500"></i>
                <span>Copiar</span>
              </button>
              <button onclick="recordCockpitOutcome('fechou')" class="px-3 py-1.5 rounded-lg text-xs font-black text-white bg-purple-700 hover:bg-purple-800 shadow-sm flex items-center gap-1 transition active:scale-95">
                <i class="fa-solid fa-trophy"></i>
                <span>Marcar Venda Fechada!</span>
              </button>
            </div>
          </div>
          <div class="md:col-span-5">
            <div class="rounded-xl overflow-hidden shadow-md border border-zinc-300 dark:border-zinc-700 bg-[#efeae2] dark:bg-[#0b141a]">
              <div class="bg-[#008069] dark:bg-[#1f2c34] text-white px-2.5 py-1.5 flex items-center justify-between text-[11px]">
                <span class="truncate font-semibold">Mensagem 4 (Fechamento)</span>
                <span class="text-[9px] text-emerald-200">` + offerPrice + `</span>
              </div>
              <div class="p-2.5">
                <div class="bg-[#d9fdd3] dark:bg-[#005c4b] text-zinc-900 dark:text-zinc-100 p-2 rounded-lg text-xs leading-relaxed shadow-xs">
                  <p>` + msg4 + `</p>
                  <div class="flex items-center justify-end gap-1 mt-1 text-[9px] text-zinc-500 dark:text-emerald-200/80 font-mono">
                    <span>` + nowTime + `</span>
                    <i class="fa-solid fa-check-double text-sky-500"></i>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      `;

      // Botões de Resposta da Lead no Passo 4
      document.getElementById('cp-step4-branches').innerHTML = `
        <button onclick="setBranch(4, 'vamos_fazer')" id="btn-4-vamos_fazer" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-emerald-50 dark:hover:bg-emerald-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-emerald-800 dark:text-emerald-300 font-bold flex items-center gap-1 transition">
          <span>🎉</span> "Vamos fazer! O que precisa?"
        </button>
        <button onclick="setBranch(4, 'parcela_pix')" id="btn-4-parcela_pix" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-sky-50 dark:hover:bg-sky-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-sky-800 dark:text-sky-300 font-medium flex items-center gap-1 transition">
          <span>💳</span> "Faz no cartão em quantas vezes?"
        </button>
        <button onclick="setBranch(4, 'falar_com_socio')" id="btn-4-falar_com_socio" class="text-left text-[11px] bg-white dark:bg-zinc-800 hover:bg-amber-50 dark:hover:bg-amber-950/40 p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 text-amber-800 dark:text-amber-300 font-medium flex items-center gap-1 transition">
          <span>🤝</span> "Preciso ver com sócio/marido"
        </button>
      `;
    }

    function copyStepWaText(step) {
      const lead = currentCockpitLead;
      if (!lead) return;
      const neighborhood = lead.dossier?.neighborhood || (lead.address ? lead.address.split(',')[0] : 'a região');
      const rating = lead.dossier?.rating || '5.0';
      const offerPrice = lead.dossier?.offerPrice || lead.value || 'R$ 289,90';
      let targetService = 'procedimentos';
      if (lead.dossier && lead.dossier.anchorServices && lead.dossier.anchorServices.length > 0) {
        targetService = lead.dossier.anchorServices[0].toLowerCase();
      } else if (lead.niche) {
        targetService = lead.niche.split(',')[0].toLowerCase().trim();
      }

      let text = '';
      if (step === 1) {
        text = 'Oi, tudo bem? Vocês atendem ' + targetService + ' aí em ' + neighborhood + '? Como funciona pra agendar com vocês?';
      } else if (step === 2) {
        text = 'Obrigado pelo retorno rápido! Gostei bastante da atenção de vocês. Na verdade eu perguntei porque vi a avaliação de vocês no Google com nota ' + rating + ' estrelas, achei super conceituado, mas reparei que quando as pessoas procuram no Google não encontram um site oficial com os procedimentos e a opção de agendar direto. O atendimento de vocês é todo manual por aqui pelo WhatsApp mesmo?';
      } else if (step === 3) {
        text = 'Faz total sentido! Eu atendo outros profissionais de beleza e estética justamente nisso. O problema de não ter uma página oficial é que a cliente nova que pesquisa no Google acha que o espaço é pequeno ou fica insegura, e você perde um tempão explicando valores um a um no WhatsApp. O que a gente faz é montar uma página leve e elegante pro ' + (lead.name || 'seu espaço') + ', que abre em 1 segundo no celular, com as fotos dos seus trabalhos e botão direto de agendamento. Você não precisa fazer nada nem entender de tecnologia, a gente cuida de tudo.';
      } else if (step === 4) {
        text = 'Como a gente já tem a estrutura validada para ' + targetService + ', a gente não cobra aquelas mensalidades caras nem taxas de agência de R$ 2.000. É uma taxa única de apenas ' + offerPrice + ' (que você pode fazer no Pix ou em até 3x no cartão sem juros), e já inclui o endereço oficial com o nome do ' + (lead.name || 'seu espaço') + ' configurado. Com 1 ou 2 atendimentos que você agendar pelo Google, o projeto já se paga 100%. Quer que eu estruture o de vocês pra colocar no ar ainda esta semana?';
      }

      if (text) {
        copyCustomText(text, 'Mensagem ' + step + ' copiada!');
      }
    }
'''

start_idx = -1
end_idx = -1

for i, l in enumerate(lines):
    if 'function renderCockpitWhatsApp()' in l:
        start_idx = i
    if start_idx != -1 and 'function renderCockpitBR(' in l:
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    lines[start_idx:end_idx] = [new_fn + '\n\n']
    with open(r'index.html', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print(f'Successfully replaced lines {start_idx+1} to {end_idx}!')
else:
    print('Failed to locate range', start_idx, end_idx)
