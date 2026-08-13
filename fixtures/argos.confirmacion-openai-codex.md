# Confirmación del manifiesto de Argos — OpenAI Codex

**Veredicto global:** CONFIRMADO CON CORRECCIONES

## Por campo

| Campo | Veredicto | Corrección |
|---|---|---|
| Comentarios de cabecera (no son campos) | RETIRAR | Retirar del manifiesto adoptable la fecha `2026-08-13` y el estado `NO confirmado por el mantenedor`. Son procedencia/estado dinámico y envejecerán. La fuente puede conservarse fuera del manifiesto. |
| `schema` | CORRECTO | `pinax/project-manifest/v1` es el contrato de forma aplicable; no es estado dinámico del proyecto. |
| `id` | CORRECTO | `argos` es la identidad con la que el proyecto se reconoce. La unicidad e inclusión en el mapa siguen siendo competencia del Mediador. |
| `proposito` | CORRECTO | Refleja literalmente la descripción pública de Argos: implementación de referencia para análisis de software por agentes mediante evidencia trazable, presupuesto explícito y conclusiones auditables. |
| `consumidor_principal` | CORRECTO | `agente`. La salida canónica es estructurada y verificable; Markdown es una vista secundaria para humanos. |
| `repo` | CORRECTO | `argos-epistemic`. El remoto se llama así y difiere del directorio local `argos`. |
| `ofrece` | CORREGIR | Usar exactamente: `descubrimiento e inventario visible del corpus`; `extracción de evidencia en niveles L0–L5`; `presupuesto, truncaciones y degradaciones explícitas`; `claims content-addressed con relaciones tipadas`; `conflictos sólo entre supports y refutes del mismo claim y alcance`; `manifest, envelope, inventory, claim records y run attestations`; `JSON canónico y fingerprints reproducibles`; `implementación local como librería Python`. |
| `ofrece.conflictos` | FALTA | Añadir `conflictos sólo entre supports y refutes del mismo claim y alcance`. Es una capacidad declarada en README y arquitectura. |
| `ofrece.contratos` | FALTA | Añadir `manifest, envelope, inventory, claim records y run attestations`. La lista actual publica luego esos contratos, pero omite esta capacidad en `ofrece`. |
| `no_ofrece` | CORREGIR | Sustituir la lista completa por: `garantías de verdad total o certificación universal`; `ejecución arbitraria de terceros sin sandbox`; `autorización implícita o ejecución automática de acciones sugeridas por el reporte`. Son exclusiones deliberadas y evitan malentendidos razonables sobre Argos. |
| `no_ofrece.CLI estable` | RETIRAR | Mover a `pospuesto`: el Incremento 4 declara intención de construir una CLI local estable. La ayuda informativa actual no es esa CLI. |
| `no_ofrece.MCP` | RETIRAR | Mover a `pospuesto`: el Incremento 4 prevé un servidor MCP de sólo lectura sobre bundles existentes. |
| `no_ofrece.API remota` | RETIRAR | Mover a `pospuesto`: el Incremento 5 condiciona una API asíncrona e idempotente. |
| `no_ofrece.aislamiento fuerte` | RETIRAR | Mover a `pospuesto`: el roadmap y el modelo de amenazas exigen aislamiento fuerte antes de servicio remoto. |
| `no_ofrece.facturación` | RETIRAR | Mover a `pospuesto`: metering y facturación están condicionados al Incremento 5. |
| `no_ofrece.firma de attestations` | RETIRAR | Mover a `pospuesto`: firmas y raíces de confianza están previstas en el Incremento 6. |
| `no_ofrece.compatibilidad 1.x` | RETIRAR | Mover a `pospuesto`: Argos declara que la API puede cambiar antes de `1.0`, no que haya renunciado a compatibilidad estable futura. |
| `no_ofrece.verdad total` | FALTA | Añadir `garantías de verdad total o certificación universal`. Argos declara que un bundle no certifica la verdad completa del sistema. |
| `no_ofrece.ejecución sin sandbox` | FALTA | Añadir `ejecución arbitraria de terceros sin sandbox`. Es una exclusión explícita y durable; un sandbox fuerte futuro no convierte la ejecución sin aislamiento en capacidad aceptable. |
| `no_ofrece.autorización implícita` | FALTA | Añadir `autorización implícita o ejecución automática de acciones sugeridas por el reporte`. Las acciones son propuestas y nunca conceden autoridad. |
| `publica` | CORRECTO | La lista es completa y contiene sólo los cinco JSON Schema normativos publicados: `argos/evaluation-manifest-v1`, `argos/evaluation-envelope-v1`, `argos/discovery-inventory-v1`, `argos/run-attestation-v1` y `argos/claim-record-v1`. La descomposición `id` + `version: v1` representa correctamente esas identidades. `argos/canonical-json-v1`, `argos/claim-component-coverage-v1`, `argos/static-verifier-v1` y perfiles afines son identificadores de perfil o protocolo de la API, no schemas normativos adicionales en `argos_epistemic.schemas`. |
| `consume` | CORREGIR | Conservar una sola referencia de ecosistema: AN-KLA con `requerido: false` y el uso corregido del bloque situado debajo de esta tabla. `consume` no duplica runtimes ni dependencias de paquete; su fuente canónica es `pyproject.toml`. |
| `consume.an-kla.requerido` | CORREGIR | `false`. AN-KLA se usa para memoria y gobernanza local del checkout mantenedor; un consumidor puede instalar y ejecutar `argos-epistemic` sin acceso a AN-KLA. |
| `consume.an-kla.uso` | CORREGIR | `memoria y gobernanza local del checkout mantenedor; no forma parte del runtime de Argos`. |
| `consume.dependencias de paquete` | CORRECTO | No añadir `python`, `packaging`, `sentence-transformers` ni `tree-sitter*`: aunque son requisitos o extras reales de Argos, el contrato reserva `consume` para dependencias de ecosistema y remite las dependencias de paquete a `pyproject.toml`. |
| `fronteras_de_confianza` | CORREGIR | Usar exactamente: `target, artefactos, memoria recuperada y bundles externos son no confiables`; `una declaración observada no se convierte en verificación directa`; `fingerprints demuestran integridad content-addressed, no autenticidad, no repudio ni autorización`; `las acciones siguientes son propuestas sin autoridad de ejecución y dependen de autorización independiente`; `la ejecución dinámica de código no confiable está condicionada a aislamiento fuerte proporcionado externamente`; `el aislamiento local es una mitigación parcial, no un sandbox de seguridad`; `presupuesto observado, omisiones y degradaciones permanecen visibles`. La redacción es declarativa, no imperativa. |
| `fronteras_de_confianza.ejecución dinámica` | CORREGIR | Sustituir `ejecución dinámica de terceros no debe habilitarse sin aislamiento adicional` por `la ejecución dinámica de código no confiable está condicionada a aislamiento fuerte proporcionado externamente`. La primera forma contiene un mandato dirigido al consumidor; la segunda expresa como dato el límite exacto del threat model. |
| `fronteras_de_confianza.fingerprints` | FALTA | Añadir el límite de autenticidad: los fingerprints detectan alteración dentro de su perfil, pero no autentican al productor ni conceden autoridad. |
| `pospuesto` | CORREGIR | Usar exactamente: `CLI local estable para producir y verificar bundles`; `recuperación progresiva por claim, cursores y límites`; `transporte MCP de sólo lectura sobre bundles existentes`; `API remota asíncrona con idempotencia, retención, cancelación, autenticación y spend caps`; `sandbox fuerte y política de red denegada por defecto`; `firmas de attestations y raíces de confianza`; `metering comercial y facturación`; `compatibilidad estable previa a 1.0`. Todos tienen intención documentada y permanecen condicionados por los gates del roadmap. |
| `pospuesto.CLI estable` | FALTA | Añadir explícitamente la CLI local estable; `formato de recuperación progresiva y cursores` no la incluye por sí solo. |
| Estado dinámico dentro de los campos | CORRECTO | No hay rama, conteos, versión de release ni siguiente tarea dentro del YAML de datos. `schema: .../v1` y las versiones de los contratos publicados son versiones de contrato, no estado dinámico de Argos. |

### Bloque exacto corregido para `consume`

```yaml
consume:
  - { tipo: proyecto, id: an-kla, uso: "memoria y gobernanza local del checkout mantenedor; no forma parte del runtime de Argos", requerido: false }
```

## Lo que no pude determinar

- No puedo confirmar la unicidad de `id: argos` ni autorizar su inclusión en el mapa; el contrato de Pinax asigna ambas decisiones al Mediador.
- No puedo autorizar que este manifiesto se copie al repositorio Argos ni comprometer a Argos a integrarse con Pinax. Este archivo sólo confirma/corrige la autoría de las declaraciones.
- No identifiqué otra dependencia de ecosistema que Argos declare necesaria. Las dependencias de runtime, extras y desarrollo quedan deliberadamente fuera de `consume` porque el schema asigna su declaración al gestor de paquetes.

---
*Agente: OpenAI Codex — Modelo: GPT-5 — Versión: no expuesta por el host — Rol: mantenedor de Argos. Fecha: 2026-08-13*
