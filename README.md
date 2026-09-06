# KUBS MS & PhD

Korea University Business School MS & PhD website.

전공별 교수진, 연구분야와 졸업생 진로를 소개하는 국문·영문 사이트입니다.

- 홈페이지: https://kubs-msphd.github.io/
- 전공별 교수진: https://kubs-msphd.github.io/faculty.html
- LSOM: https://kubs-msphd.github.io/lsom.html
- Placement: https://kubs-msphd.github.io/placements.html

## 정보 업데이트

| 수정 대상 | 파일 |
|---|---|
| 교수 이름·연구분야·프로필 | `data/faculty.json` |
| 전공 이름·코드 | `data/areas.json` |
| 선정 논문 | `data/publications.json` |
| 동문·소속·직위·출처 | `data/placements.json` |
| 본문·공통 레이아웃 | `build.py` |
| 디자인 | `dist/assets/style.css` |
| 사진 | `dist/assets/` |

새 브랜치에서 파일을 수정하고 PR로 검토한 뒤 main에 병합하면 GitHub Actions가 `python3 build.py`를 실행하여 홈페이지를 게시합니다. 로컬 생성에는 Python 표준 라이브러리만 필요합니다. 국문·영문 텍스트를 함께 수정해 주세요.

교수진의 `id`는 유지하고 `area_codes`에 해당 전공을 모두 넣습니다. 복수 전공 교수는 한 레코드로 관리합니다. 사진은 로컬 파일 또는 공식 사진 URL을 사용할 수 있으며, 없는 사진·프로필·연구분야는 `null`로 둡니다. LSOM 연구 페이지와 전공 검색 결과는 같은 데이터를 사용합니다.

Placement는 각 동문의 `area_code`, `source_id`, `source_url`과 출처별 설명을 함께 수정합니다. `institution_ko/en`은 **출처에 기재된 소속**이며, 이를 최신 소속이나 최초 임용기관으로 해석하지 않습니다. 확인되지 않은 `degree`, `graduation_year`, `first_placement`, `current_affiliation`은 `null`로 유지합니다. 출처가 제공하지 않는 영문 성명은 임의로 만들지 않습니다.

필터 결과는 `faculty.html?area=M06` 또는 `placements.html?area=M07`처럼 공유할 수 있습니다. 이름·키워드 검색은 `q`, 언어는 `lang=ko` 또는 `lang=en`에 저장됩니다. JavaScript가 없어도 전체 목록과 메뉴는 표시됩니다.

## GitHub Pages 설정

저장소 **Settings → Pages → Build and deployment → Source**는 **GitHub Actions**로 설정합니다. 게시 대상은 `dist` 폴더입니다. `Deploy from a branch`로 두면 README가 있는 저장소 루트가 별도로 게시되어 홈페이지를 덮어쓸 수 있습니다.

수동 재게시: Actions → Deploy GitHub Pages → Run workflow → main.

## 공동관리

구성원은 각자의 GitHub 계정으로 로그인합니다. Organization의 장기 운영 책임자 2명 이상을 Owner로 두고, 콘텐츠 담당자는 저장소 Write 권한으로 초대하는 구성을 권장합니다. 별도의 홈페이지 관리자 로그인 화면은 현재 없습니다.

## 자료 기준

- 교수진 96명: 2026-09-06 [국문](https://biz.korea.ac.kr/professor/professor_list1.html)·[영문](https://biz.korea.ac.kr/eng/professor/professor_list1.html) 전임교수 목록의 전체 페이지와 9개 전공 필터를 대조했습니다. 원문 97개 항목 중 노인준 교수의 중복을 통합했으며, 13명은 복수 전공입니다. 공식 명단에서 전공이 미표기된 베티 청 교수는 전체 목록에 포함합니다. 전공별 수를 단순 합산하면 중복이 생깁니다.
- 전공별 교수 수: 경영관리 9, GB 8, 마케팅 15, 재무금융 16, 전략 13, 회계학 13, IS 10, LSOM 11, BA 13. BA는 공식 소개상 1년 석사과정으로, 박사 전공과 별도로 안내합니다.
- 이름·직위·연구분야는 공식 국문·영문 표기를 사용합니다. 일부 LSOM 연구 소개는 이전에 확인한 공개 프로필·논문 요약을 보존했습니다. 공식 프로필 링크가 없는 박지호·천동욱·최재은 교수는 공식 목록으로 연결하며, 사진이 없는 박지호 교수는 이미지 대체 표시를 사용합니다.
- 선정 논문 3편: 출판사 원문 링크와 온라인 선게재·권호 연도를 구분했습니다.
- LSOM 박사 동문 14명: 프로그램 책임자 제공 명단. 소속은 최초 임용 대학으로 간주하지 않습니다. 졸업연도·최초 임용 기관의 미확인 값은 null로 보존합니다.
- IS 27명: [전공 Placement 페이지](https://sites.google.com/korea.ac.kr/mis/placement). 학위·졸업연도·최초/현재 소속 구분은 원문에 없습니다.
- GB 16명: [전공 Job placement 페이지](https://sites.google.com/view/kubsib/job-placement-%EC%A1%B8%EC%97%85%EC%83%9D-%EC%B7%A8%EC%97%85-%ED%98%84%ED%99%A9). 교수직 15명과 박사후연구원 1명이며, 학위·졸업연도·최초/현재 소속 구분은 원문에 없습니다.
- 수록 동문은 총 57명입니다. 기관명과 직위는 출처의 표기를 유지하며, 자료 수집일은 소속 확인일을 뜻하지 않습니다. 상세 출처는 실제 페이지에도 표시합니다.
- 전화번호·학회 직책은 포함하지 않습니다. 미확인 영문 이름과 경력은 추정하지 않습니다.
- 모집요강·장학·학사규정은 공식 대학원 사이트로 연결합니다.

페이지별 설명·대표 이미지·canonical URL, `robots.txt`, `sitemap.xml`을 제공합니다. 검색엔진 반영 시점은 검색엔진에 따라 달라집니다.

## 이미지 출처

- 캠퍼스: https://biz.korea.ac.kr/introduce/lg_posco_campus.html
- 캠퍼스 사진 원본: https://biz.korea.ac.kr/ft_board/upload/bbs_kubs_photo/image/20250415100451365209.JPG
- 교수 사진: https://biz.korea.ac.kr/professor/professor_list1.html
- 기존 LSOM 사진은 로컬 파일을 유지하고, 추가 교수 사진은 KUBS 공식 URL에서 불러옵니다. 95개 원본 URL의 HTTP 응답과 이미지 형식을 확인했습니다. 공식 사이트에서 사진 주소가 변경되면 `photo`와 `photo_source`를 함께 갱신합니다.
- 각 교수 사진 원본 URL은 `data/faculty.json`에 보존되어 있습니다. 이미지 저작권은 원 소유자에게 있으며 별도 재사용 라이선스를 부여하지 않습니다.
