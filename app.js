/* cartilla — arma las páginas a partir de ejemplos/manifest.json y de los mismos .py
   que corren los tests. Sin build ni dependencias: JS plano. */
(function () {
  "use strict";

  var SEPARADOR = "# ---";

  function el(tag, attrs, hijos) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      if (k === "texto") n.textContent = attrs[k];
      else if (k === "clase") n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (hijos || []).forEach(function (h) { if (h) n.appendChild(h); });
    return n;
  }

  async function leer(ruta) {
    var r = await fetch(ruta);
    if (!r.ok) throw new Error("No se pudo leer " + ruta);
    return r.text();
  }

  /* El código visible es lo que va después de "# ---"; el encabezado ya se muestra arriba. */
  function cuerpo(fuente) {
    var lineas = fuente.replace(/\r\n/g, "\n").split("\n");
    var i = lineas.findIndex(function (l) { return l.trim() === SEPARADOR; });
    return lineas.slice(i + 1).join("\n").replace(/^\n+/, "").replace(/\n+$/, "\n");
  }

  async function copiar(texto, boton) {
    var original = boton.textContent;
    try {
      await navigator.clipboard.writeText(texto);
      boton.textContent = "Copiado ✓";
    } catch (e) {
      boton.textContent = "Selecciona y copia";
    }
    setTimeout(function () { boton.textContent = original; }, 1600);
  }

  function tarjetaEjemplo(ej, n, codigo, esperada, datos) {
    var editor = el("textarea", {
      clase: "editor", spellcheck: "false", "aria-label": "Código del ejemplo " + ej.titulo,
      rows: String(Math.min(codigo.split("\n").length + 1, 26))
    });
    editor.value = codigo;

    var estado = el("span", { clase: "estado-run", role: "status" });
    var salidaPropia = el("pre", { hidden: "" });
    var etiquetaPropia = el("p", { clase: "etiqueta", texto: "Tu salida", hidden: "" });

    var bEjecutar = el("button", { type: "button", clase: "btn primario", texto: "▶ Ejecutar" });
    var bCopiar = el("button", { type: "button", clase: "btn", texto: "Copiar" });
    var bRestaurar = el("button", { type: "button", clase: "btn", texto: "Restaurar" });

    bEjecutar.addEventListener("click", async function () {
      bEjecutar.disabled = true;
      var t0 = performance.now();
      try {
        var res = await window.CartillaPython.ejecutar(editor.value, datos, function (m) { estado.textContent = m; });
        salidaPropia.textContent = res.texto || "(sin salida: agrega un print())";
        salidaPropia.className = res.ok ? "" : "error";
        estado.textContent = res.ok
          ? "Listo en " + Math.round(performance.now() - t0) + " ms"
          : "Error: lee el mensaje de abajo";
      } catch (e) {
        salidaPropia.textContent = (e && e.message) || (e && e.name) || String(e);
        salidaPropia.className = "error";
        estado.textContent = "No se pudo ejecutar";
      }
      salidaPropia.hidden = false;
      etiquetaPropia.hidden = false;
      bEjecutar.disabled = false;
    });
    bCopiar.addEventListener("click", function () { copiar(editor.value, bCopiar); });
    bRestaurar.addEventListener("click", function () {
      editor.value = codigo;
      salidaPropia.hidden = true;
      etiquetaPropia.hidden = true;
      estado.textContent = "";
    });

    var excel = el("p", { clase: "excel" }, [el("strong", { texto: "En Excel: " }), document.createTextNode(ej.excel)]);
    var detalles = el("details", {}, [
      el("summary", { texto: "Salida esperada" }),
      el("pre", { texto: esperada })
    ]);

    return el("article", { clase: "ejemplo", id: ej.id }, [
      el("div", { clase: "ejemplo-cab" }, [
        el("h3", { texto: n + ". " + ej.titulo }),
        el("p", { texto: "Qué aprendes: " + ej.aprendes }),
        excel
      ]),
      editor,
      el("div", { clase: "acciones" }, [bEjecutar, bCopiar, bRestaurar, estado]),
      el("div", { clase: "salida" }, [detalles, etiquetaPropia, salidaPropia])
    ]);
  }

  async function paginaModulo(man) {
    var id = new URLSearchParams(location.search).get("m") || man.modulos[0].id;
    var idx = man.modulos.findIndex(function (m) { return m.id === id; });
    if (idx < 0) idx = 0;
    var mod = man.modulos[idx];

    document.title = "cartilla — " + mod.titulo;
    document.getElementById("titulo-modulo").textContent = mod.id.slice(0, 2) + " · " + mod.titulo;
    document.getElementById("migas-modulo").textContent = mod.titulo;
    document.getElementById("descripcion-modulo").textContent = mod.descripcion;

    var cont = document.getElementById("ejemplos");
    var textos = await Promise.all(mod.ejemplos.map(function (ej) {
      return Promise.all([leer("ejemplos/" + ej.archivo), leer("ejemplos/" + ej.archivo.replace(/\.py$/, ".out.txt"))]);
    }));
    mod.ejemplos.forEach(function (ej, i) {
      cont.appendChild(tarjetaEjemplo(ej, i + 1, cuerpo(textos[i][0]), textos[i][1], man.datos));
    });

    var nav = document.getElementById("modulo-nav");
    var ant = man.modulos[idx - 1], sig = man.modulos[idx + 1];
    nav.appendChild(ant ? el("a", { href: "modulo.html?m=" + ant.id, texto: "← " + ant.titulo }) : el("span"));
    nav.appendChild(sig ? el("a", { href: "modulo.html?m=" + sig.id, texto: sig.titulo + " →" }) : el("a", { href: "index.html", texto: "Volver a la carátula" }));

    if (location.hash) {
      var destino = document.getElementById(location.hash.slice(1));
      if (destino) destino.scrollIntoView();
    }
  }

  function paginaInicio(man) {
    man.modulos.forEach(function (m) {
      var span = document.querySelector('.conteo[data-modulo="' + m.id + '"]');
      if (span) span.textContent = m.ejemplos.length + " ejemplos";
    });
  }

  fetch("ejemplos/manifest.json")
    .then(function (r) { return r.json(); })
    .then(function (man) {
      if (document.getElementById("ejemplos")) return paginaModulo(man);
      paginaInicio(man);
    })
    .catch(function (e) {
      var cont = document.getElementById("ejemplos");
      if (cont) cont.textContent = "No se pudo cargar el manual (" + e.message + "). Si abriste el archivo con doble clic, sírvelo con: python -m http.server";
    });
})();
