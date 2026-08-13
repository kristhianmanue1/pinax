# Encargo — ronda adversarial sobre el manifiesto propuesto de Epistates

Eres **revisor adversario**, proveedor distinto al que construyó este manifiesto
(Antigravity/agy). No eres el mantenedor de epistates: tu trabajo es intentar
refutar lo que otro agente propuso sobre epistates.

## Qué leer

- `pinax/fixtures/epistates.project-manifest.yaml` — el objeto a revisar
- `pinax/fixtures/epistates.confirmacion-antigravity.md` — su justificación por campo
- `pinax/schemas/project-manifest-v1.schema.json` — el contrato de forma
- `aria/epistates/README.md`, `CHANGELOG.md`, `docs/` — la fuente real

No necesitas nada más del ecosistema.

## Dos hallazgos ya identificados — verifícalos primero

**1. Posible omisión en `no_ofrece`.** El README §6 "No objetivos iniciales"
lista diez exclusiones. Cuenta cuántas están en el manifiesto. Si falta alguna,
dilo con la cita exacta.

**2. `consume` declara `{ tipo: proyecto, id: praxis, requerido: true }`.**
Verificado por otro agente: no hay ninguna referencia a "praxis" en el código
fuente (`src/`), sólo en el README §4 "Relación con Praxis", y toda esa sección
está en tiempo futuro ("podrá", "declarará", "deberá"). Es una relación de
diseño declarada, no una dependencia operativa hoy.

Decide: ¿`requerido: true` es correcto, o sobreafirma algo que aún no existe en
código? Si corriges, di exactamente qué cambia.

## Qué más revisar

- ¿`ofrece` y `publica` son exactos, sin inventar ni omitir?
- ¿Hay estado dinámico colado (versión, fase, conteos, próxima tarea)?
- ¿Hay algún verbo imperativo dirigido a un agente? El manifiesto es dato, no
  instrucción.
- ¿`pospuesto` refleja intención real documentada, no una lista genérica?
- ¿Las referencias en `publica`/`consume` usan tipo correcto? Recuerda:
  `consume` es de nivel ecosistema — paquetes de PyPI no van ahí.

## Reglas duras

- No escribas en `aria/epistates/`. No autoriza tocar el repositorio.
- Si corriges el manifiesto, hazlo en
  `pinax/fixtures/epistates.project-manifest.yaml` directamente y dilo.
- No hagas commit ni push.

## Salida

`pinax/fixtures/epistates.veredicto-adversario-<tu-identidad>.md`:

```markdown
# Veredicto adversario — Epistates — <tu identidad>

**Posición:** REFUTA | CONCURRE CON CORRECCIONES | CONCURRE

## Hallazgos
Uno por hallazgo: afirmación revisada · evidencia (archivo + cita) · corrección
si aplica.

## Verificación
- [ ] Validé el manifiesto corregido con `pinax/scripts/pinax.py validate`
- [ ] `pinax/tests/test_pinax.py` sigue en verde

---
*Agente: <proveedor> <modelo> <versión> — Rol: adversario. Fecha: <YYYY-MM-DD>*
```

Sin firma no se tabula.
