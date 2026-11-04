'use strict';
document.documentElement.classList.add('js');
const families = [...document.querySelectorAll('.family')];
const search = document.querySelector('#family-search');
const branch = document.querySelector('#branch');
const count = document.querySelector('#result-count');
const empty = document.querySelector('#no-results');
function filterFamilies() {
  const query = search.value.trim().toLocaleLowerCase();
  let shown = 0;
  families.forEach(f => {
    const match = f.textContent.toLocaleLowerCase().includes(query) && (branch.value === 'all' || f.dataset.branch === branch.value);
    f.hidden = !match;
    if (match) { shown++; if (query) f.open = true; }
  });
  count.textContent = `${shown} of ${families.length} family groups shown`;
  empty.hidden = shown !== 0;
}
if (search) {
  search.addEventListener('input', filterFamilies);
  branch.addEventListener('change', filterFamilies);
  document.querySelector('#reset').addEventListener('click', () => {search.value = ''; branch.value = 'all'; filterFamilies(); search.focus();});
  document.querySelector('#expand').addEventListener('click', () => families.filter(f => !f.hidden).forEach(f => f.open = true));
  document.querySelector('#collapse').addEventListener('click', () => families.forEach(f => f.open = false));
  filterFamilies();
}
function revealFamily() {
  const id = decodeURIComponent(location.hash.slice(1));
  const el = document.getElementById(id);
  const family = el?.closest('.family');
  if (family) {
    if (family.hidden && search) {search.value = ''; branch.value = 'all'; filterFamilies();}
    family.open = true;
    requestAnimationFrame(() => el.scrollIntoView({block: 'start'}));
  }
}
window.addEventListener('hashchange', revealFamily);
revealFamily();
let beforePrint = [];
window.addEventListener('beforeprint', () => {beforePrint = families.map(f => f.open); families.forEach(f => f.open = true);});
window.addEventListener('afterprint', () => families.forEach((f,i) => f.open = beforePrint[i]));
document.querySelectorAll('[data-print]').forEach(button => button.addEventListener('click', () => window.print()));
