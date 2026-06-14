const state = {
  data: null,
  filter: "all",
  sort: "rating",
  search: "",
};

const cards = document.querySelector("#cards");
const template = document.querySelector("#serviceTemplate");
const generatedAt = document.querySelector("#generatedAt");
const sourceCount = document.querySelector("#sourceCount");
const topScore = document.querySelector("#topScore");
const excludedCount = document.querySelector("#excludedCount");
const methodText = document.querySelector("#methodText");
const excludedList = document.querySelector("#excludedList");
const searchInput = document.querySelector("#searchInput");
const sortSelect = document.querySelector("#sortSelect");
const segments = document.querySelectorAll(".segment");

function formatDate(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return new Intl.DateTimeFormat(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    timeZoneName: "short",
  }).format(date);
}

function setBar(card, key, value) {
  const bar = card.querySelector(`[data-bar="${key}"]`);
  const label = card.querySelector(`[data-value="${key}"]`);
  bar.style.width = `${Math.max(0, Math.min(100, value))}%`;
  label.textContent = value;
}

function healthText(health) {
  if (!health?.checked) return "Daily job will check on deploy";
  if (health.ok) return `Reachable (${health.status})`;
  if (health.status) return `Check returned ${health.status}`;
  return `Check limited: ${health.error || "unknown"}`;
}

function matches(service) {
  const filterMatch = state.filter === "all" || service.tags.includes(state.filter);
  const searchBlob = [
    service.name,
    service.bestFor,
    service.country,
    service.signup,
    service.watchNotes,
    ...service.tags,
    ...service.latestSignals,
  ]
    .join(" ")
    .toLowerCase();
  return filterMatch && searchBlob.includes(state.search);
}

function renderSummary() {
  const services = state.data.services;
  generatedAt.textContent = formatDate(state.data.generatedAt);
  sourceCount.textContent = services.length;
  topScore.textContent = Math.max(...services.map((service) => service.rating));
  excludedCount.textContent = state.data.excluded.length;
  methodText.textContent = `${state.data.method.rating} ${state.data.method.latest}`;
}

function renderExcluded() {
  excludedList.textContent = "";
  state.data.excluded.forEach((item) => {
    const row = document.createElement("div");
    row.className = "excluded-item";

    const title = document.createElement("strong");
    title.textContent = item.name;

    const reason = document.createElement("span");
    reason.textContent = item.reason;

    const link = document.createElement("a");
    link.href = item.source;
    link.target = "_blank";
    link.rel = "noreferrer";
    link.textContent = "Source";

    row.append(title, reason, link);
    excludedList.append(row);
  });
}

function renderCards() {
  cards.textContent = "";
  const services = state.data.services
    .filter(matches)
    .sort((a, b) => b[state.sort] - a[state.sort] || a.rank - b.rank);

  if (!services.length) {
    const empty = document.createElement("div");
    empty.className = "empty";
    empty.textContent = "No legal streaming source matches that view.";
    cards.append(empty);
    return;
  }

  services.forEach((service) => {
    const fragment = template.content.cloneNode(true);
    const card = fragment.querySelector(".service-card");
    const favicon = fragment.querySelector(".favicon");
    const rank = fragment.querySelector(".rank");
    const name = fragment.querySelector(".name");
    const scoreValue = fragment.querySelector(".score-value");
    const bestFor = fragment.querySelector(".best-for");
    const signals = fragment.querySelector(".signals");
    const sources = fragment.querySelector(".sources");
    const watchLink = fragment.querySelector(".watch-link");

    favicon.src = `https://www.google.com/s2/favicons?sz=64&domain=${service.domain}`;
    rank.textContent = `Rank ${service.rank}`;
    name.textContent = service.name;
    scoreValue.textContent = service.rating;
    bestFor.textContent = service.bestFor;

    setBar(card, "movieDepth", service.movieDepth);
    setBar(card, "tvDepth", service.tvDepth);
    setBar(card, "liveDepth", service.liveDepth);

    card.querySelector('[data-field="signup"]').textContent = service.signup;
    card.querySelector('[data-field="country"]').textContent = service.country;
    card.querySelector('[data-field="health"]').textContent = healthText(service.health);

    service.latestSignals.forEach((text) => {
      const signal = document.createElement("div");
      signal.className = "signal";
      signal.textContent = text;
      signals.append(signal);
    });

    watchLink.href = service.url;
    service.sources.forEach((source) => {
      const link = document.createElement("a");
      link.href = source.url;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = source.label;
      sources.append(link);
    });

    cards.append(fragment);
  });
}

function render() {
  renderSummary();
  renderExcluded();
  renderCards();
}

segments.forEach((segment) => {
  segment.addEventListener("click", () => {
    state.filter = segment.dataset.filter;
    segments.forEach((item) => item.classList.toggle("is-active", item === segment));
    renderCards();
  });
});

searchInput.addEventListener("input", (event) => {
  state.search = event.target.value.trim().toLowerCase();
  renderCards();
});

sortSelect.addEventListener("change", (event) => {
  state.sort = event.target.value;
  renderCards();
});

fetch("data.json", { cache: "no-store" })
  .then((response) => {
    if (!response.ok) throw new Error(`Data request failed: ${response.status}`);
    return response.json();
  })
  .then((data) => {
    state.data = data;
    render();
  })
  .catch((error) => {
    cards.innerHTML = `<div class="empty">${error.message}</div>`;
  });
