# Ronda adversarial independiente — Claude CLI sobre `vision-pinax-v2.md`

**Fecha:** 2026-08-20. **Revisor:** Claude CLI (contexto fresco, repos como
única fuente). **Objeto:** `vision-pinax-v2.md` (firmante Kimi/Pinax).
**Método:** refutación de afirmaciones de **estado** contra código, git y
docs de `aria/skopos@124d31c` y `aria/ektel@2903114`.

**Coordinación con la ronda de Codex:** no repito X-1 (la visión omite la
precondición de mutación/retención C-8 y reordena las cinco precondiciones
de P-001 §5) ni X-2 (las métricas deben declararse como instantánea del
2026-08-19). Ambos los doy por buenos: verifiqué que P-001 §5 lista
`C-9 → C-8 → C-10 → C-6 → C-5` y que la visión enumera `C-10 → C-9 → C-6`
omitiendo C-8, y que las cifras 609 / 2.1 GB provienen de
`P-001:298-299,392,439` con fecha 2026-08-19. Este acta busca lo que esa
ronda no cubrió.

---

## 1. Hallazgos

### Y-1 · ALTO — «Caracterización Linux ya ejecutada (5/5 OK)» no cubre la suite actual

**Afirmación atacada:** §2, "Estado verificado": «**Caracterización Linux ya
ejecutada** (2026-08-18, `docs/evidencia/caracterizacion-linux-2026-08-18.md`,
5/5 OK, clase L)», usada en §2.2 para declarar cerrado el hueco de Linux.

**Veredicto:** **PARCIALMENTE FALSA en su alcance.** La corrida existe, pero
cubre 5 pruebas y la suite vigente tiene 8; al menos tres pruebas de la suite
actual —incluidas pruebas `Linux-only`— no tienen ejecución registrada en
ningún entorno.

**Evidencia:**
- `docs/evidencia/caracterizacion-linux-2026-08-18.md` — corrida
  `2026-08-18T16:36:43Z`, «5 de 5 pruebas: OK».
- `git show 2289d8d:tests/escape/test_host_characterization.py | grep -c "def test"` → **7**;
  `2289d8d^` → **5**. El commit `2289d8d` («cerrar hueco E2 (subreaper)…»)
  es del **2026-08-18 11:20:10 -0600**, es decir **cinco horas antes** de la
  corrida que reporta 5/5. En Linux **ninguna** prueba de la suite hace skip
  (los `skipUnless` son `posix`, `Darwin/Linux` o `Linux`:
  `tests/escape/test_host_characterization.py:25,42,63,101,131,167,204,255`),
  luego una corrida Linux del árbol de ese momento debía reportar 7, no 5.
- Suite actual: `grep -c "def test"` → **8**; la revisión cruzada
  (`docs/revisiones/revision-cruzada-final-2026-08-20.md:22`) registra «8 tests,
  3 skips Linux-only», corrida **en Darwin**.
- Consecuencia: `test_subreaper_recovers_orphaned_grandchild_cpu`
  (`:255`, `Linux-only`) y las demás Linux-only añadidas después de la corrida
  **hacen skip en Darwin y no aparecen en la corrida Linux**: no tienen
  ejecución registrada en el repositorio.

**Efecto:** la visión ofrece al dueño, como insumo del acto de autorización de
M0, un estado donde el hueco Linux está cerrado. La evidencia clase L no
respalda la suite que hoy sostiene la tabla de garantías.

### Y-2 · ALTO — «El README es falso desde el 2026-08-18» se contradice con la propia §2.3

**Afirmación atacada:** §2, dirección 2: «el README de ektel afirma "falta
ejecutarla y ampliarla en Linux" — **falso desde el 2026-08-18**».

**Veredicto:** **SOBREDECLARADA.** La frase del README tiene dos conjuntos.
«Ejecutarla» quedó obsoleto el 2026-08-18; «ampliarla» **sigue siendo cierto**
por admisión de la propia visión.

**Evidencia:**
- `README.md:53-55` — «La caracterización autorizada ya cubre cuatro casos
  seguros en Darwin; falta ejecutarla **y ampliarla** en Linux».
- `docs/evidencia/caracterizacion-linux-2026-08-18.md:50` — «RSS por muestreo
  sigue sin caracterizar aquí; esta suite no lo prueba».
- `vision-pinax-v2.md` §2, dirección 3 — «RSS por muestreo sigue sin
  caracterizar en Linux y la evidencia es clase L en aarch64-linuxkit».
- Sumado a Y-1: tampoco «ejecutarla» está completo para la suite vigente.

**Efecto:** corregir el README con la premisa «falso» sustituye una
declaración conservadora por una optimista en la **superficie pública de
claims** de ektel, justo el tipo de defecto que su tabla claims/no-claims
existe para impedir.

### Y-3 · ALTO — La verificación de ektel se apoya en una revisión no independiente, sin declararlo

**Afirmación atacada:** §2: «Revisión cruzada final (`2903114`): ADR/tabla/spec
v1.2 internamente consistentes», y §2, dirección 1: «**Pinax no añade
requisitos.** El proceso de ektel ya cubrió lo que mi v1 pedía».

**Veredicto:** **CIERTA EN EL HECHO, VICIADA EN LA INFERENCIA.** El documento
citado se autodescribe como **no externo** y fue ejecutado por el mismo agente
(«Kimi Work») que firma esta visión. La visión lo cita como fuente verificada
sin declarar esa dependencia.

**Evidencia:**
- `docs/revisiones/revision-cruzada-final-2026-08-20.md:4-8` — «Ejecutor:
  agente mantenedor (Kimi Work)… **No es una revisión externa**: es el último
  paso interno de la ruta de cierre».
- Firma de la visión: «firmante: Kimi (Moonshot AI)… modelo: kimi-k2, via
  Kimi Work».
- La misma revisión, `:37-40`, declara su hallazgo residual 3: «La autoridad de
  la especificación v1.2 sigue pendiente de consenso: **este documento no la
  adopta**».

**Efecto:** el argumento «no añado requisitos porque el proceso ya cubrió lo
que pedía mi v1» se apoya en una autoverificación del mismo firmante. Es
exactamente el sesgo que la v1 sufrió (leer el README) trasladado un nivel.

### Y-4 · MEDIO — «Cursor de ingesta primero» exige tocar una decisión arquitectónica vigente, y la visión no lo dice

**Afirmación atacada:** §1, dirección 1: «Cursor de ingesta (C-10) primero…
**Es el defecto que ya impide operar**».

**Veredicto:** **CIERTA COMO SÍNTOMA, INCOMPLETA COMO ACTO.** La relectura
completa por ciclo no es un descuido: es una decisión registrada (ADR-005), y
la política de arranque del vigilante figura como decisión **pendiente**, no
como bug. Ordenar «cursor primero» implica revisar o acotar ADR-005 y cerrar
la decisión 8 de la hoja de ruta; la visión no nombra ninguno de los dos actos.

**Evidencia:**
- `src/skopos/vigilante.py:8-10` — «La deduplicación entre ciclos vive en
  Mongo, no en un cursor local (**ADR-005**): cada ciclo relee los rollouts
  completos, pero `procesar_rollout` omite los turnos cuyo turn_id ya está
  guardado».
- `docs/f1-maquina-estados.md:31` — dedup por `turn_id` ya guardado (ADR-005).
- `docs/hoja-de-ruta.md:19` — «| 8 | Política de arranque del vigilante
  (backfill opt-in vs "desde ahora") | **Pendiente** | — |».

**Efecto:** el dueño podría autorizar «cursor de ingesta» creyendo que es
reparación de deuda, cuando es un cambio de contrato con un ADR aceptado
detrás.

### Y-5 · MEDIO — El encuadre de C-6 omite el riesgo de corrección (offsets sin integridad)

**Afirmación atacada:** §1, dirección 1: «`fragmento_completo`… Hoy se sirve
crudo y sin redactar al agente consumidor: vector de inyección y motor del
eco. **Decidir: servir / redactar / marcar como no-instrucción**».

**Veredicto:** **CIERTA PERO INSUFICIENTE.** Las tres opciones son todas de
seguridad/semántica; ninguna cubre el defecto de correctitud que el código
exhibe: el fragmento no está almacenado, se **relee del archivo original en
tiempo de consulta** por offsets capturados en la ingesta, sin verificación de
integridad y con fallos silenciosos.

**Evidencia:**
- `src/skopos/cli.py:20-27` — abre `ruta_origen`, `seek(offset_inicio)`,
  `read(offset_fin - offset_inicio)`, `decode(..., errors="replace")`, y
  `except OSError: return None`.
- `src/skopos/cli.py:38-41` — se sirve tal cual dentro del CONTRATO
  `cli-skopos-query v1`.
- No hay hash ni tamaño guardado que valide el archivo: `almacenamiento.py`
  sólo hace `insert_one` del documento (`:65`).

**Efecto:** si el rollout rota, se trunca o se edita entre ingesta y consulta,
`skopos query` devuelve bytes de otro turno (o `null`) **sin señal de error**.
Una cuarta opción —persistir el fragmento o sellar el archivo con
hash/tamaño— debe estar en la decisión, o C-6 se cerrará dejando el defecto.

### Y-6 · MEDIO — «ADR-001–009 consensuados» sin decir que el texto consensuado fue enmendado después

**Afirmación atacada:** §2: «ADR-001–009 **consensuados por el dueño**
(2026-08-19)» presentado como estado vigente.

**Veredicto:** **CIERTA EN LA FECHA, ENGAÑOSA COMO ESTADO ACTUAL.** El
consenso es del `fecf1b3` (2026-08-19); ADR-005/007/008 fueron **modificados
después** (renombre `durable` → `flush_protocol_completed`, tipos de resultado
por operación) en `82f7a19`. Lo consensuado y lo vigente no son el mismo texto.

**Evidencia:**
- `git log`: `fecf1b3` «consenso del dueno — ADR-001 a ADR-009 aceptados
  (2026-08-19)»; `82f7a19` (posterior) «C8 retirado; durable renombrado
  flush_protocol_completed; outcomes por operacion».
- `docs/especificacion/…` §19.5 — «ADR-001 a ADR-009 aceptados; **enmiendas
  posteriores con acta**, por la regla nacida del defecto de gobernanza…».

**Efecto:** la tabla de §4 le dice al dueño que su único acto es «consenso de
v1.2»; los ADR enmendados post-consenso caen dentro de ese acto y conviene
decirlo, porque el propio repo nació de un defecto de gobernanza de ese tipo.

### Y-7 · BAJO — Cita `§21` del criterio de adopción

**Afirmación atacada:** «Lo único pendiente del criterio de adopción (**§21**)».

**Veredicto:** **IMPRECISA, NO FALSA.** En la especificación v1.2 el criterio
vive en **§19** («Riesgos y criterio de adopción», `:537-560`), que reproduce
el de la *propuesta* §21. Además el punto 6 dice «autorización separada de M0
**y de cada hito**»: la visión sólo refleja M0 (coherente con la stop rule que
sí cita, pero la cita numérica exige saber a qué documento pertenece).

---

## 2. Lo que resulta CIERTO (verificado, sin objeción)

| Afirmación de la visión | Evidencia |
|---|---|
| Skopos sin commits desde `124d31c` (P-001 v4, 2026-08-19) | `HEAD = 124d31c`, fecha `2026-08-19 21:53:23 -0600`, worktree limpio |
| Sin campo de proyecto y **cero superficie de mutación** en `src/` | `almacenamiento.py` sólo `insert_one` (`:65`); sin `update_one`/`delete`/`replace_one` |
| Vigilante sin cursor de ingesta | `vigilante.py:8-10,28,44-47` |
| F3 cerrado: captura → `qwen3:8b` → Mongo → CLI → vigilante | `README.md:16,30`; `analisis.py:41` (`MODELO_POR_DEFECTO = "qwen3:8b"`) |
| Skopos sólo parsea rollouts de Codex | `captura.py:1-5,18` (`CLI_ORIGEN = "codex-cli"`) |
| P-001 v4 dejó **una sola** justificación (cobertura) | `P-001` §2.1, §6 `:338-339`, §7 punto 2 |
| §7.3 nunca fue evaluada por ninguna ronda | `P-001` §7 punto 3 `:363-366` — «Alternativa que ninguna ronda evaluó» (la numeración `§7.3` es abreviatura del ítem 3, no una subsección) |
| `fragmento_completo` se sirve crudo y sin redactar | `cli.py:20-27,38-41` |
| ektel: README con párrafo desactualizado sobre Linux | `README.md:53-55` (ver Y-2 por el matiz) |
| Suite: 8 tests OK con 3 skips Linux-only | `revision-cruzada-final-2026-08-20.md:22` (corrida Darwin; ver Y-1) |
| Evidencia Linux clase L, aarch64/linuxkit, no V ni R | `caracterizacion-linux-2026-08-18.md:5-8,29-33` |
| Ni skopos ni ektel tienen `project-manifest.yaml` | ausente en ambos árboles |
| §3 correctamente etiquetada como especulativa | autoetiquetado explícito en el texto |

---

## 3. Autocrítica adversarial de mis propias conclusiones

Ataqué cada hallazgo asumiendo que estaba equivocado.

- **Y-1 — sobrevive, con una reserva declarada.** Contraataque: el script
  `characterize-linux.sh` monta el repo `:ro` desde el árbol de trabajo, así
  que la corrida de las 16:36 pudo usar un checkout previo a `2289d8d`, y «5
  de 5» sería fiel a lo ejecutado. Concedo esa lectura: **no puedo afirmar mala
  fe ni error en el conteo**. Lo que no cambia bajo ninguna lectura es la
  conclusión operativa: no existe corrida Linux registrada de la suite de 8
  pruebas, y las Linux-only añadidas después no se ejecutan en Darwin. Reformulo
  el hallazgo de «el reporte 5/5 es inconsistente» a «la evidencia Linux no
  cubre la suite vigente». Con esa reformulación, ALTO se mantiene.
- **Y-2 — sobrevive.** Contraataque: «ampliarla» podría leerse como ambición
  futura, no como pendiente. Lo rechazo: la propia visión lista el pendiente
  concreto (RSS por muestreo) en su §2.3, dos párrafos después de llamar
  «falso» al README. Es contradicción interna del documento revisado, no
  interpretación mía.
- **Y-3 — sobrevive, acotado.** Contraataque: la revisión cruzada declara su
  propio carácter interno, así que nadie fue engañado. Acoto: **no impugno el
  contenido** de la revisión cruzada (verifiqué por muestreo su dictamen sobre
  dominios criptográficos y renombres, y es correcto). Impugno que la visión
  lo cite en «Fuentes verificadas» sin declarar que el verificador y el
  firmante son el mismo agente, mientras concluye «no añado requisitos».
- **Y-4 — lo degrado de ALTO a MEDIO.** Contraataque válido: un cursor de
  ingesta puede coexistir con la deduplicación en Mongo (ADR-005 decide *dónde
  vive la dedup*, no *que haya que releer todo*). Retiro la formulación fuerte
  («la visión pide revocar ADR-005 en silencio»). Queda el hueco real: la
  visión no menciona ADR-005 ni la decisión 8 de la hoja de ruta, ambos
  vigentes y tocados por su recomendación.
- **Y-5 — sobrevive.** Contraataque: podría ser hallazgo fuera de alcance,
  ya que P-001 §4.4 trata C-6 como problema de seguridad. Lo mantengo: la
  visión convierte C-6 en una **decisión de tres opciones** y esa decisión, tal
  como está enunciada, no puede cerrar el defecto que el código exhibe. Es
  crítica a la visión, no al proyecto.
- **Y-6 — sobrevive degradado a MEDIO.** Contraataque fuerte: la visión sí dice
  «enmiendas C1–C6 y D1–D5 aplicadas» y sitúa el consenso pendiente sobre
  v1.2, lo que implica que v1.2 no está consensuada. Concedo que no hay
  falsedad; el defecto es de presentación en la viñeta «ADR-001–009
  consensuados», que aislada sugiere ADRs cerrados.
- **Y-7 — se mantiene en BAJO.** Es imprecisión de cita; no cambia ninguna
  decisión. La incluyo por trazabilidad, no como objeción.
- **Retirado antes de publicar:** un borrador acusaba a la visión de afirmar
  falsamente «cero superficie de mutación». Lo verifiqué en
  `almacenamiento.py` y la afirmación es correcta; el hallazgo se retira (y
  el punto adyacente ya está cubierto por X-1 de Codex, que no repito).
- **Límite de mi propia ronda:** no ejecuté las suites de ninguno de los dos
  repos ni levanté Mongo/Ollama. Y-5 es lectura de código, no reproducción; su
  clase de evidencia es **inspección**, no **L**.

---

## 4. Veredicto

### APROBADA CON CORRECCIONES

La visión v2 es sustancialmente correcta: sus afirmaciones sobre el estado de
Skopos resisten la confrontación con el código casi punto por punto, y su
lectura de ektel corrige de verdad los BLOCKER de la v1. No la rechazo. Pero
su sección de ektel presenta como **cerrado** un hueco (Linux) que la evidencia
del repo no cierra, y lo hace apoyada en una verificación producida por el
mismo firmante.

**Debe cambiar, antes de circular como insumo del acto del dueño:**

1. **(Y-1)** Reescribir la viñeta de caracterización Linux: «corrida clase L
   del 2026-08-18 sobre 5 pruebas; la suite vigente tiene 8 y no hay corrida
   Linux registrada de ella». Añadir a §2.3 la vigilancia de las pruebas
   Linux-only sin ejecución registrada.
2. **(Y-2)** Sustituir «falso desde el 2026-08-18» por «desactualizado en su
   primera mitad: la ejecución existe; **la ampliación sigue pendiente**», y
   proponer redacción de README que conserve el no-claim de RSS.
3. **(Y-3)** Declarar en «Fuentes verificadas» que la revisión cruzada final
   es interna y del mismo agente que firma esta visión; y condicionar «Pinax no
   añade requisitos» a esa dependencia.
4. **(Y-4)** En §1, dirección 1, nombrar ADR-005 y la decisión 8 de la hoja de
   ruta como lo que el «cursor primero» obliga a cerrar.
5. **(Y-5)** Añadir a la decisión sobre `fragmento_completo` una cuarta opción:
   persistir el fragmento o sellar el origen (hash/tamaño), por la relectura
   por offsets sin integridad de `cli.py:20-27`.
6. **(Y-6)** Anotar que ADR-005/007/008 fueron enmendados tras el consenso del
   2026-08-19 y quedan dentro del acto de consenso de v1.2.
7. **(Y-7)** Citar §19 de la especificación v1.2 (o decir «propuesta §21»).
8. **(X-1, X-2 de Codex)** Restaurar C-8 y el orden de P-001 §5; fechar las
   métricas como instantánea del 2026-08-19.

Con 1–3 aplicados, la visión puede acompañar el acto del dueño. Sin ellos, su
§2 induce a autorizar M0 sobre un estado de evidencia mejor de lo que el
repositorio sostiene.

---

## Firmas

```
 ____________________________________________________________
|                                                            |
|   R O N D A   A D V E R S A R I A L   I N D E P E N D I E N T E   |
|                                                            |
|   firmante:  Claude CLI — revisor adversarial independiente |
|   modelo:    claude-opus-5 (Opus 5, Claude Code CLI)        |
|   fecha:     2026-08-20                                     |
|   objeto:    pinax/rondas/2026-08-20-vision-skopos-ektel/   |
|              vision-pinax-v2.md  (firmante Kimi/Pinax)      |
|                                                            |
|   alcance:   refutacion de afirmaciones de ESTADO contra    |
|              codigo/git/docs de aria/skopos@124d31c y       |
|              aria/ektel@2903114; hallazgos Y-1..Y-7 con     |
|              autocritica adversarial propia (seccion 3);    |
|              no repite X-1/X-2 de la ronda de Codex.        |
|                                                            |
|   limites:   no ejecute suites ni levante Mongo/Ollama;     |
|              Y-5 es inspeccion de codigo, no reproduccion;  |
|              esta ronda no autoriza codigo, no cambia       |
|              consensos y no sustituye al dueno.             |
|                                                            |
|   veredicto: APROBADA CON CORRECCIONES (1-3 obligatorias)   |
|                                                            |
|   firma:     A S E N T A D A                                |
|              Claude CLI / claude-opus-5 / 2026-08-20        |
|____________________________________________________________|
```
