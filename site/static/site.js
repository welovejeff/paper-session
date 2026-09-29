/* paper-session site: progressive enhancement only.
 *
 * Nothing here is required for the page to work. With JavaScript off:
 *   - "Copy instructions for your AI" is a plain link that opens
 *     copy-instructions.txt, and the masthead copy button stays hidden
 *   - the theme follows prefers-color-scheme
 *   - the scan-back copy button stays hidden, and the whole file sits open
 *     on the page (its <details> ships open) beside a link to the raw file
 *   - the landing-page film plays from the browser's own controls
 * Everything below only ever removes noise for people who have JS on.
 */
(function () {
  "use strict";

  /* ---- Clipboard ------------------------------------------------------- */

  /* True only where writing to the clipboard can actually work. Buttons ship
     hidden and are revealed one at a time, so a browser that cannot copy
     never shows a control that would do nothing. */
  var CAN_COPY = !!(
    window.isSecureContext &&
    navigator.clipboard &&
    typeof navigator.clipboard.writeText === "function"
  );

  function selectContents(el) {
    try {
      var range = document.createRange();
      range.selectNodeContents(el);
      var selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      return true;
    } catch (e) {
      return false;
    }
  }

  /* ---- Copy a whole file (Install #scan-back) --------------------------- */

  var fileBox = document.querySelector("[data-copy-file]");
  var fileBtn = document.querySelector("[data-copy-file-button]");
  var fileStatus = document.querySelector("[data-copy-file-status]");
  if (fileBox && fileBtn && fileStatus) {
    /* Only now is the button real, and only now is it safe to fold the file
       away: the script that closed it is the script that can reopen it. */
    var fileSource = document.querySelector("[data-copy-file-source]");
    fileBtn.hidden = false;
    if (fileSource) fileSource.open = false;

    var fileIdle = fileBtn.textContent;
    var fileTimer = null;

    var say = function (message, state) {
      fileStatus.textContent = message;
      fileStatus.setAttribute("data-state", state);
    };

    var fileSucceeded = function () {
      if (!fileBtn.style.minWidth) {
        fileBtn.style.minWidth = Math.ceil(fileBtn.getBoundingClientRect().width) + "px";
      }
      fileBtn.textContent = "Copied";
      say(
        "Copied. Paste it as one message into the chat your photographs are " +
          "going to, then send the pictures.",
        "ok"
      );
      if (fileTimer) clearTimeout(fileTimer);
      fileTimer = setTimeout(function () {
        fileBtn.textContent = fileIdle;
      }, 8000);
    };

    var fileFailed = function () {
      if (fileSource) fileSource.open = true;
      var selected = selectContents(fileBox);
      var ok = false;
      if (selected) {
        try {
          ok = document.execCommand("copy");
        } catch (e) {
          ok = false;
        }
      }
      if (ok) {
        fileSucceeded();
        return;
      }
      say(
        selected
          ? "This browser will not let the page reach your clipboard. The " +
              "file is open below and already selected. Copy it yourself."
          : "This browser will not let the page reach your clipboard. The " +
              "file is open below. Select all of it and copy it yourself.",
        "warn"
      );
    };

    fileBtn.addEventListener("click", function () {
      if (!CAN_COPY) {
        fileFailed();
        return;
      }
      try {
        navigator.clipboard.writeText(fileBox.textContent).then(
          fileSucceeded,
          fileFailed
        );
      } catch (e) {
        fileFailed();
      }
    });
  }

  /* ---- Copy instructions for your AI ----------------------------------

     Every [data-copy-ai] element on the page is wired here. The text copied
     is always #copy-instructions-text, which _base.html puts on every page
     from site/static/copy-instructions.txt.

     The page contract (the primary call to action, a real link):

       <div class="copy-cta">
         <a class="btn btn--primary copy-cta__btn"
            href="{{ copy_instructions_url }}" data-copy-ai>Copy instructions for your AI</a>
         <p class="copy-cta__status" data-copy-ai-status role="status"
            aria-live="polite"
            data-done="Copied. Paste it into your AI chat and say what you are working on."></p>
       </div>

     JS off: the link opens the text file, and the visitor copies it there.
     JS on: a click copies the text instead of navigating, the control reads
     "Copied" for four seconds, and the data-done sentence is written into
     the [data-copy-ai-status] inside the same .copy-cta. The sentence stays
     after the label reverts, because it says what to do next. If the page
     cannot reach the clipboard, the link navigates exactly as it would have
     without JS.

     The masthead variant is a <button data-copy-ai data-href="..." hidden>:
     a button does nothing without JS, so it ships hidden and is revealed
     here. When copying fails it opens data-href, the same text file.

     A control whose label sits in a child element can mark that child
     [data-copy-ai-label]; only the child's text is swapped then. */

  var aiSource = document.getElementById("copy-instructions-text");
  var aiControls = document.querySelectorAll("[data-copy-ai]");
  if (aiSource && aiControls.length) {
    var aiText = aiSource.textContent;

    /* The older path, for browsers without the async clipboard API or where
       it refuses. Returns whether the text actually reached the clipboard. */
    var aiLegacyCopy = function () {
      var ta = document.createElement("textarea");
      ta.value = aiText;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      var ok = false;
      try {
        ok = document.execCommand("copy");
      } catch (e) {
        ok = false;
      }
      document.body.removeChild(ta);
      return ok;
    };

    var wireAi = function (el) {
      var labelEl = el.querySelector("[data-copy-ai-label]") || el;
      var idle = labelEl.textContent;
      var timer = null;
      var wrapper = typeof el.closest === "function" ? el.closest(".copy-cta") : null;
      var status = wrapper ? wrapper.querySelector("[data-copy-ai-status]") : null;
      var fallback = el.getAttribute("href") || el.getAttribute("data-href") || "";

      el.hidden = false;
      el.setAttribute("data-state", "idle");

      var done = function () {
        /* Hold the control at its idle width, so the shorter "Copied" does
           not make it jump. Measured on first use, when it is on screen. */
        if (!el.style.minWidth) {
          el.style.minWidth = Math.ceil(el.getBoundingClientRect().width) + "px";
        }
        labelEl.textContent = "Copied";
        el.setAttribute("data-state", "done");
        if (timer) window.clearTimeout(timer);
        timer = window.setTimeout(function () {
          labelEl.textContent = idle;
          el.setAttribute("data-state", "idle");
        }, 4000);
        if (status) {
          var message = status.getAttribute("data-done") || "Copied.";
          /* Emptied first, so a second copy is announced again. */
          status.textContent = "";
          window.setTimeout(function () {
            status.textContent = message;
          }, 50);
        }
      };

      var navigate = function () {
        if (fallback) window.location.href = fallback;
      };

      el.addEventListener("click", function (event) {
        if (CAN_COPY) {
          event.preventDefault();
          var pending = null;
          try {
            pending = navigator.clipboard.writeText(aiText);
          } catch (e) {
            pending = null;
          }
          if (pending && typeof pending.then === "function") {
            pending.then(done, function () {
              if (aiLegacyCopy()) done();
              else navigate();
            });
          } else if (aiLegacyCopy()) {
            done();
          } else {
            navigate();
          }
          return;
        }
        if (aiLegacyCopy()) {
          event.preventDefault();
          done();
          return;
        }
        /* Copying failed. A link carries on to the text file by itself; a
           button has nowhere to go unless it is sent there. */
        if (el.tagName !== "A") navigate();
      });
    };

    for (var a = 0; a < aiControls.length; a++) wireAi(aiControls[a]);
  }

  /* ---- Theme toggle ---------------------------------------------------- */

  var toggle = document.querySelector("[data-theme-toggle]");
  if (toggle) {
    toggle.hidden = false;

    var label = function () {
      var explicit = document.documentElement.getAttribute("data-theme");
      var dark =
        explicit === "dark" ||
        (!explicit &&
          window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);
      toggle.textContent = dark ? "Light" : "Dark";
      toggle.setAttribute(
        "aria-label",
        dark ? "Switch to the light theme" : "Switch to the dark theme"
      );
    };

    label();

    toggle.addEventListener("click", function () {
      var explicit = document.documentElement.getAttribute("data-theme");
      var dark =
        explicit === "dark" ||
        (!explicit &&
          window.matchMedia &&
          window.matchMedia("(prefers-color-scheme: dark)").matches);
      var next = dark ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      try {
        localStorage.setItem("ps-theme", next);
      } catch (e) {}
      label();
    });
  }
})();

/* ---- Hero film: one centred play control over the poster ---------------
   The <video> ships with native controls, so with JS off it plays as-is.
   Here those controls are held back until the film starts, the centred
   button is the only thing on the poster, and both come back at the end. */
(function () {
  "use strict";
  var figure = document.querySelector("[data-film]");
  if (!figure) return;
  var video = figure.querySelector("video");
  var play = figure.querySelector("[data-film-play]");
  if (!video || !play || typeof video.play !== "function") return;

  function showPoster() {
    video.controls = false;
    play.hidden = false;
  }

  function start() {
    play.hidden = true;
    video.controls = true;
    var playing = video.play();
    if (playing && typeof playing.catch === "function") {
      /* Playback refused: the native controls are showing, one press plays. */
      playing.catch(function () {});
    }
    video.focus();
  }

  showPoster();
  play.addEventListener("click", start);
  video.addEventListener("ended", function () {
    if (document.fullscreenElement && document.exitFullscreen) {
      document.exitFullscreen().catch(function () {});
    }
    video.load(); /* back to the poster frame */
    showPoster();
    play.focus({ preventScroll: true });
  });
})();
