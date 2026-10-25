(function () {
  "use strict";
  var bolum = document.getElementById("deneyin");
  if (!bolum) return;
  var dugmeler = Array.prototype.slice.call(bolum.querySelectorAll("button[data-kimi]"));
  var ogeler = Array.prototype.slice.call(bolum.querySelectorAll("li[data-kimi]"));
  var sayac = document.getElementById("deneyin-sayac");
  function uygula() {
    var secili = dugmeler
      .filter(function (b) { return b.getAttribute("aria-pressed") === "true"; })
      .map(function (b) { return b.getAttribute("data-kimi"); });
    var gorunen = 0;
    ogeler.forEach(function (li) {
      var kimiler = li.getAttribute("data-kimi").split("|");
      var goster = secili.length === 0 || secili.some(function (s) { return kimiler.indexOf(s) !== -1; });
      li.hidden = !goster;
      if (goster) gorunen++;
    });
    if (sayac) {
      sayac.textContent = secili.length
        ? "Seçiminize uyan " + gorunen + " kayıt gösteriliyor."
        : "";
    }
  }
  dugmeler.forEach(function (b) {
    b.addEventListener("click", function () {
      b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
      uygula();
    });
  });
})();
