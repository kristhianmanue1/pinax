# Visión Pinax FINAL — dirección para Skopos y Ektel (2026-08-20)

**Estado:** FINAL — v2 corregida tras las rondas adversariales
independientes de Codex CLI (X-1, X-2) y Claude CLI (Y-1..Y-7), ambas con
autocrítica propia obligatoria y firma asentada. Veredictos: ambas
**aprobadas con correcciones**; este documento las incorpora todas.

**Cadena de evidencia:**
- `ronda-adversarial-pinax-autocritica.md` — P-1..P-7 (Kimi/Pinax).
- `vision-pinax-v2.md` — objeto revisado, firmado por Pinax antes del envío.
- `ronda-adversarial-codex.md` — X-1, X-2 (Codex CLI, firma asentada).
- `ronda-adversarial-claude.md` — Y-1..Y-7 (Claude CLI / claude-opus-5,
  firma asentada).

**Rol:** Pinax — catálogo del ecosistema. Esto es análisis, no autoridad:
no autoriza código, no cambia consensos, no sustituye al dueño.

**Fuentes y su independencia (declaración exigida por Y-3):** verificado
contra git/código/docs de `skopos@124d31c` y `ektel@2903114`, y contra el
contexto del dueño (2026-08-20). **Dependencia declarada:** la revisión
cruzada final de ektel (`docs/revisiones/revision-cruzada-final-2026-08-20.md`)
es interna y fue ejecutada por el mismo agente (Kimi Work) que firma esta
visión; su dictamen verifica consistencia interna, no adopción. Las
conclusiones de esta visión que apoyan el acto del dueño no descansan sólo
en ella: descansan en el git log y en las dos rondas adversariales
independientes adjuntas.

---

## 1. Skopos — memoria observada de agentes de IA

### Estado verificado

- F3 cerrado: pipeline real captura → `qwen3:8b` → Mongo → CLI → vigilante.
- Sin commits desde `124d31c` (P-001 v4, 2026-08-19); las cinco
  precondiciones de P-001 v4 §5 siguen sin tocarse (verificado por Codex y
  Claude contra código: sin campo de proyecto, insert-only, vigilante sin
  cursor).
- P-001 v4 redujo la justificación de la integración con AN-KLA a una
  sola: **cobertura de los agentes que Skopos no puede observar**.

### Dirección (orden real de P-001 §5, restaurado tras X-1)

P-001 permanece congelada. Las precondiciones, **en el orden de la
propuesta y sin omitir ninguna**:

1. **Eje de proyecto (C-9).** Sin campo de proyecto en el documento de
   Mongo, consolidar funde namespaces de forma irreversible.
2. **Superficie de mutación o retención (C-8).** Sin ella, la vigencia
   consolidada se pudre sin reparación posible. *(Omitida en la v2;
   restaurada por X-1 de Codex.)*
3. **Cursor de ingesta (C-10).** Medición **documentada al 2026-08-19**
   (X-2): 609 rollouts / 2.1 GB reparseados por ciclo, intervalo 5 s,
   backfill estimado 40–100 h. **Advertencia (Y-4):** este acto no es
   reparación de deuda neutra — obliga a revisar o acotar **ADR-005**
   (la dedup vive en Mongo por decisión registrada) y a cerrar la
   **decisión 8 de la hoja de ruta** (política de arranque del vigilante,
   pendiente). El dueño debe autorizarlo sabiendo que hay un ADR aceptado
   detrás.
4. **Decisión sobre `fragmento_completo` (C-6).** Hoy se sirve crudo, sin
   redactar y —**añadido por Y-5 de Claude**— se **relee del archivo
   original por offsets sin verificación de integridad y con fallos
   silenciosos** (`cli.py:20-27`). La decisión tiene cuatro opciones, no
   tres: servir / redactar / marcar como no-instrucción / **persistir el
   fragmento o sellar el origen con hash+tamaño**.
5. **Ejecutar el detector corregido de C-5** contra un corpus poblado.

Y antes de reabrir la integración: responder la pregunta 3 de P-001 §7 —
*¿debe Skopos aprender a parsear otros CLIs en vez de observar AN-KLA?* —
que ninguna ronda ha evaluado y que puede hacer innecesaria la integración
entera.

## 2. Ektel — a un acto de autorización de M0

### Estado verificado (con los matices de Y-1, Y-2, Y-6)

- ADR-001–009 aceptados por consenso del dueño el 2026-08-19; **ADR-005,
  ADR-007 y ADR-008 fueron enmendados después** (enmiendas C1–C6/D1–D5,
  spec v1.2), con acta, bajo la regla de gobernanza que el propio repo
  adoptó. Lo consensuado y lo vigente no son el mismo texto: **las
  enmiendas post-consenso caen dentro del acto de consenso de v1.2** (Y-6).
- **Caracterización Linux: ejecutada pero no cerrada (Y-1).** La corrida
  clase L del 2026-08-18 cubrió **5 pruebas**; la suite vigente tiene **8**,
  y las pruebas añadidas después —incluidas las **Linux-only**, que hacen
  skip en Darwin— **no tienen ejecución registrada en ningún entorno**.
  El hueco Linux NO está cerrado para la suite que hoy sostiene la tabla
  de garantías.
- README desactualizado **en su primera mitad** (Y-2): «ejecutarla» ya
  existe; **«ampliarla» sigue siendo cierto** — RSS por muestreo sigue sin
  caracterizar en Linux (clase L, aarch64/linuxkit, no V ni R). La
  corrección del README debe conservar ese no-claim, no borrarlo.
- Revisión cruzada final (`2903114`): ADR/tabla/spec v1.2 internamente
  consistentes — con la dependencia de independencia ya declarada arriba.
- Pendiente del criterio de adopción (**§19 de la spec v1.2**; propuesta
  §21 — Y-7): consenso explícito del dueño sobre v1.2 y autorización
  **separada de M0 y de cada hito posterior**.

### Dirección

1. **El siguiente acto es del dueño:** consenso de v1.2 (que incluye las
   enmiendas post-2026-08-19) y firma del acta de autorización de M0
   (wire schemas v1 + vectores dorados + dos parsers, uno clean-room).
   *La frase «Pinax no añade requisitos» queda condicionada (Y-3): es
   válida sólo si el dueño acepta la revisión cruzada interna como
   suficiente; si exige verificación independiente de la consistencia
   interna, ésa es la única pieza que faltaría.*
2. **Antes o dentro de M0:** ejecutar en Linux la **suite vigente de 8
   pruebas** (Y-1) — en particular las Linux-only sin ejecución
   registrada — y registrar el acta en `docs/evidencia/`. Una
   caracterización de la suite vieja no sostiene la tabla de garantías de
   la suite actual.
3. **Corregir el README en el mismo acto documental del consenso**, con
   redacción que conserve el no-claim: la ejecución Linux existe (5
   pruebas, clase L); la ampliación (suite completa, RSS por muestreo)
   sigue pendiente.
4. **Respetar la stop rule:** M0 produce sólo contratos congelables; API
   etiquetada `experimental` hasta M0 + implementación independiente.

## 3. Convergencia de ecosistema (etiqueta: especulativa, no verificada)

- **RuntimeEvent (ektel) ↔ observación (Skopos):** los eventos de ektel
  serán una fuente que Skopos no puede observar hoy. No diseñar el
  contrato ahora; sólo no cerrar puertas: ektel ya versiona sus wire
  schemas; Skopos debería tratar su parser de Codex como el primero de
  una familia.
- **AN-KLA desde dos lados:** ektel lo usa como memoria de proyecto real;
  Skopos lo analiza como sistema a integrar. La experiencia de ektel como
  consumidor es evidencia para cualquier reapertura de P-001.
- **Deuda de Pinax:** ni skopos ni ektel tienen `project-manifest.yaml`
  (`missing_manifest` en el mapa). Ambos tienen material maduro para el
  flujo de adopción: ektel con claims/no-claims consensuados, Skopos con
  riesgos declarados.

## 4. Resumen ejecutivo

| Proyecto | Próximo acto | Quien decide |
|---|---|---|
| Skopos | Precondiciones en orden P-001 §5 (C-9 → C-8 → C-10* → C-6** → C-5); luego pregunta §7.3. *C-10 toca ADR-005 y la decisión 8. **C-6 incluye la opción de persistir/sellar. | Dueño autoriza ciclo de código |
| Ektel | Consenso de v1.2 (incluye enmiendas post-consenso) → autorización de M0; corrida Linux de la suite de 8 antes/dentro de M0 | Dueño (acto de consenso) |
| Pinax | Manifiestos de ambos tras los actos anteriores | Mantenedor de cada proyecto |

---

## Firmas

Las tres firmas quedaron asentadas **antes** de este documento final:
la de Pinax en `vision-pinax-v2.md` (previo al envío de rondas), y las de
Codex y Claude en sus actas de ronda. Aquí se reasientan sobre el texto
final, que incorpora X-1, X-2 e Y-1..Y-7.

```
+------------------------------------------------------------------+
| firmante:  Kimi (Moonshot AI, kimi-k2 via Kimi Work) — Pinax      |
| fecha:     2026-08-20                                            |
| alcance:   vision final; autocritica P-1..P-7; correcciones      |
|            X-1/X-2 (Codex) e Y-1..Y-7 (Claude) incorporadas      |
| limites:   la seccion 3 es especulativa etiquetada; no autoriza  |
|            codigo ni cambia consensos; la revision cruzada de    |
|            ektel citada es interna y de este mismo agente        |
| firma:     ASENTADA — Kimi/Pinax, 2026-08-20                     |
+------------------------------------------------------------------+
| firmante:  Codex CLI — revisor adversarial independiente          |
| modelo:    no expuesto por la sesion                              |
| fecha:     2026-08-20                                            |
| alcance:   ronda adversarial + autocritica propia; X-1, X-2;     |
|            veredicto APROBADA CON CORRECCIONES (acta propia)     |
| limites:   solo lectura; sin Mongo/Ollama; sin repetir           |
|            mediciones; sin autenticar al dueno                   |
| firma:     ASENTADA en ronda-adversarial-codex.md, 2026-08-20    |
+------------------------------------------------------------------+
| firmante:  Claude CLI — revisor adversarial independiente         |
| modelo:    claude-opus-5 (Opus 5, Claude Code CLI)                |
| fecha:     2026-08-20                                            |
| alcance:   ronda adversarial + autocritica propia; Y-1..Y-7;     |
|            veredicto APROBADA CON CORRECCIONES (acta propia)     |
| limites:   no ejecuto suites ni Mongo/Ollama; Y-5 es inspeccion  |
|            de codigo, no reproduccion                            |
| firma:     ASENTADA en ronda-adversarial-claude.md, 2026-08-20   |
+------------------------------------------------------------------+
```
