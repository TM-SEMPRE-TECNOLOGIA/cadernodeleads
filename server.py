#!/usr/bin/env python3
"""
Caderno de Leads — Backend API & Static Server
Suporta sincronização em tempo real entre a UI e Agentes Autônomos (Antigravity & Hermes).
"""

import os
import json
import mimetypes
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 3333
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "leads.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"leads": [], "stickyNotes": [], "targets": {"contactsDone": 0, "contactsGoal": 10, "proposalsDone": 0, "proposalsGoal": 2}}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Loading leads.json: {e}")
        return {"leads": [], "stickyNotes": [], "targets": {}}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[ERROR] Saving leads.json: {e}")
        return False

class CadernoHandler(BaseHTTPRequestHandler):
    def send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors_headers()
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/data" or path == "/api/leads":
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_cors_headers()
            self.end_headers()
            data = load_data()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return

        # Serve static files
        if path == "/" or path == "":
            file_path = os.path.join(BASE_DIR, "index.html")
        else:
            file_path = os.path.join(BASE_DIR, path.lstrip("/"))

        if os.path.exists(file_path) and os.path.isfile(file_path):
            mime_type, _ = mimetypes.guess_type(file_path)
            self.send_response(200)
            self.send_header("Content-Type", mime_type or "application/octet-stream")
            self.send_cors_headers()
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            # Fallback to index.html
            index_path = os.path.join(BASE_DIR, "index.html")
            if os.path.exists(index_path):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_cors_headers()
                self.end_headers()
                with open(index_path, "rb") as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        payload = json.loads(body) if body else {}

        data = load_data()

        if path == "/api/data/sync":
            # Full sync from UI
            if "leads" in payload:
                data["leads"] = payload["leads"]
            if "stickyNotes" in payload:
                data["stickyNotes"] = payload["stickyNotes"]
            if "targets" in payload:
                data["targets"] = payload["targets"]
            save_data(data)
            self.send_json_response({"status": "success", "message": "Synced successfully"})
            return

        if path == "/api/leads":
            # Add or update single lead
            lead = payload
            if "id" not in lead or not lead["id"]:
                import time
                lead["id"] = str(int(time.time() * 1000))
            
            existing_idx = next((i for i, l in enumerate(data["leads"]) if l["id"] == lead["id"]), -1)
            if existing_idx >= 0:
                data["leads"][existing_idx] = lead
            else:
                data["leads"].insert(0, lead)
            
            save_data(data)
            self.send_json_response({"status": "success", "lead": lead})
            return

        if path == "/api/chat":
            # Chat com IA real (OpenCode Free — keyless, sem custo)
            import urllib.request
            import time as _time

            message = (payload.get("message") or "").strip()
            system_extra = (payload.get("system") or "").strip()
            history = payload.get("history") or []
            lead_id = payload.get("leadId")

            lead_ctx = ""
            if lead_id:
                for l in data.get("leads", []):
                    if l.get("id") == lead_id:
                        lead_ctx = (
                            f"Lead atual:\n- Nome: {l.get('name')}\n"
                            f"- Contato: {l.get('contact')}\n- Nicho: {l.get('niche')}\n"
                            f"- Status (pilar): {l.get('status')}\n- Oferta/Valor: {l.get('value')}\n"
                            f"- Notas/Dossiê: {(l.get('notes') or '')[:900]}"
                        )
                        break

            system = (
                "Você é o Hermes, copiloto de vendas de alto padrão do 'Caderno de Leads' — um CRM de vendas "
                "para criadores de sites para negócios locais (estética, clínicas, restaurantes, arquitetura). "
                "Metodologia dos 5 pilares: Prospecção, Qualificação, Negociação (cold call com sales cockpit), "
                "Fechamento (Pix R$ 539,90 ou $500 USD Stripe, domínio incluso, entrega 48h), Pós-venda (2 indicações). "
                "Responda em PORTUGUÊS do Brasil, direto e acionável, com emojis leves e formatação simples. "
                "Seja um coach de vendas: dê réplicas prontas para objeções, estratégia e próximo passo. "
                "Não invente dados que não estão no contexto. Seja conciso (2-6 frases ou listas curtas)."
                + (("\n\n" + lead_ctx) if lead_ctx else "")
                + (("\n\nInstrução extra do usuário: " + system_extra) if system_extra else "")
            )

            if not message:
                self.send_json_response({"error": "message vazio"}, code=400)
                return

            messages = [{"role": "system", "content": system}]
            messages.extend(history[-10:])  # contexto recente
            messages.append({"role": "user", "content": message})

            free_url = "https://opencode.ai/zen/v1/chat/completions"
            free_model = "nemotron-3.5-lightning-free"
            req_body = json.dumps({
                "model": free_model,
                "messages": messages,
                "max_tokens": 1100,
            }).encode("utf-8")

            headers = {
                "Content-Type": "application/json",
                "Authorization": "",
                "HTTP-Referer": "https://hermes-agent.nousresearch.com",
                "X-Title": "Caderno de Leads",
                "User-Agent": "HermesAgent/caderno-de-leads",
            }

            try:
                req = urllib.request.Request(free_url, data=req_body, headers=headers)
                with urllib.request.urlopen(req, timeout=60) as resp:
                    raw = json.loads(resp.read().decode("utf-8"))
                reply = (raw.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
                if not reply:
                    self.send_json_response({"error": "resposta vazia do modelo"}, code=502)
                    return
                # Defensivo: se o modelo vazar o raciocínio no content, mantém só a parte final
                low = reply.lower()
                marker = low.find("here's a thinking process")
                if marker >= 0:
                    # procura o fim do bloco de raciocínio — a resposta real vem depois
                    cut = reply.find("\n\n", marker)
                    while cut >= 0 and cut < len(reply) - 40:
                        nxt = reply.find("\n\n", cut + 2)
                        if nxt < 0 or nxt > len(reply) - 60:
                            break
                        cut = nxt
                    if cut >= 0:
                        reply = reply[cut + 2:].strip()
                self.send_json_response({"reply": reply, "model": free_model})
            except Exception as e:
                self.send_json_response({"error": f"Falha ao chamar IA: {e}"}, code=502)
            return

        self.send_response(404)
        self.end_headers()

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path.startswith("/api/leads/"):
            lead_id = path.split("/")[-1]
            data = load_data()
            data["leads"] = [l for l in data["leads"] if l["id"] != lead_id]
            save_data(data)
            self.send_json_response({"status": "success", "deleted": lead_id})
            return

        self.send_response(404)
        self.end_headers()

    def send_json_response(self, obj, code=200):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_cors_headers()
        self.end_headers()
        self.wfile.write(json.dumps(obj, ensure_ascii=False).encode("utf-8"))

def run():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), CadernoHandler)
    print(f"[CADERNO-SERVER] Rodando na porta {PORT}...")
    server.serve_forever()

if __name__ == "__main__":
    run()
