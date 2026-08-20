# Visión Pinax v2 — dirección para Skopos y Ektel (2026-08-20)

**Estado:** v2 — corregida por la ronda adversarial propia
(`ronda-adversarial-pinax-autocritica.md`, veredictos P-1..P-7). La v1
contenía dos BLOCKER factuales sobre ektel; esta versión los corrige.

**Rol de quien firma:** Pinax — catálogo y compilador del mapa del
ecosistema. Esta visión es análisis, no autoridad: no autoriza código,
no cambia estados de consenso, no sustituye al dueño.

**Fuentes verificadas en esta v2:** git log y `src/` de skopos
(`@124d31c`); git log, `docs/evidencia/`, `docs/revisiones/` de ektel
(`@2903114`); contexto del dueño (enmienda transversal v3 + revisión
cruzada final, 2026-08-20).

---

## 1. Skopos — memoria observada de agentes de IA

### Estado verificado

- F3 cerrado: pipeline real captura → `qwen3:8b` → Mongo → CLI → vigilante.
- Sin commits desde `124d31c` (P-001 v4, 2026-08-19). Las cinco
  precondiciones de P-001 v4 §5 **siguen sin tocarse** (verificado: sin
  campo de proyecto en `almacenamiento.py`, cero superficie de mutación en
  `src/`, vigilante sin cursor de ingesta).
- P-001 v4 redujo la justificación de la integración con AN-KLA a una
  sola: **cobertura de los agentes que Skopos no puede observar**
  (sólo parsea rollouts de Codex). Las demás cayeron contra código.

### Dirección

1. **P-001 permanece congelada.** Las tres primeras precondiciones son
   deuda propia de Skopos, no de la integración:
   - **Cursor de ingesta (C-10) primero.** Medido roto hoy: 609 rollouts /
     2.1 GB reparseados por ciclo con intervalo de 5 s; backfill estimado
     40–100 h. Es el defecto que ya impide operar.
   - **Eje de proyecto (C-9) segundo.** Sin él, `skopos query` mezcla
     turnos de toda la máquina y cualquier consolidación futura funde
     namespaces de forma irreversible (insert-only).
   - **Decisión sobre `fragmento_completo` (C-6) tercera.** Hoy se sirve
     crudo y sin redactar al agente consumidor: vector de inyección y
     motor del eco. Decidir: servir / redactar / marcar como
     no-instrucción en el contrato del CLI.
2. **Responder §7.3 antes de reabrir la integración:** ¿debe Skopos
   aprender a parsear otros CLIs en vez de observar AN-KLA? Si la
   respuesta es sí, la integración puede ser innecesaria entera. Ninguna
   de las cuatro revisiones de P-001 la evaluó.
3. Ejecutar el detector corregido de C-5 (P-001 §4.5) contra un corpus
   poblado antes de volver a discutir la hipótesis del eco.

## 2. Ektel — a un acto de autorización de M0

### Estado verificado (corregido respecto a v1)

- ADR-001–009 **consensuados por el dueño** (2026-08-19).
- Enmiendas C1–C6 (Codex) y D1–D5 (Claude) aplicadas: especificación
  **v1.2**; máquina de estados rehecha por operación; perfil criptográfico
  único byte-a-byte (HS256, cuatro dominios); CAS de nonce/identity;
  `durable` → `flush_protocol_completed`; C8 retirado de claims.
- **Caracterización Linux ya ejecutada** (2026-08-18,
  `docs/evidencia/caracterizacion-linux-2026-08-18.md`, 5/5 OK, clase L —
  una corrida, un entorno, aarch64/linuxkit; no V ni R).
- Revisión cruzada final (`2903114`): ADR/tabla/spec v1.2 internamente
  consistentes; suite 8 tests OK (3 skips Linux-only).
- **Lo único pendiente del criterio de adopción (§21): consenso
  explícito del dueño sobre v1.2 → autorización de M0** (alcance ya
  definido: wire schemas v1 + vectores dorados + dos parsers de
  referencia, uno clean-room).

### Dirección

1. **Pinax no añade requisitos.** El proceso de ektel ya cubrió lo que mi
   v1 pedía. El siguiente acto es del dueño: consenso de v1.2 y firma del
   acta de autorización de M0.
2. **Deuda editorial con efecto real:** el README de ektel afirma "falta
   ejecutarla y ampliarla en Linux" — falso desde el 2026-08-18. Ese
   párrafo desactualizado es la trampa exacta en la que cayó la visión v1
   de Pinax. Corregirlo junto con el acta de consenso.
3. **Vigilar en M0 lo que la evidencia Linux dejó abierto:** RSS por
   muestreo sigue sin caracterizar en Linux y la evidencia es clase L en
   aarch64-linuxkit — si M1–M3 apuntan a x86_64 o a Linux nativo (no
   linuxkit), la tabla de garantías debe re-sondear antes de promover
   cualquier clase. Esto ya está dentro de la disciplina de ektel; se
   registra aquí para que el mapa no lo pierda.
4. **Respetar la stop rule:** M0 produce sólo contratos congelables. La
   API pública se etiqueta `experimental` hasta M0 + implementación
   independiente.

## 3. Convergencia de ecosistema (etiquetada como dirección, no hecho)

- **RuntimeEvent (ektel) ↔ observación (Skopos):** cuando ektel exista,
  sus eventos serán una fuente que Skopos no puede observar hoy (no son
  rollouts Codex). No diseñar el contrato ahora; sólo no cerrar puertas:
  ektel ya versiona sus wire schemas y Skopos debería tratar su parser de
  Codex como el primero de una familia. *Etiqueta: especulativa, no
  verificada contra el wire format.*
- **AN-KLA desde dos lados:** ektel lo usa como memoria de proyecto real;
  Skopos lo analiza como sistema a integrar. La experiencia de ektel como
  consumidor es evidencia que la próxima ronda de P-001 (si se reabre)
  debería incorporar.
- **Deuda de Pinax:** ni skopos ni ektel tienen `project-manifest.yaml`;
  el mapa los muestra `missing_manifest`. Ektel tiene claims/no-claims
  consensuados (material listo para `no_ofrece`/`pospuesto`); Skopos tiene
  riesgos declarados en README. Ambos son candidatos maduros al flujo de
  adopción (transcripción → revisión → confirmación del mantenedor →
  autorización).

## 4. Resumen ejecutivo

| Proyecto | Próximo acto | Quien decide |
|---|---|---|
| Skopos | Cursor de ingesta → eje de proyecto → `fragmento_completo`; luego responder §7.3 | Dueño autoriza ciclo de código |
| Ektel | Consenso de v1.2 + autorización de M0 (sólo contratos) | Dueño (acto de consenso) |
| Pinax | Manifiestos de ambos tras los actos anteriores | Mantenedor de cada proyecto |

---

## Firmas

```
firmante:  Kimi (Moonshot AI) — rol: Pinax, vision de ecosistema
modelo:    Kimi (kimi-k2, via Kimi Work)
fecha:     2026-08-20
alcance:   vision v2; P-1..P-3 de la autocritica incorporados;
           verificado contra git/codigo de skopos@124d31c y
           ektel@2903114 y contra el contexto del dueno 2026-08-20
limites:   la seccion 3 es direccion especulativa etiquetada;
           esta vision no autoriza codigo ni cambia consensos
firma:     ASENTADA — Kimi/Pinax, 2026-08-20, previo al envio de
           rondas a Codex CLI y Claude CLI
```
