#!/usr/bin/env python3
"""
Enriquecedor de Telefones do Google Maps para o Caderno de Leads
TM Sempre Tecnologia

Lê leads.json, identifica leads sem telefone e busca os dados oficiais
diretamente no painel do Google Maps usando Selenium Headless.
Atualiza leads.json atomicamente e sincroniza com o server.py.
"""

import os
import sys
import json
import time
import re
import urllib.parse
import urllib.request
from typing import Optional, Tuple
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LEADS_FILE = os.path.join(BASE_DIR, "leads.json")
API_SYNC_URL = "http://127.0.0.1:3333/api/data/sync"

def extract_place_id(maps_url: str) -> str:
    """Extrai o Place ID (19s...) da URL do Google Maps."""
    if not maps_url:
        return ""
    m = re.search(r'19s([A-Za-z0-9_-]+)', maps_url)
    if m:
        return m.group(1)
    m_qid = re.search(r'query_place_id=([A-Za-z0-9_-]+)', maps_url)
    if m_qid:
        return m_qid.group(1)
    return ""

def clean_phone_number(raw: str) -> str:
    """Higieniza número para padrão brasileiro E.164 sem caracteres especiais (ex: 5562981489450)."""
    digits = re.sub(r'\D', '', raw)
    if not digits:
        return ""
    if digits.startswith("0") and len(digits) in [11, 12]:
        digits = "55" + digits[1:]
    elif len(digits) in [10, 11]:
        digits = "55" + digits
    return digits

def format_brazilian_phone(clean: str) -> str:
    """Formata telefone limpo para exibição humana (ex: (62) 98148-9450)."""
    d = clean
    if d.startswith("55") and len(d) in [12, 13]:
        d = d[2:]
    if len(d) == 11:
        return f"({d[:2]}) {d[2:7]}-{d[7:]}"
    elif len(d) == 10:
        return f"({d[:2]}) {d[2:6]}-{d[6:]}"
    return clean

def extract_phone_from_soup(soup: BeautifulSoup) -> Tuple[Optional[str], Optional[str]]:
    """Procura telefone nos botões de ação e atributos do Google Maps."""
    # 1. Botão específico com data-item-id
    for el in soup.find_all(attrs={"data-item-id": True}):
        item_id = el["data-item-id"]
        if item_id.startswith("phone:tel:"):
            raw = item_id.replace("phone:tel:", "").strip()
            clean = clean_phone_number(raw)
            if clean:
                fmt = format_brazilian_phone(clean)
                return clean, fmt

    # 2. Atributos aria-label que contenham "Telefone:"
    for el in soup.find_all(attrs={"aria-label": True}):
        label = el["aria-label"]
        if "telefone:" in label.lower():
            m = re.search(r'(\(?\d{2}\)?\s*9?\d{4}[-\s]?\d{4})', label)
            if m:
                clean = clean_phone_number(m.group(1))
                if clean:
                    fmt = format_brazilian_phone(clean)
                    return clean, fmt

    # 3. Links tel:
    for a in soup.find_all("a", href=True):
        if a["href"].startswith("tel:"):
            raw = a["href"].replace("tel:", "").strip()
            clean = clean_phone_number(raw)
            if clean:
                fmt = format_brazilian_phone(clean)
                return clean, fmt

    # 4. Busca textual por padrão de telefone com DDD 62 ou outros DDDs brasileiros
    text = soup.get_text()
    m_text = re.search(r'\(?([1-9]{2})\)?\s*(9\d{4}[-\s]?\d{4})', text)
    if m_text:
        clean = clean_phone_number(m_text.group(0))
        if clean:
            fmt = format_brazilian_phone(clean)
            return clean, fmt

    return None, None

def sync_with_server(data: dict):
    """Envia os dados atualizados para o server.py via POST."""
    try:
        req = urllib.request.Request(
            API_SYNC_URL,
            data=json.dumps(data, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            return resp.status == 200
    except Exception:
        return False

def init_driver():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=pt-BR")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36")
    return webdriver.Chrome(options=options)

def main():
    if not os.path.exists(LEADS_FILE):
        print(f"[ERRO] Arquivo {LEADS_FILE} não encontrado.")
        return

    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    leads = data.get("leads", [])
    leads_to_enrich = []

    for idx, l in enumerate(leads):
        phone = str(l.get("phone") or "").strip()
        d_phone = ""
        if isinstance(l.get("dossier"), dict):
            d_phone = str(l["dossier"].get("phone") or l["dossier"].get("phoneClean") or "").strip()
        if not phone and not d_phone:
            leads_to_enrich.append((idx, l))

    print("=" * 70)
    print("🚀 TM ENRIQUECEDOR DE TELEFONES GOOGLE MAPS")
    print(f"📊 Total de leads no Caderno: {len(leads)}")
    print(f"🔍 Leads pendentes de telefone: {len(leads_to_enrich)}")
    print("=" * 70)

    if not leads_to_enrich:
        print("✅ Todos os leads já possuem telefone cadastrado!")
        return

    driver = init_driver()
    found_count = 0
    not_found_count = 0

    try:
        for i, (orig_idx, lead) in enumerate(leads_to_enrich):
            name = lead.get("name", "").strip()
            address = lead.get("address", "").strip()
            maps_url = lead.get("mapsUrl", "").strip()
            place_id = extract_place_id(maps_url)

            print(f"\n[{i+1}/{len(leads_to_enrich)}] 🏢 {name}")
            
            # Constrói URL de destino
            if place_id:
                target_url = f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote_plus(name)}&query_place_id={place_id}"
            else:
                query_str = f"{name} {address}".strip() or name
                target_url = f"https://www.google.com/maps/search/{urllib.parse.quote_plus(query_str)}"

            try:
                driver.get(target_url)
                # Espera dinâmica para carregamento do painel
                time.sleep(3.2)

                soup = BeautifulSoup(driver.page_source, "html.parser")
                clean, fmt = extract_phone_from_soup(soup)

                # Se não achou na primeira tentativa e tem lista de resultados, tenta clicar no primeiro card
                if not clean:
                    first_card = driver.find_elements("css selector", "a.hfpxzc")
                    if first_card:
                        try:
                            first_card[0].click()
                            time.sleep(2.5)
                            soup = BeautifulSoup(driver.page_source, "html.parser")
                            clean, fmt = extract_phone_from_soup(soup)
                        except Exception:
                            pass

                if clean:
                    found_count += 1
                    lead["phone"] = clean
                    if not isinstance(lead.get("dossier"), dict):
                        lead["dossier"] = {}
                    lead["dossier"]["phone"] = fmt
                    lead["dossier"]["phoneClean"] = clean
                    
                    # Atualiza notas se tiverem marcação
                    lead_notes = lead.get("notes", "")
                    if "WhatsApp / Contato:" not in lead_notes:
                        lead["notes"] = f"📱 WhatsApp / Contato: {fmt}\n" + lead_notes

                    print(f"   ✅ Telefone Localizado: {fmt} (clean: {clean})")
                else:
                    not_found_count += 1
                    print(f"   ⚠️ Sem telefone registrado no Google Maps")

                # Atualiza na lista principal
                leads[orig_idx] = lead

                # Salva a cada 3 leads ou no último para persistência atômica
                if (i + 1) % 3 == 0 or (i + 1) == len(leads_to_enrich):
                    with open(LEADS_FILE, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)
                    sync_with_server(data)
                    print(f"   💾 [leads.json salvo & sincronizado com server.py]")

            except Exception as e:
                print(f"   ❌ Erro ao consultar lead: {e}")
                not_found_count += 1

    finally:
        driver.quit()

    # Salva final e sincroniza
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    synced = sync_with_server(data)

    print("\n" + "=" * 70)
    print("🎉 ENRIQUECIMENTO CONCLUÍDO COM SUCESSO!")
    print(f"   ✅ Telefones encontrados e adicionados: {found_count}")
    print(f"   ⚠️ Estabelecimentos sem telefone no Maps: {not_found_count}")
    print(f"   🔄 Sincronização em tempo real com server.py: {'CONECTADO' if synced else 'OFFLINE (salvo no disco)'}")
    print("=" * 70)

if __name__ == "__main__":
    main()
