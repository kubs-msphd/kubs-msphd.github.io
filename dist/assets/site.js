(() => {
  'use strict';

  const languageButtons = document.querySelectorAll('[data-language]');
  const directories = [];
  const validLanguage = value => ['ko', 'en'].includes(value);
  const normalize = value => (value || '').normalize('NFKC').toLocaleLowerCase().trim();
  let language = 'ko';

  function updateURL(updates) {
    const url = new URL(location.href);
    Object.entries(updates).forEach(([key, value]) => {
      if (value) url.searchParams.set(key, value);
      else url.searchParams.delete(key);
    });
    if (url.href !== location.href) {
      try { history.replaceState(history.state, '', url); } catch (_) {}
    }
  }

  function updateInternalLinks() {
    document.querySelectorAll('a[href]').forEach(anchor => {
      const href = anchor.getAttribute('href');
      if (!href || href.startsWith('#') || anchor.hasAttribute('download')) return;
      let url;
      try { url = new URL(href, location.href); } catch (_) { return; }
      if (url.origin !== location.origin || !/^https?:$/.test(url.protocol)) return;
      if (!/\.html?$/.test(url.pathname) && !url.pathname.endsWith('/')) return;
      url.searchParams.set('lang', language);
      anchor.href = url.href;
    });
  }

  function applyFilters(directory, writeURL = false) {
    const area = directory.area?.value || 'all';
    const query = directory.search?.value.trim() || '';
    const terms = normalize(query).split(/\s+/).filter(Boolean);
    let count = 0;
    // Aggregate career panels depend only on the field, never the person search.
    directory.outcomes.forEach(panel => {
      panel.hidden = panel.dataset.outcomePanel !== area;
    });
    directory.items.forEach(({ element, areas, search }) => {
      const matches = (area === 'all' || areas.includes(area)) && terms.every(term => search.includes(term));
      element.hidden = !matches;
      if (matches) count += 1;
    });
    if (directory.count) {
      const total = directory.items.length;
      directory.count.textContent = language === 'ko'
        ? `${directory.type === 'placements' ? '학계·연구 동문 ' : ''}전체 ${total}명 중 ${count}명`
        : `${count} of ${total} ${directory.type === 'faculty' ? 'faculty' : 'academic and research alumni'}`;
    }
    if (directory.empty) directory.empty.hidden = count !== 0;
    if (directory.clear) directory.clear.disabled = area === 'all' && !query;
    if (writeURL) updateURL({ area: area === 'all' ? '' : area, q: query });
  }

  function readFilterURL(directory) {
    const params = new URLSearchParams(location.search);
    const area = params.get('area') || 'all';
    if (directory.area) {
      const allowed = Array.from(directory.area.options).some(option => option.value === area);
      directory.area.value = allowed ? area : 'all';
    }
    if (directory.search) directory.search.value = params.get('q') || '';
  }

  function setLanguage(value, writeURL = true) {
    language = validLanguage(value) ? value : 'ko';
    document.documentElement.lang = language;
    document.querySelectorAll('[data-ko][data-en]').forEach(element => {
      element.textContent = element.dataset[language];
    });
    [['alt', 'alt'], ['aria-label', 'aria'], ['placeholder', 'placeholder'], ['content', 'content']]
      .forEach(([attribute, key]) => {
        document.querySelectorAll(`[data-${key}-ko][data-${key}-en]`).forEach(element => {
          element.setAttribute(attribute, element.getAttribute(`data-${key}-${language}`));
        });
      });
    document.querySelectorAll('[data-href-ko][data-href-en]').forEach(element => {
      element.href = element.getAttribute(`data-href-${language}`);
    });
    languageButtons.forEach(button => {
      button.setAttribute('aria-pressed', String(button.dataset.language === language));
    });
    try { localStorage.setItem('kubs-language', language); } catch (_) {}
    if (writeURL) updateURL({ lang: language });
    updateInternalLinks();
    directories.forEach(directory => applyFilters(directory));
  }

  document.querySelectorAll('[data-directory]').forEach(root => {
    const directory = {
      type: root.dataset.directory,
      area: root.querySelector('[data-area-filter]'),
      search: root.querySelector('[data-search-input]'),
      clear: root.querySelector('[data-clear-filters]'),
      count: root.querySelector('[data-result-count]'),
      empty: root.querySelector('[data-empty]'),
      outcomes: Array.from(root.querySelectorAll('[data-outcome-panel]')),
      items: Array.from(root.querySelectorAll('[data-filter-item]'), element => ({
        element,
        areas: (element.dataset.areas || '').split(/\s+/),
        search: normalize(element.dataset.search || element.textContent)
      }))
    };
    readFilterURL(directory);
    directory.area?.addEventListener('change', () => applyFilters(directory, true));
    directory.search?.addEventListener('input', () => applyFilters(directory, true));
    directory.search?.addEventListener('search', () => applyFilters(directory, true));
    directory.clear?.addEventListener('click', () => {
      if (directory.area) directory.area.value = 'all';
      if (directory.search) directory.search.value = '';
      applyFilters(directory, true);
      directory.search?.focus();
    });
    root.querySelectorAll('[data-filter-controls]').forEach(controls => { controls.hidden = false; });
    directories.push(directory);
  });

  let savedLanguage = 'ko';
  try { savedLanguage = localStorage.getItem('kubs-language') || 'ko'; } catch (_) {}
  const requestedLanguage = new URLSearchParams(location.search).get('lang');
  setLanguage(validLanguage(requestedLanguage) ? requestedLanguage : savedLanguage);
  languageButtons.forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.language)));

  window.addEventListener('popstate', () => {
    directories.forEach(readFilterURL);
    const requested = new URLSearchParams(location.search).get('lang');
    setLanguage(validLanguage(requested) ? requested : language, false);
  });

  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  if (toggle && navigation) {
    const closeMenu = (restoreFocus = false) => {
      toggle.setAttribute('aria-expanded', 'false');
      navigation.classList.remove('is-open');
      if (restoreFocus) toggle.focus();
    };
    toggle.addEventListener('click', () => {
      const open = toggle.getAttribute('aria-expanded') !== 'true';
      toggle.setAttribute('aria-expanded', String(open));
      navigation.classList.toggle('is-open', open);
    });
    navigation.addEventListener('click', event => {
      if (event.target.closest('a')) closeMenu();
    });
    document.addEventListener('keydown', event => {
      if (event.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
        closeMenu(true);
      }
    });
    document.addEventListener('click', event => {
      if (!navigation.contains(event.target) && !toggle.contains(event.target)) closeMenu();
    });
    const desktop = window.matchMedia('(min-width: 981px)');
    desktop.addEventListener?.('change', event => { if (event.matches) closeMenu(); });
  }
  document.documentElement.classList.add('js');
})();
