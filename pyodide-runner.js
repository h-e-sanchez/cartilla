/* Ejecuta código Python en el navegador con Pyodide.
   - Carga diferida: Python (~10 MB) se descarga recién al primer "Ejecutar".
   - Versión fijada para que la salida sea estable.
   - Los CSV de data/ se copian al sistema de archivos virtual, así los ejemplos usan
     las mismas rutas relativas ("data/ventas_mensuales.csv") que en un Python local.
   - Cada ejecución corre en un espacio de nombres nuevo: un ejemplo no ensucia al otro. */
(function () {
  "use strict";

  var VERSION = "0.26.4";
  var BASE = "https://cdn.jsdelivr.net/pyodide/v" + VERSION + "/full/";
  var cargando = null;
  var openpyxlListo = false;

  function cargarScript(src) {
    return new Promise(function (ok, falla) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = ok;
      s.onerror = function () { falla(new Error("No se pudo descargar Pyodide. Revisa tu conexión.")); };
      document.head.appendChild(s);
    });
  }

  function obtener(datos, avisar) {
    if (!cargando) {
      cargando = (async function () {
        avisar("Descargando Python (solo la primera vez)…");
        await cargarScript(BASE + "pyodide.js");
        var py = await window.loadPyodide({ indexURL: BASE });
        avisar("Cargando pandas…");
        await py.loadPackage(["pandas"]);
        avisar("Copiando datos de ejemplo…");
        var dir = py.FS.cwd() + "/data";  // /home/pyodide/data: mismas rutas relativas que en local
        py.FS.mkdirTree(dir);
        await Promise.all(datos.map(async function (nombre) {
          var r = await fetch("data/" + nombre);
          if (!r.ok) throw new Error("No se pudo leer data/" + nombre);
          py.FS.writeFile(dir + "/" + nombre, new Uint8Array(await r.arrayBuffer()));
        }));
        return py;
      })();
      cargando.catch(function () { cargando = null; });  // permite reintentar
    }
    return cargando;
  }

  /* Deja solo la parte del traceback que corresponde al código del ejemplo. */
  function limpiarError(texto) {
    var i = texto.indexOf('File "<exec>"');
    return i >= 0 ? "Traceback:\n  " + texto.slice(i) : texto;
  }

  async function ejecutar(codigo, datos, avisar) {
    var py = await obtener(datos, avisar);
    if (!openpyxlListo && /to_excel|read_excel|ExcelWriter|openpyxl/.test(codigo)) {
      // openpyxl no viene en la distribución de Pyodide: se instala desde PyPI (es Python puro).
      avisar("Instalando openpyxl…");
      await py.loadPackage(["micropip"]);
      await py.pyimport("micropip").install("openpyxl");
      openpyxlListo = true;
    }
    var lineas = [];
    py.setStdout({ batched: function (s) { lineas.push(s); } });
    py.setStderr({ batched: function (s) { lineas.push(s); } });
    var ns = py.globals.get("dict")();
    try {
      await py.runPythonAsync(codigo, { globals: ns });
      return { ok: true, texto: lineas.join("\n") };
    } catch (e) {
      var previo = lineas.length ? lineas.join("\n") + "\n\n" : "";
      return { ok: false, texto: previo + limpiarError(String(e && e.message ? e.message : e)) };
    } finally {
      ns.destroy();
    }
  }

  window.CartillaPython = { ejecutar: ejecutar, version: VERSION };
})();
