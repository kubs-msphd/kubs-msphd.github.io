"""Build three portable static pages from shared templates and public content data."""
from pathlib import Path
from html import escape
import json

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'dist'
FACULTY = json.loads((ROOT / 'data/faculty.json').read_text())
PAPERS = json.loads((ROOT / 'data/publications.json').read_text())
PLACEMENTS = json.loads((ROOT / 'data/placements.json').read_text())
OFFICIAL = 'https://biz.korea.ac.kr/msphd/intro.html'

def t(ko, en, tag='span', cls=''):
    return f'<{tag} class="{escape(cls)}" data-ko="{escape(ko, quote=True)}" data-en="{escape(en, quote=True)}">{escape(ko)}</{tag}>'

def link(url, ko, en, cls='text-link', external=False):
    mark = '↗' if external else '→'
    return f'<a class="{cls}" href="{escape(url, quote=True)}">{t(ko,en)}<span aria-hidden="true">{mark}</span></a>'

def heading(label, ko, en, aside=''):
    return f'<div class="section-heading"><div><p class="eyebrow">{label}</p>{t(ko,en,"h2")}</div>{aside}</div>'

def faculty_card(row):
    return f'''<article class="faculty-card">
      <div class="faculty-heading"><img src="{row['photo']}" width="86" height="108" loading="lazy" alt="{escape(row['name_ko'])}">
      <div>{t(row['name_ko'],row['name_en'],'h3')}<p class="english-name">{t(row['name_en'],row['name_ko'])}</p><p class="position">LSOM · {t('교수진','Faculty')}</p></div></div>
      {t(row['interests_ko'],row['interests_en'],'p','interests')}
      {link(row['url'],'프로필 및 연구','Profile & research',external=True)}
    </article>'''

def official_band():
    return f'''<div class="wrap"><section class="official-band" aria-label="Official information"><div>{t('지원과 학사 안내','Admissions & academic information','h2')}{t('모집요강, 장학제도, 학사규정은 공식 홈페이지에서 확인하세요.','Find application requirements, funding details and academic regulations on the official website.','p')}</div><div class="official-links">
      <a href="https://biz.korea.ac.kr/msphd/process.html" data-href-ko="https://biz.korea.ac.kr/msphd/process.html" data-href-en="https://biz.korea.ac.kr/eng/msphd/process.html">{t('학위과정','Degree programmes')} ↗</a>
      <a href="https://graduate.korea.ac.kr/">{t('입학안내','Admissions')} ↗</a>
      <a href="https://biz.korea.ac.kr/msphd/scholarship.html" data-href-ko="https://biz.korea.ac.kr/msphd/scholarship.html" data-href-en="https://biz.korea.ac.kr/eng/msphd/scholarship.html">{t('장학제도','Funding')} ↗</a>
    </div></section></div>'''

def layout(active, ko_title, en_title, body):
    navigation=''.join(f'<a href="{url}"'+(' aria-current="page"' if active==key else '')+f'>{t(ko,en)}</a>' for key,url,ko,en in [('home','index.html','홈','Home'),('lsom','lsom.html','LSOM','LSOM'),('placements','placements.html','졸업생 진로','Placements')])
    return f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title data-ko="{escape(ko_title)} · KUBS MS &amp; PhD" data-en="{escape(en_title)} · KUBS MS &amp; PhD">{escape(ko_title)} · KUBS MS &amp; PhD</title>
<meta name="description" content="Explore research, faculty and doctoral alumni at Korea University Business School. LSOM, MS and PhD research programmes.">
<meta name="robots" content="noindex, nofollow"><meta name="theme-color" content="#860027">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/style.css"><script src="assets/site.js" defer></script></head>
<body><a class="skip" href="#main">{t('본문 바로가기','Skip to content')}</a>
<div class="prototype"><div class="wrap">{t('검토용 프로토타입 · KUBS MS & PhD','Review prototype · KUBS MS & PhD')}<span>KOREA UNIVERSITY BUSINESS SCHOOL</span></div></div>
<header><div class="wrap header-inner"><a class="brand" href="index.html" aria-label="KUBS MS and PhD home"><span class="brand-mark">KUBS</span><span class="brand-copy"><strong>MS & PhD</strong><span>Korea University Business School</span></span></a>
<div class="nav-wrap"><nav class="nav" id="navigation" aria-label="Main navigation">{navigation}<a href="{OFFICIAL}" data-href-ko="{OFFICIAL}" data-href-en="https://biz.korea.ac.kr/eng/msphd/intro.html">{t('공식 대학원 안내','Official programme')} ↗</a></nav><div class="language" aria-label="Language"><button type="button" data-language="ko" aria-pressed="true" lang="ko">KO</button><button type="button" data-language="en" aria-pressed="false" lang="en">EN</button></div><button type="button" class="menu-toggle" aria-controls="navigation" aria-expanded="false">{t('메뉴','Menu')}</button></div></div></header>
<main id="main">{body}{official_band()}</main>
<footer><div class="wrap"><div class="footer-top"><div><div class="footer-title">KUBS <span>MS & PhD</span></div>{t('고려대학교 경영대학 일반대학원','Korea University Business School · Graduate Research Programmes','p')}{t('서울특별시 성북구 안암로 145','145 Anam-ro, Seongbuk-gu, Seoul, Republic of Korea','p')}</div><div><a href="mailto:kubs_msphd@korea.ac.kr">kubs_msphd@korea.ac.kr</a>{t('일반대학원 문의','Graduate programme enquiries','p')}</div></div><div class="footer-bottom">{t('연구와 사람을 소개하는 대학원 웹사이트 프로토타입','A graduate research website prototype')}<span>© 2026 Korea University Business School</span></div></div></footer></body></html>'''

def home():
    areas=[('경영관리','Management',OFFICIAL),('글로벌비즈니스','Global Business','https://sites.google.com/view/kubsib'),('마케팅','Marketing',OFFICIAL),('재무금융','Finance',OFFICIAL),('전략','Strategy',OFFICIAL),('회계학','Accounting',OFFICIAL),('정보시스템','Information Systems','https://sites.google.com/korea.ac.kr/mis')]
    area_links=''.join(f'<a href="{url}"><span>{t(ko,en)}<small>{en}</small></span><span aria-hidden="true">↗</span></a>' for ko,en,url in areas)
    faculty=''.join(faculty_card(FACULTY[i]) for i in [4,6,9])
    alumni=''.join(f'<div><strong>{a["name"]}</strong>{t(a["institution_ko"],a["institution_en"])}</div>' for a in PLACEMENTS['alumni'][:3])
    return f'''<section class="hero wrap"><div class="hero-grid"><div><p class="eyebrow">Graduate research at KUBS</p><h1>{t('좋은 질문에서 시작해,','Start with a question.')}<br><em>{t('새로운 지식으로.','Create new knowledge.')}</em></h1>{t('경영의 중요한 문제를 연구하는 사람들. 고려대학교 경영대학에서 나의 연구 주제와 함께할 교수진, 그 이후의 진로를 만나보세요.','Meet the people studying important questions in business. Explore research interests, faculty and the paths our graduates take.','p','hero-text')}<div class="actions">{link('lsom.html','LSOM 연구와 교수진','Explore LSOM','button')}{link('placements.html','졸업생 진로','Meet our alumni')}</div></div><figure class="hero-figure"><img src="assets/campus.jpg" width="720" height="480" fetchpriority="high" alt="Korea University Business School LG-POSCO building and courtyard"><figcaption>{t('고려대학교 경영대학 · LG-POSCO경영관','Korea University Business School · LG-POSCO Building')}</figcaption></figure></div><div class="degree-strip"><p><strong>{t('석사 · 박사 · 석박사통합','MS · PhD · Integrated MS–PhD')}</strong></p><p>{t('연구 주제로 전공을 탐색하고, 사람으로 그 가능성을 확인하세요.','Find your field. Meet the people who make it possible.')}</p></div></section>
    <section class="section wrap" id="research">{heading('Research areas','어떤 질문을 연구하고 싶나요?','What do you want to understand?')}
      <div class="areas"><article class="featured-area"><p class="eyebrow">Explore the field</p><h3>LSOM</h3><p>Logistics, Service and<br>Operations Management</p>{link('lsom.html','연구 주제와 교수진 보기','Research & faculty')}</article><div><div class="area-list">{area_links}</div>{t('다른 전공은 현재 운영 중인 전공·대학원 안내로 연결됩니다.','Other fields link to their existing programme information.','p','area-context')}</div></div>
    </section><section class="section wash"><div class="wrap">{heading('People behind the research','질문을 함께 발전시키는 교수진','Meet the researchers',link('lsom.html#faculty','LSOM 교수진 전체 보기','All LSOM faculty'))}<div class="faculty-grid preview">{faculty}</div></div></section>
    <section class="wrap split-section"><div><p class="eyebrow">Life after the PhD</p>{t('연구의 다음 장을 써가는 동문들','The next chapter in a life of research','h2')}{t('LSOM에서 박사학위를 취득한 동문들은 여러 대학에서 연구와 교육을 이어가고 있습니다.','LSOM doctoral alumni continue their work as researchers and educators at universities.','p')}{link('placements.html','졸업생과 소속 대학 보기','Explore academic careers')}</div><div class="alumni-preview">{alumni}</div></section>'''

def lsom():
    topics=[('공급망은 어떻게 더 잘 회복할 수 있을까?','How can supply chains recover better?','의약품 공급부족, 품질관리, 공급사슬의 운영과 회복을 연구합니다.','Drug shortages, quality management, and the operation and recovery of supply chains.'),('서비스의 기다림과 자원 배분을 어떻게 개선할까?','How can services make better use of time and resources?','서비스 시스템의 수요와 용량, 대기행렬, 수익관리와 의사결정을 연구합니다.','Demand, capacity, queueing, revenue management and decisions in service systems.'),('플랫폼과 AI는 경쟁을 어떻게 바꾸는가?','How do platforms and AI change competition?','디지털 전환, 플랫폼 경쟁, 새로운 기술과 비즈니스 모델을 연구합니다.','Digital transformation, platform competition, emerging technologies and business models.')]
    topic_html=''.join(f'<article class="topic"><span class="topic-number">0{i+1}</span>{t(a,b,"h3")}{t(c,d,"p")}</article>' for i,(a,b,c,d) in enumerate(topics))
    papers=''.join(f'<article class="publication"><span class="year">{p["year"]}</span><div><h3><a href="{p["url"]}">{escape(p["title"])}</a></h3><p class="authors">{escape(p["authors"])}</p><p class="journal">{escape(p["journal"])}</p>{t(p["status_ko"],p["status_en"],"p","paper-status")}{t(p["summary_ko"],p["summary_en"],"p","paper-summary")}</div>{link(p["url"],"논문 보기","Read paper",external=True)}</article>' for p in PAPERS)
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span>{t('연구 전공','Research areas')}<span>/</span><span>LSOM</span></div><div class="page-hero-grid"><div><p class="eyebrow">Research area</p><h1>LSOM</h1><p class="subtitle">Logistics, Service and<br>Operations Management</p></div>{t('공급망부터 서비스, 플랫폼까지. 실제 경영 문제를 데이터와 이론으로 이해하고 더 나은 의사결정을 연구합니다.','From supply chains to services and platforms, we use data and theory to understand business problems and improve decisions.','p','lede')}</div></div></section>
    <nav class="jump-nav" aria-label="LSOM sections"><div class="wrap"><a href="#questions">{t('연구 주제','Research')}</a><a href="#faculty">{t('교수진','Faculty')}</a><a href="#publications">{t('최근 논문','Publications')}</a><a href="#community">{t('세미나와 진로','Community')}</a></div></nav>
    <section class="section wrap" id="questions">{heading('Questions we study','현실의 문제를 연구의 질문으로','Real problems. Research questions.')}<div class="research-topics">{topic_html}</div><div class="method-line"><strong>{t('연구 방법','Methods')}</strong>{t('실증분석 · 인과추론 · 최적화 · 게임이론 · 대기행렬 · 시뮬레이션','Empirical analysis · Causal inference · Optimization · Game theory · Queueing · Simulation')}</div></section>
    <section class="section wash" id="faculty"><div class="wrap">{heading('LSOM faculty','함께 연구할 교수진을 만나보세요','Find your research connections',t('관심 주제와 최근 연구를 살펴보고 나의 질문과 연결해 보세요.','Explore research interests and recent work to find connections with your own questions.','p'))}<div class="faculty-grid faculty-full">{''.join(faculty_card(f) for f in FACULTY)}</div>{t('전임교수 명단은 KUBS 공식 교수소개 기준입니다. 연구 키워드는 공개 프로필과 논문을 바탕으로 요약했습니다.','Faculty membership follows the official KUBS directory. Research keywords summarize public profiles and publications.','p','section-note')}</div></section>
    <section class="section wrap" id="publications">{heading('Selected recent publications','최근 연구를 살펴보세요','A closer look at recent research',t('2025–2026년 게재논문 중 선정','Selected publications, 2025–2026','p'))}<div class="publications">{papers}</div>{t('전체 논문 목록은 각 교수님의 프로필에서 확인할 수 있습니다.','Visit individual faculty profiles for complete publication lists.','p','section-note')}</section>
    <section class="section wash" id="community"><div class="wrap next-cards"><article class="next-card"><p class="eyebrow">Research conversations</p>{t('세미나와 연구 교류','Seminars & research exchange','h2')}{t('경영대학에서 열리는 세미나와 연구 행사는 KUBS 캘린더에서 확인할 수 있습니다.','Explore seminars and research events through the KUBS calendar.','p')}{link('https://biz.korea.ac.kr/news/calendar.html','KUBS 세미나 일정','KUBS events calendar',external=True)}</article><article class="next-card"><p class="eyebrow">Academic careers</p>{t('LSOM 박사 이후의 여정','Where an LSOM PhD can lead','h2')}{t('졸업 후 대학 교수로 진출한 동문들과 소속 대학을 만나보세요.','Meet doctoral alumni who have gone on to academic careers.','p')}{link('placements.html','졸업생 진로 보기','Explore alumni careers')}</article></div></section>'''

def placements():
    rows=''.join(f'<tr><td>{escape(a["name"])}</td><td>{t(a["institution_ko"],a["institution_en"])}</td><td>{t("LSOM 박사","PhD · LSOM")}</td></tr>' for a in sorted(PLACEMENTS['alumni'],key=lambda a:a['name']))
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span><span>Placements</span></div><div class="page-hero-grid"><div><p class="eyebrow">Academic placements</p>{t('연구에서 시작된, 학문적 여정.','From doctoral research to academic careers.','h1','ko-heading')}</div>{t('LSOM 박사학위를 취득한 뒤 대학 교수로 진출한 동문들을 소개합니다.','Meet LSOM doctoral graduates who have gone on to become university faculty.','p','lede')}</div></div></section>
    <section class="section wrap"><div class="placement-layout"><aside class="placement-aside"><div><p class="eyebrow">Research area</p><h2>LSOM</h2><p>Logistics, Service and<br>Operations Management</p></div><div><span class="count">{len(PLACEMENTS['alumni'])}</span>{t('수록 동문','Alumni featured','p')}</div>{t('소속은 제공된 동문 명단 기준입니다. 최초 부임 대학을 뜻하지 않으며, 전체 졸업생에 대한 통계가 아닙니다.','Affiliations follow the supplied alumni directory. They do not necessarily represent first placements; this is not a complete graduate-outcomes dataset.','p','source-note')}</aside><div><table class="placement-table"><caption>{t('LSOM 박사 동문 · 성명 가나다순','LSOM doctoral alumni · Ordered by Korean name')}</caption><thead><tr><th scope="col">{t('성명','Name')}</th><th scope="col">{t('소속 대학','University affiliation')}</th><th scope="col">{t('학위 · 전공','Degree · Field')}</th></tr></thead><tbody>{rows}</tbody></table>{t('자료 반영: 2026년 9월. 졸업연도와 최초 임용 정보는 확인 후 보완할 예정입니다.','Directory added in September 2026. Graduation years and initial appointments will be added after verification.','p','placement-note')}<div class="end-link"><p>{t('이들의 연구가 시작된 곳을 살펴보세요.','Explore the research community behind these academic journeys.')}</p>{link('lsom.html','LSOM 연구와 교수진','LSOM research & faculty')}</div></div></div></section>'''

for filename, active, ko, en, body in [
    ('index.html','home','연구와 사람','Research & People',home()),
    ('lsom.html','lsom','LSOM 연구와 교수진','LSOM Research & Faculty',lsom()),
    ('placements.html','placements','졸업생 진로','Academic Placements',placements())
]:
    (OUT / filename).write_text(layout(active,ko,en,body),encoding='utf-8')
    print(f'Built {filename}')
