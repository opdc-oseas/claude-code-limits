# claude-code-limits

A statusline de **cota** para o Claude Code. Veja quanto já usou dos limites de **5 horas** e
**7 dias** e **quando reseta**, direto na barra de status. Um arquivo Python, sem dependência.

```
Opus 4.8 · meu-projeto · CTX ██░░░░░░ 20% · 5H █░░░░░░░ 8% ↻ 12:50 · 7D ████░░░░ 47% ↻ 09/10 11h
```

> O custo em dólar você já vê no faturamento. O que trava a sua sessão é a **cota**: o limite
> de 5 horas e o de 7 dias. Esta statusline mostra os dois, com o horário de reset, para você
> saber se dá pra continuar ou se é hora de parar.

## O que mostra

| Medidor | O que é |
| --- | --- |
| **CTX** | uso da janela de contexto da sessão atual |
| **5H** | uso do limite de 5 horas, com horário de reset (`HH:MM`) |
| **7D** | uso do limite de 7 dias, com data e hora de reset (`DD/MM HHh`) |

Cor por percentual: verde abaixo de 60%, amarelo de 60% a 84%, vermelho a partir de 85%.

## Diferença para os outros

- **Foco em cota, não em gasto.** A maioria das statuslines calcula custo em dólar a partir dos
  tokens. Esta mostra quanto falta dos limites de 5h e 7d e quando eles zeram.
- **Zero dependência, um arquivo.** Python puro da biblioteca padrão. Sem `jq`, `curl`, `node`,
  `npm` nem arquivo de configuração. São ~55 linhas: dá pra ler tudo antes de instalar.
- **Honesta quando não há dado.** Sem conta Pro/Max, ou antes da primeira resposta da sessão, os
  medidores 5H e 7D aparecem como `--%` com a barra apagada, em vez de inventar número.

## Instalar

```bash
git clone <url-do-repo> claude-code-limits
cd claude-code-limits
./instalar.sh
```

Abra uma sessão nova do Claude Code.

Registro manual, se preferir, no `~/.claude/settings.json`:

```json
"statusLine": { "type": "command", "command": "python3 -I ~/.claude/statusline.py", "padding": 0 }
```

Requisito: `python3` no PATH (vem no macOS e na maioria das distribuições Linux; no Windows, use
WSL).

## Como funciona

O Claude Code chama o comando da statusline passando um JSON pelo stdin a cada atualização. O
script lê esse JSON e imprime uma linha. Campos usados:

| Campo no JSON | Uso |
| --- | --- |
| `model.display_name` | nome do modelo (em negrito) |
| `workspace.current_dir` (fallback `project_dir`) | último diretório do caminho |
| `context_window.used_percentage` | medidor CTX |
| `rate_limits.five_hour.used_percentage` / `.resets_at` | medidor 5H + reset |
| `rate_limits.seven_day.used_percentage` / `.resets_at` | medidor 7D + reset |

`resets_at` é epoch em segundos, formatado no fuso local.

> Só funciona no **Claude Code**: esses campos e o recurso de statusline são dele. A ideia é
> portável para outras ferramentas, mas a fonte dos números mudaria.

## Customizar

- Número de blocos da barra: parâmetro `n` em `barra()` (padrão 8).
- Faixas de cor: função `cor()`.
- Formato dos resets: strings de `time.strftime` nas chamadas de `reset()`.
- Tirar o diretório ou o modelo: remover o `append` correspondente em `partes`.

## Desinstalar

Remova o bloco `statusLine` do `~/.claude/settings.json` e apague `~/.claude/statusline.py`.

## Licença

MIT. Veja `LICENSE`.
