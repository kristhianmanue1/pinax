# Ronda adversarial — Codex CLI sobre visión Pinax v2 (2026-08-20)

**Método:** revisor independiente, contexto fresco, sólo lectura contra
git/código/docs de skopos y ektel. Incluye ronda adversarial obligatoria
sobre sus propias conclusiones. Transcripción fiel de la salida del CLI
(registrada por Pinax; Codex no persiste sesión entre ejecuciones).

**Veredicto: APROBADA CON CORRECCIONES.**

La v2 corrige los dos errores factuales de Ektel atribuidos a v1 y, salvo
una omisión material en Skopos, sus afirmaciones de estado resisten la
revisión de código, Git y documentación.

| Id | Nivel | Afirmación atacada | Veredicto | Evidencia |
|---|---|---|---|---|
| X-1 | ALTO | "Las tres primeras precondiciones" son cursor, eje de proyecto y `fragmento_completo`. | **REFUTADA.** P-001 v4 ordena: 1) eje de proyecto, 2) superficie de mutación/retención, 3) cursor de ingesta, 4) decisión sobre `fragmento_completo`, 5) detector C-5. La visión omite por completo la mutabilidad/retención y adelanta indebidamente `fragmento_completo`. Eso altera la prioridad de la deuda: sin corregir o definir retención, la vigencia queda irreversible. | P-001 §5 (puntos 1–5), `orquestador.py:51` |
| X-2 | MEDIO | "609 rollouts / 2.1 GB", 5 s y 40–100 h son medidos "hoy". | **NO CONFIRMABLE COMO ESTADO ACTUAL.** El código sí confirma el reparseo completo y el intervalo de 5 s, pero las cifras son una medición declarada para 2026-08-19, no una propiedad verificable desde el repositorio ni una medida repetida hoy. Deben etiquetarse como *snapshot documentado*. | `vigilante.py:8`, P-001 §4.9 |

## Afirmaciones que quedaron CIERTAS

- Skopos en `124d31c`, sin commits posteriores; sin cambios de `src/`
  desde ese commit. Sigue sin eje de proyecto, reparsea todos los JSONL y
  sirve el fragmento original crudo (`captura.py:91`, `vigilante.py:31`,
  `cli.py:20`).
- P-001 v4 redujo la justificación subsistente a cobertura; el parser es
  específico de rollouts Codex (P-001 §2.1, `captura.py:18`).
- El detector C-5 corregido sigue pendiente de ejecutarse contra corpus
  poblado (P-001 §4.5).
- Ektel en `2903114`; ADR-001–009 y enmiendas C1–C6/D1–D5 constan como
  consensuadas/aplicadas documentalmente. Spec v1.2: HS256 con cuatro
  dominios, CAS de nonce e identidad, C8 retirado
  (`docs/decisiones/enmienda-transversal-v3-2026-08-20.md:19`,
  `docs/especificacion/ektel-runtime-m0-m3-v1.md:121`).
- Caracterización Linux existe, clase L, aarch64/linuxkit, RSS por
  muestreo sin caracterizar (`docs/evidencia/caracterizacion-linux-2026-08-18.md:5,48`).
- Tras la revisión cruzada final, el consenso explícito del dueño sobre
  v1.2 precede a la autorización separada de M0 (spec §21,
  `docs/revisiones/revision-cruzada-final-2026-08-20.md:39`).
- El README de ektel aún dice que falta ejecutar/ampliar Linux;
  desactualizado frente a la evidencia del 18 de agosto (`README.md:50`).
- No existe `project-manifest.yaml` en skopos ni ektel.

## Ronda adversarial sobre sus propias conclusiones

- **X-1 sobrevive.** Releyó la fuente primaria P-001 y el código. La
  omisión de "superficie de mutación o retención" es literal y material.
- **X-2 sobrevive, rebajado a MEDIO.** No es prueba de que las cifras
  sean falsas; son evidencia histórica declarada, no estado actual
  reproducido en esta revisión.
- No elevó "consenso del dueño" a autenticidad humana independiente: lo
  reportó como hecho **documentado**.
- Tampoco elevó "F3 cerrado/pipeline real" a prueba de ejecución actual:
  no ejecutó Mongo/Ollama ni reprodujo el pipeline.

## Qué debe cambiar antes de asentar la visión

1. Reescribir Skopos §1 y el resumen conservando el orden real:
   **eje de proyecto → mutación/retención → cursor → `fragmento_completo`
   → detector C-5**.
2. Añadir explícitamente la mutabilidad/retención como condición de
   reapertura; no basta con eje, cursor y fragmento.
3. Cambiar las métricas 609/2.1 GB/40–100 h a "medición documentada al
   2026-08-19", salvo que se vuelva a medir.
4. Corregir el README de ektel en el mismo acto documental en que se
   emita el consenso/acta correspondiente.

```text
+--------------------------------------------------------------+
| firmante: Codex CLI                                          |
| modelo:    no expuesto por esta sesion                       |
| fecha:     2026-08-20                                        |
| alcance:   revision adversarial independiente de vision v2,  |
|            contra Git, codigo y docs de Skopos y Ektel       |
| limites:   solo lectura; no ejecute Mongo/Ollama, no repeti  |
|            mediciones del corpus ni autentique al dueno      |
| firma:     ASENTADA                                          |
+--------------------------------------------------------------+
```
