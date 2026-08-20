# Encargo para el agente de Skopos (2026-08-20)

**Emisor:** Pinax (visión de ecosistema), tras visión final firmada por tres
modelos (`/Users/krisnova/www/pinax/rondas/2026-08-20-vision-skopos-ektel/vision-final-firmada.md`)
— rondas adversariales de Codex CLI (X-1, X-2) y Claude CLI (Y-1..Y-7) ya
incorporadas (actas en la misma carpeta:
`/Users/krisnova/www/pinax/rondas/2026-08-20-vision-skopos-ektel/`).
**Naturaleza:** encargo, no autorización. Los actos marcados con 🔒
requieren autorización explícita del dueño, una vez por operación, según
`/Users/krisnova/www/aria/skopos/AGENTS.md`.

**Repo del proyecto:** `/Users/krisnova/www/aria/skopos` — todas las rutas
de este encargo son absolutas; si una referencia interna usa `:línea` es
sobre ese árbol (ej. `captura.py:18` =
`/Users/krisnova/www/aria/skopos/src/skopos/captura.py`, línea 18).

## 0. Antes de tocar nada (orden de lectura obligatorio)

1. `/Users/krisnova/www/aria/skopos/AGENTS.md` y
   `/Users/krisnova/www/aria/skopos/docs/guia-rapida.md`.
2. `/Users/krisnova/www/aria/skopos/docs/hoja-de-ruta.md` — qué está
   cerrado y qué falta.
3. `/Users/krisnova/www/aria/skopos/docs/propuestas/P-001-integracion-an-kla-memory.md`
   §5 — las cinco precondiciones en su orden real.
4. `/Users/krisnova/www/pinax/rondas/2026-08-20-vision-skopos-ektel/vision-final-firmada.md`
   — contexto de por qué este ciclo y qué correcciones de las rondas
   aplican.

Las decisiones de diseño cerradas (F0/F1, ADR-001..006, en
`/Users/krisnova/www/aria/skopos/docs/`) no se reinventan ni se
contradicen sin un ADR nuevo que las sustituya.

## 1. Contexto que cambió (decisión del dueño, 2026-08-20)

- **Skopos será multi-CLI:** hoy sólo parsea rollouts de Codex
  (`captura.py:18`, `CLI_ORIGEN = "codex-cli"`); el dueño confirma que se
  usará para Claude Code, Kimi CLI, Qwen CLI y otros.
- **Consecuencia registrada:** P-001 (integración con AN-KLA) queda
  **superada por esta decisión** — su única justificación en pie era la
  cobertura de agentes que Skopos no podía observar, y la cobertura se
  resolverá con parsers propios. P-001 no se reabre; el agente puede
  anotarlo en la propuesta con una línea de estado y fecha, nada más.
- **El parser de Codex deja de ser el corazón:** pasa a ser el primer
  adaptador de una familia, detrás de una interfaz común por CLI.

## 2. Trabajo del ciclo, en este orden (P-001 §5, sin omitir ninguno)

1. **C-9 · Eje de proyecto.** Añadir campo de proyecto al documento de
   Mongo y a `skopos query`. Sin esto, cualquier consolidación futura
   funde namespaces de forma irreversible (el store es insert-only).
   En el mundo multi-CLI, considerar también el eje `cli_origen` — hoy
   está fijo a Codex por constante.
2. **C-8 · Superficie de mutación o retención.** Propuesta con ADR nuevo:
   o el store deja de ser insert-only, o hay política de retención. La
   vigencia consolidada no puede pudrirse sin reparación. 🔒 la elección
   entre ambas es del dueño; el agente prepara el ADR con alternativas.
3. **C-10 · Cursor de ingesta.** Medición documentada al 2026-08-19
   (trátala como snapshot fechado, no como estado actual — X-2): 609
   rollouts / 2.1 GB reparseados por ciclo a intervalo de 5 s; backfill
   estimado 40–100 h. **Advertencia de la ronda de Claude (Y-4):** esto
   no es reparación neutra — obliga a revisar o acotar **ADR-005**
   (`/Users/krisnova/www/aria/skopos/docs/adr/ADR-005-deduplicacion-via-mongo.md`,
   la dedup vive en Mongo por decisión registrada) y a cerrar la
   **decisión 8** de
   `/Users/krisnova/www/aria/skopos/docs/hoja-de-ruta.md` (política de
   arranque del vigilante). 🔒 la
   política de arranque (backfill opt-in vs "desde ahora") la decide el
   dueño; el agente prepara la decisión, no la toma.
4. **C-6 · `fragmento_completo`.** Hoy se sirve crudo, sin redactar, y se
   **relee del archivo original por offsets sin verificación de
   integridad, con fallos silenciosos** (`cli.py:20-27` — hallazgo Y-5).
   La decisión tiene **cuatro** opciones, no tres: servir / redactar /
   marcar como no-instrucción en el contrato del CLI / **persistir el
   fragmento o sellar el origen con hash+tamaño**. 🔒 decisión del dueño.
5. **C-5 · Ejecutar el detector corregido** (§4.5 de
   `/Users/krisnova/www/aria/skopos/docs/propuestas/P-001-integracion-an-kla-memory.md`)
   contra un corpus poblado. Ninguna ronda lo ha hecho; sin este dato no
   se discute más la hipótesis del eco.

## 3. Ensayo del canal escrubery (REQ-10, pendiente 3 de
`/Users/krisnova/www/aria/skopos/README.md`)

- Probar la integración con escrubery contra el repo real
  (`/Users/krisnova/www/aria/escrubery`), exigiendo `escrubery_script`
  explícito, como ya está implementado en
  `/Users/krisnova/www/aria/skopos/src/skopos/analisis.py` pero nunca
  ejercitado.
- Propósito de ecosistema: es el ensayo del canal por el que luego fluirá
  la metadata versionada de CLIs (qué versión del CLI es vigente, qué
  cambió, cuándo un parser quedó obsoleto).
  `/Users/krisnova/www/aria/skopos/docs/adr/ADR-004-escrubery-fuente-opcional.md`
  lo mantiene opcional y no bloqueante — no lo conviertas en dependencia
  dura.
- Límite: escrubery no parsea rollouts; aporta la verdad versionada del
  CLI. Los parsers los escribe Skopos.

## 4. Diseño del contrato de parser por CLI (después de las precondiciones)

- Sólo cuando 1–5 estén cerrados: proponer la interfaz común de parser
  (`detectar formato → turnos normalizados`), con Codex como adaptador de
  referencia, indexada por `(cli, versión)` usando las fichas de
  escrubery.
- Forma: ADR nuevo + SPEC nueva por la frontera nueva (en
  `/Users/krisnova/www/aria/skopos/docs/adr/` y
  `/Users/krisnova/www/aria/skopos/docs/specs/`). Un archivo por
  frontera de F1, como manda `/Users/krisnova/www/aria/skopos/AGENTS.md`.
- No agregar el segundo CLI sobre la base rota: las precondiciones van
  primero, o el defecto se duplica por CLI.

## 5. Reglas del proyecto que aplican a todo lo anterior

- Español; Python 3.9+; `unittest` de stdlib; cero placeholders; cero
  dependencias especulativas. 🔒 instalar dependencias nuevas, `git push`
  y borrar/mover docs de decisiones cerradas requieren autorización
  explícita, una vez por operación.
- Editar no implica commit; commit no implica push.
- Toda métrica que cites en docs o reportes va fechada como snapshot
  (regla nacida de X-2).
- Antes de declarar terminado: `python3 -m unittest discover -s tests` en
  verde; diff leído completo; si tocaste specs/contratos, implementación
  y tests consistentes con lo que esos documentos prometen.
- Límites de tamaño por declaración: 800 líneas por archivo, 200
  `AGENTS.md`, 300 `README.md`.

## 6. Qué NO es parte de este encargo

- Reabrir o rediseñar P-001 (superada, ver §1).
- Integración con AN-KLA en cualquier dirección.
- Búsqueda semántica/embeddings (sigue como evaluación pendiente).
- Cualquier cambio fuera del repo de skopos.
