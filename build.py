"""Build the KUBS research website from shared templates and public content data."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
FACULTY = json.loads((ROOT / 'data/faculty.json').read_text())
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
PLACEMENTS = json.loads((ROOT / 'data/placements.json').read_text())
AREAS = json.loads((ROOT / 'data/areas.json').read_text())
AREA_MAP = {a['code']: a for a in AREAS}
OFFICIAL = 'https://biz.korea.ac.kr/msphd/intro.html'
DIRECTORY = 'https://biz.korea.ac.kr/professor/professor_list1.html'
SITE = 'https://kubs-msphd.github.io/'
VERIFIED = '2026-09-06'

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
        'placements': ('고려대학교 경영대학 LSOM, IS, GB 동문의 소속·직급·이메일과 교수 프로필.', 'Explore KUBS LSOM, IS and Global Business alumni affiliations, academic ranks, email contacts and faculty profiles.'),
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
    alumni=''.join(f'<div><strong>{source["id"]}</strong><a href="placements.html?area={source["area_code"]}">{t(str(sum(a["source_id"]==source["id"] for a in PLACEMENTS["alumni"]))+"명 수록",str(sum(a["source_id"]==source["id"] for a in PLACEMENTS["alumni"]))+" alumni records")} →</a></div>' for source in PLACEMENTS['sources'])
    return f'''<section class="hero wrap"><div class="hero-grid"><div><p class="eyebrow">Graduate research at KUBS</p><h1>{t('좋은 질문에서 시작해,','Start with a question.')}<br><em>{t('새로운 지식으로.','Create new knowledge.')}</em></h1>{t('경영의 중요한 문제를 연구하는 사람들. 고려대학교 경영대학에서 나의 연구 주제와 연결되는 교수진, 그 이후의 진로를 만나보세요.','Meet the people studying important questions in business. Explore research interests, faculty and the paths our graduates take.','p','hero-text')}<div class="actions">{link('faculty.html','전공별 교수진 찾기','Find faculty','button')}{link('placements.html','졸업생 진로','Meet our alumni')}</div></div><figure class="hero-figure"><img src="assets/campus.jpg" width="720" height="480" fetchpriority="high" alt="고려대학교 경영대학 LG-POSCO경영관과 정원" data-alt-ko="고려대학교 경영대학 LG-POSCO경영관과 정원" data-alt-en="Korea University Business School LG-POSCO building and courtyard"><figcaption>{t('고려대학교 경영대학 · LG-POSCO경영관','Korea University Business School · LG-POSCO Building')}</figcaption></figure></div><div class="degree-strip"><p><strong>{t('석사 · 박사 · 석박사통합','MS · PhD · Integrated MS–PhD')}</strong></p><p>{t('연구 주제로 전공을 탐색하고, 사람으로 그 가능성을 확인하세요.','Find your field. Meet the people who make it possible.')}</p></div></section>
    <section class="section wrap" id="research">{heading('Research areas','어떤 질문을 연구하고 싶나요?','What do you want to understand?')}
      <div class="areas"><article class="featured-area"><p class="eyebrow">Find your research connections</p>{t('연구와 사람','Research & people','h3')}{t('전공과 연구 키워드로 교수진을 살펴보세요.','Explore faculty by field and research interests.','p')}{link('faculty.html',f'전체 교수진 {len(FACULTY)}명 보기',f'Explore all {len(FACULTY)} faculty')}</article><div><div class="area-list">{area_links}</div><p class="area-context">{link('faculty.html?area=M08','Business Analytics 교수진','Business Analytics faculty')} · {link(OFFICIAL,'BA 1년 석사과정 안내','BA one-year MS programme',external=True)}</p></div></div>
    </section><section class="section wash"><div class="wrap">{heading('Research spotlight · LSOM','질문을 함께 발전시키는 교수진','Meet the researchers',link('lsom.html','LSOM 연구와 최근 논문','LSOM research & publications'))}<div class="faculty-grid preview">{faculty}</div></div></section>
    <section class="wrap split-section"><div><p class="eyebrow">Academic careers</p>{t('연구의 다음 장을 써가는 동문들','The next chapter in a life of research','h2')}{t('LSOM, IS, GB 동문들의 학계 진출을 살펴보세요. 대학별 공개 프로필을 대조한 소속·직급과 연구 홈페이지를 함께 모았습니다.','Explore the academic careers of LSOM, IS and Global Business alumni, with affiliations, academic ranks and research profiles checked against public sources.','p')}{link('placements.html','졸업생 진로와 자료 출처','Explore alumni careers')}</div><div class="alumni-preview">{alumni}</div></section>'''

def directory_controls(codes, kind):
    # Option elements contain text only, with the same bilingual attributes as other labels.
    options = '<option value="all" data-ko="전체 전공" data-en="All fields">전체 전공</option>'
    for code in codes:
        area = AREA_MAP[code]
        options += f'<option value="{code}" data-ko="{attr(area["name_ko"])}" data-en="{attr(area["name_en"])}">{escape(area["name_ko"])}</option>'
    search_ko, search_en = ('이름 또는 연구 키워드', 'Name or research keyword') if kind == 'faculty' else ('이름 또는 소속 기관', 'Name or institution')
    return f'''<div class="directory-controls" data-filter-controls hidden>
      <label class="filter-field">{t('전공','Field')}<select data-area-filter>{options}</select></label>
      <label class="filter-field search-field">{t('검색','Search')}<input type="search" data-search-input placeholder="{search_ko}" data-placeholder-ko="{search_ko}" data-placeholder-en="{search_en}" autocomplete="off"></label>
      <button type="button" data-clear-filters>{t('초기화','Reset')}</button>
    </div><div class="result-bar" data-filter-controls hidden><span data-result-count role="status" aria-live="polite"></span>{t('국문·영문으로 검색할 수 있습니다.','Search in Korean or English.')}</div>'''

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
        return t('공개 연락처 미확인', 'Public contact not verified', 'p', 'placement-meta')
    return '<div class="alumni-contacts">' + ''.join(links) + '</div>'

def alumni_evidence(person):
    verification = person.get('profile_verification') or {}
    sources, used = [], set()
    original = person.get('source_url') or '#source-LSOM'
    for source in verification.get('sources', []):
        if not source.get('url') or source['url'] in used or source['url'] == original:
            continue
        used.add(source['url'])
        sources.append(f'<li><a href="{attr(source["url"])}">{escape(source.get("title") or "Profile source")} ↗</a></li>')
    sources.append(f'<li>{alumni_link(original, "동문 명단 원문", "Original alumni listing", person)}</li>')
    checked = verification.get('checked_at')
    date = f'<p class="placement-meta">{t("확인일", "Checked")}: {escape(checked)}</p>' if checked else ''
    return f'<details class="alumni-evidence"><summary>{t("확인 출처", "Verification sources")}</summary>{date}<ul>{"".join(sources)}</ul></details>'

def placements():
    rows = []
    for a in sorted(PLACEMENTS['alumni'], key=lambda a: a['name']):
        name = t(a.get('name_ko'), a.get('name_en'))
        area = AREA_MAP[a['area_code']]
        degree_ko, degree_en = (' · 박사', ' · PhD') if a['degree'] == 'PhD' else ('', '')
        meta = t(area['name_ko'] + degree_ko, area['name_en'] + degree_en, 'p', 'placement-meta')
        institution = t(a.get('institution_ko'), a.get('institution_en'))
        department = t(a.get('department_ko'), a.get('department_en'), 'p', 'placement-department')
        if a.get('department_ko') or a.get('department_en'):
            institution += department
        verification = a.get('profile_verification') or {}
        if verification.get('rank_status') in ['verified', 'dated_verified']:
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
        search = ' '.join(str(a.get(k) or '') for k in ['name','name_ko','name_en','institution_ko','institution_en','department_ko','department_en','position_ko','position_en','email','area']) + ' ' + area['name_ko'] + ' ' + area['name_en']
        rows.append(f'<tr id="{attr(a["id"])}" role="row" data-filter-item data-areas="{a["area_code"]}" data-search="{attr(search)}"><td role="cell" data-label-ko="성명 · 전공" data-label-en="Name · Field">{name}{meta}</td><td role="cell" data-label-ko="소속 · 직급" data-label-en="Affiliation · Rank">{institution}{position}</td><td role="cell" data-label-ko="연락처 · 홈페이지" data-label-en="Contact · Profile">{contacts}</td></tr>')
    sources = []
    for source in PLACEMENTS['sources']:
        source_link = link(source['url'],'원문 보기','View source',external=True) if source['url'] else ''
        sources.append(f'<article class="source-card" id="source-{source["id"]}">{t(source["label_ko"],source["label_en"],"h3")}{t(source["note_ko"],source["note_en"],"p")}{source_link}</article>')
    counts = {source['id']: sum(a['source_id'] == source['id'] for a in PLACEMENTS['alumni']) for source in PLACEMENTS['sources']}
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span><span>Placements</span></div><div class="page-hero-grid"><div><p class="eyebrow">Academic careers</p>{t('연구에서 시작된, 학문적 여정.','From research to academic careers.','h1','ko-heading')}</div>{t('LSOM, IS, GB 동문들의 학계 진출을 소개합니다. 대학별 공개 프로필을 통해 소속과 직급을 살펴보고, 동문들의 연구와 연결해 보세요.','Meet LSOM, IS and Global Business alumni in academia. Explore their affiliations, academic ranks and research through university and personal profiles.','p','lede')}</div></div></section>
    <section class="section wrap" data-directory="placements"><div class="directory-intro">{t(f'LSOM {counts["LSOM"]}명 · IS {counts["IS"]}명 · GB {counts["GB"]}명, 총 {len(PLACEMENTS["alumni"])}명을 수록했습니다.',f'{len(PLACEMENTS["alumni"])} alumni records: {counts["LSOM"]} LSOM · {counts["IS"]} IS · {counts["GB"]} Global Business.','p')}{t('각 대학과 연구자의 공개 프로필을 대조한 소속·직급·연락처입니다. 직급을 명확히 확인할 수 없는 경우에는 별도로 표시했습니다.','Affiliations, ranks and contacts were checked against university and researcher profiles. Ranks that could not be established explicitly are marked.','p')}{link('#sources','자료 기준 보기','About these records')}</div>
    {directory_controls(['M06','M07','M02'], 'placements')}<table class="placement-table" role="table"><caption>{t('졸업생 진로 · 성명 가나다순','Alumni careers · Korean name order')}</caption><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">{t('성명 · 전공','Name · Field')}</th><th scope="col" role="columnheader">{t('소속 · 직급','Affiliation · Rank')}</th><th scope="col" role="columnheader">{t('연락처 · 홈페이지','Contact · Profile')}</th></tr></thead><tbody role="rowgroup">{''.join(rows)}</tbody></table>{empty_state()}</section>
    <section class="section wash" id="sources"><div class="wrap">{heading('About the records','동문 명단과 정보 확인 기준','Alumni sources & verification')}<div class="source-cards">{''.join(sources)}</div>{t('프로필 확인: 2026년 9월 6일. 각 행의 확인 출처에서 소속·직급·연락처 근거를 볼 수 있습니다. 공개 프로필의 업데이트 시점에 따라 실제 재직 정보와 차이가 있을 수 있습니다.','Profiles checked on 6 September 2026. Open each record’s verification sources for its affiliation, rank and contact evidence. Public profiles may lag behind appointment changes.','p','section-note')}{t('직급은 출처의 명시적 표기를 따릅니다. 과거 자료에서만 확인된 직급은 자료 기준일을 함께 표시했습니다. 교수라는 호칭만으로 정교수로 분류하지 않으며, Lecturer·Senior Lecturer 등은 원래 직함을 유지했습니다.','Ranks follow explicit source titles. Ranks established only in dated records are shown with the source date. The generic Korean honorific for faculty is not treated as evidence of full-professor rank; titles such as Lecturer and Senior Lecturer are retained.','p','section-note')}{t('이 페이지는 최초 임용기관 목록이나 전체 졸업생 취업률 통계가 아닙니다. 학위 표시는 고려대학교에서 취득한 학위가 확인된 경우에 한합니다.','This page is not a first-placement register or a graduate employment-rate dataset. Degree labels refer only to verified Korea University degrees.','p','section-note')}</div></section>'''

for filename, active, ko, en, body in [
    ('index.html','home','연구와 사람','Research & People',home()),
    ('faculty.html','faculty','전공별 교수진','Faculty & Research Interests',faculty_directory()),
    ('lsom.html','lsom','LSOM 연구와 교수진','LSOM Research & Faculty',lsom()),
    ('placements.html','placements','졸업생 진로','Academic Placements',placements())
]:
    (OUT / filename).write_text(layout(active,ko,en,body),encoding='utf-8')
    print(f'Built {filename}')

(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}sitemap.xml\n')
urls = ['', 'faculty.html', 'lsom.html', 'placements.html']
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'  <url><loc>{SITE}{path}</loc><lastmod>{VERIFIED}</lastmod></url>\n' for path in urls) + '</urlset>\n')
