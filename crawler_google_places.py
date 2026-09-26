#!/usr/bin/env python3
"""
Crawler Google Places (Apify compass/crawler-google-places)
Executa buscas qualificadas no Google Maps para encontrar estabelecimentos sem site.
"""

import sys
import json
import time
import argparse
import urllib.request
import urllib.error

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

APIFY_TOKEN = os.getenv("APIFY_TOKEN", "")
ACTOR_ID = "compass~crawler-google-places"

def map_stars_to_enum(stars):
    if stars >= 4.5:
        return "fourAndHalf"
    elif stars >= 4.0:
        return "four"
    elif stars >= 3.5:
        return "threeAndHalf"
    elif stars >= 3.0:
        return "three"
    return ""

def run_google_places_crawler(search_queries, max_places=10, only_without_website=True, min_stars=4.5):
    website_filter = "withoutWebsite" if only_without_website else "allPlaces"
    stars_enum = map_stars_to_enum(min_stars)
    
    payload = {
        "searchStringsArray": search_queries if isinstance(search_queries, list) else [search_queries],
        "maxCrawledPlacesPerSearch": max_places,
        "language": "pt-BR",
        "countryCode": "br",
        "website": website_filter,
        "placeMinimumStars": stars_enum,
        "skipClosedPlaces": True,
        "scrapeContacts": True,
        "scrapeSocialMediaProfiles": True
    }
    
    print(f"🚀 Iniciando crawler no Apify ({ACTOR_ID})...")
    print(f"🔍 Buscas: {payload['searchStringsArray']}")
    print(f"⚙️ Filtro de Website: {website_filter} | Mínimo de Estrelas: {min_stars} ★")
    
    start_url = f"https://api.apify.com/v2/acts/{ACTOR_ID}/runs?token={APIFY_TOKEN}"
    req = urllib.request.Request(
        start_url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            run_data = json.loads(resp.read().decode("utf-8"))["data"]
            run_id = run_data["id"]
            dataset_id = run_data["defaultDatasetId"]
            print(f"✅ Execução iniciada! Run ID: {run_id}")
            print(f"📦 Dataset ID: {dataset_id}")
    except Exception as e:
        print(f"❌ Erro ao iniciar execução: {e}")
        return []

    # Polling status
    print("⏳ Aguardando conclusão do crawler...")
    status_url = f"https://api.apify.com/v2/actor-runs/{run_id}?token={APIFY_TOKEN}"
    while True:
        time.sleep(5)
        try:
            with urllib.request.urlopen(status_url, timeout=15) as resp:
                status_info = json.loads(resp.read().decode("utf-8"))["data"]
                status = status_info["status"]
                print(f"   Status atual: {status}...")
                if status in ["SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"]:
                    break
        except Exception as e:
            print(f"   Aviso polling: {e}")

    if status != "SUCCEEDED":
        print(f"❌ Crawler finalizou com status: {status}")
        return []

    # Fetch results from dataset
    items_url = f"https://api.apify.com/v2/datasets/{dataset_id}/items?token={APIFY_TOKEN}&format=json"
    try:
        with urllib.request.urlopen(items_url, timeout=30) as resp:
            items = json.loads(resp.read().decode("utf-8"))
            print(f"🎉 Extração concluída! {len(items)} locais encontrados.")
            return items
    except Exception as e:
        print(f"❌ Erro ao buscar dataset: {e}")
        return []

def format_lead_item(item):
    return {
        "name": item.get("title") or item.get("name"),
        "phone": item.get("phone") or item.get("phoneUnformatted"),
        "website": item.get("website"),
        "address": item.get("address"),
        "category": item.get("categoryName"),
        "rating": item.get("totalScore"),
        "reviewsCount": item.get("reviewsCount"),
        "mapsUrl": item.get("url"),
        "instagram": (item.get("socialMediaProfiles") or {}).get("instagram") or (item.get("additionalInfo") or {}).get("instagram")
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Google Places Lead Scraper (Apify)")
    parser.add_argument("--query", type=str, default="Harmonização Facial Moema", help="Termo de busca")
    parser.add_argument("--max", type=int, default=5, help="Quantidade máxima de resultados")
    parser.add_argument("--min-stars", type=float, default=4.5, help="Nota mínima de estrelas")
    parser.add_argument("--all", action="store_true", help="Buscar todos os lugares (com ou sem site)")
    
    args = parser.parse_args()
    
    results = run_google_places_crawler(
        search_queries=[args.query],
        max_places=args.max,
        only_without_website=not args.all,
        min_stars=args.min_stars
    )
    
    leads = [format_lead_item(r) for r in results]
    print("\n" + "="*80)
    print(f"📋 RESULTADOS FILTRADOS (SEM SITE): {len(leads)}")
    print("="*80)
    print(json.dumps(leads, indent=2, ensure_ascii=False))
