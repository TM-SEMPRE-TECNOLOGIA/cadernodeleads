// Vercel Serverless Function — API de Persistência Caderno de Leads CRM
// Gerencia persistência híbrida: Nuvem (KV/Upstash/REST) + Memória/Disco (/tmp) + leads.json

const fs = require('fs');
const path = require('path');

const TMP_FILE = '/tmp/caderno_crm_data.json';
const SEED_FILE = path.join(process.cwd(), 'leads.json');

// Carrega os dados iniciais do leads.json canônico
function loadSeedData() {
  try {
    if (fs.existsSync(SEED_FILE)) {
      const raw = fs.readFileSync(SEED_FILE, 'utf8');
      return JSON.parse(raw);
    }
  } catch (err) {
    console.error('[Caderno API] Erro ao carregar seed leads.json:', err);
  }
  return { leads: [], stickyNotes: [], targets: {} };
}

// Carrega dados persistidos
async function getStoredData() {
  // 1. Tenta Upstash / Vercel KV via REST se configurado nas ENVs
  if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
    try {
      const res = await fetch(`${process.env.KV_REST_API_URL}/get/tm_caderno_crm_data`, {
        headers: { Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}` }
      });
      if (res.ok) {
        const json = await res.json();
        if (json && json.result) {
          const parsed = typeof json.result === 'string' ? JSON.parse(json.result) : json.result;
          if (parsed && parsed.leads && parsed.leads.length > 0) {
            return parsed;
          }
        }
      }
    } catch (e) {
      console.warn('[Caderno API] Falha no Upstash KV, tentando fallback:', e.message);
    }
  }

  // 2. Tenta /tmp (persistência quente em Serverless)
  try {
    if (fs.existsSync(TMP_FILE)) {
      const raw = fs.readFileSync(TMP_FILE, 'utf8');
      const data = JSON.parse(raw);
      if (data && data.leads && data.leads.length > 0) {
        return data;
      }
    }
  } catch (e) {
    console.warn('[Caderno API] Falha ao ler /tmp:', e.message);
  }

  // 3. Fallback: Dados canônicos do seed leads.json
  const seed = loadSeedData();
  try {
    fs.writeFileSync(TMP_FILE, JSON.stringify(seed, null, 2), 'utf8');
  } catch (_) {}
  return seed;
}

// Salva dados no backend
async function setStoredData(data) {
  let savedCloud = false;

  // 1. Salva no Upstash / Vercel KV se configurado
  if (process.env.KV_REST_API_URL && process.env.KV_REST_API_TOKEN) {
    try {
      const res = await fetch(`${process.env.KV_REST_API_URL}/set/tm_caderno_crm_data`, {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${process.env.KV_REST_API_TOKEN}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
      });
      if (res.ok) savedCloud = true;
    } catch (e) {
      console.warn('[Caderno API] Erro salvando no KV:', e.message);
    }
  }

  // 2. Salva no /tmp do container serverless
  try {
    fs.writeFileSync(TMP_FILE, JSON.stringify(data, null, 2), 'utf8');
  } catch (e) {
    console.warn('[Caderno API] Erro salvando em /tmp:', e.message);
  }

  return { success: true, savedCloud };
}

module.exports = async (req, res) => {
  // CORS Headers
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method === 'GET') {
    try {
      const data = await getStoredData();
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.setHeader('Cache-Control', 'no-store, max-age=0');
      return res.status(200).json(data);
    } catch (err) {
      return res.status(500).json({ error: 'Erro ao buscar dados', details: err.message });
    }
  }

  if (req.method === 'POST') {
    try {
      let body = req.body;
      if (typeof body === 'string') {
        body = JSON.parse(body);
      }

      if (!body || !body.leads) {
        return res.status(400).json({ error: 'Payload inválido. Objeto com array leads é obrigatório.' });
      }

      body.lastSyncedAt = new Date().toISOString();

      const result = await setStoredData(body);
      return res.status(200).json({
        success: true,
        message: 'Dados persistidos com sucesso no backend!',
        leadsCount: body.leads.length,
        savedCloud: result.savedCloud,
        timestamp: body.lastSyncedAt
      });
    } catch (err) {
      return res.status(500).json({ error: 'Erro ao salvar dados', details: err.message });
    }
  }

  return res.status(405).json({ error: 'Método não permitido' });
};
