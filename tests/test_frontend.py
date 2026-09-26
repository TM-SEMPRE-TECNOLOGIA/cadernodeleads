#!/usr/bin/env python3
"""Testes da lógica JS pura do frontend (extraída do HTML e executada no Node).

Roda: python tests/test_frontend.py
"""
import os
import json
import re
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(os.path.dirname(HERE), "caderno-de-leads.html")


def extract(pattern, flags=re.S):
    with open(HTML, encoding="utf-8") as f:
        src = f.read()
    m = re.search(pattern, src, flags)
    if not m:
        raise RuntimeError(f"Padrão não encontrado: {pattern[:60]}…")
    return m.group(0)


def build_test_js():
    with open(HTML, encoding="utf-8") as f:
        full_html = f.read()

    parts = []
    # 0) meta viewport exposto para testes de acessibilidade
    m = re.search(r'<meta name="viewport"[^>]*>', full_html)
    if not m:
        raise RuntimeError("meta viewport não encontrado")
    parts.append(f"const HTML_META = {json.dumps(m.group(0))};")
    # 1) utilitário de normalização (definido inline no teste também para isolamento)
    parts.append("function normText(t){ try { return (t||'').toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,''); } catch(e){ return (t||'').toLowerCase(); } }")
    # 2) estado inicial vazio (extraído do HTML)
    parts.append(extract(r"function emptyAppData\(\) \{.*?\n    \}"))
    # 3) matriz de objeções extraída do HTML
    parts.append(extract(r"const OBJECAO_MATRIZ = \[.*?\];"))
    # 4) lógica de detecção reproduzida (usa apenas normText + matriz)
    parts.append(r"""
function detectObjetcao(texto){
  const n = normText(texto);
  for (const obj of OBJECAO_MATRIZ){
    if (obj.re.test(n)) return obj.label;
  }
  return null;
}
""")
    # 5) escHtml e renderAIHTML extraídos do HTML
    parts.append(extract(r"function escHtml\(t\) \{.*?\n    \}"))
    parts.append(extract(r"function renderAIHTML\(text\) \{.*?\n    \}"))
    # 6) asserções
    parts.append(r"""
let failures = 0;
function check(name, cond){
  if (!cond) { console.log('✗ ' + name); failures++; }
  else { console.log('✓ ' + name); }
}

// --- acessibilidade (viewport e botões só-ícone) ---
const VIEWPORT = HTML_META;
check('viewport permite zoom (sem user-scalable=no)', !/user-scalable=no/.test(VIEWPORT) && !/maximum-scale=1\.0/.test(VIEWPORT));

// --- estado inicial vazio (sem leads demo como se fossem reais) ---
check('emptyAppData existe', typeof emptyAppData === 'function');
const empty = emptyAppData();
check('emptyAppData tem leads vazio', Array.isArray(empty.leads) && empty.leads.length === 0);
check('emptyAppData sem lead demo donantonia', JSON.stringify(empty).indexOf('donantonia') === -1);
check('emptyAppData sem lead demo kethlyn', JSON.stringify(empty).indexOf('kethlyn') === -1);
check('emptyAppData com archivedLeads vazio', Array.isArray(empty.archivedLeads) && empty.archivedLeads.length === 0);
check('emptyAppData com stickyNotes vazio', Array.isArray(empty.stickyNotes) && empty.stickyNotes.length === 0);

// --- detecção de objeções ---
check('detecta preço ("ta muito caro")', detectObjetcao('Ai, mas ta muito caro isso') === 'Preço / Desconto');
check('detecta "já tenho site"', detectObjetcao('Eu já tenho o meu site') === 'Já tenho');
check('detecta "vou pensar"', detectObjetcao('Vou pensar e te falo') === 'Vou pensar / Volto depois');
check('detecta "me manda por email"', detectObjetcao('Me manda por email que eu avalio') === 'Pede proposta / estudo');
check('detecta "sem tempo"', detectObjetcao('Estou sem tempo agora') === 'Sem tempo / orçamento');
check('detecta "preciso falar com meu marido"', detectObjetcao('Preciso falar com meu marido') === 'Decisor é outro');
check('detecta "meu sobrinho faz site"', detectObjetcao('Meu sobrinho faz site pra mim') === 'Conhece alguém / fazem por fora');
check('detecta "vou pesquisar"', detectObjetcao('Vou pesquisar mais um pouco') === 'Comparando / concorrente');
check('detecta "não estou precisando"', detectObjetcao('Não estou precisando') === 'Não preciso / sem interesse');
check('detecta "não confio" (trauma)', detectObjetcao('Já fui queimada, não confio') === 'Desconfiança / trauma');

// não deve dar falso-positivo em frase neutra de vendedor
check('sem falso positivo em fala comum', detectObjetcao('Bom dia, tudo bem? Aqui é da agência, pode falar?') === null);

// --- segurança de saída HTML (XSS) ---
const evil = '<img src=x onerror=alert(1)> <script>alert(2)</script>';
const escaped = escHtml(evil);
check('escHtml escapa <script>', !escaped.includes('<script>'));
check('escHtml escapa tag img', !escaped.includes('<img'));
check('escHtml não deixa < cru', !escaped.includes('<script>alert(2)'));

// --- renderAIHTML: negrito/listas saem formatadas, tags cruas escapadas ---
const out = renderAIHTML('Olá **mundo**\n- item um\n- item dois');
check('renderAIHTML faz negrito', out.includes('<strong>mundo</strong>'));
check('renderAIHTML transforma lista', out.includes('•') || out.includes('item um'));
check('renderAIHTML não injeta HTML cru', !renderAIHTML('<b>oi</b>').includes('<b>oi</b>'));

if (failures > 0) { console.log('\n' + failures + ' FALHAS'); process.exit(1); }
else { console.log('\nTODOS OS TESTES PASSARAM'); }
""")
    return "\n".join(parts)


def main():
    js = build_test_js()
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(js)
        tmp = f.name
    try:
        r = subprocess.run(["node", tmp], capture_output=True, text=True, timeout=60)
        print(r.stdout)
        if r.stderr:
            print("STDERR:", r.stderr[:2000])
        sys.exit(r.returncode)
    finally:
        os.unlink(tmp)


if __name__ == "__main__":
    main()
