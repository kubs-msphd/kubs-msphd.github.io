# KUBS MS & PhD

Korea University Business School MS & PhD website.

홈 · LSOM · Placement의 국문·영문 프로토타입입니다.

- 홈페이지: https://kubs-msphd.github.io/
- LSOM: https://kubs-msphd.github.io/lsom.html
- Placement: https://kubs-msphd.github.io/placements.html

## 정보 업데이트

| 수정 대상 | 파일 |
|---|---|
| 교수 이름·연구분야·프로필 | `data/faculty.json` |
| 선정 논문 | `data/publications.json` |
| 박사 동문·소속 대학 | `data/placements.json` |
| 본문·공통 레이아웃 | `build.py` |
| 디자인 | `dist/assets/style.css` |
| 사진 | `dist/assets/` |

새 브랜치에서 파일을 수정하고 PR로 검토한 뒤 main에 병합하면 GitHub Actions가 `python3 build.py`를 실행하여 홈페이지를 게시합니다. 로컬 생성에는 Python 표준 라이브러리만 필요합니다. 국문·영문 텍스트를 함께 수정해 주세요.

## GitHub Pages 설정

저장소 **Settings → Pages → Build and deployment → Source**는 **GitHub Actions**로 설정합니다. 게시 대상은 `dist` 폴더입니다. `Deploy from a branch`로 두면 README가 있는 저장소 루트가 별도로 게시되어 홈페이지를 덮어쓸 수 있습니다.

수동 재게시: Actions → Deploy GitHub Pages → Run workflow → main.

## 공동관리

구성원은 각자의 GitHub 계정으로 로그인합니다. Organization의 장기 운영 책임자 2명 이상을 Owner로 두고, 콘텐츠 담당자는 저장소 Write 권한으로 초대하는 구성을 권장합니다. 별도의 홈페이지 관리자 로그인 화면은 현재 없습니다.

## 자료 기준

- LSOM 교수 11명: 2026-09-06 KUBS 공식 전임교수 명단. 연구 키워드는 공개 프로필·논문을 요약했습니다.
- 선정 논문 3편: 출판사 원문 링크와 온라인 선게재·권호 연도를 구분했습니다.
- LSOM 박사 동문 14명: 프로그램 책임자 제공 명단. 소속은 최초 임용 대학으로 간주하지 않습니다. 졸업연도·최초 임용 기관의 미확인 값은 null로 보존합니다.
- 전화번호·학회 직책은 포함하지 않습니다. 미확인 영문 이름과 경력은 추정하지 않습니다.
- 모집요강·장학·학사규정은 공식 대학원 사이트로 연결합니다.

프로토타입 안내와 `noindex`를 유지하고 있습니다. 검색 제외 요청은 접근 제한 기능이 아니며, GitHub Pages와 이 저장소는 공개 상태입니다.

## 이미지 출처

- 캠퍼스: https://biz.korea.ac.kr/introduce/lg_posco_campus.html
- 캠퍼스 사진 원본: https://biz.korea.ac.kr/ft_board/upload/bbs_kubs_photo/image/20250415100451365209.JPG
- 교수 사진: https://biz.korea.ac.kr/professor/professor_list1.html?major=M06
- 각 교수 사진 원본 URL은 `data/faculty.json`에 보존되어 있습니다. 이미지 저작권은 원 소유자에게 있으며 별도 재사용 라이선스를 부여하지 않습니다.
