/* paper-session site — progressive enhancement only.
 *
 * Nothing here is required for the page to work. With JavaScript off:
 *   - the compatibility ledger shows in full as an open <details> table
 *   - the chips never appear
 *   - the theme follows prefers-color-scheme
 *   - every copy button stays hidden and its text stays plain and selectable
 *   - the print button stays hidden and Ctrl+P prints the sheet
 *   - the whole of scan-back/SKILL.md sits open on the page
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

  /* ---- Copyable sentences (the first-session openers) ------------------- */

  var sayButtons = document.querySelectorAll("[data-copy]");
  if (sayButtons.length && CAN_COPY) {
    var sayStatus = document.getElementById("copy-status");
    var sayTimer = null;

    var announce = function (message) {
      if (sayStatus) sayStatus.textContent = message;
    };

    var wireSay = function (button) {
      var source = document.getElementById(button.getAttribute("data-copy"));
      if (!source) return;
      var original = button.firstChild.nodeValue;

      button.hidden = false;
      button.setAttribute("data-state", "idle");

      button.addEventListener("click", function () {
        var text = source.textContent.replace(/\s+/g, " ").trim();
        if (sayTimer) window.clearTimeout(sayTimer);
        navigator.clipboard.writeText(text).then(
          function () {
            button.setAttribute("data-state", "done");
            button.firstChild.nodeValue = "Copied";
            announce("Copied to the clipboard.");
            sayTimer = window.setTimeout(function () {
              button.setAttribute("data-state", "idle");
              button.firstChild.nodeValue = original;
              announce("");
            }, 4000);
          },
          function () {
            selectContents(source);
            button.firstChild.nodeValue = "Selected";
            announce(
              "The clipboard is not available. The sentence is selected — " +
                "press Ctrl or Command and C."
            );
            sayTimer = window.setTimeout(function () {
              button.setAttribute("data-state", "idle");
              button.firstChild.nodeValue = original;
            }, 6000);
          }
        );
      });
    };

    for (var s = 0; s < sayButtons.length; s++) wireSay(sayButtons[s]);
  }

  /* ---- Copy a whole file (the return-trip page) ------------------------- */

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
              "file is open below and already selected — copy it yourself."
          : "This browser will not let the page reach your clipboard. The " +
              "file is open below — select all of it and copy it yourself.",
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

  /* ---- Print is a verb ------------------------------------------------- */

  /* The sheet page carries one control and it does one thing. It ships hidden
     and is revealed only where a print can actually be asked for, the same way
     the copy buttons are, so a browser that cannot print never shows a dead
     button. Ctrl+P does the same job with JavaScript off, which is why the
     page is the sheet rather than a preview of one. */

  var printButtons = document.querySelectorAll("[data-print]");
  if (printButtons.length && typeof window.print === "function") {
    for (var p = 0; p < printButtons.length; p++) {
      (function (button) {
        button.hidden = false;
        button.addEventListener("click", function () {
          window.print();
        });
      })(printButtons[p]);
    }
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

  /* ---- "What are you using?" ------------------------------------------- */

  var root = document.querySelector("[data-ledger]");
  var dataEl = document.getElementById("ledger-data");
  if (!root || !dataEl) return;

  var data;
  try {
    data = JSON.parse(dataEl.textContent);
  } catch (e) {
    return; /* leave the full table exactly as it is */
  }
  if (!data || !data.rows || !data.rows.length) return;

  var chips = root.querySelector("[data-chips]");
  var answer = root.querySelector("[data-answer]");
  var full = root.querySelector("[data-ledger-full]");
  if (!chips || !answer) return;

  var buttons = chips.querySelectorAll(".chip");
  if (!buttons.length) return;

  chips.hidden = false;
  if (full) full.open = false;

  var printHref = root.getAttribute("data-link-print") || "";
  var installHref = root.getAttribute("data-link-install") || "";

  function textNode(tag, className, text) {
    var el = document.createElement(tag);
    if (className) el.className = className;
    el.textContent = text;
    return el;
  }

  function show(index, button) {
    var row = data.rows[index];
    if (!row) return;

    for (var i = 0; i < buttons.length; i++) {
      buttons[i].setAttribute("aria-pressed", buttons[i] === button ? "true" : "false");
    }

    answer.textContent = "";

    if (row.status) {
      answer.appendChild(textNode("span", "answer__status", row.status));
    }

    /* One honest sentence, assembled out of the ledger row itself. */
    var line = textNode("p", "answer__line", "");
    var agent = document.createElement("strong");
    agent.textContent = row.agent;
    line.appendChild(agent);
    line.appendChild(document.createTextNode(" — " + row.loop + "."));
    answer.appendChild(line);

    var how = textNode("p", "answer__line", "How you install it: " + row.install + ".");
    answer.appendChild(how);

    /* Every ledger column past the third, whatever it turns out to be. The
       table grew an "Also install" column once already; an answer that
       silently omits it tells someone how to install without saying what
       else they have to install. */
    if (row.extra && row.extra.length) {
      var extras = document.createElement("dl");
      extras.className = "answer__extra";
      var wrote = false;
      for (var e = 0; e < row.extra.length; e++) {
        var cell = row.extra[e];
        if (!cell || !cell.value) continue;
        extras.appendChild(textNode("dt", null, cell.header || "Also"));
        extras.appendChild(textNode("dd", null, cell.value));
        wrote = true;
      }
      if (wrote) answer.appendChild(extras);
    }

    var links = document.createElement("p");
    links.className = "btn-row";
    if (printHref) {
      var a = document.createElement("a");
      a.className = "btn";
      a.href = printHref;
      a.textContent = "Print a specimen first";
      links.appendChild(a);
    }
    if (installHref) {
      var b = document.createElement("a");
      b.className = "btn";
      b.href = installHref;
      b.textContent = "Install directions";
      links.appendChild(b);
    }
    answer.appendChild(links);
  }

  for (var i = 0; i < buttons.length; i++) {
    (function (button) {
      button.setAttribute("aria-pressed", "false");
      button.addEventListener("click", function () {
        show(parseInt(button.getAttribute("data-row"), 10), button);
      });
    })(buttons[i]);
  }
})();
