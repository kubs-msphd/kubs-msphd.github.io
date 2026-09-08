"""Shared research pages. Publication evidence remains in data, not public notes."""
from html import escape


SLUGS = {
    'M01': 'management', 'M02': 'global-business', 'M03': 'marketing',
    'M04': 'finance', 'M09': 'strategy', 'M05': 'accounting',
    'M07': 'information-systems', 'M06': 'lsom', 'M08': 'business-analytics',
}


def research_filename(code):
    return SLUGS[code] + '.html'


def area_navigation(ctx, current=None):
    t = ctx['t']
    links = []
    for area in ctx['AREAS']:
        active = ' aria-current="page"' if area['code'] == current else ''
        links.append(f'<a href="{research_filename(area["code"])}"{active}>{t(area["name_ko"], area["name_en"])}</a>')
    return f'<nav class="research-area-nav" aria-label="연구 전공" data-aria-ko="연구 전공" data-aria-en="Research fields"><div class="wrap">{"".join(links)}</div></nav>'


def publication_card(paper, ctx):
    t, link, attr = ctx['t'], ctx['link'], ctx['attr']
    authors = ', '.join(paper['authors']) if isinstance(paper['authors'], list) else paper['authors']
    return f'''<article class="publication"><span class="year">{paper['year']}</span><div><h3><a href="{attr(paper['url'])}">{escape(paper['title'])}</a></h3><p class="authors">{escape(authors)}</p><p class="journal">{escape(paper['journal'])}</p>{t(paper['status_ko'],paper['status_en'],'p','paper-status')}{t(paper['summary_ko'],paper['summary_en'],'p','paper-summary')}</div>{link(paper['url'],'논문 보기','Read paper',external=True)}</article>'''


def render_research_index(ctx):
    t, link, heading = ctx['t'], ctx['link'], ctx['heading']
    cards = []
    for area in ctx['AREAS']:
        content = ctx['RESEARCH_AREAS'][area['code']]
        topics = ' · '.join(topic['label_ko'] for topic in content['topics'])
        topics_en = ' · '.join(topic['label_en'] for topic in content['topics'])
        degree = t('1년 석사과정','One-year MS programme','p','research-degree') if area['code'] == 'M08' else ''
        cards.append(f'''<article class="research-area-card"><p class="eyebrow">{escape(area['name_en'])}</p>{t(area['name_ko'],area['name_en'],'h2')}{degree}{t(content['intro_ko'],content['intro_en'],'p')}{t(topics,topics_en,'p','research-tags')}{link(research_filename(area['code']),'연구·논문·교수진 보기','Explore research, papers & faculty')}</article>''')
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span>{t('연구','Research')}</div><div class="page-hero-grid"><div><p class="eyebrow">Research across KUBS</p>{t('질문에서 시작하는 경영 연구','Business research begins with a question.','h1','ko-heading')}</div>{t('사람과 조직, 시장과 기술을 탐구합니다. 전공별 연구 주제, UTD 저널 선정 논문과 함께 연구할 교수진을 만나보세요.','Explore people and organizations, markets and technology. Discover research questions, selected UTD journal papers and faculty across our fields.','p','lede')}</div></div></section>
    <section class="section wrap">{heading('Find your field','나의 질문은 어디로 이어질까요?','Where will your question take you?')}<div class="research-area-grid">{''.join(cards)}</div></section>'''


def render_research_area(code, ctx):
    t, link, heading = ctx['t'], ctx['link'], ctx['heading']
    area, content = ctx['AREA_MAP'][code], ctx['RESEARCH_AREAS'][code]
    topics = ''.join(f'<article class="topic"><span class="topic-number">0{i+1}</span>{t(topic["question_ko"],topic["question_en"],"h3")}{t(topic["description_ko"],topic["description_en"],"p")}</article>' for i,topic in enumerate(content['topics']))
    papers = [paper for paper in ctx['PAPERS'] if paper['area_code'] == code]
    years = sorted(set(paper['year'] for paper in papers))
    period = str(years[0]) if len(years) == 1 else f'{years[0]}–{years[-1]}'
    paper_note = t(f'UTD 저널 선정 논문 · {period}',f'Selected UTD journal papers · {period}','p')
    faculty = ''.join(ctx['faculty_card'](person) for person in ctx['FACULTY'] if code in person['area_codes'])
    degree = t('Business Analytics · 1년 석사과정','Business Analytics · One-year MS programme','p','subtitle') if code == 'M08' else ''
    subtitle = '<p class="subtitle">Logistics, Service and<br>Operations Management</p>' if code == 'M06' else degree
    community_link = link(content['community_url'],'전공 홈페이지','Programme website',external=True) if content.get('community_url') else ''
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span><a href="research.html">{t('연구','Research')}</a><span>/</span>{t(area['name_ko'],area['name_en'])}</div><div class="page-hero-grid"><div><p class="eyebrow">Research area · {escape(area['name_en'])}</p>{t(area['name_ko'],area['name_en'],'h1','ko-heading')}{subtitle}</div>{t(content['intro_ko'],content['intro_en'],'p','lede')}</div></div></section>
    {area_navigation(ctx,code)}
    <nav class="jump-nav" aria-label="페이지 목차" data-aria-ko="페이지 목차" data-aria-en="On this page"><div class="wrap"><a href="#questions">{t('연구 주제','Research')}</a><a href="#publications">{t('최근 논문','Publications')}</a><a href="#faculty">{t('교수진','Faculty')}</a><a href="#community">{t('세미나와 진로','Community')}</a></div></nav>
    <section class="section wrap" id="questions">{heading('Questions we study','현실의 문제를 연구의 질문으로','Real problems. Research questions.')}<div class="research-topics">{topics}</div><div class="method-line"><strong>{t('연구 방법','Methods')}</strong>{t(content['methods_ko'],content['methods_en'])}</div></section>
    <section class="section wash" id="publications"><div class="wrap">{heading('Selected recent publications','최근 연구를 살펴보세요','A closer look at recent research',paper_note)}<div class="publications">{''.join(publication_card(paper,ctx) for paper in papers)}</div>{t('더 많은 논문은 교수님의 프로필에서 만나보세요.','Explore faculty profiles for more publications.','p','section-note')}</div></section>
    <section class="section wrap" id="faculty">{heading('Meet the faculty','함께 연구할 교수진을 만나보세요','Find your research connections')}<div class="faculty-grid faculty-full">{faculty}</div>{link('faculty.html','전체 전공 교수진','Explore all faculty')}</section>
    <section class="section wash" id="community"><div class="wrap next-cards"><article class="next-card"><p class="eyebrow">Research conversations</p>{t('세미나와 연구 교류','Seminars & research exchange','h2')}{t('경영대학의 세미나와 연구 행사에서 새로운 질문과 아이디어를 나눕니다.','Discover new questions and ideas at KUBS seminars and research events.','p')}{link('https://biz.korea.ac.kr/news/calendar.html','KUBS 세미나 일정','KUBS events calendar',external=True)}{community_link}</article><article class="next-card"><p class="eyebrow">Careers after KUBS</p>{t('연구, 그 이후의 여정','The next chapter after KUBS','h2')}{t('전공에서 쌓은 경험이 이어지는 다양한 진로를 만나보세요.','Explore the paths that build on the experience gained in this field.','p')}{link('placements.html?area='+code,area['name_ko']+' 졸업생 진로',area['name_en']+' alumni careers')}</article></div></section>'''
