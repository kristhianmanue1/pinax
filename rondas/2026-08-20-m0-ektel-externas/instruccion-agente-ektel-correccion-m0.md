# Instrucción para el agente de ektel — corrección de M0 tras rondas externas

**De:** Pinax (orquestador), con síntesis verificada.
**Fecha:** 2026-08-20.
**Base:** `rondas/2026-08-20-m0-ektel-externas/sintesis-pinax.md` (léela
completa; los logs crudos de Codex y Claude están en el mismo directorio).
**Veredicto de las rondas: NO-GO doble y convergente. M0 no se cierra.**

## Encargo, en orden

### 1. Brief de decisión 🔒 PRIMERO (nada de código antes)

**Decisión nueva del dueño: canonicalidad de base64url.** De ella cuelgan
dos bloqueantes de Claude: maleabilidad de firma (flip del último char
aceptado, mismo `identity_digest` para dos secuencias de bytes distintas) e
inestabilidad de `identity_digest` frente a re-encoding del payload.
Alternativas mínimas a presentar: (a) rechazar b64url no canónico en el
parser (bits residuales deben ser cero) — recomendable de entrada; (b)
normalizar antes de verificar (peligrosa: cambia qué se firma); (c) fijar la
canonicalidad en el *digest* pero no en el wire. Con costos, consecuencias
sobre antirreplay, y ronda adversarial pre-decisión. Formato ADR, decisión 🔒.

### 2. Correcciones (tras la firma de la decisión 1)

1. **Parser A (referencia) debe aplicar las reglas completas de los schemas**
   o cargarlos como B: `$ref` no puede ser `("any", None)`,
   `minimum`/`minLength`/`pattern`/`enum` obligatorios, `GUARANTEES_ENUM`
   muerto hoy. Incluye la fuga `schema_version: true` (bool → `!= 1`).
2. **Parser B (clean-room)**: `re.search` → `re.fullmatch` (o `\Z`) en todo
   campo con `pattern`; `B64U_RE` igual.
3. **Schemas con discriminación de unión**: `oneOf`/`if-then` por alternativa
   en `start-outcome`, `admission-outcome`, `termination-outcome` — que
   `started` sin `handle` sea irrechazable hoy es el defecto tipo.
4. **Vocabulario de admisión**: colapsar `capability_invalid/expired/reused`
   a `capability_rejected` (letra de §8.3 + ADR-005) **o** enmendar §8.3 —
   decisión explícita, no silencio. Ojo: el vector dorado
   `aout-valid-rejected` canoniza el código inventado; hay que regenerarlo.
5. **`capability_rejected` en `StartFailed` queda** (conflicto interno de la
   spec, resuelto por Pinax a favor de Claude): la enmienda es a §8.3 para
   reconocer el tercer código, no al schema. Codex no retrató su bloqueante 3;
   asíéntelo en el acta de corrección.

### 3. Enmiendas de spec (documentales, mismo ciclo)

- §8.3: tercer código de `StartFailed`; causa de garantía
  (`guarantee_unsupported`); asiento de `cause_code` y de los enums de
  `ActionRequest` (hoy nacen en el schema sin respaldo normativo).
- §6.6/§6.8: la construcción sobre-JWS implementada es *mejor* que la letra
  (elimina la ambigüedad de concatenación) — enmendar la letra, no el código.
- §5.5: fijar precedencia de diagnósticos (A y B la invierten; 90 casos).
- §5.1: los "límites de tamaño por tipo" no existen en la norma — o se
  escriben o se declara el techo global de 64 KiB como la regla, sin
  ambigüedad.

### 4. Corpus de vectores

Ampliar con las clases propuestas por ambos revisores: envelope/proof
escalares, enteros negativos y `exp < nbf`, decimales, orden de campos,
`typ` cruzado entre dominios con MAC correcta, b64url canónico/no-canónico
(segun la decisión 🔒), uniones mal formadas, `\n` final en campos con
patrón, y mutaciones de doble causa (precedencia de diagnósticos). El fuzz
de Claude (79 divergencias de veredicto clasificadas) es la mina: pedirle la
lista clasificada es legítimo.

### 5. Cierre del ciclo

Ronda adversarial propia sobre la corrección + **re-verificación externa con
ambos revisores** (Codex y Claude) sobre el diff. El gate de salida: los dos
parsers deben **divergir en cero** de las clases anteriores y el corpus debe
incluir al menos un vector por cada divergencia histórica encontrada.

## Restricciones

- Todo commit/push requiere autorización del dueño, por operación.
- Nada de M1: sigue sin haber runtime autorizado.
- Toda métrica citada, fechada como snapshot.
- Si una corrección contradice la síntesis, detenerse y reportar — no
  improvisar una tercera interpretación.
