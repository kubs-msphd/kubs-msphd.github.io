(() => {
  const buttons = document.querySelectorAll('[data-language]');
  function setLanguage(language) {
    if (!['ko', 'en'].includes(language)) language = 'ko';
    document.documentElement.lang = language;
    document.querySelectorAll('[data-ko][data-en]').forEach(element => {
      element.textContent = element.dataset[language];
    });
    document.querySelectorAll('[data-href-ko][data-href-en]').forEach(element => {
      element.href = language === 'ko' ? element.dataset.hrefKo : element.dataset.hrefEn;
    });
    buttons.forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
    const title = document.querySelector('title');
    if (title?.dataset[language]) document.title = title.dataset[language];
    try { localStorage.setItem('kubs-language', language); } catch (_) {}
  }
  let initial = 'ko';
  try { initial = localStorage.getItem('kubs-language') || initial; } catch (_) {}
  const requested = new URLSearchParams(location.search).get('lang');
  setLanguage(requested || initial);
  buttons.forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.language)));
  const toggle = document.querySelector('.menu-toggle');
  const navigation = document.querySelector('#navigation');
  toggle?.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && toggle?.getAttribute('aria-expanded') === 'true') {
      toggle.setAttribute('aria-expanded', 'false');
      navigation.classList.remove('is-open');
      toggle.focus();
    }
  });
})();
