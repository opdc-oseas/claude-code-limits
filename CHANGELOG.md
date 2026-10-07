# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/).
Versionamento semântico.

## [1.0.0] - 2026-10-07

### Adicionado
- Statusline de cota para o Claude Code: modelo, diretório e medidores CTX / 5H / 7D.
- Medidores 5H e 7D com horário de reset (limite de 5 horas e de 7 dias).
- Barrinhas de 8 blocos com cor por percentual (verde abaixo de 60%, amarelo 60-84%, vermelho a partir de 85%).
- `instalar.sh`: copia o script e registra o bloco `statusLine` no `settings.json` preservando o resto.
- Tratamento de ausência de `rate_limits` (conta não Pro/Max ou antes da 1a resposta) e de erro de leitura do stdin.
- Script em Python puro, sem dependências.
