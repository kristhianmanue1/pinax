# Cambio aditivo v1: campo `descubrimiento` — quién hace qué (2026-08-20)

**Qué se hizo:** el schema `pinax/project-manifest/v1` acepta ahora
`descubrimiento: {argv, expected_exit_code?}` — los argumentos estructurados
que describen cómo descubrir qué ofrece una herramienta sin leer memoria ni
estado. No es una cadena de shell. Cambio **aditivo y retrocompatible** dentro
de v1 (regla de compatibilidad de AGENTS.md): los manifiestos existentes siguen
válidos (33/33 pruebas en el gate final, snapshot 2026-08-21) y los que no lo
declaren no cambian.

**Por qué:** el análisis `docs/analisis-garantias-2026-08-20.md` mostró que
el descubrimiento de herramientas vivía en un documento temporal
(REANUDAR.md). Con este campo pasa a ser dato del mapa — y un claim
**verificable bajo autorización del operador**, no sólo autodeclarado.

## Reparto de propiedad (quién tiene que hacer esto)

| Quién | Qué | Estado |
|---|---|---|
| **Pinax** (schema, validador, generador) | Añadir el campo al schema; renderizarlo en MAPA.md bajo "Cómo descubrir cada herramienta"; nunca ejecutar el comando en `build` | **Hecho** 2026-08-20 (commit de este documento) |
| **Pinax** (futuro) | Verificación opt-in (`pinax verify-descubrimiento` o similar): construye `argv` directamente, con `shell=False`, cwd controlado, entorno mínimo y límites; comprueba `expected_exit_code`, **sólo bajo autorización explícita sobre el argv exacto** | Propuesto, no autorizado |
| **Mediador** | Nada que hacer: el campo no introduce identificadores nuevos ni afecta la inclusión en el mapa | — |
| **Mantenedor de cada proyecto** | Declarar `descubrimiento` en su `project-manifest.yaml` como lista argv real (`["python3", "-m", "an_kla", "capabilities"]`, por ejemplo). Adopción **voluntaria**, como todo en v1 | Pendiente — proyecto por proyecto |
| **Agentes consumidores** | Leer el mapa; cualquier ejecución requiere autorización separada y un runner sin shell | Regla de uso, no obligación técnica |

## Frontera de confianza declarada

`descubrimiento` es autodeclaración: que un manifiesto publique una lista argv
no prueba que funcione, y ejecutarla sin autorización sería una violación de la
frontera (texto no confiable → proceso). La forma estructurada evita que una
futura implementación necesite interpretar shell, pero no concede autoridad.
`shell=False` sólo evita que el runner introduzca un shell implícito: no vuelve
seguro el programa declarado, que puede ser por sí mismo un shell o intérprete.
Por eso no se usa una lista negra incompleta; el operador revisa ejecutable y
argumentos exactos antes de cada corrida autorizada.

## Compatibilidad

- Dentro de v1: aditivo, núcleo cerrado intacto (campos desconocidos siguen
  rechazándose).
- Ningún manifiesto viejo se reinterpreta: ausencia del campo = ausencia de
  claim, nada más.
