# Cambio aditivo v1: campo `descubrimiento` — quién hace qué (2026-08-20)

**Qué se hizo:** el schema `pinax/project-manifest/v1` acepta ahora
`descubrimiento: {comando, esperado?}` — el comando estático que un agente
puede ejecutar para descubrir qué ofrece una herramienta sin leer memoria
ni estado. Cambio **aditivo y retrocompatible** dentro de v1 (regla de
compatibilidad de AGENTS.md): los manifiestos existentes siguen válidos
(27/27 pruebas en verde) y los que no lo declaren no cambian.

**Por qué:** el análisis `docs/analisis-garantias-2026-08-20.md` mostró que
el descubrimiento de herramientas vivía en un documento temporal
(REANUDAR.md). Con este campo pasa a ser dato del mapa — y un claim
**verificable bajo autorización del operador**, no sólo autodeclarado.

## Reparto de propiedad (quién tiene que hacer esto)

| Quién | Qué | Estado |
|---|---|---|
| **Pinax** (schema, validador, generador) | Añadir el campo al schema; renderizarlo en MAPA.md bajo "Cómo descubrir cada herramienta"; nunca ejecutar el comando en `build` | **Hecho** 2026-08-20 (commit de este documento) |
| **Pinax** (futuro) | Comando de verificación opt-in (`pinax verify-descubrimiento` o similar): ejecuta `comando` y comprueba `esperado`, **sólo bajo autorización explícita del operador por corrida** — ejecutar autodeclaraciones a ciegas es ejecutar texto no confiable | Propuesto, no autorizado |
| **Mediador** | Nada que hacer: el campo no introduce identificadores nuevos ni afecta la inclusión en el mapa | — |
| **Mantenedor de cada proyecto** | Declarar `descubrimiento` en su `project-manifest.yaml` con su comando real (`an_kla capabilities`, `epistates describe`, `consultar listar`, …). Adopción **voluntaria**, como todo en v1 | Pendiente — proyecto por proyecto |
| **Agentes consumidores** | Antes de usar una herramienta de aria: leer el mapa y ejecutar su comando de descubrimiento | Regla de uso, no obligación técnica (la obligación estructural sigue siendo de ektel, inexistente) |

## Frontera de confianza declarada

`descubrimiento` es autodeclaración: que un manifiesto afirme un comando no
prueba que funcione, y ejecutarlo sin autorización sería una violación de la
frontera (texto no confiable → proceso). Por eso el mapa lo publica con la
advertencia y la verificación es un acto separado y autorizado.

## Compatibilidad

- Dentro de v1: aditivo, núcleo cerrado intacto (campos desconocidos siguen
  rechazándose).
- Ningún manifiesto viejo se reinterpreta: ausencia del campo = ausencia de
  claim, nada más.
