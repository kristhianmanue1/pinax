# Congelación — Runtime Capability Matrix v0

Registro de congelación (F0.1, saneamiento de baseline). Congela **exactamente**
el fichero `runtime-capability-matrix-v0.yaml` del estado que lo introdujo
(`1dd90dc`), sin modificación alguna desde entonces (`VERIFIED`: `git diff
HEAD -- <fichero>` vacío en el commit de congelación).

| Campo | Valor |
|---|---|
| Fichero congelado | `docs/baseline-aria-v0/runtime-capability-matrix-v0.yaml` |
| Schema | `pinax/runtime-capability-matrix/v0` (esqueleto, sin requisitos) |
| SHA-256 | `8e7e373aa2cc9d00da9a1202aa2cea65def1f309f585d50ee8d6f1e380297598` |
| Tamaño | 2477 bytes |
| Commit que introdujo la matriz | `1dd90dcaeb668a8215b4caa792d0ca79403f50be` (2026-09-10) |
| Timestamp del freeze (UTC) | `2026-09-10T18:35:43.218Z` |
| Commit de congelación | El commit que introduce este fichero; su hash se consulta con `git log --oneline -- docs/baseline-aria-v0/congelacion-matrix-v0.md` |

## Relación con el protocolo Runtime Contract v0

La matriz es el **vocabulario común** del experimento regulado por
`protocolo-runtime-contract-v0.md` (Entregable E). El protocolo exige que
AN-KLA, Skopos y Ágora deriven sus filas **independientemente** sobre esta
misma matriz; la congelación por identidad criptográfica existe para que los
tres participantes no reciban vocabularios distintos.

## Política de distribución

Toda copia entregada a AN-KLA, Skopos o Ágora debe ser **byte-identical** al
fichero congelado (mismo SHA-256 y tamaño) o, si viaja dentro de otro
artefacto, **verificablemente derivada** de él (hash citado y comprobable
contra este registro). Verificación:

```bash
shasum -a 256 runtime-capability-matrix-v0.yaml
# esperado: 8e7e373aa2cc9d00da9a1202aa2cea65def1f309f585d50ee8d6f1e380297598
```

## Lo que la congelación NO hace

- No rellena celdas: prohibido por la regla 3 de la propia matriz. Las filas
  las producen AN-KLA, Skopos y Ágora; Pinax sólo congela, distribuye, recibe,
  valida forma y posteriormente compara.
- No autoriza el experimento: el despacho de los tres análisis es una
  transición protegida aparte, decidida por el Mediador (sección 9 del encargo
  F0.1).
- No altera la matriz: cualquier cambio futuro exige `v1` o superación
  explícita del freeze, nunca una edición silenciosa.
