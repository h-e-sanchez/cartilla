# ROADMAP

Estado al **2026-10-01**. Este archivo se edita a mano.

## Camino A — MVP · hecho

- [x] Carátula, página de módulo y glosario con estilo «técnico cálido» (tokens de `consulta`)
- [x] Generador de datos sintéticos con semilla fija y test de reproducibilidad
- [x] 15 ejemplos en 4 módulos, cada uno con *Qué aprendes* y *En Excel*
- [x] Ejecución en el navegador con Pyodide (carga diferida), botones Copiar y Restaurar
- [x] Salidas esperadas verificadas por `pytest` (local)
- [ ] CI con `ruff` + `pytest` en GitHub Actions: el workflow existe en local, pero publicarlo exige `gh auth refresh -s workflow`

## Camino B — profundidad · pendiente

- [ ] Módulo 02: tipos numéricos con separador de miles chileno, validaciones con reglas de negocio
- [ ] Módulo 03: estacionalidad, días hábiles chilenos, cierre mensual a mitad de mes
- [ ] Módulo 04: formato de Excel con openpyxl (anchos, números, encabezados), script CLI con argparse
- [ ] Ejercicios con solución escondida al final de cada módulo

## Camino C — puente con el resto del portafolio · pendiente

- [ ] Módulo 05 "De pandas a SQL": la misma consulta en pandas y en SQL, enlazada a `consulta`
- [ ] Módulo 06 "Datos para Power BI": exportar un modelo estrella desde pandas, enlazado a `centinela`

## Backlog P1 — robustez

- [ ] Aviso visible si Pyodide falla (sin conexión o bloqueo del CDN) con el enlace para copiar y correr local
- [ ] Probar la salida en Pyodide contra los `.out.txt` (hoy los tests usan pandas local)

## Backlog P2 — alcance

- [ ] Versión en inglés de los encabezados
- [ ] Modo "solo lectura" liviano, sin Pyodide, para conexiones lentas

## No hacer (por ahora)

- Notebooks `.ipynb`: duplicarían la fuente de los ejemplos.
- Un paso de build: la página debe seguir siendo HTML, CSS y JS planos.

## Relato

**Comercial Ejemplo S.A.** es una empresa ficticia de retail con tres sucursales (Norte, Centro y
Sur) y tres líneas de producto (hogar, ferretería y jardín). Vende más en diciembre y menos en
febrero, crece cerca de 8% en 2026 y tiene dos líneas de gasto que se desvían del presupuesto
desde julio: el material para el ejemplo de alertas. Su planilla de dotación llega "sucia", como
llegan las reales.

## Bitácora

### 2026-10-01
- Primera versión: 4 módulos, 15 ejemplos, Pyodide 0.26.4, glosario y CI.
