/**
 * Client-side access gate for index.html (hub only).
 * Not a substitute for server auth; the SHA-256 hash is visible in source.
 * Default passphrase: SignosCopiapo2026 — regenerate PASSWORD_SHA256_HEX if you change it.
 */
(function () {
  var STORAGE_KEY = "signos_hub_auth_v1";
  var PASSWORD_SHA256_HEX =
    "b572b0f48606cc092630abe6046fb22e3583f6ce51bbf19731e3003a73204292";

  var screen = document.getElementById("hub-auth-screen");
  var app = document.getElementById("hub-app");
  var form = document.getElementById("hub-auth-form");
  var input = document.getElementById("hub-auth-pass");
  var err = document.getElementById("hub-auth-error");

  if (!screen || !app || !form || !input) {
    return;
  }

  function unlock() {
    screen.classList.add("hub-auth-screen--done");
    screen.setAttribute("aria-hidden", "true");
    app.classList.add("hub-app--ready");
    app.removeAttribute("hidden");
  }

  function showError(msg) {
    if (!err) return;
    err.textContent = msg;
    err.hidden = false;
  }

  function clearError() {
    if (!err) return;
    err.textContent = "";
    err.hidden = true;
  }

  function sha256Hex(text) {
    var enc = new TextEncoder();
    return crypto.subtle
      .digest("SHA-256", enc.encode(text))
      .then(function (buf) {
        return Array.from(new Uint8Array(buf))
          .map(function (b) {
            return b.toString(16).padStart(2, "0");
          })
          .join("");
      });
  }

  if (sessionStorage.getItem(STORAGE_KEY) === "1") {
    unlock();
    return;
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    clearError();
    var value = (input.value || "").trim();
    if (!value) {
      showError("Ingrese la contraseña.");
      return;
    }
    sha256Hex(value)
      .then(function (hex) {
        if (hex === PASSWORD_SHA256_HEX) {
          sessionStorage.setItem(STORAGE_KEY, "1");
          unlock();
          input.value = "";
        } else {
          showError("Contraseña incorrecta.");
          input.select();
        }
      })
      .catch(function () {
        showError("No se pudo verificar la contraseña en este navegador.");
      });
  });
})();
