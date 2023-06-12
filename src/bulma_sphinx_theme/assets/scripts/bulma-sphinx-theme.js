import Gumshoe from "./gumshoe-patched.js";

var tocScroll = null;
var header = null;
var lastScrollTop = window.pageYOffset || document.documentElement.scrollTop;
const GO_TO_TOP_OFFSET = 64;
var prefersDark = window.matchMedia("(prefers-color-scheme: dark)");

/*******************************************************************************
 * Theme switcher
 */

function autoTheme(e) {
  document.documentElement.dataset.theme = prefersDark.matches
    ? "dark"
    : "light";
}

function setTheme(mode) {
  if (mode !== "light" && mode !== "dark" && mode !== "auto") {
    console.error(`Got invalid theme mode: ${mode}. Resetting to auto.`);
    mode = "auto";
  }

  // get the theme
  var colorScheme = prefersDark.matches ? "dark" : "light";
  document.documentElement.dataset.mode = mode;
  var theme = mode == "auto" ? colorScheme : mode;
  document.documentElement.dataset.theme = theme;

  // save mode and theme
  localStorage.setItem("mode", mode);
  localStorage.setItem("theme", theme);
  console.log(`[BST]: Changed to ${mode} mode using the ${theme} theme.`);

  // add a listener if set on auto
  prefersDark.onchange = mode == "auto" ? autoTheme : "";
}

function cycleMode() {
  const defaultMode = document.documentElement.dataset.defaultMode || "auto";
  const currentMode = localStorage.getItem("mode") || defaultMode;

  var loopArray = (arr, current) => {
    var nextPosition = arr.indexOf(current) + 1;
    if (nextPosition === arr.length) {
      nextPosition = 0;
    }
    return arr[nextPosition];
  };

  // make sure the next theme after auto is always a change
  var modeList = prefersDark.matches
    ? ["auto", "light", "dark"]
    : ["auto", "dark", "light"];
  var newMode = loopArray(modeList, currentMode);
  setTheme(newMode);
}

function addModeListener() {
  // the theme was set a first time using the initial mini-script
  // running setMode will ensure the use of the dark mode if auto is selected
  setTheme(document.documentElement.dataset.mode);

  // Attach event handlers for toggling themes colors
  document.querySelectorAll(".theme-switch-button").forEach((el) => {
    el.addEventListener("click", cycleMode);
  });
}

////////////////////////////////////////////////////////////////////////////////

function scrollHandlerForHeader() {
  if (Math.floor(header.getBoundingClientRect().top) == 0) {
    header.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
  }
}

function scrollHandlerForBackToTop(positionY) {
  if (positionY < GO_TO_TOP_OFFSET) {
    document.documentElement.classList.remove("show-back-to-top");
  } else {
    if (positionY < lastScrollTop) {
      document.documentElement.classList.add("show-back-to-top");
    } else if (positionY > lastScrollTop) {
      document.documentElement.classList.remove("show-back-to-top");
    }
  }
  lastScrollTop = positionY;
}

function scrollHandlerForTOC(positionY) {
  if (tocScroll === null) {
    return;
  }

  // top of page.
  if (positionY == 0) {
    tocScroll.scrollTo(0, 0);
  } else if (
    // bottom of page.
    Math.ceil(positionY) >=
    Math.floor(document.documentElement.scrollHeight - window.innerHeight)
  ) {
    tocScroll.scrollTo(0, tocScroll.scrollHeight);
  } else {
    // somewhere in the middle.
    const current = document.querySelector(".scroll-current");
    if (current == null) {
      return;
    }

    // https://github.com/pypa/pip/issues/9159 This breaks scroll behaviours.
    // // scroll the currently "active" heading in toc, into view.
    // const rect = current.getBoundingClientRect();
    // if (0 > rect.top) {
    //   current.scrollIntoView(true); // the argument is "alignTop"
    // } else if (rect.bottom > window.innerHeight) {
    //   current.scrollIntoView(false);
    // }
  }
}

function scrollHandler(positionY) {
  scrollHandlerForHeader();
  scrollHandlerForBackToTop(positionY);
  scrollHandlerForTOC(positionY);
}

////////////////////////////////////////////////////////////////////////////////
// Setup
////////////////////////////////////////////////////////////////////////////////
function setupScrollHandler() {
  // Taken from https://developer.mozilla.org/en-US/docs/Web/API/Document/scroll_event
  let last_known_scroll_position = 0;
  let ticking = false;

  window.addEventListener("scroll", function (e) {
    last_known_scroll_position = window.scrollY;

    if (!ticking) {
      window.requestAnimationFrame(function () {
        scrollHandler(last_known_scroll_position);
        ticking = false;
      });

      ticking = true;
    }
  });
  window.scroll();
}

function addTOCInteractivity() {
  document.addEventListener("gumshoeActivate", function (event) {
    const navLinks = document.querySelectorAll(".table-of-contents li>a");

    navLinks.forEach((navLink) => {
      navLink.parentElement.classList.remove("active");
    });

    const activeNavLinks = document.querySelectorAll(
      ".table-of-contents li.scroll-current>a",
    );
    activeNavLinks.forEach((navLink) => {
      navLink.parentElement.classList.add("active");
    });
  });
}

function setupScrollSpy() {
  if (tocScroll === null) {
    return;
  }

  // Scrollspy -- highlight table on contents, based on scroll
  new Gumshoe(".table-of-contents a", {
    reflow: true,
    recursive: true,
    navClass: "scroll-current",
    nested: true,
    nestedClass: "scroll-current", //
    events: true,
    offset: () => {
      let rem = parseFloat(getComputedStyle(document.documentElement).fontSize);
      return header.getBoundingClientRect().height + 4.5 * rem + 1;
    },
  });
}

function setup() {
  setupScrollHandler();
  addTOCInteractivity();
  setupScrollSpy();
}

/*******************************************************************************
 * Search
 */

/**
 * Find any search forms on the page and return their input element
 */
var findSearchInput = () => {
  let forms = document.querySelectorAll("form.search-wrapper");
  if (!forms.length) {
    // no search form found
    return;
  } else {
    var form;
    if (forms.length == 1) {
      // there is exactly one search form (persistent or hidden)
      form = forms[0];
    } else {
      // must be at least one persistent form, use the first persistent one
      form = document.querySelector(
        "div:not(.search-button__search-container) > form.search-wrapper",
      );
    }
    return form.querySelector("input");
  }
};

/**
 * Activate the search field on the page.
 * - If there is a search field already visible it will be activated.
 * - If not, then a search field will pop up.
 */
var toggleSearchField = () => {
  // Find the search input to highlight
  let input = findSearchInput();

  // if the input field is the hidden one (the one associated with the
  // search button) then toggle the button state (to show/hide the field)
  let searchPopupWrapper = document.querySelector(".search-button__wrapper");
  let hiddenInput = searchPopupWrapper.querySelector("input");
  if (input === hiddenInput) {
    searchPopupWrapper.classList.toggle("show");
  }
  // when toggling off the search field, remove its focus
  if (document.activeElement === input) {
    input.blur();
  } else {
    input.focus();
    input.select();
    input.scrollIntoView({ block: "center" });
  }
};

/**
 * Add an event listener for toggleSearchField() for Ctrl/Cmd + K
 */
var addEventListenerForSearchKeyboard = () => {
  window.addEventListener(
    "keydown",
    (event) => {
      let input = findSearchInput();
      // toggle on Ctrl+k or ⌘+k
      if ((event.ctrlKey || event.metaKey) && event.code == "KeyK") {
        event.preventDefault();
        toggleSearchField();
      }
      // also allow Escape key to hide (but not show) the dynamic search field
      else if (document.activeElement === input && event.code == "Escape") {
        toggleSearchField();
      }
    },
    true,
  );
};

/**
 * Change the search hint to `meta key` if we are a Mac
 */
var changeSearchShortcutKey = () => {
  let buttons = document.querySelectorAll("button.search-button");
  var isMac = window.navigator.platform.toUpperCase().indexOf("MAC") >= 0;
  if (isMac) {
    buttons.forEach(
      (f) => (f.querySelector("kbd.kbd-shortcut__modifier").innerText = "⌘"),
    );
  }
};

/**
 * Activate callbacks for search button popup
 */
var setupSearchButtons = () => {
  changeSearchShortcutKey();
  addEventListenerForSearchKeyboard();

  // Add the search button trigger event callback
  document.querySelectorAll(".search-button__button").forEach((btn) => {
    btn.onclick = toggleSearchField;
  });

  // Add the search button overlay event callback
  let overlay = document.querySelector(".search-button__overlay");
  if (overlay) {
    overlay.onclick = toggleSearchField;
  }
};

/*******************************************************************************
 * dropdown trigger setup for bulma, see https://bulma.io/lib/main.js?v=202305240833 and https://siongui.github.io/2018/01/19/bulma-dropdown-with-javascript/
 */

function getAll(selector) {
  var parent =
    arguments.length > 1 && arguments[1] !== undefined
      ? arguments[1]
      : document;

  return Array.prototype.slice.call(parent.querySelectorAll(selector), 0);
}

var setupDropdwon = () => {
  var $dropdowns = getAll(".dropdown:not(.is-hoverable)");

  if ($dropdowns.length > 0) {
    $dropdowns.forEach(function ($el) {
      $el.addEventListener("click", function (event) {
        event.stopPropagation();
        $el.classList.toggle("is-active");
      });
    });

    document.addEventListener("click", function (event) {
      closeDropdowns();
    });
  }

  function closeDropdowns() {
    $dropdowns.forEach(function ($el) {
      $el.classList.remove("is-active");
    });
  }
};
/*******************************************************************************
 * dropdown trigger ended
 */

/*******************************************************************************
 * https://bulma.io/documentation/components/navbar/#navbar-menu
 */
function toggleBurger(selector, target_selector) {
  // Get all "navbar-burger" elements
  const $toggleBurgers = Array.prototype.slice.call(
    document.querySelectorAll(selector),
    0,
  );

  if ($toggleBurgers.length > 0) {
    // Add a click event on each of them
    $toggleBurgers.forEach(function ($el) {
      $el.addEventListener("click", function (event) {
        // Get the target from the "data-target" attribute
        const target = $el.dataset.target;
        const $target = document.getElementById(target);

        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        event.stopPropagation();
        $el.classList.toggle("is-active");
        $target.classList.toggle("is-active");
      });
    });

    // see https://segmentfault.com/q/1010000000452465 for close navburger when click empty place
    // and https://g-dragon.gitbooks.io/-javascript/content/di-si-zhang-shi-li/83001-pan-duan-shi-jian-fa-sheng-zai-mou-ge-div-wai.html
    document.addEventListener("click", function (event) {
      var _con = document.querySelector(target_selector);
      if (!_con.contains(event.target) && !(_con == event.target)) {
        closetoggleBurgers();
      }
    });
  }

  function closetoggleBurgers() {
    $toggleBurgers.forEach(function ($el) {
      const target = $el.dataset.target;
      const $target = document.getElementById(target);

      $el.classList.remove("is-active");
      $target.classList.remove("is-active");
    });
  }
}

function setupToggleButton() {
  toggleBurger(".navbar .navbar-burger", "#navbarMenu");
  toggleBurger(".bulma-content .navbar-burger", "#sidenavMenu");
}
////////////////////////////////////////////////////////////////////////////////
// Main entrypoint
////////////////////////////////////////////////////////////////////////////////
function main() {
  document.body.parentNode.classList.remove("no-js");
  addModeListener();
  setupSearchButtons();
  setupDropdwon();
  setupToggleButton();
  header = document.querySelector("header");
  tocScroll = document.querySelector(".toc-scroll");
  setup();
}

document.addEventListener("DOMContentLoaded", main);
