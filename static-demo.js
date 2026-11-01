// Soulsolid static demo shim.
//
// The static demo is a crawl of a real Soulsolid instance (see demo/crawl.py).
// Every HTMX fragment the crawler fetched is saved as /_hx/<hash>/, where
// <hash> is the FNV-1a hash of the canonical request URL. This script rewrites
// HTMX GET requests to those files and blocks everything that would change
// state, since there is no server behind the demo.
(function () {
  "use strict";

  var READ_ONLY_MSG = "This is a read-only demo. Run Soulsolid yourself to try this out.";
  var MISSING_MSG = "Not available in the static demo.";
  var REPO_URL = "https://github.com/contre95/soulsolid";

  // There is no server to rebuild a page on a history cache miss, so fall back to a full load.
  function configure() {
    if (window.htmx) {
      htmx.config.refreshOnHistoryMiss = true;
      htmx.config.historyCacheSize = 20;
    }
  }
  configure();
  document.addEventListener("DOMContentLoaded", configure);

  // Must match canonical_url() and fnv1a() in demo/crawl.py.
  function fnv1a(str) {
    var bytes = new TextEncoder().encode(str);
    var h = 0x811c9dc5;
    for (var i = 0; i < bytes.length; i++) {
      h ^= bytes[i];
      h = Math.imul(h, 0x01000193) >>> 0;
    }
    return ("0000000" + h.toString(16)).slice(-8);
  }

  function canonicalURL(pathname, pairs) {
    var kept = pairs
      .filter(function (p) { return p[1] !== "" && p[0] !== "org.htmx.cache-buster"; })
      .map(function (p) { return [String(p[0]), String(p[1])]; })
      .sort(function (a, b) {
        return a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : 0;
      });
    if (!kept.length) return pathname;
    return pathname + "?" + kept.map(function (p) {
      return encodeURIComponent(p[0]) + "=" + encodeURIComponent(p[1]);
    }).join("&");
  }

  function toast(msg) {
    if (typeof window.showErrToast === "function") {
      window.showErrToast(msg);
    } else {
      alert(msg);
    }
  }

  // Static file path -> the URL the app would have shown, for hx-push-url.
  var prettyURLs = {};

  // Skip the app's "Are you sure?" dialog for writes: they are blocked anyway.
  document.addEventListener("htmx:confirm", function (evt) {
    if (evt.detail.verb && evt.detail.verb !== "get") {
      evt.preventDefault();
      evt.stopImmediatePropagation();
      toast(READ_ONLY_MSG);
    }
  });

  document.addEventListener("htmx:configRequest", function (evt) {
    var d = evt.detail;
    if (d.verb !== "get") {
      evt.preventDefault();
      toast(READ_ONLY_MSG);
      return;
    }
    var url = new URL(d.path, location.origin);
    if (url.origin !== location.origin) return;

    var pairs = [];
    url.searchParams.forEach(function (v, k) { pairs.push([k, v]); });
    d.formData.forEach(function (v, k) { pairs.push([k, v]); });

    var canonical = canonicalURL(url.pathname, pairs);
    var staticPath = "/_hx/" + fnv1a(canonical) + "/";
    prettyURLs[staticPath] = canonical;

    d.path = staticPath;
    d.parameters = {};
  });

  document.addEventListener("htmx:beforeHistoryUpdate", function (evt) {
    var h = evt.detail.history;
    var pretty = prettyURLs[h.path.split("#")[0]];
    if (pretty) h.path = pretty;
  });

  document.addEventListener("htmx:responseError", function (evt) {
    if (evt.detail.xhr && evt.detail.xhr.status === 404) {
      toast(MISSING_MSG);
    }
  });

  function addBanner() {
    if (document.getElementById("static-demo-banner")) return;
    var b = document.createElement("a");
    b.id = "static-demo-banner";
    b.href = REPO_URL;
    b.target = "_blank";
    b.rel = "noopener";
    b.textContent = "Read-only demo \u00b7 Get Soulsolid on GitHub \u2192";
    b.style.cssText = [
      "position:fixed", "bottom:12px", "right:12px", "z-index:60",
      "padding:6px 12px", "border-radius:9999px", "font:600 12px/1.4 system-ui,sans-serif",
      "background:#7c3aed", "color:#fff", "text-decoration:none",
      "box-shadow:0 4px 14px rgba(0,0,0,.25)", "opacity:.92",
    ].join(";");
    document.body.appendChild(b);
  }
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", addBanner);
  } else {
    addBanner();
  }
})();
