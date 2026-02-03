#!/usr/bin/env python3
"""
VIRDY 기획 문서 통합 HTML 생성기
모든 .md 파일을 읽어 페이지 기반 HTML 온보딩 문서로 변환합니다.
"""

import os
import re
from pathlib import Path
from datetime import datetime

# 문서 카테고리 정의
CATEGORIES = {
    "01_Product": {"name": "제품 정의", "icon": "📦"},
    "02_Features": {"name": "핵심 기능", "icon": "⚙️"},
    "03_Operations": {"name": "운영 기획", "icon": "🔒"},
    "04_Design": {"name": "UI/UX", "icon": "🎨"},
    "05_Technical": {"name": "기술 설계", "icon": "🛠️"}
}

# 문서 순서 정의
DOCUMENT_ORDER = [
    "01_Product/01_Product_Overview.md",
    "01_Product/02_User_Flow.md",
    "02_Features/01_Avatar_System.md",
    "02_Features/02_Tracker_System.md",
    "02_Features/03_Camera_System.md",
    "02_Features/04_World_System.md",
    "02_Features/05_Network_System.md",
    "02_Features/06_SDK.md",
    "03_Operations/01_User_Roles.md",
    "03_Operations/02_License_System.md",
    "03_Operations/03_Security.md",
    "03_Operations/04_Data_Lifecycle.md",
    "03_Operations/05_Risk_Management.md",
    "03_Operations/06_Account_System.md",
    "03_Operations/07_Cost_Analysis.md",
    "04_Design/01_UI_Specification.md",
    "05_Technical/01_Architecture.md",
    "05_Technical/02_Development_Status.md"
]


def extract_title(md_content):
    """Markdown 파일에서 제목 추출"""
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip()
    return "제목 없음"


def extract_h2_sections(md_content):
    """Markdown에서 h2 섹션 추출 (TOC 생성용)"""
    sections = []
    lines = md_content.split('\n')
    for line in lines:
        if line.startswith('## '):
            title = line[3:].strip()
            # ID 생성 (특수문자 제거, 공백을 하이픈으로)
            section_id = re.sub(r'[^\w가-힣\s-]', '', title)
            section_id = re.sub(r'\s+', '-', section_id).lower()
            sections.append({'title': title, 'id': section_id})
    return sections


def convert_md_to_html(md_content, add_ids=True):
    """간단한 Markdown → HTML 변환"""
    html = md_content

    # 코드 블록 (```로 둘러싸인 부분)
    html = re.sub(r'```(\w+)?\n(.*?)\n```', r'<pre><code class="\1">\2</code></pre>', html, flags=re.DOTALL)

    # 인용구 제거 (문서 헤더용)
    html = re.sub(r'^>\s*\*\*문서 버전\*\*.*$', '', html, flags=re.MULTILINE)
    html = re.sub(r'^>\s*\*\*최종 수정일\*\*.*$', '', html, flags=re.MULTILINE)
    html = re.sub(r'^>\s*\*\*작성자\*\*.*$', '', html, flags=re.MULTILINE)
    html = re.sub(r'^>\s*$', '', html, flags=re.MULTILINE)

    # 제목 변환
    html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)

    # h2에 ID 추가 (TOC 링크용)
    if add_ids:
        def add_id_to_h2(match):
            title = match.group(1)
            section_id = re.sub(r'[^\w가-힣\s-]', '', title)
            section_id = re.sub(r'\s+', '-', section_id).lower()
            return f'<h2 id="{section_id}">{title}</h2>'
        html = re.sub(r'^## (.+)$', add_id_to_h2, html, flags=re.MULTILINE)
    else:
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)

    html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^#### (.+)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)

    # 표 변환 (간단한 버전)
    def convert_table(match):
        lines = match.group(0).split('\n')
        result = '<table>\n'
        for i, line in enumerate(lines):
            if not line.strip() or '---' in line:
                continue
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            if i == 0:
                result += '<thead><tr>'
                for cell in cells:
                    result += f'<th>{cell}</th>'
                result += '</tr></thead>\n<tbody>\n'
            else:
                result += '<tr>'
                for cell in cells:
                    result += f'<td>{cell}</td>'
                result += '</tr>\n'
        result += '</tbody></table>\n'
        return result

    # 표 패턴 찾기
    table_pattern = r'(\|.+\|[\r\n]+\|[-:\s|]+\|[\r\n]+(?:\|.+\|[\r\n]*)*)'
    html = re.sub(table_pattern, convert_table, html, flags=re.MULTILINE)

    # 볼드/이탤릭
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
    html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)

    # 링크 제거 (내부 문서 링크는 단일 HTML이므로 불필요)
    html = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', html)

    # 리스트
    html = re.sub(r'^\- (.+)$', r'<li>\1</li>', html, flags=re.MULTILINE)
    html = re.sub(r'(<li>.*</li>\n?)+', r'<ul>\g<0></ul>', html, flags=re.DOTALL)

    # 수평선
    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)

    # 줄바꿈
    html = re.sub(r'<br\s*/?>', r'<br>', html)
    html = html.replace('\n\n', '</p><p>')

    # 단락 감싸기
    html = f'<p>{html}</p>'
    html = html.replace('<p><h', '<h').replace('</h1></p>', '</h1>')
    html = html.replace('</h2></p>', '</h2>').replace('</h3></p>', '</h3>')
    html = html.replace('</h4></p>', '</h4>')
    html = html.replace('<p><hr></p>', '<hr>')
    html = html.replace('<p><table>', '<table>').replace('</table></p>', '</table>')
    html = html.replace('<p><ul>', '<ul>').replace('</ul></p>', '</ul>')
    html = html.replace('<p><pre>', '<pre>').replace('</pre></p>', '</pre>')
    html = html.replace('<p></p>', '')

    return html


def generate_html():
    """통합 HTML 생성"""
    base_dir = Path(__file__).parent
    documents = []

    # UPDATES.md 읽기
    updates_content = ""
    updates_path = base_dir / "UPDATES.md"
    if updates_path.exists():
        with open(updates_path, 'r', encoding='utf-8') as f:
            updates_content = f.read()

    # CHANGELOG.md 읽기
    changelog_content = ""
    changelog_path = base_dir / "CHANGELOG.md"
    if changelog_path.exists():
        with open(changelog_path, 'r', encoding='utf-8') as f:
            changelog_content = f.read()

    # 문서 읽기
    for doc_path in DOCUMENT_ORDER:
        full_path = base_dir / doc_path
        if not full_path.exists():
            print(f"[WARN] 파일 없음: {doc_path}")
            continue

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()

        title = extract_title(content)
        h2_sections = extract_h2_sections(content)
        html_content = convert_md_to_html(content, add_ids=True)
        category = doc_path.split('/')[0]

        documents.append({
            'path': doc_path,
            'title': title,
            'content': html_content,
            'category': category,
            'id': doc_path.replace('/', '_').replace('.md', ''),
            'sections': h2_sections
        })
        print(f"[OK] {title}")

    # 좌측 네비게이션 생성
    nav_html = ""

    # 업데이트 섹션 추가
    if updates_content or changelog_content:
        nav_html += '<div class="nav-category">📝 최신 업데이트</div>\n<ul>\n'
        if updates_content:
            nav_html += '<li><a href="#" onclick="showPage(\'updates\'); return false;">최근 4주 업데이트</a></li>\n'
        if changelog_content:
            nav_html += '<li><a href="#" onclick="showPage(\'changelog\'); return false;">전체 변경 이력</a></li>\n'
        nav_html += '</ul>\n'

    current_category = None
    for doc in documents:
        if doc['category'] != current_category:
            if current_category:
                nav_html += "</ul>\n"
            current_category = doc['category']
            cat_info = CATEGORIES.get(current_category, {"name": current_category, "icon": "📄"})
            nav_html += f'<div class="nav-category">{cat_info["icon"]} {cat_info["name"]}</div>\n<ul>\n'

        nav_html += f'<li><a href="#" onclick="showPage(\'{doc["id"]}\'); return false;" id="nav-{doc["id"]}">{doc["title"]}</a></li>\n'

    if current_category:
        nav_html += "</ul>\n"

    # 페이지 콘텐츠 생성
    pages_html = ""

    # 업데이트 페이지
    if updates_content:
        updates_html = convert_md_to_html(updates_content, add_ids=False)
        updates_sections = extract_h2_sections(updates_content)
        pages_html += f'''
        <div class="page-content" id="page-updates">
            <div class="doc-header"><span class="doc-category">📝 최신 업데이트</span></div>
            {updates_html}
        </div>
        '''

    # CHANGELOG 페이지
    if changelog_content:
        changelog_html = convert_md_to_html(changelog_content, add_ids=False)
        changelog_sections = extract_h2_sections(changelog_content)
        pages_html += f'''
        <div class="page-content" id="page-changelog">
            <div class="doc-header"><span class="doc-category">📋 전체 변경 이력</span></div>
            {changelog_html}
        </div>
        '''

    # 각 문서 페이지
    for doc in documents:
        cat_name = CATEGORIES.get(doc["category"], {}).get("name", doc["category"])
        pages_html += f'''
        <div class="page-content" id="page-{doc["id"]}">
            <div class="doc-header"><span class="doc-category">{cat_name}</span></div>
            {doc["content"]}
        </div>
        '''

    # 최종 HTML 조합
    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIRDY 온보딩 문서</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans KR', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}

        .container {{
            display: flex;
            min-height: 100vh;
        }}

        /* 좌측 사이드바 */
        .sidebar {{
            width: 280px;
            background: #2c3e50;
            color: white;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            box-shadow: 2px 0 10px rgba(0,0,0,0.1);
            z-index: 100;
        }}

        .sidebar-header {{
            padding: 30px 20px;
            background: #1a252f;
            border-bottom: 2px solid #34495e;
        }}

        .sidebar-header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
            color: #3498db;
        }}

        .sidebar-header p {{
            font-size: 12px;
            color: #95a5a6;
        }}

        .nav-category {{
            padding: 15px 20px 5px;
            font-weight: bold;
            font-size: 13px;
            color: #ecf0f1;
            text-transform: uppercase;
            margin-top: 10px;
        }}

        .sidebar ul {{
            list-style: none;
            padding: 0 10px 15px;
        }}

        .sidebar li {{
            margin: 0;
        }}

        .sidebar a {{
            display: block;
            padding: 8px 15px;
            color: #bdc3c7;
            text-decoration: none;
            border-radius: 5px;
            transition: all 0.2s;
            font-size: 14px;
        }}

        .sidebar a:hover {{
            background: #34495e;
            color: #fff;
            transform: translateX(5px);
        }}

        .sidebar a.active {{
            background: #3498db;
            color: white;
            font-weight: bold;
        }}

        /* 메인 콘텐츠 영역 */
        .main-wrapper {{
            flex: 1;
            margin-left: 280px;
            display: flex;
        }}

        .main-content {{
            flex: 1;
            padding: 40px;
            max-width: 1000px;
        }}

        /* 우측 TOC */
        .toc {{
            width: 250px;
            position: fixed;
            right: 20px;
            top: 40px;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            max-height: calc(100vh - 80px);
            overflow-y: auto;
        }}

        .toc-title {{
            font-size: 14px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #3498db;
        }}

        .toc ul {{
            list-style: none;
            padding: 0;
        }}

        .toc li {{
            margin: 8px 0;
        }}

        .toc a {{
            color: #555;
            text-decoration: none;
            font-size: 13px;
            display: block;
            padding: 5px 10px;
            border-radius: 4px;
            transition: all 0.2s;
        }}

        .toc a:hover {{
            background: #f0f0f0;
            color: #3498db;
        }}

        /* 페이지 콘텐츠 */
        .page-content {{
            display: none;
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}

        .page-content.active {{
            display: block;
        }}

        .doc-header {{
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #3498db;
        }}

        .doc-category {{
            display: inline-block;
            background: #3498db;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
        }}

        h1 {{
            font-size: 32px;
            margin: 20px 0;
            color: #2c3e50;
        }}

        h2 {{
            font-size: 24px;
            margin: 30px 0 15px;
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            scroll-margin-top: 20px;
        }}

        h3 {{
            font-size: 20px;
            margin: 25px 0 10px;
            color: #555;
        }}

        h4 {{
            font-size: 16px;
            margin: 20px 0 10px;
            color: #666;
        }}

        p {{
            margin: 10px 0;
            color: #555;
        }}

        /* 테이블 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}

        th {{
            background: #34495e;
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: 600;
        }}

        td {{
            padding: 12px;
            border-bottom: 1px solid #ecf0f1;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        /* 코드 */
        code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 13px;
        }}

        pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 15px 0;
        }}

        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}

        /* 리스트 */
        .main-content ul {{
            margin: 15px 0;
            padding-left: 30px;
        }}

        .main-content li {{
            margin: 8px 0;
            color: #555;
        }}

        /* 구분선 */
        hr {{
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }}

        /* 강조 */
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}

        em {{
            color: #555;
        }}

        /* 반응형 */
        @media (max-width: 1400px) {{
            .toc {{
                display: none;
            }}
        }}

        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                position: relative;
                height: auto;
            }}

            .main-wrapper {{
                margin-left: 0;
            }}

            .main-content {{
                padding: 20px;
            }}
        }}
    </style>
    <script>
        // 현재 활성 페이지 추적
        let currentPage = '';
        let documentData = {documents};

        // 페이지 표시 함수
        function showPage(pageId) {{
            // 모든 페이지 숨기기
            const pages = document.querySelectorAll('.page-content');
            pages.forEach(page => page.classList.remove('active'));

            // 선택된 페이지 표시
            const targetPage = document.getElementById('page-' + pageId);
            if (targetPage) {{
                targetPage.classList.add('active');
                currentPage = pageId;

                // 좌측 네비게이션 활성화 표시
                const navLinks = document.querySelectorAll('.sidebar a');
                navLinks.forEach(link => link.classList.remove('active'));
                const activeNav = document.getElementById('nav-' + pageId);
                if (activeNav) {{
                    activeNav.classList.add('active');
                }}

                // TOC 업데이트
                updateTOC(pageId);

                // 페이지 상단으로 스크롤
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
            }}
        }}

        // TOC 업데이트 함수
        function updateTOC(pageId) {{
            const toc = document.getElementById('toc-content');
            if (!toc) return;

            // 현재 페이지의 문서 데이터 찾기
            const docData = documentData.find(doc => doc.id === pageId);

            if (!docData || !docData.sections || docData.sections.length === 0) {{
                toc.innerHTML = '<p style="color: #999; font-size: 12px;">이 페이지에는 섹션이 없습니다.</p>';
                return;
            }}

            // TOC 생성
            let tocHtml = '<ul>';
            docData.sections.forEach(section => {{
                tocHtml += `<li><a href="#${{section.id}}" onclick="scrollToSection('${{section.id}}'); return false;">${{section.title}}</a></li>`;
            }});
            tocHtml += '</ul>';
            toc.innerHTML = tocHtml;
        }}

        // 섹션으로 스크롤
        function scrollToSection(sectionId) {{
            const element = document.getElementById(sectionId);
            if (element) {{
                element.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
            }}
        }}

        // 페이지 로드 시 첫 페이지 표시
        document.addEventListener('DOMContentLoaded', function() {{
            const firstPageId = documentData.length > 0 ? documentData[0].id : 'updates';
            showPage(firstPageId);
        }});
    </script>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>🎬 VIRDY</h1>
                <p>기획 문서 통합본</p>
                <p style="margin-top: 10px; font-size: 11px;">생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
            </div>
            <nav>
                {nav_html}
            </nav>
        </aside>

        <div class="main-wrapper">
            <main class="main-content">
                {pages_html}
            </main>

            <aside class="toc">
                <div class="toc-title">📑 이 페이지</div>
                <div id="toc-content"></div>
            </aside>
        </div>
    </div>
</body>
</html>
"""

    # JavaScript 데이터 생성
    import json
    doc_data = []
    for doc in documents:
        doc_data.append({
            'id': doc['id'],
            'title': doc['title'],
            'sections': doc['sections']
        })

    # updates와 changelog도 추가
    if updates_content:
        doc_data.insert(0, {
            'id': 'updates',
            'title': '최근 4주 업데이트',
            'sections': extract_h2_sections(updates_content)
        })
    if changelog_content:
        insert_pos = 1 if updates_content else 0
        doc_data.insert(insert_pos, {
            'id': 'changelog',
            'title': '전체 변경 이력',
            'sections': extract_h2_sections(changelog_content)
        })

    html_template = html_template.replace('{documents}', json.dumps(doc_data, ensure_ascii=False))

    # HTML 파일 저장
    output_path = base_dir / 'VIRDY_Onboarding.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"\n[SUCCESS] 생성 완료: {output_path}")
    print(f"[INFO] 총 {len(documents)}개 문서 통합")
    return output_path


if __name__ == '__main__':
    generate_html()
