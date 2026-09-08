"""Shared research pages. Publication evidence remains in data, not public notes."""
from html import escape


SLUGS = {
    'M01': 'management', 'M02': 'global-business', 'M03': 'marketing',
    'M04': 'finance', 'M09': 'strategy', 'M05': 'accounting',
    'M07': 'information-systems', 'M06': 'lsom', 'M08': 'business-analytics',
}


DESCRIPTIONS = {
    'M01': (
        '리더십, 협상, 인적자원관리, 조직 변화와 지속가능경영을 연구합니다.',
        'Research in leadership, negotiation, human resource management, organizational change and sustainability.',
    ),
    'M02': (
        '국제무역과 금융, 글로벌 마케팅, 국가별 제도와 기업 활동을 연구합니다.',
        'Research in international trade and finance, global marketing, institutions and international business.',
    ),
    'M03': (
        '소비자 행동, 브랜드, 유통과 플랫폼, 마케팅 전략과 성과를 연구합니다.',
        'Research in consumer behavior, brands, channels and platforms, marketing strategy and performance.',
    ),
    'M04': (
        '기업재무와 지배구조, 투자와 자산가격, 금융기관과 위험관리를 연구합니다.',
        'Research in corporate finance and governance, investments and asset pricing, financial institutions and risk management.',
    ),
    'M09': (
        '기업의 경쟁전략, 기술혁신과 창업, 글로벌 전략과 지속가능경영을 연구합니다.',
        'Research in competitive strategy, innovation and entrepreneurship, global strategy and sustainability.',
    ),
    'M05': (
        '재무보고와 공시, 기업가치평가, 투자자 판단, 감사와 조세를 연구합니다.',
        'Research in financial reporting and disclosure, valuation, investor judgment, auditing and taxation.',
    ),
    'M07': (
        '디지털 플랫폼, AI와 사용자 경험, 정보기술의 도입과 기업 성과를 연구합니다.',
        'Research in digital platforms, AI and user experiences, technology adoption and business performance.',
    ),
    'M06': (
        '물류·공급망, 서비스 운영, 플랫폼과 기술을 실증분석과 수리모형으로 연구합니다.',
        'Research in logistics and supply chains, service operations, platforms and technology using empirical and analytical methods.',
    ),
    'M08': (
        '데이터 분석, 인과추론과 최적화를 경영 의사결정에 적용하는 1년 석사과정입니다.',
        'A one-year MS programme applying data analytics, causal inference and optimization to business decisions.',
    ),
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
    t, link = ctx['t'], ctx['link']
    rows = []
    for area in ctx['AREAS']:
        content = ctx['RESEARCH_AREAS'][area['code']]
        topics = ' · '.join(topic['label_ko'] for topic in content['topics'])
        topics_en = ' · '.join(topic['label_en'] for topic in content['topics'])
        intro_ko, intro_en = DESCRIPTIONS[area['code']]
        degree = t('1년 석사과정','One-year MS programme','p','research-degree') if area['code'] == 'M08' else ''
        english_name = t(area['name_en'],'','p','english-name') if area['name_ko'] != area['name_en'] else ''
        rows.append(f'''<article class="research-field-row"><div class="research-field-name">{t(area['name_ko'],area['name_en'],'h2')}{english_name}{degree}</div><div class="research-field-content">{t(intro_ko,intro_en,'p')}{t(topics,topics_en,'p','research-tags')}</div><div class="research-field-links">{link(research_filename(area['code']),'연구 및 논문','Research & publications')}{link('faculty.html?area='+area['code'],'교수진','Faculty')}</div></article>''')
    return f'''{ctx['page_intro']('전공별 연구','Research areas','연구','Research','전공별 연구분야, 주요 논문과 교수진을 안내합니다.','Research interests, selected publications and faculty by field.')}
    <section class="section wrap"><div class="research-field-list">{''.join(rows)}</div></section>'''


def render_research_area(code, ctx):
    t, link, heading = ctx['t'], ctx['link'], ctx['heading']
    area, content = ctx['AREA_MAP'][code], ctx['RESEARCH_AREAS'][code]
    topics = ''.join(f'<article class="topic">{t(topic["label_ko"],topic["label_en"],"h3")}{t(topic["description_ko"],topic["description_en"],"p")}</article>' for topic in content['topics'])
    papers = [paper for paper in ctx['PAPERS'] if paper['area_code'] == code]
    years = sorted(set(paper['year'] for paper in papers))
    period = str(years[0]) if len(years) == 1 else f'{years[0]}–{years[-1]}'
    paper_note = t(f'UTD 저널 선정 논문 · {period}',f'Selected UTD journal papers · {period}','p')
    faculty = ''.join(ctx['faculty_card'](person) for person in ctx['FACULTY'] if code in person['area_codes'])
    intro_ko, intro_en = DESCRIPTIONS[code]
    community_link = link(content['community_url'],'전공 홈페이지','Programme website',external=True) if content.get('community_url') else ''
    return f'''{ctx['page_intro'](area['name_ko'],area['name_en'],'연구','Research',intro_ko,intro_en,section_url='research.html')}
    {area_navigation(ctx,code)}
    <nav class="jump-nav" aria-label="페이지 목차" data-aria-ko="페이지 목차" data-aria-en="On this page"><div class="wrap"><a href="#questions">{t('연구분야','Research interests')}</a><a href="#publications">{t('최근 논문','Publications')}</a><a href="#faculty">{t('교수진','Faculty')}</a><a href="#seminars">{t('세미나','Seminars')}</a><a href="#careers">{t('졸업생 진로','Graduate careers')}</a></div></nav>
    <section class="section wrap" id="questions">{heading('','연구분야','Research interests')}<div class="research-topics">{topics}</div><div class="method-line"><strong>{t('연구 방법','Methods')}</strong>{t(content['methods_ko'],content['methods_en'])}</div></section>
    <section class="section wash" id="publications"><div class="wrap">{heading('','최근 논문','Selected publications',paper_note)}<div class="publications">{''.join(publication_card(paper,ctx) for paper in papers)}</div>{t('교수별 전체 논문은 교수진 프로필에서 확인할 수 있습니다.','Full publication lists are available in faculty profiles.','p','section-note')}</div></section>
    <section class="section wrap" id="faculty">{heading('','교수진','Faculty')}<div class="faculty-grid faculty-full">{faculty}</div>{link('faculty.html','전체 전공 교수진','All faculty')}</section>
    <section class="section wash" id="community"><div class="wrap next-cards"><article class="next-card" id="seminars">{t('세미나','Seminars','h2')}{t('경영대학 연구 세미나와 학술행사 일정을 확인할 수 있습니다.','Schedules for KUBS research seminars and academic events.','p')}{link('https://biz.korea.ac.kr/news/calendar.html','KUBS 세미나 일정','KUBS events calendar',external=True)}{community_link}</article><article class="next-card" id="careers">{t('졸업생 진로','Graduate careers','h2')}{t('전공별 졸업생 진로와 학계 진출 현황을 안내합니다.','Graduate career outcomes and academic placements by field.','p')}{link('placements.html?area='+code,area['name_ko']+' 졸업생 진로',area['name_en']+' alumni careers')}</article></div></section>'''
