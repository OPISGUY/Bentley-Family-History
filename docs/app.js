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

const generations = [...document.querySelectorAll('.generation')];
if (generations.length) {
  const choice = document.querySelector('#generation-select');
  const younger = document.querySelector('#younger');
  const older = document.querySelector('#older');
  let current = 3;
  function show(index) {
    current = index;
    const key = generations[index].id;
    choice.value = key;
    generations.forEach((panel, i) => panel.hidden = i !== index);
    document.querySelectorAll('.index a').forEach((link, i) => {
      if (i === index) link.setAttribute('aria-current', 'true');
      else link.removeAttribute('aria-current');
    });
    younger.disabled = index === 0;
    older.disabled = index === generations.length - 1;
  }
  function followHash() {
    const index = generations.findIndex(panel => '#' + panel.id === location.hash);
    if (index >= 0) show(index);
  }
  function jump(index) {
    show(index);
    location.hash = generations[index].id;
  }
  choice.addEventListener('change', () => jump(choice.selectedIndex));
  younger.addEventListener('click', () => jump(current - 1));
  older.addEventListener('click', () => jump(current + 1));
  window.addEventListener('hashchange', followHash);
  show(current);
  followHash();
}
