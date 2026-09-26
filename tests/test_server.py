#!/usr/bin/env python3
"""Testes da API do Caderno de Leads (server.py) — rodam num servidor
temporário em porta efêmera, sem tocar no servidor real da porta 3333.

Uso:
    python tests/test_server.py
    python -m unittest tests.test_server -v
"""
import importlib.util
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT = os.path.dirname(HERE)
SERVER_PY = os.path.join(PROJECT, "server.py")


def load_server_module():
    spec = importlib.util.spec_from_file_location("caderno_server", SERVER_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class ServerTestCase(unittest.TestCase):
    """Sobe um servidor de teste isolado (DATA_FILE temporário)."""

    @classmethod
    def setUpClass(cls):
        cls.server_mod = load_server_module()
        cls.tmpdir = tempfile.TemporaryDirectory()
        cls.data_file = os.path.join(cls.tmpdir.name, "leads_test.json")
        # seed com dados conhecidos
        with open(cls.data_file, "w", encoding="utf-8") as f:
            json.dump({
                "leads": [{
                    "id": "lead-test-1",
                    "name": "Cliente Teste",
                    "status": "negociacao",
                    "value": "R$ 539,90",
                }],
                "stickyNotes": [{"id": "1", "text": "nota", "done": False}],
                "targets": {"contactsDone": 1, "contactsGoal": 10},
            }, f, ensure_ascii=False, indent=2)

        cls.server_mod.DATA_FILE = cls.data_file
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), cls.server_mod.CadernoHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.tmpdir.cleanup()

    # ── helpers ──────────────────────────────────────────────
    def url(self, path):
        return f"http://127.0.0.1:{self.port}{path}"

    def get(self, path):
        with urllib.request.urlopen(self.url(path), timeout=10) as r:
            return r.status, r.read().decode("utf-8"), dict(r.headers)

    def post(self, path, payload):
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.url(path), data=data,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8")), dict(r.headers)

    def delete(self, path):
        req = urllib.request.Request(self.url(path), method="DELETE")
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, json.loads(r.read().decode("utf-8"))
    def test_servidor_entrega_pagina_index(self):
        status, body, _ = self.get("/")
        self.assertEqual(status, 200)
        self.assertIn("Caderno de Leads", body)

    def test_api_data_retorna_leads(self):
        status, body, _ = self.get("/api/data")
        self.assertEqual(status, 200)
        data = json.loads(body)
        self.assertEqual(len(data["leads"]), 1)
        self.assertEqual(data["leads"][0]["id"], "lead-test-1")

    def test_api_data_tem_cache_control_no_store(self):
        _, _, headers = self.get("/api/data")
        self.assertEqual(headers.get("Cache-Control"), "no-store")

    def test_api_retorna_cors_aberto(self):
        _, _, headers = self.get("/api/data")
        self.assertEqual(headers.get("Access-Control-Allow-Origin"), "*")

    # ── POST /api/data/sync ──────────────────────────────────
    def test_sync_sobrescreve_leads_e_notes(self):
        payload = {"leads": [{"id": "novo", "name": "Lead Novo"}],
                   "stickyNotes": [], "targets": {}}
        status, resp, _ = self.post("/api/data/sync", payload)
        self.assertEqual(status, 200)
        self.assertEqual(resp.get("status"), "success")
        _, body, _ = self.get("/api/data")
        data = json.loads(body)
        self.assertEqual([l["id"] for l in data["leads"]], ["novo"])

    # ── POST /api/leads (add/update) ─────────────────────────
    def test_post_lead_novo_insere_no_inicio(self):
        status, resp, _ = self.post("/api/leads", {"id": "l2", "name": "Segundo"})
        self.assertEqual(status, 200)
        self.assertEqual(resp["lead"]["id"], "l2")
        _, body, _ = self.get("/api/data")
        data = json.loads(body)
        self.assertEqual(data["leads"][0]["id"], "l2")

    def test_post_lead_sem_id_gera_id(self):
        status, resp, _ = self.post("/api/leads", {"name": "Sem ID"})
        self.assertEqual(status, 200)
        self.assertTrue(resp["lead"]["id"])

    def test_post_lead_existente_atualiza(self):
        self.post("/api/leads", {"id": "lead-test-1", "name": "Atualizado"})
        _, body, _ = self.get("/api/data")
        data = json.loads(body)
        lead = next(l for l in data["leads"] if l["id"] == "lead-test-1")
        self.assertEqual(lead["name"], "Atualizado")

    # ── DELETE /api/leads/{id} ───────────────────────────────
    def test_delete_lead_remove(self):
        self.post("/api/leads", {"id": "l-del", "name": "Vai sumir"})
        status, resp = self.delete("/api/leads/l-del")
        self.assertEqual(status, 200)
        self.assertEqual(resp["deleted"], "l-del")
        _, body, _ = self.get("/api/data")
        data = json.loads(body)
        self.assertNotIn("l-del", [l["id"] for l in data["leads"]])

    # ── POST /api/chat (validação local, sem rede) ───────────
    def test_chat_rejeita_mensagem_vazia(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            self.post("/api/chat", {"message": "   "})
        self.assertEqual(ctx.exception.code, 400)


if __name__ == "__main__":
    unittest.main(verbosity=2)
