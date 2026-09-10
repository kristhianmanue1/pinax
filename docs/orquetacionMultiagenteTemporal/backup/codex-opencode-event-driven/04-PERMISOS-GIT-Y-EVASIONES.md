# 04 — Permisos Git y evasiones

## Política vigente

OpenCode puede crear commits locales sólo si una tarjeta concreta lo autoriza:

- staging por rutas exactas y separador `--`;
- sin `git add -A`, `--all` o `.`;
- sin `git commit -a/--all`;
- sin `--amend`, rebase, reset o reescritura;
- sin push;
- SHA, rutas y checks en el recibo.

PR y merge pertenecen al usuario. Deploy/release requieren autorización nueva.

## Problema observado

El validador inicial recibió `scope.commands` como strings y usó listas de
palabras permitidas/prohibidas. Las pruebas previstas pasaban, pero comandos
válidos sintácticamente podían cambiar estado.

### Evasiones confirmadas

- worktree relativo;
- dependencia `BLOCKED` aceptada como lista;
- `git reset --hard` en texto libre;
- `gh pr create` oculto como comando normal;
- commit permitido sin write scope;
- flags destructivos contradictorios con `allowed=false`;
- escritura en `.git/config`;
- path con newline;
- variante case-insensitive de `.git`;
- `git branch -D`;
- `git hash-object -w`;
- `git symbolic-ref` mutante;
- `git diff --output=...`;
- gestor de paquetes mediante intérprete;
- wrappers `command`/`time` para ocultar Git;
- `git commit -a/--all`;
- `git commit --only` con path ajeno.

## Causa raíz

Un subcomando no tiene un único efecto. Opciones y argumentos cambian su
semántica. Wrappers e intérpretes hacen incompleta una denylist.

Ejemplos:

```text
git branch          # puede listar
git branch -D x     # elimina

git hash-object f   # calcula
git hash-object -w f# escribe objeto
```

Por ello, etiquetar `branch`, `hash-object`, `symbolic-ref` o incluso `diff`
como read-only en bloque es incorrecto.

## Diseño recomendado

### 1. Invocaciones estructuradas

```json
{
  "program": "git",
  "argv": ["status", "--porcelain=v1"],
  "cwd": "/worktree/exacto",
  "effect": "read",
  "writes": [],
  "external": false
}
```

- Sin string shell.
- Sin reinterpretación por `bash -c`.
- `argv` validado elemento por elemento.
- CWD y efectos explícitos.

### 2. Allowlist exacta

No permitir familias completas. Autorizar plantillas precisas:

- lectura Git exacta;
- tests conocidos;
- staging generado por el controlador;
- commit generado por el controlador.

### 3. Staging/commit construidos

El controlador debe comparar las rutas con la tarjeta y construir:

```text
git add -- <ruta1> <ruta2>
git diff --cached --name-only
git commit -m <mensaje-controlado>
```

Antes del commit, el set staged debe ser exactamente igual al autorizado. No
permitir flags que agreguen contenido implícitamente.

### 4. Capas separadas

- Schema: intención y autoridad.
- Policy engine: coherencia y generación de argv.
- Sandbox: filesystem, red y procesos.
- Auditoría: diff/staging/commit/tests reproducidos.

Un schema nunca debe presentarse como sustituto del sandbox.

## Decisión pendiente

Evaluar si los comandos arbitrarios deben:

- prohibirse;
- referenciar scripts versionados con hash;
- ejecutarse sólo en sandbox sin red;
- o requerir revisión humana específica.

