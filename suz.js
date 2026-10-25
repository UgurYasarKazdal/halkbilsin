(function () {
  "use strict";
  var bolum = document.getElementById("deneyin");
  if (!bolum) return;
  var dugmeler = Array.prototype.slice.call(bolum.querySelectorAll("button[data-kimi]"));
  var ogeler = Array.prototype.slice.call(bolum.querySelectorAll("li[data-kimi]"));
  var sayac = document.getElementById("deneyin-sayac");
  var bos = document.getElementById("deneyin-bos");
  function uygula() {
    var secili = dugmeler
      .filter(function (b) { return b.getAttribute("aria-pressed") === "true"; })
      .map(function (b) { return b.getAttribute("data-kimi"); });
    var gorunen = 0;
    ogeler.forEach(function (li) {
      var kimiler = li.getAttribute("data-kimi").split("|");
      var goster = secili.length > 0 && secili.some(function (s) { return kimiler.indexOf(s) !== -1; });
      li.hidden = !goster;
      if (goster) gorunen++;
    });
    if (bos) bos.hidden = secili.length > 0;
    if (sayac) {
      sayac.textContent = secili.length
        ? (gorunen
            ? "Profilinize uyan " + gorunen + " kayıt gösteriliyor."
            : "Bu seçim için henüz kayıt yok; kapsam genişledikçe eklenecek.")
        : "";
    }
  }
  dugmeler.forEach(function (b) {
    b.addEventListener("click", function () {
      b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
      uygula();
    });
  });
  uygula(); // JS varsa: seçim yapılmadan kart gösterilmez; JS yoksa tüm liste görünür kalır
})();
