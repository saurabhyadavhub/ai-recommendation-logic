const grid = document.getElementById("interest-grid");
const count = document.getElementById("selected-count");
const category = document.getElementById("category");
const limit = document.getElementById("limit");
const limitValue = document.getElementById("limit-value");
const resultsList = document.getElementById("results-list");
const resultCount = document.getElementById("result-count");
const intro = document.getElementById("result-intro");
const recommendButton = document.getElementById("recommend-button");
const clearButton = document.getElementById("clear-button");

function selectedInterests() {
  return [...grid.querySelectorAll('input[type="checkbox"]:checked')].map(input => input.value);
}
function updateSelectedCount() {
  const n = selectedInterests().length;
  count.textContent = `${n} selected`;
  limitValue.textContent = limit.value;
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, char => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  })[char]);
}
function renderResults(payload) {
  const items = payload.recommendations || [];
  resultCount.textContent = `${items.length} ${items.length === 1 ? "idea" : "ideas"}`;
  intro.textContent = payload.personalized
    ? "Ranked by how closely each item matches your selected interests."
    : "Popular starter ideas. Choose interests for personalized matching.";
  if (!items.length) {
    resultsList.innerHTML = '<div class="loading-card"><span class="sparkle">✧</span><h3>No items in this category</h3><p>Try a different category or increase the result count.</p></div>';
    return;
  }
  resultsList.innerHTML = items.map((item, index) => {
    const tags = item.matched_tags?.length
      ? item.matched_tags.map(tag => `<span>${escapeHtml(tag.replaceAll("-", " "))}</span>`).join("")
      : `<span>${payload.personalized ? "No direct tag match" : "Popular pick"}</span>`;
    return `<article class="result-card" style="animation-delay:${index * 35}ms">
      <div class="result-emoji" aria-hidden="true">${escapeHtml(item.emoji || "✦")}</div>
      <div>
        <span class="category-label">${escapeHtml(item.category)}</span>
        <h3>${escapeHtml(item.title)}</h3>
        <p>${escapeHtml(item.description)}</p>
        <div class="matched-tags">${tags}</div>
      </div>
      <div class="match"><strong>${payload.personalized ? item.match_percent : "★" + item.popularity}</strong><span>${payload.personalized ? "% MATCH" : "POPULARITY"}</span>
      ${payload.personalized ? `<div class="match-track"><span style="width:${Math.max(0, Math.min(100, item.match_percent))}%"></span></div>` : ""}
      </div>
    </article>`;
  }).join("");
}
async function loadRecommendations() {
  recommendButton.disabled = true;
  recommendButton.innerHTML = 'Finding matches <span>…</span>';
  const params = new URLSearchParams({
    interests: selectedInterests().join(","),
    category: category.value,
    limit: limit.value
  });
  try {
    const response = await fetch(`/api/recommendations?${params}`);
    if (!response.ok) throw new Error("Request failed");
    renderResults(await response.json());
  } catch (error) {
    resultsList.innerHTML = '<div class="loading-card"><h3>Could not load recommendations</h3><p>Check that the Flask app is running, then try again.</p></div>';
  } finally {
    recommendButton.disabled = false;
    recommendButton.innerHTML = 'Find recommendations <span>↗</span>';
  }
}
grid.addEventListener("change", updateSelectedCount);
limit.addEventListener("input", updateSelectedCount);
recommendButton.addEventListener("click", loadRecommendations);
clearButton.addEventListener("click", () => {
  grid.querySelectorAll('input[type="checkbox"]').forEach(input => { input.checked = false; });
  category.value = "All";
  limit.value = "6";
  updateSelectedCount();
  loadRecommendations();
});
updateSelectedCount();
loadRecommendations();
