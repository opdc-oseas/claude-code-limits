#!/usr/bin/env python3
# claude-code-limits: statusline de cota do Claude Code.
# Mostra modelo, diretorio e tres medidores: CTX (contexto), 5H e 7D (limites de uso),
# com horario de reset. Le o JSON do Claude Code no stdin e imprime uma linha.
# settings.json: "command": "python3 -I ~/.claude/statusline.py"
import sys, json, time

try:
    d = json.load(sys.stdin)
except Exception:
    sys.exit(0)

R = "\033[0m"; DIM = "\033[38;5;245m"; BOLD = "\033[1m"  # DIM = cinza claro legivel (nao o atributo dim \033[2m, que some em varios terminais)

def cor(p):
    if p is None: return DIM
    if p < 60: return "\033[32m"      # verde
    if p < 85: return "\033[33m"      # amarelo
    return "\033[31m"                  # vermelho

def barra(p, n=8):
    if p is None: return DIM + ("." * n) + R
    cheio = int(round(min(100, max(0, p)) / 100 * n))
    return cor(p) + ("█" * cheio) + R + DIM + ("░" * (n - cheio)) + R

def pct(p):
    return "--%" if p is None else f"{int(round(p))}%"

def seg(rot, p):
    return f"{DIM}{rot}{R} {barra(p)} {cor(p)}{pct(p)}{R}"

def reset(ts, fmt):
    if not ts: return ""
    try:
        return f" {DIM}↻ {time.strftime(fmt, time.localtime(int(ts)))}{R}"
    except Exception:
        return ""

model = (d.get("model") or {}).get("display_name") or "?"
ws = d.get("workspace") or {}
cwd = ws.get("current_dir") or ws.get("project_dir") or ""
dirname = cwd.rstrip("/").split("/")[-1] if cwd else ""

ctx = (d.get("context_window") or {}).get("used_percentage")
rl = d.get("rate_limits") or {}
h5 = rl.get("five_hour") or {}
d7 = rl.get("seven_day") or {}

partes = [f"{BOLD}{model}{R}"]
if dirname:
    partes.append(f"{DIM}{dirname}{R}")
partes.append(seg("CTX", ctx))
partes.append(seg("5H", h5.get("used_percentage")) + reset(h5.get("resets_at"), "%H:%M"))
partes.append(seg("7D", d7.get("used_percentage")) + reset(d7.get("resets_at"), "%d/%m %Hh"))

print(f" {DIM}·{R} ".join(partes))
