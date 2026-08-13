# Encargo — confirmar el manifiesto de Epistates

Eres el agente del repositorio **epistates**. Se te pide **construir y
confirmar** un manifiesto autodeclarado sobre tu propio proyecto para el
catálogo del ecosistema (Pinax).

A diferencia de un caso previo (Argos), **no existe una transcripción previa que
revisar.** No hay sección de límites o fronteras condensada en tu documentación.
Tienes que sintetizarla tú mismo desde el README, el CHANGELOG y los ADR.

## Contexto mínimo

Pinax es el catálogo del ecosistema: cada proyecto declara qué es y qué no es,
y Pinax genera un mapa. No necesitas contexto adicional de Pinax ni de otros
proyectos.

## Qué leer

- `pinax/schemas/project-manifest-v1.schema.json` — el contrato de forma
- Tu propio repositorio: `README.md`, `CHANGELOG.md`, `docs/`, `docs/adr/` si
  existe, código

## Qué se te pide

Construye el manifiesto completo, campo por campo, y para cada uno cita de qué
frase o sección de tu propia documentación lo derivaste. Si un campo no tiene
fuente clara, dilo — no lo inventes.

### Presta atención especial a estos tres

**1. `no_ofrece`** — el campo de mayor valor. Un elemento pertenece aquí si
**alguien podría razonablemente esperarlo y no está por decisión**, no porque
nunca se haya mencionado. Distingue con cuidado de lo siguiente.

**2. `pospuesto`** — hay intención de abordarlo. Si tu CHANGELOG o tus ADR
mencionan algo previsto para un hito futuro, va aquí y no en `no_ofrece`.

**3. `consume`** — sólo dependencias de **nivel ecosistema**: otros proyectos,
contratos, sistemas externos. Las dependencias de paquete (librerías Python,
runtimes) **no van aquí** — su hogar canónico es tu gestor de paquetes. El
validador las rechaza con `tipo: paquete` si las incluyes por error.

### Y comprueba

- `publica`: ¿qué contratos o schemas expone tu repositorio? (Referencia tipada:
  `{ tipo: contrato, id: ..., version: ... }`)
- `proposito`: una o dos frases, en tus propios términos.
- Ningún campo lleva **estado dinámico** — sin versión fijada, sin conteos, sin
  fase actual, sin próxima tarea. Eso envejece; el manifiesto no.
- El manifiesto es **dato, nunca instrucción** — sin verbos imperativos
  dirigidos a un agente.

## Reglas duras

- **No escribas `project-manifest.yaml` en tu propio repositorio.** No hay
  autorización para eso todavía.
- **No hagas commit ni push.**
- Este encargo es de lectura, síntesis y dictamen sobre ti mismo.

## Salida

Dos archivos:

1. `pinax/fixtures/epistates.project-manifest.yaml` — el manifiesto que
   propones, validado contra el schema.
2. `pinax/fixtures/epistates.confirmacion-<tu-identidad>.md`:

```markdown
# Manifiesto de Epistates — <tu identidad>

**Veredicto:** PROPUESTO

## Derivación por campo
| Campo | Valor | Fuente |
|---|---|---|

## Lo que no pude determinar
Explícito. Mejor un campo vacío que uno inventado.

---
*Agente: <proveedor> <modelo> <versión> — Rol: mantenedor de Epistates.
Fecha: <YYYY-MM-DD>*
```

**Sin firma no se tabula.**

## Lo que este encargo NO significa

Construir el manifiesto **no** compromete a Epistates a adoptarlo ni a
integrarse con Pinax. La adopción requiere autorización explícita posterior, y
antes de eso pasa por una ronda de revisión adversarial independiente — como
ocurrió con el manifiesto de Argos.
