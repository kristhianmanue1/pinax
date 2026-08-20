# Encargo para el agente de Ágora (2026-08-20)

**Emisor:** Pinax, por autorización del dueño. Decisión de fundación:
`/Users/krisnova/www/pinax` memoria AN-KLA, evento
`evento-decision-agora-cagf-2026-08-20` — **agora se funda simple, sin CAGF
ni ektel**; CAGF queda como árbitro futuro vía adaptador.
**Naturaleza:** encargo, no autorización. Los actos 🔒 son del dueño.

**Repo del proyecto:** `/Users/krisnova/www/aria/agora` — todas las rutas
de este encargo son absolutas.

## 0. Lectura obligatoria, en orden

1. `/Users/krisnova/www/aria/agora/AGENTS.md` — el contrato completo:
   4 reglas, front-matter de 7 campos, archivos laterales para binarios,
   organización mínima, decisiones pendientes.
2. `/Users/krisnova/www/aria/agora/2026-08-13-estado-estandar-huerfano.md`
   — el único artefacto depositado; sirve de ejemplo de front-matter.

## 1. Trabajo del ciclo

1. **Validador ejecutable de front-matter** (`scripts/check_agora.py` o
   nombre equivalente), en el espíritu de
   `/Users/krisnova/www/aria/escrubery/scripts/check_sizes.py`:
   - forma del front-matter (los 7 campos obligatorios, tipos, formato de
     fecha, `estado` en el vocabulario cerrado);
   - unicidad de `id` en todo el almacén plano;
   - integridad de `superado_por`: obligatorio si `estado: superado`,
     ausente si no, y el id referenciado existe;
   - coherencia de binarios: todo archivo no-texto con su `.yaml` lateral
     (regla de archivos laterales);
   - **exit 1 con mensaje claro ante cualquier violación** — es un gate,
     no un aviso.
   - Python stdlib puro (como `check_sizes.py`); sin dependencias nuevas
     🔒. Si YAML sin dependencia se complica, parsear sólo el
     front-matter con un parser mínimo propio y declararlo en el docstring.
2. **Documentar el gate** en
   `/Users/krisnova/www/aria/agora/AGENTS.md` §Decisiones pendientes:
   marcar "chequeo ejecutable del front-matter" como **implementado** con
   la ruta del script — esa sección decía que sin él las reglas eran
   guidance; ahora son contrato.
3. **Depositar dos artefactos del ciclo 2026-08-20** (copias con
   front-matter propio, nombre `YYYY-MM-DD-<id>.md`):
   - `2026-08-20-vision-pinax-skopos-ektel-firmada.md` — copia de
     `/Users/krisnova/www/pinax/rondas/2026-08-20-vision-skopos-ektel/vision-final-firmada.md`,
     autor: Pinax (Kimi), proyectos: [pinax, skopos, ektel],
     estado: vigente.
   - `2026-08-20-estado-hueco-manifiesto-cubierto-por-pinax.md` —
     artefacto nuevo breve que registra que el hueco documentado en
     `estado-estandar-huerfano` (manifiesto + auditor: "nadie") está
     cubierto de facto por Pinax (schema v1 + campo `descubrimiento`),
     `derivado_de: [estado-estandar-huerfano]`, estado: vigente.
     Redáctalo como registro de estado, no como propuesta — regla 1:
     evidencia, nunca autoridad.

## 2. NO es parte de este encargo

- Binarios (la decisión LFS vs blobs sigue pendiente del dueño 🔒).
- El catálogo/vista generada (se justifica ~30 artefactos).
- Cualquier integración con CAGF, ektel o AN-KLA.
- Tocar el artefacto existente de Claude salvo error de forma.

## 3. Reglas

- Español; `python3 scripts/check_agora.py` (o el nombre elegido) debe
  pasar en verde con los artefactos existentes + los dos nuevos antes de
  declarar terminado.
- Editar no implica commit; commit no implica push. 🔒 ambos requieren
  autorización explícita del dueño, una vez por operación.
- Reporte: diff leído completo, salida del validador, lista de archivos
  creados.
