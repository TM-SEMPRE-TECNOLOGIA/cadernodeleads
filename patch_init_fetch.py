with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """      // 2. Tenta buscar da API viva do server.py
      try {
        const res = await fetch('/api/data?_=' + Date.now(), { cache: 'no-store' });
        if (res.ok) {
          const remoteData = await res.json();
          if (remoteData && remoteData.leads && remoteData.leads.length >= (appData.leads || []).length) {
            appData = remoteData;
          }
        }
      } catch (e) {
        console.log("Operando via embutido / offline");
      }"""

replacement = """      // 2. Tenta buscar da API viva do server.py ou direto do leads.json estático
      try {
        let res = await fetch('/api/data?_=' + Date.now(), { cache: 'no-store' });
        if (!res.ok) {
          res = await fetch('/leads.json?_=' + Date.now(), { cache: 'no-store' });
        }
        if (res.ok) {
          const remoteData = await res.json();
          if (remoteData && remoteData.leads && remoteData.leads.length > 0) {
            appData = remoteData;
          }
        }
      } catch (e) {
        console.log("Operando via embutido / offline / leads.json");
      }"""

if target in html:
    html = html.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Successfully patched init fetch!")
else:
    print("Target not found, checking variations...")
