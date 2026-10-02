# cartilla

> Manual rápido de Python y pandas para analistas de control de gestión y finanzas que vienen de Excel. Cada ejemplo trae su equivalente en Excel, se copia con un clic y se ejecuta en el navegador, sin instalar nada.

**Demo:** <https://h-e-sanchez.github.io/cartilla/>

Parte del portafolio **Control de gestión, construido como software**, de Hernán Elías Sánchez:
[`centinela`](https://h-e-sanchez.github.io/centinela/) es la vitrina de reportes Power BI,
[`consulta`](https://h-e-sanchez.github.io/consulta/) es el taller de SQL en el navegador y
`cartilla` es el manual.

## Diseño

- **Una sola fuente de verdad:** cada ejemplo es un `.py` en `ejemplos/`. La página lee ese mismo archivo y los tests lo ejecutan, así que el código mostrado y el probado no pueden divergir.
- **Salida verificada:** `herramientas/ejemplos.py` corre cada ejemplo y guarda su salida en un `.out.txt`. `pytest` falla si un cambio en el código o en los datos altera lo que el manual promete.
- **Python en el navegador:** [Pyodide](https://pyodide.org/) (versión fijada) se descarga recién al primer "Ejecutar". El código es editable: se aprende cambiándolo y volviendo a correr.
- **Datos 100% sintéticos y reproducibles:** `data/generar_datos_sinteticos.py` (`SEMILLA = 42`, solo biblioteca estándar) crea los CSV de "Comercial Ejemplo S.A.". Están en formato tidy, con columnas en snake_case en español y sin tildes.
- **Formato pensado para quien viene de Excel:** cada ejemplo abre con *Qué aprendes* y *En Excel*, y el [glosario](https://h-e-sanchez.github.io/cartilla/glosario.html) traduce los términos.

## Uso

```bash
pip install -r requirements.txt -r requirements-dev.txt
python data/generar_datos_sinteticos.py   # regenera los CSV (idénticos con la misma semilla)
python -m herramientas.ejemplos           # regenera manifest.json y las salidas esperadas
python -m pytest -q                       # ejemplos, salidas y generador
ruff check .
python -m http.server 8000                # abre http://localhost:8000
```

Cada ejemplo también se puede correr directo desde la raíz del repo, por ejemplo
`python ejemplos/01-pandas-basico/04_agrupar.py`.

## Módulos

| # | Módulo | Ejemplos |
|---|---|---|
| 01 | pandas básico | importar, inspeccionar, filtrar, agrupar, unir, exportar |
| 02 | Limpieza y calidad de datos | nulos y fechas mixtas, duplicados y nombres inconsistentes |
| 03 | Series de tiempo | fechas, resample mensual, promedio móvil, YoY, presupuesto vs. real |
| 04 | Automatización de reportes | Excel con varias hojas, función con prueba |

Para agregar un ejemplo, crea `ejemplos/<módulo>/NN_nombre.py` con el encabezado
`# Título:`, `# Qué aprendes:`, `# En Excel:` y `# ---`, y corre `python -m herramientas.ejemplos`.

El plan de crecimiento está en [`ROADMAP.md`](ROADMAP.md). El despliegue es estático (GitHub
Pages desde `main`), sin paso de build.

## English

A hands-on Python and pandas primer by Hernán Elías Sánchez (management control, FP&A, People
Analytics) for analysts coming from Excel. Each example states what it teaches and its Excel equivalent, can be copied with one
click and runs in the browser through Pyodide, with no installation. Examples are plain `.py`
files that the page renders and the test suite executes, so the published code always matches
its expected output. All data is synthetic, generated with a fixed seed.
