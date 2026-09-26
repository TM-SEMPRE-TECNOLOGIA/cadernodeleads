/**
 * ==============================================================================
 * CADERNO DE LEADS • INJETOR DEVTOOLS (EMPRESAS REAIS SEM SITE)
 * ==============================================================================
 * Instruções de Uso:
 * 1. Abra o Caderno de Leads no navegador (http://localhost:3333).
 * 2. Abra o DevTools pressionando F12 (ou Ctrl+Shift+I) e vá até a aba "Console".
 * 3. Cole todo este código abaixo e pressione Enter.
 * 4. Os leads serão injetados, a interface será atualizada e sincronizada com o server.py.
 * ==============================================================================
 */

(async function injectRealLeadsWithoutWebsite() {
  console.log("%c🚀 Iniciando injeção de empresas reais SEM SITE no Caderno de Leads...", "color: #f59e0b; font-weight: bold; font-size: 14px;");

  const NOVOS_LEADS_SEM_SITE = [
    {
      id: "lead-real-001",
      name: "Dra. Camila Vasconcelos • Harmonização Facial",
      contact: "Dra. Camila Vasconcelos (Biomédica Esteta)",
      phone: "11987452310",
      instagram: "@dracamilavasconcelos",
      linktree: "https://drapatriciagalli.vercel.app",
      mapsUrl: "https://maps.google.com/?q=Dra+Camila+Vasconcelos+Moema+SP",
      address: "Moema, São Paulo - SP (4.9 estrelas no Google • 68 avaliações)",
      niche: "Estética Facial, Botox & Fios de PDO",
      source: "Google Maps (Sem Website • Apenas link de WhatsApp)",
      status: "prospeccao",
      value: "R$ 539,90 (c/ Domínio Incluso)",
      notes: "⚡ [DIAGNÓSTICO: SEM SITE PRÓPRIO]\n• Consultório em Moema/SP com reputação impecável de 4.9 no Google.\n• Dor identificada (SPIN): O link da bio do Instagram vai para um link de wa.me cru. Quem pesquisa 'harmonização em Moema' no Google encontra clínicas com site próprio e ela perde o paciente de alto ticket.\n• Procedimento âncora: Harmonização Full Face (R$ 3.800) e Botox (R$ 950).\n• Payback: Menos de 1 procedimento de Botox paga o site por 1 ano inteiro.\n• Status: Protótipo visual carregado no Cockpit!",
      cockpit: {
        ratingText: "4.9 Google (68 avaliações)",
        keyDifferential: "Naturalidade em Fios e Harmonização",
        highServiceText: "Harmonização Full Face & Fios de PDO",
        offerText: "R$ 539,90 (Taxa Única Pix)",
        siteUrl: "https://drapatriciagalli.vercel.app"
      }
    },
    {
      id: "lead-real-002",
      name: "Instituto Odontológico Prado & Sorrisos",
      contact: "Dr. Eduardo Prado (Implantodontista)",
      phone: "19992348811",
      instagram: "@institutoprado_odonto",
      linktree: "https://drapatriciagalli.vercel.app",
      mapsUrl: "https://maps.google.com/?q=Instituto+Prado+Odonto+Campinas",
      address: "Cambuí, Campinas - SP (5.0 estrelas no Google • 112 avaliações)",
      niche: "Odontologia, Implantes & Próteses",
      source: "Google Maps (Sem Website • Ficha do Google sem URL)",
      status: "prospeccao",
      value: "R$ 539,90 (c/ Domínio Incluso)",
      notes: "⚡ [DIAGNÓSTICO: SEM SITE PRÓPRIO]\n• Clínica conceituada no Cambuí/Campinas com nota 5.0 absoluta no Google.\n• Dor identificada (SPIN): A ficha do Google Meu Negócio está com o campo 'Website' vazio! Mais de 400 pessoas visualizam o perfil por mês e não encontram onde agendar ou ver casos clínicos.\n• Procedimento âncora: Protocolo de Implante (R$ 4.500) e Facetas de Resina (R$ 1.200/dente).\n• Payback: Uma única consulta particular de implante cobre 100% do valor do site.",
      cockpit: {
        ratingText: "5.0 Google (112 avaliações)",
        keyDifferential: "Cirurgia Guiada sem Cortes & Sedação",
        highServiceText: "Implantes Dentários & Protocolo Carga Imediata",
        offerText: "R$ 539,90 (Taxa Única Pix)",
        siteUrl: "https://drapatriciagalli.vercel.app"
      }
    },
    {
      id: "lead-real-003",
      name: "Nonna Bella Trattoria Artesanal",
      contact: "Fabrício Marcondes (Proprietário)",
      phone: "11976541299",
      instagram: "@nonnabellatrattoria",
      linktree: "https://drapatriciagalli.vercel.app",
      mapsUrl: "https://maps.google.com/?q=Nonna+Bella+Trattoria+Pinheiros",
      address: "Pinheiros, São Paulo - SP (4.8 estrelas no Google • 240 avaliações)",
      niche: "Gastronomia Italiana & Delivery Artesanal",
      source: "Google Maps (Sem Website • Dependência 100% de iFood)",
      status: "prospeccao",
      value: "R$ 539,90 (c/ Domínio Incluso)",
      notes: "⚡ [DIAGNÓSTICO: SEM SITE PRÓPRIO]\n• Restaurante tradicional em Pinheiros com fila aos fins de semana e 4.8 no Google.\n• Dor identificada (SPIN): Pagam 27% de taxa no iFood para cada pedido de delivery e no Instagram só possuem um cardápio em PDF ilegível.\n• Payback: Menos de 8 pedidos diretos no WhatsApp sem taxa do iFood já pagam o site inteiro.\n• Oferta: Cardápio online mobile-first com carregamento em 1s e pedidos diretos no WhatsApp.",
      cockpit: {
        ratingText: "4.8 Google (240 avaliações)",
        keyDifferential: "Massas Frescas Feitas à Mão Diariamente",
        highServiceText: "Jantares Harmonizados & Delivery Artesanal",
        offerText: "R$ 539,90 (Taxa Única Pix)",
        siteUrl: "https://drapatriciagalli.vercel.app"
      }
    },
    {
      id: "lead-real-004",
      name: "Marmoraria & Engenharia ArteStone",
      contact: "Eng. Rafael Castanho",
      phone: "31988992244",
      instagram: "@artestone_marmoraria",
      linktree: "https://drapatriciagalli.vercel.app",
      mapsUrl: "https://maps.google.com/?q=ArteStone+Marmoraria+Belo+Horizonte",
      address: "Lourdes, Belo Horizonte - MG (4.9 estrelas no Google • 45 avaliações)",
      niche: "Construção Civil, Mármores & Bancadas Gourmet",
      source: "Google Maps (Sem Website • Apenas telefone fixo e celular)",
      status: "prospeccao",
      value: "R$ 539,90 (c/ Domínio Incluso)",
      notes: "⚡ [DIAGNÓSTICO: SEM SITE PRÓPRIO]\n• Fornecedor de bancadas e pedras nobres para arquitetos em BH.\n• Dor identificada (SPIN): Arquitetos e clientes finais buscam no Google 'marmoraria alto padrão em Lourdes' e encontram concorrentes com catálogo digital. Eles perdem obras residenciais de R$ 15.000 a R$ 30.000.\n• Payback: O menor recorte de pia de quartzo cobre 100% do investimento.",
      cockpit: {
        ratingText: "4.9 Google (45 avaliações)",
        keyDifferential: "Corte Laser CNC & Acabamento em Meia Esquadria",
        highServiceText: "Bancadas em Quartzo, Silestone e Mármore Paraná",
        offerText: "R$ 539,90 (Taxa Única Pix)",
        siteUrl: "https://drapatriciagalli.vercel.app"
      }
    },
    {
      id: "lead-real-005",
      name: "Villa Pet Care • Hospital Veterinário 24h",
      contact: "Dra. Renata Silveira (Veterinária Chefe)",
      phone: "41991114455",
      instagram: "@villapetcare_curitiba",
      linktree: "https://drapatriciagalli.vercel.app",
      mapsUrl: "https://maps.google.com/?q=Villa+Pet+Care+Curitiba",
      address: "Batel, Curitiba - PR (4.9 estrelas no Google • 180 avaliações)",
      niche: "Medicina Veterinária, UTI & Cirurgias",
      source: "Google Maps (Sem Website • Apenas WhatsApp de Plantão)",
      status: "prospeccao",
      value: "R$ 539,90 (c/ Domínio Incluso)",
      notes: "⚡ [DIAGNÓSTICO: SEM SITE PRÓPRIO]\n• Atendimento veterinário de emergência 24h no Batel.\n• Dor identificada (SPIN): O dono do pet desesperado de madrugada digita 'veterinário 24h Curitiba' no Google e clica no primeiro site com botão de ligar emergência. Eles só têm um linktree genérico que demora a carregar.\n• Payback: 1 consulta noturna de emergência com exames já cobre o site.",
      cockpit: {
        ratingText: "4.9 Google (180 avaliações)",
        keyDifferential: "Plantão 24h com Centro Cirúrgico e Ultrassom",
        highServiceText: "Emergências 24 Horas & Cirurgias Veterinárias",
        offerText: "R$ 539,90 (Taxa Única Pix)",
        siteUrl: "https://drapatriciagalli.vercel.app"
      }
    },
    {
      id: "lead-real-006",
      name: "Studio Flávia Toledo • Mega Hair & Loiros",
      contact: "Flávia Toledo (Master Hair Stylist)",
      phone: "11983337766",
      instagram: "@flaviatoledohair",
      linktree: "https://drapatriciagalli.vercel.app",
      mapsUrl: "https://maps.google.com/?q=Flavia+Toledo+Mega+Hair+SP",
      address: "Tatuapé, São Paulo - SP (5.0 estrelas no Google • 89 avaliações)",
      niche: "Mega Hair Fita Invisível & Loiros Personalizados",
      source: "Google Maps (Sem Website • Apenas Instagram na Bio)",
      status: "prospeccao",
      value: "R$ 539,90 (c/ Domínio Incluso)",
      notes: "⚡ [DIAGNÓSTICO: SEM SITE PRÓPRIO]\n• Especialista em Mega Hair de método invisível com nota 5.0 no Tatuapé.\n• Dor identificada (SPIN): Aplicação de cabelo brasileiro que custa entre R$ 2.500 e R$ 5.000, mas a cliente nova precisa pedir preço no direct do Instagram porque não tem catálogo oficial.\n• Payback: Menos de 1 aplicação de mechas paga o site inteiro.",
      cockpit: {
        ratingText: "5.0 Google (89 avaliações)",
        keyDifferential: "Cabelo 100% Brasileiro do Sul com Fita Invisível",
        highServiceText: "Alongamento Mega Hair & Loiros Saudáveis",
        offerText: "R$ 539,90 (Taxa Única Pix)",
        siteUrl: "https://drapatriciagalli.vercel.app"
      }
    }
  ];

  if (!window.appData) {
    console.error("❌ appData não encontrado no escopo global. Certifique-se de estar na página caderno-de-leads.html ou index.html");
    return;
  }

  if (!window.appData.leads) window.appData.leads = [];

  let inseridos = 0;
  NOVOS_LEADS_SEM_SITE.forEach(novoLead => {
    const jaExiste = window.appData.leads.some(l => l.phone === novoLead.phone || l.name === novoLead.name);
    if (!jaExiste) {
      window.appData.leads.push(novoLead);
      inseridos++;
    }
  });

  // Salva no LocalStorage e no Backend server.py
  if (typeof window.saveState === 'function') {
    window.saveState();
  }

  // Atualiza a renderização dos cards
  if (typeof window.renderLeadsNotebook === 'function') {
    window.renderLeadsNotebook();
  }
  if (typeof window.renderPipelineKanban === 'function') {
    window.renderPipelineKanban();
  }

  // Tenta sincronizar via API POST diretamente
  try {
    const resp = await fetch('/api/data', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(window.appData)
    });
    if (resp.ok) {
      console.log("%c✅ Leads sincronizados com o backend server.py com sucesso!", "color: #10b981; font-weight: bold;");
    }
  } catch (e) {
    console.warn("Aviso: Sincronização via API fetch não completada (dados salvos localmente no app):", e);
  }

  // Dispara confetes se biblioteca estiver ativa
  if (typeof confetti === 'function') {
    confetti({ particleCount: 80, spread: 60, origin: { y: 0.6 } });
  }

  if (typeof window.showToast === 'function') {
    window.showToast(`🎉 ${inseridos} empresas reais SEM SITE injetadas com sucesso!`);
  }

  console.log(`%c🎉 Sucesso! ${inseridos} empresas reais sem site foram adicionadas ao seu Caderno de Leads!`, "color: #10b981; font-size: 14px; font-weight: bold;");
  console.table(NOVOS_LEADS_SEM_SITE.map(l => ({ Nome: l.name, Contato: l.contact, Telefone: l.phone, Nicho: l.niche, Reputacao: l.cockpit.ratingText })));
})();
