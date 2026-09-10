# Entregable E — Protocolo del experimento Runtime Contract (v0)

Estado: `CONGELADO-PARA-REVISION` — Pinax lo prepara, **no lo ejecuta**.
Nada de este documento es decisión de los proyectos participantes: cada uno
conserva su gobernanza.

## 1. Pregunta arquitectónica

Qué capacidades debe proporcionar un runtime neutral para que distintos
componentes de Aria funcionen sin acoplarse a una implementación concreta.

## 2. Hipótesis (PROPOSED, no decisión)

> **H1**: Existe un conjunto mínimo y suficientemente estable de capacidades
> de runtime que puede expresarse mediante un contrato neutral e
> independiente de EKTEL y que permite satisfacer las necesidades
> fundamentales de AN-KLA, Skopos y Ágora sin absorber responsabilidades
> propias de esos sistemas.

### Condiciones de falsación (cualquiera debilita o falsa H1)

1. Los tres sistemas requieren modelos de ejecución estructuralmente
   incompatibles.
2. El supuesto contrato común sólo puede expresarse incorporando lógica
   específica de AN-KLA, Skopos o Ágora.
3. La abstracción obliga a trasladar responsabilidades de dominio al runtime.
4. EKTEL debe conocer semántica interna de las memorias para implementarlo.
5. Las capacidades comunes son tan triviales que el contrato no aporta
   interoperabilidad real.
6. Consumidores posteriores no relacionados con memoria no pueden expresar
   razonablemente sus necesidades mediante el contrato.

## 3. Participantes (congelados)

* **Derivación inicial (exclusiva)**: AN-KLA + Skopos + Ágora.
* **Validación fuera de muestra**: Epistates + Argos Epistemic — reciben el
  contrato resultante SIN modificarlo; se comprueba si generaliza.
* **Pruebas especializadas posteriores** (no contaminan la derivación):
  Llavero → capability de secrets; Glosomata → sesión/canal/interrupción/I/O.
  Utilidad: comprobar que el contrato incorpora capabilities especializadas
  sin absorber la responsabilidad de los proveedores.
* **Excluidos**: EKTEL (evita diseñar desde sus capacidades existentes);
  Propylon (`PROPOSED_COMPONENT`, sin implementación suficiente).

## 4. Reglas de independencia

1. NO modificar AN-KLA, Skopos, Ágora, EKTEL ni ningún otro repos durante la
   derivación.
2. NO autorizar EKTEL M3; NO reanudar Ágora M2; NO iniciar AN-KLA G3.
3. NO crear integraciones entre proyectos.
4. NO declarar contratos que los proyectos no hayan adoptado.
5. NO convertir propuestas de este ciclo en decisiones de los consumidores.
6. Cada participante analiza INDEPENDIENTEMENTE: sin ver las respuestas de
   los otros hasta que el Mediador libere la comparación.
7. Pinax observa, registra, contrasta y prepara; no diseña el Runtime
   Contract.

## 5. Formato esperado de resultados

Cada participante entrega una matriz instanciada conforme a
`runtime-capability-matrix-v0.yaml`:

* una celda por categoría (y sub-capabilidad de secrets), con
  `REQUIRED | OPTIONAL | FORBIDDEN | NOT_APPLICABLE | UNRESOLVED`;
* `proveedor_esperado` por celda (`internal | external | adapted |
  unresolved`) — sin asumir que el runtime implementa internamente;
* enlaces de evidencia por celda y `provenance` por celda;
* una sección de capacidades ausentes del vocabulario (el participante
  puede proponer categorías nuevas; quedan marcadas como propuestas);
* prohibido declarar necesidades de OTROS proyectos.

Respuestas comparables porque el vocabulario y la forma están congelados
aquí; el contenido es libre.

## 6. Criterios de falsación aplicados

Tras la derivación: si algún condition 1–5 del §2 se cumple con las tres
respuestas en mano, H1 queda debilitada o falsada y el resultado se registra
en el mapa como tal. Tras la validación fuera de muestra: si
Epistates/Argos no pueden expresar sus necesidades sin modificar el
contrato, se cumple la condición 6 y H1 queda falsada en generalización.

## 7. Propiedad transversal bajo observación

`gate reachability` (existencia ≠ alcanzabilidad ≠ enforcement inevitable)
viaja como concepto candidato; los participantes pueden clasificarla en sus
matrices, pero ninguna propiedad se impone en esta fase.

## 8. Condiciones de arranque (no cumplidas aún)

1. Revisión adversarial del Mediador sobre esta baseline y este protocolo.
2. Autorización explícita del dueño para despachar los encargos de análisis
   a los tres participantes de derivación (vía task-card, G1/G2 del grafo).
3. Congelación de la versión de la matriz entregada a los participantes.
