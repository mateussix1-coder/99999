#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/5] Verificando definições únicas das funções deduplicadas..."
rg -n "def render_upload_box|def render_upload_section|def render_tolerance_section|def render_kpis|def render_chart|def render_exports" app.py

echo "[2/5] Compilando app.py..."
python -m py_compile app.py

echo "[3/5] Compileall (silencioso)..."
python -m compileall -q app.py

echo "[4/6] Rodando testes automatizados do parser..."
python -m unittest discover -s tests

echo "[5/6] Subindo Streamlit em modo headless para smoke check..."
PORT="${PORT:-8510}"
LOG_FILE="${LOG_FILE:-/tmp/auditoria_streamlit_smoke.log}"
streamlit run app.py --server.headless true --server.port "$PORT" >"$LOG_FILE" 2>&1 &
ST_PID=$!
trap 'kill "$ST_PID" >/dev/null 2>&1 || true' EXIT
sleep 7

echo "[6/6] Validando resposta HTTP local..."
curl -fsS "http://127.0.0.1:${PORT}" >/tmp/auditoria_smoke_index.html
BYTES=$(wc -c </tmp/auditoria_smoke_index.html)
echo "OK: app respondeu em http://127.0.0.1:${PORT} (${BYTES} bytes)."

echo "Logs Streamlit (últimas linhas):"
tail -n 20 "$LOG_FILE" || true

echo "\nChecklist técnico concluído com sucesso."
