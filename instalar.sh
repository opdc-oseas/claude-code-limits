#!/usr/bin/env bash
# Instala a statusline claude-code-limits no Claude Code.
# Uso: ./instalar.sh
set -euo pipefail

CLAUDE_DIR="${HOME}/.claude"
SKILL_DST="${CLAUDE_DIR}/skills/claude-code-limits"
SETTINGS="${CLAUDE_DIR}/settings.json"
SCRIPT_SRC="$(cd "$(dirname "$0")" && pwd)/skill/statusline.py"
SCRIPT_DST="${CLAUDE_DIR}/statusline.py"

command -v python3 >/dev/null 2>&1 || { echo "python3 nao encontrado no PATH." >&2; exit 1; }

mkdir -p "${SKILL_DST}"

# 1) Copia a skill (SKILL.md + script) para ~/.claude/skills/claude-code-limits
cp "$(dirname "$SCRIPT_SRC")/SKILL.md" "${SKILL_DST}/SKILL.md"
cp "${SCRIPT_SRC}" "${SKILL_DST}/statusline.py"

# 2) Copia o script da statusline para ~/.claude/statusline.py
cp "${SCRIPT_SRC}" "${SCRIPT_DST}"
chmod +x "${SCRIPT_DST}"

# 3) Registra o bloco statusLine no settings.json (preserva o resto)
python3 - "$SETTINGS" "$SCRIPT_DST" <<'PY'
import json, os, sys
settings, script = sys.argv[1], sys.argv[2]
try:
    with open(settings, encoding="utf-8") as f:
        d = json.load(f)
except FileNotFoundError:
    d = {}
except Exception as e:
    print(f"settings.json invalido ({e}); abortei sem alterar.", file=sys.stderr)
    sys.exit(1)
d["statusLine"] = {"type": "command", "command": f"python3 -I {script}", "padding": 0}
os.makedirs(os.path.dirname(settings), exist_ok=True)
with open(settings, "w", encoding="utf-8") as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
    f.write("\n")
print(f"statusLine registrado em {settings}")
PY

echo "Pronto. Abra uma sessao nova do Claude Code."
