"""Build the KUBS research website from shared templates and public content data."""
from pathlib import Path
from html import escape
import json
from research_views import research_filename, render_research_index, render_research_area, publication_card
from placement_views import render_placements

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
FACULTY = json.loads((ROOT / 'data/faculty.json').read_text())
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
PLACEMENTS = json.loads((ROOT / 'data/placements.json').read_text())
OUTCOMES = json.loads((ROOT / 'data/outcomes.json').read_text())
AREAS = json.loads((ROOT / 'data/areas.json').read_text())
AREA_MAP = {a['code']: a for a in AREAS}
RESEARCH_AREAS = json.loads((ROOT / 'data/research-areas.json').read_text())
OFFICIAL = 'https://biz.korea.ac.kr/msphd/intro.html'
DIRECTORY = 'https://biz.korea.ac.kr/professor/professor_list1.html'
SITE = 'https://kubs-msphd.github.io/'
UPDATED = '2026-09-08'

def attr(value):
    return escape(str(value), quote=True)

def t(ko, en, tag='span', cls=''):
    ko, en = ko or en or '', en or ko or ''
    return f'<{tag} class="{escape(cls)}" data-ko="{escape(ko, quote=True)}" data-en="{escape(en, quote=True)}">{escape(ko)}</{tag}>'

def link(url, ko, en, cls='text-link', external=False):
    mark = '↗' if external else '→'
    return f'<a class="{cls}" href="{escape(url, quote=True)}">{t(ko,en)}<span aria-hidden="true">{mark}</span></a>'

def heading(label, ko, en, aside=''):
    return f'<div class="section-heading"><div><p class="eyebrow">{label}</p>{t(ko,en,"h2")}</div>{aside}</div>'

def faculty_card(row):
    ko, en = row['name_ko'], row['name_en'] or row['name_ko']
    image = (f'<img src="{attr(row["photo"])}" width="86" height="108" loading="lazy" decoding="async" alt="{attr(ko)}" data-alt-ko="{attr(ko)}" data-alt-en="{attr(en)}">'
             if row.get('photo') else '<div class="portrait-fallback" aria-hidden="true">KUBS</div>')
    keywords_ko, keywords_en = row.get('interests_ko'), row.get('interests_en')
    if not keywords_ko or keywords_ko == 'LSOM':
        keywords_ko = row.get('research_summary_ko') or keywords_ko
    if not keywords_en or keywords_en == 'LSOM':
        keywords_en = row.get('research_summary_en') or keywords_en
    interests = t(keywords_ko, keywords_en, 'p', 'interests') if keywords_ko or keywords_en else t('공식 소개에서 연구정보를 확인하세요.', 'See the official directory for research information.', 'p', 'interests')
    url = row.get('url') or DIRECTORY
    url_en = row.get('url_en') or url
    profile_ko, profile_en = ('프로필 및 연구', 'Profile & research') if row.get('url') else ('공식 교수진 목록', 'Official faculty directory')
    profile = f'<a class="text-link" href="{attr(url)}" data-href-ko="{attr(url)}" data-href-en="{attr(url_en)}" aria-label="{attr(ko + " · " + profile_ko)}" data-aria-ko="{attr(ko + " · " + profile_ko)}" data-aria-en="{attr(en + " · " + profile_en)}">{t(profile_ko,profile_en)} <span aria-hidden="true">↗</span></a>'
    personal = row.get('personal_url')
    if personal and personal != url:
        profile += f'<a class="source-link" href="{attr(personal)}" aria-label="{attr(ko + " 개인 홈페이지")}" data-aria-ko="{attr(ko + " 개인 홈페이지")}" data-aria-en="{attr(en + " personal website")}">{t("개인 홈페이지","Personal website")} ↗</a>'
    search = ' '.join(str(v or '') for v in [ko, en, row.get('title_ko'), row.get('title_en'), keywords_ko, keywords_en, *[AREA_MAP[code]['name_ko']+' '+AREA_MAP[code]['name_en'] for code in row['area_codes']]])
    return f'''<article class="faculty-card" id="{attr(row['id'])}" data-filter-item data-areas="{attr(' '.join(row['area_codes']))}" data-search="{attr(search)}">
      <div class="faculty-heading">{image}<div>{t(ko,en,'h3')}<p class="english-name">{t(en,ko)}</p></div></div>
      {t(row['title_ko'],row['title_en'],'p','position faculty-meta')}{interests}{profile}
    </article>'''

def official_band():
    return f'''<div class="wrap"><section class="official-band" aria-label="Official information"><div>{t('지원과 학사 안내','Admissions & academic information','h2')}{t('모집요강, 장학제도, 학사규정은 공식 홈페이지에서 확인하세요.','Find application requirements, funding details and academic regulations on the official website.','p')}</div><div class="official-links">
      <a href="https://biz.korea.ac.kr/msphd/process.html" data-href-ko="https://biz.korea.ac.kr/msphd/process.html" data-href-en="https://biz.korea.ac.kr/eng/msphd/process.html">{t('학위과정','Degree programmes')} ↗</a>
      <a href="https://graduate.korea.ac.kr/">{t('입학안내','Admissions')} ↗</a>
      <a href="https://biz.korea.ac.kr/msphd/scholarship.html" data-href-ko="https://biz.korea.ac.kr/msphd/scholarship.html" data-href-en="https://biz.korea.ac.kr/eng/msphd/scholarship.html">{t('장학제도','Funding')} ↗</a>
    </div></section></div>'''

def layout(active, ko_title, en_title, body, filename=None):
    navigation=''.join(f'<a href="{url}"'+(' aria-current="page"' if active==key else '')+f'>{t(ko,en)}</a>' for key,url,ko,en in [('home','index.html','홈','Home'),('faculty','faculty.html','교수진','Faculty'),('research','research.html','연구','Research'),('placements','placements.html','졸업생 진로','Placements')])
    descriptions = {
        'home': ('고려대학교 경영대학의 전공별 교수진, 연구분야와 졸업생 진로를 만나보세요.', 'Explore faculty, research interests and alumni careers at Korea University Business School.'),
        'faculty': ('고려대학교 경영대학 전 전공 교수진과 연구분야. 전공과 연구 키워드로 찾아보세요.', 'Find Korea University Business School faculty by field, name and research interests.'),
        'research': ('고려대학교 경영대학 전공별 연구 주제, UTD 저널 선정 논문, 교수진과 세미나.', 'Explore research questions, selected UTD journal papers, faculty and seminars across KUBS fields.'),
        'placements': ('고려대학교 경영대학 석사·박사 졸업 후 진학과 취업, 전공별 학계·연구 경력.', 'Explore further study, employment, and academic and research careers after a KUBS master’s or doctoral degree.'),
    }
    desc_ko, desc_en = descriptions[active]
    canonical = SITE + ('' if active == 'home' else filename or active + '.html')
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title data-ko="{escape(ko_title)} · KUBS MS &amp; PhD" data-en="{escape(en_title)} · KUBS MS &amp; PhD">{escape(ko_title)} · KUBS MS &amp; PhD</title>
<meta name="description" content="{attr(desc_ko)}" data-content-ko="{attr(desc_ko)}" data-content-en="{attr(desc_en)}">
<meta name="theme-color" content="#860027"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="website"><meta property="og:site_name" content="KUBS MS &amp; PhD"><meta property="og:title" content="{attr(ko_title)} · KUBS MS &amp; PhD"><meta property="og:description" content="{attr(desc_ko)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}assets/campus.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script></head>
<body><a class="skip" href="#main">{t('본문 바로가기','Skip to content')}</a>
<header><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="KUBS MS and PhD home"><span class="brand-mark">KUBS</span><span class="brand-copy"><strong>MS & PhD</strong><span>Korea University Business School</span></span></a>
<div class="nav-wrap"><button type="button" class="menu-toggle" aria-controls="navigation" aria-expanded="false">{t('메뉴','Menu')}</button><nav class="nav" id="navigation" aria-label="주요 메뉴" data-aria-ko="주요 메뉴" data-aria-en="Main navigation">{navigation}<a href="{OFFICIAL}" data-href-ko="{OFFICIAL}" data-href-en="https://biz.korea.ac.kr/eng/msphd/intro.html">{t('공식 안내','Official programme')} ↗</a></nav><div class="language" aria-label="언어 선택" data-aria-ko="언어 선택" data-aria-en="Language"><button type="button" data-language="ko" aria-label="한국어" aria-pressed="true" lang="ko">KO</button><button type="button" data-language="en" aria-label="English" aria-pressed="false" lang="en">EN</button></div></div></div></header>
<main id="main">{body}{official_band()}</main>
<footer><div class="wrap"><div class="footer-top"><div><div class="footer-title">KUBS <span>MS & PhD</span></div>{t('고려대학교 경영대학 일반대학원','Korea University Business School · Graduate Research Programmes','p')}{t('서울특별시 성북구 안암로 145','145 Anam-ro, Seongbuk-gu, Seoul, Republic of Korea','p')}</div><div><a href="mailto:kubs_msphd@korea.ac.kr">kubs_msphd@korea.ac.kr</a>{t('일반대학원 문의','Graduate programme enquiries','p')}</div></div><div class="footer-bottom">{t('경영의 질문을 탐구하는 사람들','People exploring the questions that shape business')}<span>© 2026 Korea University Business School</span></div></div></footer></body></html>'''

def home():
    area_links=''.join(f'<a href="{research_filename(a["code"])}"><span>{t(a["name_ko"],a["name_en"])}<small>{a["name_en"]}</small></span><span aria-hidden="true">→</span></a>' for a in AREAS if a['code'] != 'M08')
    featured = [next(p for p in PAPERS if p['area_code'] == code) for code in ['M07', 'M04', 'M05']]
    paper_spotlight = ''.join(publication_card(p, globals()) for p in featured)
    alumni_counts = {area['code']: sum(a['area_code'] == area['code'] for a in PLACEMENTS['alumni']) for area in AREAS}
    alumni=''.join(f'<div><strong>{t(area["name_ko"],area["name_en"])}</strong><a href="placements.html?area={area["code"]}">{t(str(alumni_counts[area["code"]])+"명의 동문",str(alumni_counts[area["code"]])+" alumni")} →</a></div>' for area in AREAS if alumni_counts[area['code']])
    return f'''<section class="hero wrap"><div class="hero-grid"><div><p class="eyebrow">Graduate research at KUBS</p><h1>{t('좋은 질문에서 시작해,','Start with a question.')}<br><em>{t('새로운 지식으로.','Create new knowledge.')}</em></h1>{t('경영의 중요한 문제를 연구하는 사람들. 고려대학교 경영대학에서 나의 연구 주제와 연결되는 교수진, 그 이후의 진로를 만나보세요.','Meet the people studying important questions in business. Explore research interests, faculty and the paths our graduates take.','p','hero-text')}<div class="actions">{link('faculty.html','전공별 교수진 찾기','Find faculty','button')}{link('placements.html','졸업생 진로','Meet our alumni')}</div></div><figure class="hero-figure"><img src="assets/campus.jpg" width="720" height="480" fetchpriority="high" alt="고려대학교 경영대학 LG-POSCO경영관과 정원" data-alt-ko="고려대학교 경영대학 LG-POSCO경영관과 정원" data-alt-en="Korea University Business School LG-POSCO building and courtyard"><figcaption>{t('고려대학교 경영대학 · LG-POSCO경영관','Korea University Business School · LG-POSCO Building')}</figcaption></figure></div><div class="degree-strip"><p><strong>{t('석사 · 박사 · 석박사통합','MS · PhD · Integrated MS–PhD')}</strong></p><p>{t('연구 주제로 전공을 탐색하고, 사람으로 그 가능성을 확인하세요.','Find your field. Meet the people who make it possible.')}</p></div></section>
    <section class="section wrap" id="research">{heading('Research areas','어떤 질문을 연구하고 싶나요?','What do you want to understand?')}
      <div class="areas"><article class="featured-area"><p class="eyebrow">Find your research connections</p>{t('연구와 사람','Research & people','h3')}{t('전공과 연구 키워드로 교수진을 살펴보세요.','Explore faculty by field and research interests.','p')}{link('faculty.html',f'전체 교수진 {len(FACULTY)}명 보기',f'Explore all {len(FACULTY)} faculty')}</article><div><div class="area-list">{area_links}</div><p class="area-context">{link('business-analytics.html','Business Analytics 연구와 교수진','Business Analytics research & faculty')} · {link(OFFICIAL,'BA 1년 석사과정 안내','BA one-year MS programme',external=True)}</p></div></div>
    </section><section class="section wash"><div class="wrap">{heading('Research spotlight','새로운 지식이 만들어지는 곳','Where new knowledge takes shape',link('research.html','전체 전공 연구와 논문','Explore research across all fields'))}<div class="publications">{paper_spotlight}</div></div></section>
    <section class="wrap split-section"><div><p class="eyebrow">Careers after KUBS</p>{t('연구의 다음 장을 써가는 동문들','The next chapter after KUBS','h2')}{t('진학과 취업, 학계와 연구 현장까지. 석사·박사 졸업 후의 다양한 진로와 전공별 동문들을 만나보세요.','Explore further study, employment and academic careers after KUBS, and meet alumni from each field.','p')}{link('placements.html','졸업생 진로','Explore alumni careers')}</div><div class="alumni-preview">{alumni}</div></section>'''

def directory_controls(codes, kind):
    # Option elements contain text only, with the same bilingual attributes as other labels.
    options = '<option value="all" data-ko="전체 전공" data-en="All fields">전체 전공</option>'
    for code in codes:
        area = AREA_MAP[code]
        options += f'<option value="{code}" data-ko="{attr(area["name_ko"])}" data-en="{attr(area["name_en"])}">{escape(area["name_ko"])}</option>'
    search_ko, search_en = ('이름 또는 연구 키워드', 'Name or research keyword') if kind == 'faculty' else ('이름 또는 소속 기관', 'Name or institution')
    controls = f'''<div class="directory-controls" data-filter-controls hidden>
      <label class="filter-field">{t('전공','Field')}<select data-area-filter>{options}</select></label>
      <label class="filter-field search-field">{t('학계 동문 검색','Search academic alumni') if kind == 'placements' else t('검색','Search')}<input type="search" data-search-input placeholder="{search_ko}" data-placeholder-ko="{search_ko}" data-placeholder-en="{search_en}" autocomplete="off"></label>
      <button type="button" data-clear-filters>{t('초기화','Reset')}</button>
    </div>'''
    if kind == 'placements':
        return controls + t('전공 선택은 통계와 학계 동문 명단에 함께 적용됩니다. 이름·기관 검색은 명단에만 적용됩니다.', 'The field selection updates both statistics and academic alumni. Name and institution searches apply only to the alumni list.', 'p', 'filter-help')
    return controls + f'<div class="result-bar" data-filter-controls hidden><span data-result-count role="status" aria-live="polite"></span>{t("국문·영문으로 검색할 수 있습니다.","Search in Korean or English.")}</div>'

def empty_state():
    return f'<div class="empty-state" data-empty hidden>{t("검색 결과가 없습니다. 전공을 전체로 바꾸거나 다른 키워드로 검색해 보세요.","No matches. Try all fields or a different keyword.","p")}</div>'

def faculty_directory():
    cards = ''.join(faculty_card(f) for f in FACULTY)
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span>{t('교수진','Faculty')}</div><div class="page-hero-grid"><div><p class="eyebrow">Faculty & research interests</p>{t('나의 질문과 연결되는 교수진','Find your research connections','h1','ko-heading')}</div>{t('전공, 이름, 연구 키워드를 통해 교수진을 살펴보고 공식 프로필에서 최근 연구를 확인하세요.','Explore faculty by field, name and research interests, then follow their profiles to learn about recent work.','p','lede')}</div></div></section>
    <section class="section wrap" data-directory="faculty">{directory_controls([a['code'] for a in AREAS], 'faculty')}<div class="faculty-grid faculty-full">{cards}</div>{empty_state()}</section>'''

def alumni_link(url, ko, en, person, cls='source-link'):
    """Give repeated profile/contact links a person-specific accessible name."""
    name_ko = person.get('name_ko') or person['name']
    name_en = person.get('name_en') or name_ko
    return f'<a class="{cls}" href="{attr(url)}" aria-label="{attr(name_ko + " · " + ko)}" data-aria-ko="{attr(name_ko + " · " + ko)}" data-aria-en="{attr(name_en + " · " + en)}">{t(ko,en)}</a>'


pages = [
    ('index.html','home','연구와 사람','Research & People',home()),
    ('faculty.html','faculty','전공별 교수진','Faculty & Research Interests',faculty_directory()),
    ('research.html','research','전공별 연구','Research across KUBS',render_research_index(globals())),
    ('placements.html','placements','졸업생 진로','Graduate Careers',render_placements(globals())),
]
for area in AREAS:
    pages.append((research_filename(area['code']), 'research', area['name_ko']+' 연구와 교수진', area['name_en']+' Research & Faculty', render_research_area(area['code'], globals())))
for filename, active, ko, en, body in pages:
    (OUT / filename).write_text(layout(active,ko,en,body,filename),encoding='utf-8')
    print(f'Built {filename}')

(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
urls = ['' if page[0] == 'index.html' else page[0] for page in pages]
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{path}</loc><lastmod>{UPDATED}</lastmod></url>\n' for path in urls) + '</urlset>\n')
