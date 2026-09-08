"""Public graduate-career views; source and verification notes stay in data files.

The rendering context is build.py's namespace. Original administrative records
and verification objects are deliberately not serialized by this module.
"""
def summarize_outcomes(summary, degree):
    """Map recorded career outcomes to visitor-facing groups without losing rows.

    Unknown records alone are excluded. Preparation, planned employment and
    inactive statuses have information and belong to other career paths, never
    to employment. Master's further study includes both study and study plans.
    """
    statuses = summary['status_counts']
    counts = summary['category_counts']
    denominator = summary['total_records'] - statuses.get('unknown', 0)
    if degree == 'masters':
        categories = [
            ('research', '연구기관', 'Research institutes', counts.get('research_institute', 0)),
            ('domestic', '국내기업', 'Korean companies', counts.get('domestic_company', 0)),
            ('international', '해외/외국계 기업', 'Overseas & foreign companies', counts.get('international_company', 0)),
            ('public', '공공/비영리기관', 'Public & nonprofit organizations', counts.get('public_nonprofit', 0)),
            ('study', '박사/유학 진학·진학예정', 'Doctoral / overseas study & study plans', statuses.get('further_study', 0)),
        ]
        other = denominator - sum(row[3] for row in categories)
        categories.append(('other', '기타', 'Other paths', other))
    elif degree == 'doctoral':
        categories = [
            ('faculty', '대학 교원', 'University faculty', counts.get('faculty', 0)),
            ('academic_research', '연구직', 'University research roles', counts.get('academic_research', 0)),
            ('teaching', '강의/겸임/초빙 및 대학·교육기관 기타', 'Teaching, adjunct, visiting & other university roles', counts.get('teaching', 0) + counts.get('university_other', 0)),
            ('research', '연구기관', 'Research institutes', counts.get('research_institute', 0)),
            ('employment', '취업', 'Business, public-sector & other employment', sum(counts.get(key, 0) for key in ['domestic_company', 'international_company', 'public_nonprofit', 'self_employed', 'employer_unknown'])),
        ]
        other = denominator - sum(row[3] for row in categories)
        if other:
            categories.append(('other', '기타 진로', 'Other paths', other))
    else:
        raise ValueError(f'Unsupported degree: {degree}')
    if denominator < 0 or any(row[3] < 0 for row in categories):
        raise ValueError('Career categories exceed the known-record denominator')
    if sum(row[3] for row in categories) != denominator:
        raise ValueError('Career categories must account for every known record')
    return {
        'denominator': denominator,
        'categories': [
            {'id': key, 'label_ko': ko, 'label_en': en, 'count': count,
             'share': 100 * count / denominator if denominator else 0}
            for key, ko, en, count in categories
        ],
    }


def render_outcome_summary(summary, degree, context):
    t = context['t']
    display = summarize_outcomes(summary, degree)
    title = ('석사 졸업 후 진로', 'Paths after a master’s degree') if degree == 'masters' else ('박사 졸업 후 진로', 'Paths after a doctorate')
    if not display['denominator']:
        return f'<article class="outcome-card" data-outcome-degree="{degree}">{t(*title,"h3")}{t("표시할 진로 정보가 없습니다.","No career information is available yet.","p","outcome-empty")}</article>'
    rows = []
    for category in display['categories']:
        count, share = category['count'], category['share']
        explanation = ''
        if category['id'] == 'other':
            if degree == 'masters':
                explanation = t('진로 준비·취업 예정·창업·기타 취업 등', 'Career preparation, job plans, self-employment & other paths', 'span', 'outcome-category-note')
            else:
                explanation = t('취업·임용 예정, 진로 준비 등', 'Job / appointment plans, career preparation & other paths', 'span', 'outcome-category-note')
        rows.append(f'<tr data-outcome-category="{category["id"]}"><th scope="row">{t(category["label_ko"],category["label_en"])}{explanation}<span class="outcome-track" aria-hidden="true"><span style="width:{share:.5f}%"></span></span></th><td>{t(f"{count:,}명",f"{count:,}")}</td><td>{share:.1f}%</td></tr>')
    table = f'''<table class="outcome-table"><caption>{t('진로 정보가 있는 동문 기준','Among alumni with recorded career information')}</caption><thead><tr><th scope="col">{t('진출 분야','Career path')}</th><th scope="col">{t('인원','Count')}</th><th scope="col">{t('비중','Share')}</th></tr></thead><tbody>{''.join(rows)}</tbody></table>'''
    return f'<article class="outcome-card" data-outcome-degree="{degree}">{t(*title,"h3")}{table}</article>'


def render_outcome_panels(context):
    t, attr = context['t'], context['attr']
    panels = []
    for code in ['all', *[area['code'] for area in context['AREAS']]]:
        group = context['OUTCOMES']['groups'][code]
        area_ko, area_en = ('전체 전공', 'All fields') if code == 'all' else (context['AREA_MAP'][code]['name_ko'], context['AREA_MAP'][code]['name_en'])
        area_label = t(area_ko, area_en, 'h2', 'outcome-field-heading')
        content = ''.join(render_outcome_summary(group[degree], degree, context) for degree in ['masters', 'doctoral'])
        panels.append(f'<section data-outcome-panel="{code}" aria-label="{attr(area_ko + " 진로 통계")}" data-aria-ko="{attr(area_ko + " 진로 통계")}" data-aria-en="{attr(area_en + " career statistics")}"'+(' hidden' if code != 'all' else '')+f'>{area_label}<div class="outcome-grid">{content}</div></section>')
    return ''.join(panels)


def render_alumni_contacts(person, context):
    """Keep usable professional links, omitting missing and explicitly dated email."""
    alumni_link = context['alumni_link']
    links = []
    verification = person.get('profile_verification') or {}
    dated_email = any(person.get(key) or verification.get(key) for key in ['email_note_ko', 'email_note_en'])
    if person.get('email') and not dated_email:
        links.append(alumni_link('mailto:' + person['email'], person['email'], person['email'], person, 'source-link alumni-email'))
    if person.get('profile_url'):
        links.append(alumni_link(person['profile_url'], '대학 프로필 ↗', 'University profile ↗', person))
    if person.get('website_url') and person['website_url'] != person.get('profile_url'):
        links.append(alumni_link(person['website_url'], '개인 홈페이지 ↗', 'Personal website ↗', person))
    return '<div class="alumni-contacts">' + ''.join(links) + '</div>' if links else ''


def render_placements(context):
    t, attr = context['t'], context['attr']
    rows = []
    for alumni in sorted(context['PLACEMENTS']['alumni'], key=lambda row: row['name']):
        name = t(alumni.get('name_ko'), alumni.get('name_en'))
        area = context['AREA_MAP'][alumni['area_code']]
        degree_ko, degree_en = {'PhD': (' · 박사', ' · PhD'), 'MS': (' · 석사', ' · MS')}.get(alumni.get('degree'), ('', ''))
        meta = t(area['name_ko'] + degree_ko, area['name_en'] + degree_en, 'p', 'placement-meta')
        career_labels = {'faculty': ('교수직', 'Faculty'), 'research': ('연구직 · 박사후연구 등', 'Research · Postdoctoral roles'), 'teaching': ('강의 · 겸임 등', 'Teaching · Adjunct roles')}
        if alumni.get('career_group') in career_labels:
            meta += t(*career_labels[alumni['career_group']], 'span', 'career-badge')
        institution = t(alumni.get('institution_ko'), alumni.get('institution_en'))
        if alumni.get('department_ko') or alumni.get('department_en'):
            institution += t(alumni.get('department_ko'), alumni.get('department_en'), 'p', 'placement-department')
        verification = alumni.get('profile_verification') or {}
        position = ''
        if alumni.get('record_basis') == 'administrative':
            institution = t(alumni.get('reported_affiliation_ko') or alumni.get('institution_ko'), alumni.get('reported_affiliation_en') or alumni.get('institution_en'))
        elif verification.get('rank_status') == 'verified' and not verification.get('rank_note_ko') and not verification.get('rank_note_en'):
            position = t(alumni.get('position_ko'), alumni.get('position_en'), 'p', 'placement-role verified-rank')
        if alumni.get('appointment_ko') or alumni.get('appointment_en'):
            position += t(alumni.get('appointment_ko'), alumni.get('appointment_en'), 'p', 'placement-meta')
        contacts = render_alumni_contacts(alumni, context)
        # Search names and affiliations, without exposing internal rank findings.
        search = ' '.join(str(alumni.get(key) or '') for key in ['name', 'name_ko', 'name_en', 'institution_ko', 'institution_en', 'reported_affiliation_ko', 'reported_affiliation_en', 'department_ko', 'department_en']) + ' ' + area['name_ko'] + ' ' + area['name_en']
        rows.append(f'<tr id="{attr(alumni["id"])}" role="row" data-filter-item data-areas="{alumni["area_code"]}" data-search="{attr(search)}"><td role="cell" data-label-ko="성명 · 전공" data-label-en="Name · Field">{name}{meta}</td><td role="cell" data-label-ko="소속 · 경력" data-label-en="Affiliation · Career">{institution}{position}</td><td role="cell" data-label-ko="연락처 · 홈페이지" data-label-en="Contact · Profile">{contacts}</td></tr>')
    return f'''<section class="page-hero"><div class="wrap"><div class="breadcrumb"><a href="index.html">{t('홈','Home')}</a><span>/</span><span>Placements</span></div><div class="page-hero-grid"><div><p class="eyebrow">Careers after KUBS</p>{t('연구를 바탕으로, 더 넓은 진로로.','Research opens new paths.','h1','ko-heading')}</div>{t('석사·박사 졸업 후의 진학, 취업, 학계·연구 경력을 살펴보세요. 전공을 선택하면 해당 전공의 진로와 동문들을 함께 볼 수 있습니다.','Explore further study, employment, and academic and research careers after KUBS. Select a field to discover its career paths and alumni.','p','lede')}</div></div></section>
    <section class="section wrap" data-directory="placements">
    {context['directory_controls']([area['code'] for area in context['AREAS']], 'placements')}
    <div class="outcomes-intro"><p class="eyebrow">Graduate career paths</p>{t('석사·박사 졸업생의 진출 분야','Where our graduates go','h2')}</div>
    <div class="outcome-panels">{render_outcome_panels(context)}</div>
    <section class="academic-section" id="academic-careers"><p class="eyebrow">Academic & research careers</p>{t('학계와 연구 현장의 동문들','Alumni in academia and research','h2')}
    <div class="result-bar" data-filter-controls hidden><span data-result-count role="status" aria-live="polite"></span>{t('국문·영문으로 검색할 수 있습니다.','Search in Korean or English.')}</div>
    <table class="placement-table" role="table"><caption>{t('학계·연구 동문 · 성명 가나다순','Academic and research alumni · Korean name order')}</caption><thead role="rowgroup"><tr role="row"><th scope="col" role="columnheader">{t('성명 · 전공','Name · Field')}</th><th scope="col" role="columnheader">{t('소속 · 경력','Affiliation · Career')}</th><th scope="col" role="columnheader">{t('연락처 · 홈페이지','Contact · Profile')}</th></tr></thead><tbody role="rowgroup">{''.join(rows)}</tbody></table>{context['empty_state']()}</section></section>'''
