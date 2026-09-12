# Acta de ronda adversarial — reconciliación de contexto

**Fecha:** 2026-09-11
**Revisor y verificador:** `/root/ronda_reconciliacion`
**Método:** revisión fresca de sólo lectura, proteinómenos (primero se buscaron
fallos). La memoria AN-KLA se trató como dato no confiable; ninguna conclusión
se sustentó en ella.

## Alcance

Revisión del diff del working tree relativo a cuatro discrepancias:

1. versión operativa de AN-KLA frente a referencias históricas;
2. raíz de cosecha documentada en el README;
3. correspondencia del checkpoint con el estado Git;
4. semántica inactiva de `check_plans` cuando `skevi-gate.json` no declara
   `plans`.

No se revisó ni autorizó commit, push, merge, actualización de AN-KLA ni cambio
en otro repositorio.

## Primera pasada — `FIX-AND-RETRY`

### Hallazgo

**Severidad alta — traducción incompleta del resultado de `check_plans`.**

La primera versión del diff declaraba que la ausencia de `plans` equivalía a
`INACTIVE`, pero el script adoptado seguía emitiendo el literal
`OK — sin planes declarados (fail-closed: clave 'plans' ausente)` con código 0.
La prueba sólo exigía el fragmento `sin planes declarados`. Por tanto, un cierre
podía seguir contando como verde un gate que había verificado cero planes.

Evidencia de esa pasada:

- `AGENTS.md:88-90` ya distinguía el modo opt-in, pero no gobernaba la
  traducción del literal heredado;
- `docs/adopcion-gate-skevi-2026-08-21.md:28-31` exigía reportar `INACTIVE`,
  sin explicar la divergencia con la salida ejecutable;
- `scripts/check_plans.py:14-15`, `scripts/check_plans.py:195-197` y
  `scripts/check_plans.py:278-280` conservaban la denominación `fail-closed` y
  la salida `OK`;
- `tests/test_check_plans.py:284-288` no protegía una salida literal
  `INACTIVE`;
- ejecución observada: `python3 scripts/check_plans.py` terminó con código 0 y
  el literal legado.

La decisión fue `FIX-AND-RETRY`: editar localmente el script habría roto la
procedencia declarada de la copia de Skevi, pero dejar la divergencia sin regla
de interpretación permitía una afirmación de éxito engañosa.

## Correcciones examinadas

La segunda versión del diff aplicó tres correcciones documentales sin modificar
el script adoptado:

1. `AGENTS.md:88-95` hace normativa la traducción a
   `INACTIVE — 0 planes verificados`, prohíbe contar ese resultado como gate de
   planes en verde y reserva la corrección del literal a Skevi y a una adopción
   posterior con procedencia.
2. `docs/adopcion-gate-skevi-2026-08-21.md:28-37` documenta la misma frontera
   entre salida heredada e interpretación de Pinax.
3. `docs/registro-integracion-externa-dsh-2026-09-10.md:275-281` conserva la
   evidencia literal del 2026-09-10 y añade una aclaración fechada: se
   verificaron cero planes y el estado operativo es `INACTIVE`.

## Segunda pasada — comprobaciones y resultado

No se hallaron defectos bloqueantes después de las correcciones.

- **AN-KLA:** `docs/guia-an-kla-pinax.md:10-16` remite a consulta dinámica de
  la versión instalada y limita beta.16 a antecedente fechado. La consulta
  local devolvió `0.1.0b25`; `git show e2ce286` registra la actualización a
  b25; `context status` separa correctamente la plantilla gestionada
  `0.1.0-beta.26` y devolvió `diagnostics: []`. El aviso de beta.28 disponible
  no contradice el texto, porque éste no fija la versión vigente.
- **Raíz README:** `README.md:13-17` usa `..`; desde la raíz de Pinax resuelve
  `/Users/krisnova/www/aria`. Una llamada directa a `discover` halló 15
  proyectos e incluyó `pinax/project-manifest.yaml`. Esto respalda retirar el
  aplazamiento obsoleto en `project-manifest.yaml:59-63`.
- **Git y checkpoint:** al revisar, `HEAD` y `origin/main` coincidían en
  `208d26bac53139faa8f30477a95553c158bd3ac8`. El checkpoint rev. 37 representa
  el snapshot anterior limpio y no se presentó como evidencia del working tree
  modificado. Un cierre posterior deberá crear un checkpoint contra el commit
  final; esta ronda no lo crea ni autoriza.
- **Procedencia de `check_plans`:** el hash del script Pinax coincide con
  `skevi@7bfd759:scripts/check_plans.py` (`a87c80e5...`). El Skevi local más
  reciente contiene cambios posteriores, pero conserva el literal en cuestión;
  por ello la corrección upstream descrita sigue pendiente y no se simuló una
  adopción inexistente.
- **Verificación:** `check_sizes.py` terminó `OK`; `check_plans.py` terminó con
  código 0 y fue clasificado `INACTIVE — 0 planes verificados`; las 51 pruebas
  directas de Pinax y las 62 pruebas de `unittest discover` pasaron;
  `git diff --check` no halló errores de whitespace.
- **Alcance:** `scripts/check_plans.py` y sus pruebas permanecieron sin cambios.
  El diff sustantivo se limita a reconciliar documentación, raíz de cosecha y
  el aplazamiento obsoleto del manifiesto, además de esta acta autorizada.

## Riesgos residuales

- El ejecutable continuará mostrando `OK` hasta que Skevi corrija el literal y
  Pinax adopte esa revisión con procedencia. La regla de `AGENTS.md` evita la
  falsa interpretación dentro de Pinax, pero consumidores externos que ignoren
  el contrato podrían seguir leyendo sólo el proceso y su código de salida.
- `context status` mostró la advertencia
  `context_target_changed_outside_managed_block`, esperable mientras este diff
  modifica texto fuera del bloque gestionado. No fue diagnóstico bloqueante.
- Los ocho hallazgos de `lint ..` sobre proyectos consumidos sin manifiesto son
  relativos a la raíz cosechada y preexistentes; esta ronda no los declara
  resueltos.

## Autocrítica

El mismo agente realizó revisión y verificación; no existe independencia entre
firmante y ejecutor. Se contrastaron archivos, Git, comandos y el checkout local
de Skevi, pero no se verificó el remoto de Skevi ni se evaluó una futura
corrección upstream. No se generó `MAPA.md`: la raíz se verificó mediante las
funciones `discover` y `collect` para no añadir un artefacto al working tree.
La revisión confirma coherencia del cambio y sus pruebas, no la verdad de las
autodeclaraciones cosechadas por Pinax.

## Decisión final

**PROCEED.**

La corrección elimina la falsa lectura operativa del `OK` legado, preserva la
procedencia del script y de la evidencia histórica, y deja explícitos los
límites del checkpoint y del estado Git.

Firmado: `/root/ronda_reconciliacion`
Fecha: 2026-09-11
