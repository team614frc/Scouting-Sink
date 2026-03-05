async function fetchJSON(url, opts) {
  const r = await fetch(url, opts);
  if (!r.ok) throw new Error(await r.text());
  return await r.json();
}

async function loadDb() {
  const db = await fetchJSON("/api/database");
  document.getElementById("out").textContent = JSON.stringify(db, null, 2);
}

document.getElementById("refreshBtn").addEventListener("click", loadDb);

document.getElementById("rebuildBtn").addEventListener("click", async () => {
  await fetchJSON("/api/rebuild", { method: "POST" });
  await loadDb();
});

loadDb();