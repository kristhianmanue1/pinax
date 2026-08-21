# Síntesis Pinax — rondas externas M0 ektel (2026-08-20)

**Objeto:** M0 @ `33da6f8` (encargo `docs/revisiones/encargo-revision-m0-contratos-2026-08-20.md`).
**Revisores:** Codex CLI (una corrida completa) y Claude CLI (cuatro corridas
acotadas: frentes 1-2, 5, 4; frente 3 cubierto de facto por el fuzz del
frente 4 y las propuestas de Codex). Cada uno cerró con ronda adversarial
propia y retracciones, como exige F5.
**Logs:** `codex-raw.log`, `claude-frentes-1-2.log`, `claude-frente-4.log`,
`claude-frente-5.log` (este directorio).

## Veredictos

- **Codex: NO-GO** — 3 bloqueantes, 1 menor, 2 notas. Retracciones: 2.
- **Claude: NO-GO implícito** ("el corpus debe crecer antes de declarar M0
  cerrado") — bloqueantes propios, fuzz diferencial de 1,191 mutaciones con
  **307 divergencias (79 de veredicto)** entre los parsers.
- **Pinax (yo):** reproduje los 3 bloqueantes de Codex con mis propias manos
  antes de aceptarlos (divergencia A/B en `capability_envelope` escalar,
  `started` sin `handle` aceptado por ambos, `capability_rejected` en el enum
  de `StartFailed`). Los hallazgos de Claude vienen de su fuzz reproducible
  (`/tmp/fuzz.py` de su sesión); los marco como *reportados con evidencia,
  no re-reproducidos por mí* — la corrección los re-ejecutará.

## Convergencias (ambos, independientemente)

| Tema | Codex | Claude |
|---|---|---|
| Parser A (referencia) no aplica las reglas de los schemas (`$ref` como `any`, sin `minimum`/`pattern`/`enum`; `GUARANTEES_ENUM` muerto) | Bloqueante 1 | Bloqueantes 7-8 |
| Los 31 vectores no discriminan: acuerdo en el corpus no prueba interoperabilidad | Bloqueante 1 + menor 4 | Veredicto R5 |
| Schemas sin discriminación de uniones (`started` sin `handle`, campos por alternativa no obligatorios) | Bloqueante 2 | Compartido 3 |
| C2 byte-exacto (`cap-valid-01`) verificado a mano: MAC e `identity_digest` coinciden | Nota 5 | Frente 2 ✅ |
| `budget_exceeded` ausente; 4 estados post-inicio; 4 clases de garantía | Bloqueante 3 (lo confirma) | Frente 5 conformes |

## Hallazgos únicos de Claude (que Codex no vio)

1. **Bloqueante — maleabilidad de firma por base64url no canónico**: flip del
   último char de `signature` aceptado por ambos con el mismo digest; dos
   secuencias de bytes → mismo `identity_digest`. Antirreplay por hash
   evadible. Codex lo rozó como "ambigüedad" (retractado como incumplimiento);
   Claude lo demuestra explotable. **Requiere decisión normativa** (¿"estricto"
   incluye canonicalidad de bits residuales?) + vector.
2. **Bloqueante — `identity_digest` inestable frente a re-encoding del
   payload**: mismo contenido decodificado, digest distinto. La identidad es
   función del encoding, no del contenido.
3. **Bloqueante — parser B acepta `\n` final** en todo campo con `pattern`
   (`re.search` en vez de `re.fullmatch`): A rechaza, B acepta. Hueco real.
4. **Bloqueante — vocabulario de admisión desdoblado**: schemas/parser A
   admiten `capability_invalid/expired/reused` donde §8.3 y ADR-005 colapsan
   en `capability_rejected`. Agravante: el vector dorado `aout-valid-rejected`
   canoniza el código inventado.
5. Menores: precedencia de diagnósticos invertida (90 casos), cardinalidades
   (`invalid_type` vs `invalid_value`), `size_exceeded` ausente del
   vocabulario documentado de A, entrypoints que fallan con base64 sin
   padding, `exp < nbf` aceptado (decisión a fijar con vector).
6. Notas de spec: `guarantee_unsupported` sin causa en §8.3; `cause_code` y
   enums de `ActionRequest` nacen en el schema sin asiento normativo.

## Contradicción Codex ↔ Claude (requiere decisión del mantenedor)

- **`capability_rejected` en `StartFailed`.** Codex (bloqueante 3): el schema
  rompe el vocabulario cerrado — quitarlo. Claude (frente 5, nota 3): el
  schema sigue correctamente §7.4 (perdedor de `start` concurrente); el
  conflicto es **interno de la spec** — enmendar §8.3. Leídas ambas citas,
  **la posición de Claude es la correcta**: §7.4 exige ese código para la
  carrera de `start`; §8.3 lo niega. La enmienda va a la spec, no al schema.
  Codex no retrató esto; queda asentado como divergencia resuelta por Pinax.

## Lo que quedó CIERTO

- Perfil criptográfico C2 correcto y byte-exacto (verificado dos veces, por
  ambos revisores, con la clave de prueba).
- Dominios `ektel/{capability,pop,admission,termination}/v1`, b64url sin
  padding, sin HKDF.
- Vocabularios centrales (estados, garantías, ausencia de `budget_exceeded`)
  conformes.
- La independencia clean-room **existe** (las implementaciones difieren de
  verdad) pero **el corpus no la ejerce**.

## Dirección para el agente de ektel

1. **M0 no se cierra.** Corregir: parser A debe aplicar los schemas completos
   (o cargarlos como B); B pasa a `re.fullmatch`/`\Z`; schemas con
   discriminación de unión (`oneOf`); vocabulario de admisión colapsado a
   `capability_rejected` **o** enmienda de §8.3 — decisión, no silencio.
2. **Decisión normativa nueva 🔒 del dueño**: canonicalidad de base64url
   (bits residuales) — de ella cuelgan los hallazgos de maleabilidad y la
   estabilidad de `identity_digest`. Preparar brief con alternativas antes de
   implementar.
3. Ampliar el corpus con los vectores propuestos por ambos (Codex lista 7
   clases; el fuzz de Claude es la mina: 79 divergencias de veredicto
   clasificadas).
4. Enmiendas de spec: §8.3 (StartFailed, garantía), asiento de `cause_code`
   y enums de `ActionRequest`; redacción de §6.6/§6.8 (la implementación es
   mejor que la letra — enmendar la letra).
5. Ronda de verificación post-corrección con ambos revisores.

*Pinax (Kimi/kimi-k2) — 2026-08-20. Síntesis sobre logs crudos; mis
reproducciones marcadas arriba; el resto es evidencia reportada por los
revisores, no re-verificada por mí.*
