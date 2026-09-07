"""Build the KUBS research website from shared templates and public content data."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
FACULTY = json.loads((ROOT / 'data/faculty.json').read_text())
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
PLACEMENTS = json.loads((ROOT / 'data/placements.json').read_text())
OUTCOMES = json.loads((ROOT / 'data/outcomes.json').read_text())
AREAS = json.loads((ROOT / 'data/areas.json').read_text())
AREA_MAP = {a['code']: a for a in AREAS}
OFFICIAL = 'https://biz.korea.ac.kr/msphd/intro.html'
DIRECTORY = 'https://biz.korea.ac.kr/professor/professor_list1.html'
SITE = 'https://kubs-msphd.github.io/'
VERIFIED = '2026-09-07'

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

def layout(active, ko_title, en_title, body):
    navigation=''.join(f'<a href="{url}"'+(' aria-current="page"' if active==key else '')+f'>{t(ko,en)}</a>' for key,url,ko,en in [('home','index.html','홈','Home'),('faculty','faculty.html','교수진','Faculty'),('lsom','lsom.html','LSOM 연구','LSOM Research'),('placements','placements.html','졸업생 진로','Placements')])
    descriptions = {
        'home': ('고려대학교 경영대학의 전공별 교수진, 연구분야와 졸업생 진로를 만나보세요.', 'Explore faculty, research interests and alumni careers at Korea University Business School.'),
        'faculty': ('고려대학교 경영대학 전 전공 교수진과 연구분야. 전공과 연구 키워드로 찾아보세요.', 'Find Korea University Business School faculty by field, name and research interests.'),
        'lsom': ('고려대학교 경영대학 LSOM 교수진, 연구 주제, 최근 논문과 세미나 안내.', 'Explore LSOM faculty, research questions, selected publications and seminars at KUBS.'),
        'placements': ('고려대학교 경영대학 석사·박사 취업자의 진출 분야와 전공별 학계 동문 경력.', 'Explore employment fields of KUBS master’s and doctoral graduates and alumni careers in academia by field.'),
    }
    desc_ko, desc_en = descriptions[active]
    canonical = SITE + ('' if active == 'home' else active + '.html')
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
<footer><div class="wrap"><div class="footer-top"><div><div class="footer-title">KUBS <span>MS & PhD</span></div>{t('고려대학교 경영대학 일반대학원','Korea University Business School · Graduate Research Programmes','p')}{t('서울특별시 성북구 안암로 145','145 Anam-ro, Seongbuk-gu, Seoul, Republic of Korea','p')}</div><div><a href="mailto:kubs_msphd@korea.ac.kr">kubs_msphd@korea.ac.kr</a>{t('일반대학원 문의','Graduate programme enquiries','p')}</div></div><div class="footer-bottom">{t('경영의 질문을 탐구하는 사람들','People exploring the questions that shape business')}<a href="faculty.html#sources">{t('자료 출처 · 2026.09.06','Sources · 6 September 2026')}</a><span>© 2026 Korea University Business School</span></div></div></footer></body></html>'''

def home():
    area_links=''.join(f'<a href="faculty.html?area={a["code"]}"><span>{t(a["name_ko"],a["name_en"])}<small>{a["name_en"]}</small></span><span aria-hidden="true">→</span></a>' for a in AREAS if a['code'] != 'M08')
    faculty_by_id = {f['id']: f for f in FACULTY}
    featured_ids = ['faculty-27cc39d50220', 'faculty-5965053325d6', 'faculty-7aacf1915e00']
    faculty=''.join(faculty_card(faculty_by_id[key]) for key in featured_ids)
    alumni_counts = {area['code']: sum(a['area_code'] == area['code'] for a in PLACEMENTS['alumni']) for area in AREAS}
    alumni=''.join(f'<div><strong>{t(area["name_ko"],area["name_en"])}</strong><a href="placements.html?area={area["code"]}">{t(str(alumni_counts[area["code"]])+"명 수록",str(alumni_counts[area["code"]])+" alumni records")} →</a></div>' for area in AREAS if alumni_counts[area['code']])
    return f'''<section class="hero wrap"><div class="hero-grid"><div><p class="eyebrow">Graduate research at KUBS</p><h1>{t('좋은 질문에서 시작해,','Start with a question.')}<br><em>{t('새로운 지식으로.','Create new knowledge.')}</em></h1>{t('경영의 중요한 문제를 연구하는 사람들. 고려대학교 경영대학에서 나의 연구 주제와 연결되는 교수진, 그 이후의 진로를 만나보세요.','Meet the people studying important questions in business. Explore research interests, faculty and the paths our graduates take.','p','hero-text')}<div class="actions">{link('faculty.html','전공별 교수진 찾기','Find faculty','button')}{link('placements.html','졸업생 진로','Meet our alumni')}</div></div><figure class="hero-figure"><img src="assets/campus.jpg" width="720" height="480" fetchpriority="high" alt="고려대학교 경영대학 LG-POSCO경영관과 정원" data-alt-ko="고려대학교 경영대학 LG-POSCO경영관과 정원" data-alt-en="Korea University Business School LG-POSCO building and courtyard"><figcaption>{t('고려대학교 경영대학 · LG-POSCO경영관','Korea University Business School · LG-POSCO Building')}</figcaption></figure></div><div class="degree-strip"><p><strong>{t('석사 · 박사 · 석박사통합','MS · PhD · Integrated MS–PhD')}</strong></p><p>{t('연구 주제로 전공을 탐색하고, 사람으로 그 가능성을 확인하세요.','Find your field. Meet the people who make it possible.')}</p></div></section>
    <section class="section wrap" id="research">{heading('Research areas','어떤 질문을 연구하고 싶나요?','What do you want to understand?')}
      <div class="areas"><article class="featured-area"><p class="eyebrow">Find your research connections</p>{t('연구와 사람','Research & people','h3')}{t('전공과 연구 키워드로 교수진을 살펴보세요.','Explore faculty by field and research interests.','p')}{link('faculty.html',f'전체 교수진 {len(FACULTY)}명 보기',f'Explore all {len(FACULTY)} faculty')}</article><div><div class="area-list">{area_links}</div><p class="area-context">{link('faculty.html?area=M08','Business Analytics 교수진','Business Analytics faculty')} · {link(OFFICIAL,'BA 1년 석사과정 안내','BA one-year MS programme',external=True)}</p></div></div>
    </section><section class="section wash"><div class="wrap">{heading('Research spotlight · LSOM','질문을 함께 발전시키는 교수진','Meet the researchers',link('lsom.html','LSOM 연구와 최근 논문','LSOM research & publications'))}<div class="faculty-grid preview">{faculty}</div></div></section>
    <section class="wrap split-section"><div><p class="eyebrow">Careers after KUBS</p>{t('연구의 다음 장을 써가는 동문들','The next chapter after KUBS','h2')}{t('석사·박사 취업자의 진출 분야와 학계에서 활동하는 동문들을 만나보세요. 전공을 선택하면 해당 전공의 통계와 동문 경력을 함께 볼 수 있습니다.','Explore the employment fields of master’s and doctoral graduates and meet alumni in academia. Choose a field to view its career statistics and alumni records together.','p')}{link('placements.html','졸업생 진로와 자료 출처','Explore alumni careers')}</div><div class="alumni-preview">{alumni}</div></section>'''

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
    notes = t('KUBS 공식 전임교수 목록 기준입니다. 복수 전공 교수진은 각 전공에서 조회되며, 전체 명단에서는 한 번만 표시됩니다.', 'Based on the official KUBS full-time faculty directory. Cross-listed faculty appear in each relevant field and only once in the full directory.', 'p', 'directory-intro')
    cards = ''.join(faculty_card(f) for f in FACULTY)
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span>{t('교수진','Faculty')}</div><div class="page-hero-grid"><div><p class="eyebrow">Faculty & research interests</p>{t('나의 질문과 연결되는 교수진','Find your research connections','h1','ko-heading')}</div>{t('전공, 이름, 연구 키워드를 통해 교수진을 살펴보고 공식 프로필에서 최근 연구를 확인하세요.','Explore faculty by field, name and research interests, then follow their profiles to learn about recent work.','p','lede')}</div></div></section>
    <section class="section wrap" data-directory="faculty">{notes}{directory_controls([a['code'] for a in AREAS], 'faculty')}<div class="faculty-grid faculty-full">{cards}</div>{empty_state()}</section>
    <section class="section wash" id="sources"><div class="wrap">{heading('Sources & programme links','자료 출처와 전공 홈페이지','Sources & programme websites')}
      <div class="source-cards"><article class="source-card"><h3>{t('교수진 · 연구분야','Faculty & research interests')}</h3>{t('공식 국문·영문 명단과 전공별 분류를 대조했습니다. 연구분야는 공식 소개를 따르며, 일부 LSOM 교수의 키워드는 공개 프로필·논문을 요약했습니다. 공식 명단에서 전공이 표시되지 않은 교수 1명은 전체 목록에 포함했습니다.','The Korean and English directories and field listings were cross-checked. Research fields follow official entries, with selected LSOM summaries from public profiles and papers. One faculty member without a listed field is included in the full directory.','p')}{link(DIRECTORY,'KUBS 공식 교수진','Official KUBS directory',external=True)}</article>
      <article class="source-card"><h3>{t('전공별 연구 공동체','Programme communities')}</h3><p>{link('https://sites.google.com/korea.ac.kr/mis','IS 전공 홈페이지','IS programme website',external=True)}</p><p>{link('https://sites.google.com/view/kubsib','GB 전공 홈페이지','GB programme website',external=True)}</p><p>{link('lsom.html','LSOM 연구·논문·세미나','LSOM research, papers & seminars')}</p></article></div>
      {t('자료 확인: 2026년 9월 6일. 교수 사진과 캠퍼스 사진의 출처는 고려대학교 경영대학입니다.', 'Sources checked on 6 September 2026. Faculty and campus photographs are sourced from Korea University Business School.', 'p', 'section-note')}
    </div></section>'''

def lsom():
    topics=[('공급망은 어떻게 더 잘 회복할 수 있을까?','How can supply chains recover better?','의약품 공급부족, 품질관리, 공급사슬의 운영과 회복을 연구합니다.','Drug shortages, quality management, and the operation and recovery of supply chains.'),('서비스의 기다림과 자원 배분을 어떻게 개선할까?','How can services make better use of time and resources?','서비스 시스템의 수요와 용량, 대기행렬, 수익관리와 의사결정을 연구합니다.','Demand, capacity, queueing, revenue management and decisions in service systems.'),('플랫폼과 AI는 경쟁을 어떻게 바꾸는가?','How do platforms and AI change competition?','디지털 전환, 플랫폼 경쟁, 새로운 기술과 비즈니스 모델을 연구합니다.','Digital transformation, platform competition, emerging technologies and business models.')]
    topic_html=''.join(f'<article class="topic"><span class="topic-number">0{i+1}</span>{t(a,b,"h3")}{t(c,d,"p")}</article>' for i,(a,b,c,d) in enumerate(topics))
    papers=''.join(f'<article class="publication"><span class="year">{p["year"]}</span><div><h3><a href="{p["url"]}">{escape(p["title"])}</a></h3><p class="authors">{escape(p["authors"])}</p><p class="journal">{escape(p["journal"])}</p>{t(p["status_ko"],p["status_en"],"p","paper-status")}{t(p["summary_ko"],p["summary_en"],"p","paper-summary")}</div>{link(p["url"],"논문 보기","Read paper",external=True)}</article>' for p in PAPERS)
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span>{t('연구 전공','Research areas')}<span>/</span><span>LSOM</span></div><div class="page-hero-grid"><div><p class="eyebrow">Research area</p><h1>LSOM</h1><p class="subtitle">Logistics, Service and<br>Operations Management</p></div>{t('공급망부터 서비스, 플랫폼까지. 실제 경영 문제를 데이터와 이론으로 이해하고 더 나은 의사결정을 연구합니다.','From supply chains to services and platforms, we use data and theory to understand business problems and improve decisions.','p','lede')}</div></div></section>
    <nav class="jump-nav" aria-label="LSOM sections"><div class="wrap"><a href="#questions">{t('연구 주제','Research')}</a><a href="#faculty">{t('교수진','Faculty')}</a><a href="#publications">{t('최근 논문','Publications')}</a><a href="#community">{t('세미나와 진로','Community')}</a></div></nav>
    <section class="section wrap" id="questions">{heading('Questions we study','현실의 문제를 연구의 질문으로','Real problems. Research questions.')}<div class="research-topics">{topic_html}</div><div class="method-line"><strong>{t('연구 방법','Methods')}</strong>{t('실증분석 · 인과추론 · 최적화 · 게임이론 · 대기행렬 · 시뮬레이션','Empirical analysis · Causal inference · Optimization · Game theory · Queueing · Simulation')}</div></section>
    <section class="section wash" id="faculty"><div class="wrap">{heading('LSOM faculty','함께 연구할 교수진을 만나보세요','Find your research connections',t('관심 주제와 최근 연구를 살펴보고 나의 질문과 연결해 보세요.','Explore research interests and recent work to find connections with your own questions.','p'))}<div class="faculty-grid faculty-full">{''.join(faculty_card(f) for f in FACULTY if 'M06' in f['area_codes'])}</div>{t('전임교수 명단과 연구분야는 KUBS 공식 교수소개 기준이며, 일부 연구 키워드는 공개 프로필과 논문을 바탕으로 요약했습니다.','Faculty membership and research fields follow the official KUBS directory, with selected research summaries from public profiles and publications.','p','section-note')}{link('faculty.html','전체 전공 교수진과 자료 출처','All faculty & sources')}</div></section>
    <section class="section wrap" id="publications">{heading('Selected recent publications','최근 연구를 살펴보세요','A closer look at recent research',t('2025–2026년 게재논문 중 선정','Selected publications, 2025–2026','p'))}<div class="publications">{papers}</div>{t('전체 논문 목록은 각 교수님의 프로필에서 확인할 수 있습니다.','Visit individual faculty profiles for complete publication lists.','p','section-note')}</section>
    <section class="section wash" id="community"><div class="wrap next-cards"><article class="next-card"><p class="eyebrow">Research conversations</p>{t('세미나와 연구 교류','Seminars & research exchange','h2')}{t('경영대학에서 열리는 세미나와 연구 행사는 KUBS 캘린더에서 확인할 수 있습니다.','Explore seminars and research events through the KUBS calendar.','p')}{link('https://biz.korea.ac.kr/news/calendar.html','KUBS 세미나 일정','KUBS events calendar',external=True)}</article><article class="next-card"><p class="eyebrow">Academic careers</p>{t('LSOM 박사 이후의 여정','Where an LSOM PhD can lead','h2')}{t('졸업 후 대학 교수로 진출한 동문들과 소속 대학을 만나보세요.','Meet doctoral alumni who have gone on to academic careers.','p')}{link('placements.html?area=M06','LSOM 졸업생 진로 보기','Explore LSOM alumni careers')}</article></div></section>'''

def alumni_link(url, ko, en, person, cls='source-link'):
    """Give repeated profile/contact links a person-specific accessible name."""
    name_ko = person.get('name_ko') or person['name']
    name_en = person.get('name_en') or name_ko
    return f'<a class="{cls}" href="{attr(url)}" aria-label="{attr(name_ko + " · " + ko)}" data-aria-ko="{attr(name_ko + " · " + ko)}" data-aria-en="{attr(name_en + " · " + en)}">{t(ko,en)}</a>'

def alumni_contacts(person):
    links = []
    if person.get('email'):
        links.append(alumni_link('mailto:' + person['email'], person['email'], person['email'], person, 'source-link alumni-email'))
        if person.get('email_note_ko') or person.get('email_note_en'):
            links.append(t(person.get('email_note_ko'), person.get('email_note_en'), 'p', 'placement-meta contact-note'))
    if person.get('profile_url'):
        links.append(alumni_link(person['profile_url'], '대학 프로필 ↗', 'University profile ↗', person))
    if person.get('website_url') and person['website_url'] != person.get('profile_url'):
        links.append(alumni_link(person['website_url'], '개인 홈페이지 ↗', 'Personal website ↗', person))
    if not links:
        if person.get('record_basis') == 'administrative':
            return t('연락처 추후 보완', 'Contact details to follow', 'p', 'placement-meta')
        return t('공개 연락처 미확인', 'Public contact not verified', 'p', 'placement-meta')
    return '<div class="alumni-contacts">' + ''.join(links) + '</div>'

def alumni_evidence(person):
    verification = person.get('profile_verification') or {}
    sources, used = [], set()
    original = person.get('source_url') or '#source-' + person.get('source_id', 'LSOM')
    for source in verification.get('sources', []):
        if not source.get('url') or source['url'] in used or source['url'] == original:
            continue
        used.add(source['url'])
        sources.append(f'<li><a href="{attr(source["url"])}">{escape(source.get("title") or "Profile source")} ↗</a></li>')
    source_label = ('행정실 자료 기준', 'Administrative record source') if person.get('record_basis') == 'administrative' else ('동문 명단 원문', 'Original alumni listing')
    sources.append(f'<li>{alumni_link(original, *source_label, person)}</li>')
    checked = verification.get('checked_at')
    date = f'<p class="placement-meta">{t("확인일", "Checked")}: {escape(checked)}</p>' if checked else ''
    summary_label = ('자료 출처', 'Record source') if person.get('record_basis') == 'administrative' else ('확인 출처', 'Verification sources')
    return f'<details class="alumni-evidence"><summary>{t(*summary_label)}</summary>{date}<ul>{"".join(sources)}</ul></details>'

def outcome_summary(summary, degree):
    """Render aggregate counts only; personal administrative records are never embedded."""
    title_ko, title_en = ('석사 취업자의 진출 분야', 'Employment fields · Master’s') if degree == 'masters' else ('박사 취업자의 진출 분야', 'Employment fields · Doctoral')
    total, employed = summary['total_records'], summary['employed_total']
    start, end = summary.get('period_start'), summary.get('period_end')
    period = f'{start.replace("-", ".")}–{end.replace("-", ".")}' if start and end else ''
    period_text = t('자료에 수록된 졸업 시기: ' + period, 'Graduation dates in the records: ' + period, 'p', 'outcome-period') if period else ''
    metrics = f'''<dl class="outcome-metrics"><div><dt>{t('자료 수록','Recorded graduates')}</dt><dd>{t(f'{total:,}명',f'{total:,}')}</dd></div><div><dt>{t('취업 기록','Employment records')}</dt><dd>{t(f'{employed:,}명',f'{employed:,}')}</dd></div></dl>'''
    if not total:
        return f'<article class="outcome-card">{t(title_ko,title_en,"h3")}{t("해당 전공·학위의 집계 자료가 없습니다.","No records are available for this field and degree.","p","outcome-empty")}</article>'
    statuses = ''.join(f'<li>{t(status["label_ko"],status["label_en"])} <strong>{t(str(summary["status_counts"].get(status["id"],0))+"명",str(summary["status_counts"].get(status["id"],0)))}</strong></li>' for status in OUTCOMES['statuses'])
    status_list = f'<ul class="outcome-statuses">{statuses}</ul>'
    if employed:
        categories = OUTCOMES['sectors'] if degree == 'masters' else OUTCOMES['categories']
        counts = summary['sector_counts'] if degree == 'masters' else summary['category_counts']
        rows = []
        for category in categories:
            count = counts.get(category['id'], 0)
            share = 100 * count / employed
            rows.append(f'<tr><th scope="row">{t(category["label_ko"],category["label_en"])}<span class="outcome-track" aria-hidden="true"><span style="width:{share:.5f}%"></span></span></th><td>{t(f"{count:,}명",f"{count:,}")}</td><td>{share:.1f}%</td></tr>')
        table = f'''<table class="outcome-table"><caption>{t(f'취업 기록 {employed:,}명을 분모로 계산한 분야별 비중',f'Shares of {employed:,} graduates with an employment record')}</caption><thead><tr><th scope="col">{t('진출 분야','Employment field')}</th><th scope="col">{t('인원','Count')}</th><th scope="col">{t('비중','Share')}</th></tr></thead><tbody>{''.join(rows)}</tbody></table>'''
    else:
        table = t('분류할 취업 기록이 없습니다.', 'No employment records are available to classify.', 'p', 'outcome-empty')
    return f'<article class="outcome-card">{t(title_ko,title_en,"h3")}{period_text}{metrics}{status_list}{table}</article>'

def outcome_panels():
    panels = []
    for code in ['all', *[area['code'] for area in AREAS]]:
        group = OUTCOMES['groups'][code]
        area_ko, area_en = ('전체 전공', 'All fields') if code == 'all' else (AREA_MAP[code]['name_ko'], AREA_MAP[code]['name_en'])
        area_label = t(area_ko, area_en, 'h2', 'outcome-field-heading')
        content = ''.join(outcome_summary(group[degree], degree) for degree in ['masters', 'doctoral'])
        no_records = not any(group[degree]['total_records'] for degree in ['masters', 'doctoral'])
        note = t('이 자료에는 전략 전공이 별도로 구분되어 있지 않습니다.', 'Strategy is not separately identified in these records.', 'p', 'section-note') if code == 'M09' and no_records else ''
        panels.append(f'<section data-outcome-panel="{code}" aria-label="{attr(area_ko + " 진로 통계")}" data-aria-ko="{attr(area_ko + " 진로 통계")}" data-aria-en="{attr(area_en + " career statistics")}"'+(' hidden' if code != 'all' else '')+f'>{area_label}{note}<div class="outcome-grid">{content}</div></section>')
    return ''.join(panels)

def placements():
    rows = []
    for a in sorted(PLACEMENTS['alumni'], key=lambda a: a['name']):
        name = t(a.get('name_ko'), a.get('name_en'))
        area = AREA_MAP[a['area_code']]
        degree_ko, degree_en = {'PhD': (' · 박사', ' · PhD'), 'MS': (' · 석사', ' · MS')}.get(a.get('degree'), ('', ''))
        meta = t(area['name_ko'] + degree_ko, area['name_en'] + degree_en, 'p', 'placement-meta')
        administrative = a.get('record_basis') == 'administrative'
        career_labels = {'faculty': ('교수직', 'Faculty'), 'research': ('연구직 · 박사후연구 등', 'Research · Postdoctoral roles'), 'teaching': ('강의 · 겸임 등', 'Teaching · Adjunct roles')}
        if a.get('career_group') in career_labels:
            meta += t(*career_labels[a['career_group']], 'span', 'career-badge')
        institution = t(a.get('institution_ko'), a.get('institution_en'))
        department = t(a.get('department_ko'), a.get('department_en'), 'p', 'placement-department')
        if a.get('department_ko') or a.get('department_en'):
            institution += department
        verification = a.get('profile_verification') or {}
        if administrative:
            institution = t(a.get('reported_affiliation_ko') or a.get('institution_ko'), a.get('reported_affiliation_en') or a.get('institution_en'))
            position = t('행정실 기록 · 2026.09.07', 'Administrative record · 7 September 2026', 'p', 'placement-meta administrative-record')
        elif verification.get('rank_status') in ['verified', 'dated_verified']:
            position = t(a.get('position_ko'), a.get('position_en'), 'p', 'placement-role verified-rank')
            if verification.get('rank_as_of'):
                position += t('직급 자료 기준: ' + verification['rank_as_of'], 'Rank source dated ' + verification['rank_as_of'], 'p', 'placement-meta rank-date')
        else:
            position = t('직급 미확인', 'Rank not verified', 'p', 'placement-role unverified-rank')
        if a.get('appointment_ko') or a.get('appointment_en'):
            position += t(a.get('appointment_ko'), a.get('appointment_en'), 'p', 'placement-meta')
        if verification.get('status') == 'unresolved':
            position += t('소속은 기존 동문 명단 기준', 'Affiliation from the original alumni listing', 'p', 'placement-meta')
        if a.get('verification_note_ko') or a.get('verification_note_en'):
            position += t(a.get('verification_note_ko'), a.get('verification_note_en'), 'p', 'verification-note')
        contacts = alumni_contacts(a) + alumni_evidence(a)
        search = ' '.join(str(a.get(k) or '') for k in ['name','name_ko','name_en','institution_ko','institution_en','reported_affiliation_ko','reported_affiliation_en','department_ko','department_en','position_ko','position_en','email','area']) + ' ' + area['name_ko'] + ' ' + area['name_en']
        rows.append(f'<tr id="{attr(a["id"])}" role="row" data-filter-item data-areas="{a["area_code"]}" data-search="{attr(search)}"><td role="cell" data-label-ko="성명 · 전공" data-label-en="Name · Field">{name}{meta}</td><td role="cell" data-label-ko="소속 · 경력" data-label-en="Affiliation · Career">{institution}{position}</td><td role="cell" data-label-ko="연락처 · 홈페이지" data-label-en="Contact · Profile">{contacts}</td></tr>')
    sources = []
    for source in PLACEMENTS['sources']:
        source_link = link(source['url'],'원문 보기','View source',external=True) if source['url'] else ''
        sources.append(f'<article class="source-card" id="source-{source["id"]}">{t(source["label_ko"],source["label_en"],"h3")}{t(source["note_ko"],source["note_en"],"p")}{source_link}</article>')
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span><span>Placements</span></div><div class="page-hero-grid"><div><p class="eyebrow">Careers after KUBS</p>{t('연구를 바탕으로, 더 넓은 진로로.','Research opens new paths.','h1','ko-heading')}</div>{t('석사·박사 졸업생들의 취업 분야와 학계·연구 경력을 살펴보세요. 전공을 선택하면 해당 전공의 통계와 동문 명단을 함께 볼 수 있습니다.','Explore employment fields and academic and research careers after KUBS. Select a field to view its statistics and alumni records together.','p','lede')}</div></div></section>
    <section class="section wrap" data-directory="placements">
    {directory_controls([a['code'] for a in AREAS], 'placements')}
    <div class="outcomes-intro"><p class="eyebrow">Graduate career records</p>{t('석사·박사 졸업생의 진출 분야','Where our graduates work','h2')}{t('행정실 취업 현황 자료를 분류했습니다. 아래 비중은 취업 기록이 있는 졸업생 중 각 분야가 차지하는 비중이며, 전체 졸업생의 취업률은 아닙니다.','These summaries classify administrative career records. Percentages show the distribution among graduates with an employment record, not an employment rate for all graduates.','p')}{t('석사 자료는 2024년 8월–2026년 8월, 박사 자료는 2014년 8월–2026년 8월 졸업생을 포함합니다.','The master’s records cover August 2024–August 2026 graduates; the doctoral records cover August 2014–August 2026 graduates.','p','outcome-period-note')}{link('#sources','자료 기준 보기','About these records')}</div>
    <div class="outcome-panels">{outcome_panels()}</div>
    {t('분야별 비중의 분모에는 기업 유형 미확인 취업 기록도 포함됩니다. 인턴·비정규 경력이 포함될 수 있으며, 졸업 직후와 이후 시점의 기록이 혼재합니다. 소수점 반올림으로 비중의 합계가 100%와 다를 수 있습니다.','The denominator includes employment records with an unclassified company type. Records may include internships and non-permanent roles and mix initial and later career information. Percentages may not sum to 100% because of rounding.','p','section-note')}
    <section class="academic-section" id="academic-careers"><p class="eyebrow">Academic & research careers</p>{t('학계와 연구 현장의 동문들','Alumni in academia and research','h2')}
    <div class="directory-intro">{t(f'학계·연구 경력 {len(PLACEMENTS["alumni"])}명을 수록했습니다. 대학·연구자 공개 프로필을 확인한 기존 명단과 새로 받은 행정실 기록을 함께 모았습니다.',f'{len(PLACEMENTS["alumni"])} alumni records in academia and research. This list combines previously checked public university and researcher profiles with newly supplied administrative records.','p')}{t('행정실 기록은 별도로 표시했으며, 해당 경력이 현재 재직 정보인지와 연락처는 추후 보완합니다. 각 행의 자료 기준을 확인해 주세요.','Administrative records are labelled separately. Their current appointment status and contacts will be updated later; check the source basis on each record.','p')}</div>
    <div class="result-bar" data-filter-controls hidden><span data-result-count role="status" aria-live="polite"></span>{t('국문·영문으로 검색할 수 있습니다.','Search in Korean or English.')}</div>
    <table class="placement-table" role="table"><caption>{t('학계·연구 동문 · 성명 가나다순','Academic and research alumni · Korean name order')}</caption><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">{t('성명 · 전공','Name · Field')}</th><th scope="col" role="columnheader">{t('소속 · 경력','Affiliation · Career')}</th><th scope="col" role="columnheader">{t('연락처 · 홈페이지','Contact · Profile')}</th></tr></thead><tbody role="rowgroup">{''.join(rows)}</tbody></table>{empty_state()}</section></section>
    <section class="section wash" id="sources"><div class="wrap">{heading('About the records','진로 통계와 동문 명단의 자료 기준','Career statistics & alumni sources')}<div class="source-cards">{''.join(sources)}</div>
    {t('행정실 자료 업데이트: 2026년 9월 7일. 진로 통계는 자료에 수록된 기록의 분류이며, 모든 졸업생을 포괄하는 전수조사나 현재 재직 현황이 아닙니다. 공란·X 등은 진로 미확인으로 처리하고 미취업으로 단정하지 않았습니다.','Administrative records updated on 7 September 2026. These statistics classify the available records and are not a comprehensive survey of all graduates or a current appointment register. Blank or X entries are treated as unknown, not as evidence of unemployment.','p','section-note')}
    {t('공개 프로필 명단 확인: 2026년 9월 6일. 기존 명단의 소속·직급·연락처 근거는 각 행의 확인 출처에서 볼 수 있습니다. 행정실에서 추가된 경력은 행정실 기록으로 구분하며, 공개 프로필의 재확인은 추후 진행합니다.','Public-profile records were checked on 6 September 2026. Their affiliation, rank and contact evidence remains available under each record’s verification sources. Newly added careers are labelled as administrative records; their public profiles will be reviewed later.','p','section-note')}
    {t('공개 프로필의 직급은 출처의 명시적 표기를 따릅니다. 과거 자료에서만 확인된 직급은 자료 기준일을 함께 표시했습니다. 교수라는 호칭만으로 정교수로 분류하지 않으며, Lecturer·Senior Lecturer 등은 원래 직함을 유지했습니다.','Ranks in public-profile records follow explicit source titles. Ranks found only in dated records show the source date. The generic Korean honorific for faculty is not evidence of full-professor rank; titles such as Lecturer and Senior Lecturer are retained.','p','section-note')}
    {t('학계·연구 동문 명단은 취업 통계의 분모와 별개이며, 최초 임용기관 목록이 아닙니다. 학위 표시는 고려대학교에서 취득한 학위를 기준으로 합니다.','The academic and research alumni list is separate from the statistical denominator and is not a first-placement register. Degree labels refer to degrees earned at Korea University.','p','section-note')}</div></section>'''


for filename, active, ko, en, body in [
    ('index.html','home','연구와 사람','Research & People',home()),
    ('faculty.html','faculty','전공별 교수진','Faculty & Research Interests',faculty_directory()),
    ('lsom.html','lsom','LSOM 연구와 교수진','LSOM Research & Faculty',lsom()),
    ('placements.html','placements','졸업생 진로','Graduate Careers',placements())
]:
    (OUT / filename).write_text(layout(active,ko,en,body),encoding='utf-8')
    print(f'Built {filename}')

(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
urls = ['', 'faculty.html', 'lsom.html', 'placements.html']
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{path}</loc><lastmod>{VERIFIED}</lastmod></url>\n' for path in urls) + '</urlset>\n')
