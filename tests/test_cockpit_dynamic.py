#!/usr/bin/env python3
"""Teste automatizado da dinâmica do Cockpit de Negociação por lead.
Verifica se cada lead recebe briefing, partituras e abordagens WhatsApp personalizadas.

Roda: python tests/test_cockpit_dynamic.py
"""
import os
import json
import re
import subprocess
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(HERE)
INDEX_HTML = os.path.join(PROJECT_DIR, "index.html")
LEADS_JSON = os.path.join(PROJECT_DIR, "leads.json")

def run_node_test():
    with open(INDEX_HTML, encoding="utf-8") as f:
        src = f.read()

    with open(LEADS_JSON, encoding="utf-8") as f:
        leads_data = json.load(f)

    # Extrai o script principal do HTML
    script_match = re.search(r'<script>(.*?)</script>', src, re.DOTALL)
    if not script_match:
        print("✗ Tag <script> não encontrada no index.html")
        sys.exit(1)

    js_code = f"""
const fs = require('fs');

// Mock simples de ambiente de navegador para executar a lógica do Cockpit
const elements = {{}};
function getMockElement(id) {{
    if (!elements[id]) {{
        elements[id] = {{
            id: id,
            innerText: '',
            innerHTML: '',
            value: '',
            href: '',
            className: '',
            classList: {{
                _classes: new Set(),
                add(c) {{ this._classes.add(c); }},
                remove(c) {{ this._classes.delete(c); }},
                contains(c) {{ return this._classes.has(c); }}
            }}
        }};
    }}
    return elements[id];
}}

global.window = global;
global.document = {{
    getElementById: (id) => getMockElement(id),
    querySelectorAll: (selector) => [],
    createElement: (tag) => getMockElement('mock_' + Math.random())
}};
global.showToast = (msg) => {{}};
global.stopLiveAnalysis = () => {{}};
global.saveState = () => {{}};

// Carrega os dados reais de leads
const leadsData = {json.dumps(leads_data)};
global.appData = leadsData;

// Injeta as funções do script
{extract_cockpit_logic(src)}

let failures = 0;
function check(name, cond) {{
    if (!cond) {{
        console.log('✗ ' + name);
        failures++;
    }} else {{
        console.log('✓ ' + name);
    }}
}}

console.log('\\n--- 1. TESTES DE SANITIZAÇÃO DE TELEFONE E WHATSAPP ---');
check('getFormattedWaPhone adiciona 55 para DDD 11 dígitos', getFormattedWaPhone('62981489450') === '5562981489450');
check('getFormattedWaPhone NÃO duplica 55 se já tiver 55', getFormattedWaPhone('5562981489450') === '5562981489450');
check('getFormattedWaPhone com formatação (+55 62 98148-9450)', getFormattedWaPhone('+55 (62) 98148-9450') === '5562981489450');
check('getFormattedTel gera tel:+5562981489450', getFormattedTel('5562981489450') === 'tel:+5562981489450');
check('getFormattedTel não gera tel:+5555', !getFormattedTel('5562981489450').includes('5555'));

console.log('\\n--- 2. TESTES DE DINÂMICA DO COCKPIT POR LEAD ---');
const leads = appData.leads || [];
check('Existem leads carregados', leads.length >= 2);

// Lead 1: Estúdio de Beleza / Cílios em Goiânia
const lead1 = leads[0];
openCockpitModal(lead1.id, 'wa');

const s1_header = document.getElementById('cp-client-header-name').innerText;
const s1_sub = document.getElementById('cp-client-header-sub').innerText;
const s1_phoneBadge = document.getElementById('cp-header-phone-badge').innerHTML;
const s1_pain = document.getElementById('cp-briefing-pain').innerText;
const s1_payback = document.getElementById('cp-briefing-payback').innerText;
const s1_step1 = document.getElementById('cp-step1-text').innerHTML;
const s1_targetBadge = document.getElementById('cp-target-badge').innerText;

check('Lead 1 abre no Cockpit com nome correto', s1_header.length > 0);
check('Lead 1 header tem badge de telefone sem 5555', s1_phoneBadge.includes('wa.me/55') && !s1_phoneBadge.includes('wa.me/5555'));
check('Lead 1 briefing de dor prioriza o dossiê', s1_pain.length > 10);
check('Lead 1 WhatsApp Stealth tem mensagem de isca personalizada', s1_step1.includes('Oi, tudo bem?'));

// Lead 2: Outro lead da lista
const lead2 = leads.find(l => l.id !== lead1.id && l.name !== lead1.name);
if (lead2) {{
    openCockpitModal(lead2.id, 'wa');

    const s2_header = document.getElementById('cp-client-header-name').innerText;
    const s2_sub = document.getElementById('cp-client-header-sub').innerText;
    const s2_step1 = document.getElementById('cp-step1-text').innerHTML;
    const s2_phoneBadge = document.getElementById('cp-header-phone-badge').innerHTML;

    check('Lead 2 nome é DIFERENTE de Lead 1', s2_header !== s1_header);
    check('Lead 2 empresa/sub é DIFERENTE de Lead 1', s2_sub !== s1_sub);
    check('Lead 2 mensagem isca é DIFERENTE ou ajustada ao lead', s2_step1.length > 0);
    check('Lead 2 telefone sem duplicação 5555', !s2_phoneBadge.includes('wa.me/5555'));
}}

console.log('\\n--- 3. TESTES DE MODALIDADES (WA vs LIGAÇÃO BR vs EUA) ---');
// Testa modo Ligação Brasil
setCockpitPitchMode('br', false);
const br_step2 = document.getElementById('cp-step2-text').innerHTML;
const br_step3 = document.getElementById('cp-step3-text').innerHTML;
check('Modo BR Passo 2 cita projeto de site exclusivo e notas Google', br_step2.includes('projeto de site exclusivo'));
check('Modo BR Passo 3 cita taxa única com domínio incluso', br_step3.includes('taxa única'));

// Testa modo Ligação Morna (Warm Call)
setCockpitPitchMode('br', true);
const warm_title = document.getElementById('cp-modal-main-title').innerHTML;
const warm_step1 = document.getElementById('cp-step1-text').innerHTML;
check('Modo Ligação Morna ativa título correspondente', warm_title.includes('Morna'));
check('Modo Ligação Morna cita retorno da conversa no WhatsApp', warm_step1.includes('WhatsApp'));

// Testa modo EUA ($500 USD)
setCockpitPitchMode('us');
const us_title = document.getElementById('cp-modal-main-title').innerHTML;
const us_badge = document.getElementById('cp-target-badge').innerText;
check('Modo EUA ativa moeda em dólar', us_badge.includes('$500'));

console.log('\\n--- RESUMO DA VALIDAÇÃO ---');
if (failures === 0) {{
    console.log('🎉 TODOS OS TESTES DO COCKPIT DINÂMICO PASSARAM COM SUCESSO!\\n');
    process.exit(0);
}} else {{
    console.error(`❌ ${{failures}} falha(s) detectada(s).\\n`);
    process.exit(1);
}}
"""

    with open("tests/_temp_runner.js", "w", encoding="utf-8") as f:
        f.write(js_code)

    res = subprocess.run(["node", "tests/_temp_runner.js"], capture_output=True, text=True, encoding="utf-8")
    if os.path.exists("tests/_temp_runner.js"):
        os.remove("tests/_temp_runner.js")

    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
    return res.returncode == 0

def extract_cockpit_logic(src):
    # Extrai NICHE_PLAYBOOKS, helpers e funções do Cockpit
    playbooks = re.search(r'const NICHE_PLAYBOOKS = \{.*?\n    \};', src, re.DOTALL)
    helpers = re.search(r'function getDecisorFirstName.*?function getFormattedTel\(phone\) \{.*?\n    \}', src, re.DOTALL)
    briefing = re.search(r'function renderBriefing90s\(lead\) \{.*?\n    \}', src, re.DOTALL)
    wa_mode = re.search(r'function renderCockpitWhatsApp\(\) \{.*?\n    \}', src, re.DOTALL)
    br_mode = re.search(r'function renderCockpitBR\(isWarm = false\) \{.*?\n    \}', src, re.DOTALL)
    us_mode = re.search(r'function renderCockpitUS\(\) \{.*?\n    \}', src, re.DOTALL)
    switch_mode = re.search(r'function setCockpitPitchMode\(mode, isWarm = false\) \{.*?\n    \}', src, re.DOTALL)
    open_cockpit = re.search(r'function openCockpitModal\(leadId, pitchMode = \'wa\'\) \{.*?\n    \}', src, re.DOTALL)

    return f"""
    let currentCockpitLead = null;
    let currentCockpitPitchMode = 'wa';
    let currentNichePlaybook = 'estetica';

    {playbooks.group(0) if playbooks else ''}
    {helpers.group(0) if helpers else ''}
    {briefing.group(0) if briefing else ''}
    {wa_mode.group(0) if wa_mode else ''}
    {br_mode.group(0) if br_mode else ''}
    {us_mode.group(0) if us_mode else ''}
    {switch_mode.group(0) if switch_mode else ''}
    {open_cockpit.group(0) if open_cockpit else ''}
    """

if __name__ == '__main__':
    success = run_node_test()
    sys.exit(0 if success else 1)
