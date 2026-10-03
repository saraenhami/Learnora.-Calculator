const display = document.getElementById("display");
const historyList = document.getElementById("history");
const historyItems = [];
const aboutDialog = document.getElementById("about-dialog");
const factDialog = document.getElementById("fact-dialog");

const facts = {
  0: "Zero represents nothing, but changed math forever! 🔢",
  1: "One is the loneliest number, but also the start of everything!🌟",
  2: "There are 2 eyes, 2 ears, 2 hands… symmetry is everywhere!👀✋",
  3: "3 is a magical number in many cultures! ✨",
  3.14: "Pi! The ratio of a circle’s circumference to its diameter.🥧🔵",
  4: "Four seasons make our year colorful!🍁❄️🌸☀️",
  5: "High five!🖐️ Did you know humans have 5 fingers per hand?",
  6: "Six legs? Ants have them! 🐜",
  6.7: "Interesting! 6.7 cm is roughly the length of a baby hummingbird at birth!🐦",
  7: "There are 7 continents on Earth!🌎",
  7.5: "The average human walking speed is about 7.5 km/h! 🚶",
  8: "Spiders have 8 legs!🕷️",
  9: "Cats supposedly have 9 lives!🐱",
  9.81: "Earth’s gravity pulls objects down at about 9.81 m/s²!🌍",
  10: "10 fingers and 10 toes – perfect for counting!🖐️🖐️",
  12: "12 months in a year, 12 zodiac signs!📅♈",
  24: "24 hours in a day – time waits for no one!⏰",
  32: "32 teeth in a full adult human mouth!😁",
  42: "42 is the Answer to the Ultimate Question of Life, the Universe, and Everything!😏",
  50: "There are 50 stars on the United States flag! 🇺🇸",
  60: "There are 60 seconds in a minute and 60 minutes in an hour!⏱️",
  100: "100°C is the boiling point of water!💧",
  360: "360 degrees complete a full circle!🔵",
  365: "365 days in a year – time flies!⏳",
  6371: "The approximate radius of Earth in km!🌍",
  149600000: "The distance from Earth to the Sun is about 149.6 million km!☀️",
  1000: "1,000 is a thousand! Big numbers, big dreams!💫",
  1000000: "1 million! That’s a lot of stars in a small patch of the night sky!✨",
  42.195: "The length of a marathon in kilometers!🏃‍♀️",
  299792458: "The speed of light in m/s – literally the fastest thing in the universe!⚡"
};

function showMessage(message) {
  display.value = message;
}
function append(value) {
  if (["Invalid input", "Division by zero", "Math error", "Invalid"].includes(display.value)) {
    display.value = "";
  }
  display.value += value;
  display.focus();
}
function clearDisplay() { display.value = ""; }
function backspace() {
  if (["Invalid input", "Division by zero", "Math error", "Invalid"].includes(display.value)) {
    clearDisplay();
  } else {
    display.value = display.value.slice(0, -1);
  }
}
function renderHistory() {
  historyList.replaceChildren();
  historyItems.forEach(item => {
    const li = document.createElement("li");
    li.textContent = item;
    historyList.appendChild(li);
  });
}
function addHistory(expression, result) {
  historyItems.push(`${expression} = ${result}`);
  if (historyItems.length > 5) historyItems.shift();
  renderHistory();
}
function showFact(result) {
  const key = Object.keys(facts).find(k => Number(k) === result);
  if (key !== undefined) {
    document.getElementById("fact-text").textContent = facts[key];
    factDialog.showModal();
  }
}

// A small arithmetic parser avoids evaluating arbitrary JavaScript.
function evaluateExpression(source) {
  const tokens = source.match(/\d*\.?\d+|[()+\-*/]/g);
  if (!tokens || tokens.join("") !== source.replace(/\s/g, "")) throw new Error("Invalid");
  let pos = 0;
  function parseExpression() {
    let value = parseTerm();
    while (tokens[pos] === "+" || tokens[pos] === "-") {
      const op = tokens[pos++];
      const right = parseTerm();
      value = op === "+" ? value + right : value - right;
    }
    return value;
  }
  function parseTerm() {
    let value = parseUnary();
    while (tokens[pos] === "*" || tokens[pos] === "/") {
      const op = tokens[pos++];
      const right = parseUnary();
      if (op === "/" && right === 0) throw new RangeError("Division by zero");
      value = op === "*" ? value * right : value / right;
    }
    return value;
  }
  function parseUnary() {
    if (tokens[pos] === "+") { pos++; return parseUnary(); }
    if (tokens[pos] === "-") { pos++; return -parseUnary(); }
    return parsePrimary();
  }
  function parsePrimary() {
    const token = tokens[pos++];
    if (token === "(") {
      const value = parseExpression();
      if (tokens[pos++] !== ")") throw new Error("Invalid");
      return value;
    }
    if (token === undefined || !/^\d*\.?\d+$/.test(token)) throw new Error("Invalid");
    return Number(token);
  }
  const result = parseExpression();
  if (pos !== tokens.length || !Number.isFinite(result)) throw new Error("Invalid");
  return result;
}
function calculate() {
  const expression = display.value.trim();
  if (!expression) return;
  try {
    const result = evaluateExpression(expression);
    addHistory(expression, result);
    display.value = String(result);
    showFact(result);
  } catch (error) {
    showMessage(error instanceof RangeError ? "Division by zero" : "Math error");
  }
}
function unaryAction(action) {
  const raw = display.value.trim();
  if (!raw) return;
  try {
    const value = Number(raw);
    if (!Number.isFinite(value)) throw new Error();
    let result, label;
    if (action === "square") { result = value ** 2; label = `${value}²`; }
    if (action === "sqrt") {
      if (value < 0) throw new Error();
      result = Math.sqrt(value); label = `√${value}`;
    }
    if (action === "percent") { result = value / 100; label = `${value}%`; }
    if (!Number.isFinite(result)) throw new Error();
    addHistory(label, result);
    display.value = String(result);
    showFact(result);
  } catch {
    showMessage("Invalid");
  }
}

document.getElementById("keypad").addEventListener("click", event => {
  const button = event.target.closest("button");
  if (!button) return;
  if (button.dataset.value !== undefined) append(button.dataset.value);
  else {
    const action = button.dataset.action;
    if (action === "calculate") calculate();
    else if (action === "clear") clearDisplay();
    else if (action === "backspace") backspace();
    else unaryAction(action);
  }
});
document.getElementById("theme-toggle").addEventListener("click", () => {
  document.body.classList.toggle("dark");
  document.getElementById("theme-toggle").textContent =
    document.body.classList.contains("dark") ? "☀️" : "🌙";
});
document.getElementById("about-button").addEventListener("click", () => aboutDialog.showModal());
document.getElementById("close-dialog").addEventListener("click", () => aboutDialog.close());
document.getElementById("close-fact").addEventListener("click", () => factDialog.close());
document.getElementById("clear-history").addEventListener("click", () => {
  historyItems.length = 0;
  renderHistory();
});
display.addEventListener("keydown", event => {
  if (event.key === "Enter" || event.key === "=") {
    event.preventDefault(); calculate();
  } else if (event.key === "Escape") {
    clearDisplay();
  }
});
