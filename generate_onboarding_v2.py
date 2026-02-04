#!/usr/bin/env python3
"""
VIRDY 기획 문서 통합 HTML 생성기 (v2 - 깔끔한 디자인)
모든 .md 파일을 읽어 페이지 기반 HTML 온보딩 문서로 변환합니다.
참조 디자인: VIRDY_사용자흐름_시스템아키텍처_v1.html
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
    "05_Technical/02_Development_Status.md",
    "05_Technical/03_API_Specification.md"
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

    # 인용구(blockquote) 변환
    def convert_blockquotes(text):
        """연속된 인용구를 <blockquote>로 감싸기"""
        lines = text.split('\n')
        result = []
        in_blockquote = False
        blockquote_lines = []

        for line in lines:
            # 인용구인지 확인 (> 로 시작하는 줄)
            quote_match = re.match(r'^>\s*(.*)$', line)

            if quote_match:
                if not in_blockquote:
                    in_blockquote = True
                content = quote_match.group(1).strip()
                if content:  # 빈 인용구가 아닌 경우
                    blockquote_lines.append(content)
            else:
                if in_blockquote:
                    if blockquote_lines:
                        result.append('<blockquote>' + '<br>'.join(blockquote_lines) + '</blockquote>')
                    blockquote_lines = []
                    in_blockquote = False
                result.append(line)

        # 마지막에 인용구가 열려있으면 닫기
        if in_blockquote and blockquote_lines:
            result.append('<blockquote>' + '<br>'.join(blockquote_lines) + '</blockquote>')

        return '\n'.join(result)

    html = convert_blockquotes(html)

    # 리스트 변환 (중첩 리스트 지원)
    def convert_lists(text):
        """연속된 리스트 항목들을 <ul>로 감싸기 (중첩 리스트 지원)"""
        lines = text.split('\n')
        result = []
        list_stack = []  # 현재 열린 리스트들의 들여쓰기 레벨 추적

        for line in lines:
            # 리스트 항목인지 확인 (들여쓰기 + - 로 시작하는 줄)
            list_match = re.match(r'^(\s*)- (.+)$', line)

            if list_match:
                indent = len(list_match.group(1))
                content = list_match.group(2)

                # 들여쓰기 레벨 계산 (2칸 = 1레벨)
                level = indent // 2

                # 현재 레벨보다 깊은 리스트들 닫기
                while list_stack and list_stack[-1] > level:
                    result.append('</ul>')
                    list_stack.pop()

                # 새로운 레벨이면 ul 열기
                if not list_stack or list_stack[-1] < level:
                    result.append('<ul>')
                    list_stack.append(level)

                result.append(f'<li>{content}</li>')
            else:
                # 리스트 항목이 아니면 모든 열린 리스트 닫기
                while list_stack:
                    result.append('</ul>')
                    list_stack.pop()
                result.append(line)

        # 마지막에 열린 리스트들 모두 닫기
        while list_stack:
            result.append('</ul>')
            list_stack.pop()

        return '\n'.join(result)

    html = convert_lists(html)

    # 수평선
    html = re.sub(r'^---$', r'<hr>', html, flags=re.MULTILINE)

    # 줄바꿈 정규화
    html = re.sub(r'<br\s*/?>', r'<br>', html)

    # 블록 요소가 아닌 텍스트를 단락으로 감싸기
    def wrap_paragraphs(text):
        """텍스트를 적절히 <p> 태그로 감싸기"""
        lines = text.split('\n')
        result = []
        paragraph_lines = []

        # 블록 요소 태그들
        block_tags = ['<h1', '<h2', '<h3', '<h4', '<hr', '<table', '</table',
                      '<thead', '</thead', '<tbody', '</tbody', '<tr', '</tr',
                      '<th', '</th', '<td', '</td',
                      '<ul', '</ul', '<li', '</li',
                      '<pre', '</pre', '<code', '</code',
                      '<blockquote', '</blockquote']

        def is_block_line(line):
            stripped = line.strip()
            if not stripped:
                return True  # 빈 줄도 블록으로 처리
            for tag in block_tags:
                if stripped.startswith(tag):
                    return True
            return False

        def flush_paragraph():
            if paragraph_lines:
                content = ' '.join(paragraph_lines)
                if content.strip():
                    result.append(f'<p>{content}</p>')
                paragraph_lines.clear()

        for line in lines:
            stripped = line.strip()

            if is_block_line(line):
                flush_paragraph()
                if stripped:  # 빈 줄이 아니면 추가
                    result.append(line)
            else:
                # 일반 텍스트 줄
                if stripped:
                    paragraph_lines.append(stripped)
                else:
                    flush_paragraph()

        flush_paragraph()
        return '\n'.join(result)

    html = wrap_paragraphs(html)

    # 빈 단락 제거
    html = re.sub(r'<p>\s*</p>', '', html)

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
        nav_html += '<div class="nav-category">📝 최신 업데이트</div>\n<ul class="nav-list">\n'
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
            nav_html += f'<div class="nav-category">{cat_info["icon"]} {cat_info["name"]}</div>\n<ul class="nav-list">\n'

        nav_html += f'<li><a href="#" onclick="showPage(\'{doc["id"]}\'); return false;" id="nav-{doc["id"]}">{doc["title"]}</a></li>\n'

    if current_category:
        nav_html += "</ul>\n"

    # 페이지 콘텐츠 생성
    pages_html = ""

    # 업데이트 페이지
    if updates_content:
        updates_html = convert_md_to_html(updates_content, add_ids=False)
        pages_html += f'''
        <div class="page-content" id="page-updates">
            <div class="section-header">
                <h2>📝 최근 4주 업데이트</h2>
            </div>
            {updates_html}
        </div>
        '''

    # CHANGELOG 페이지
    if changelog_content:
        changelog_html = convert_md_to_html(changelog_content, add_ids=False)
        pages_html += f'''
        <div class="page-content" id="page-changelog">
            <div class="section-header">
                <h2>📋 전체 변경 이력</h2>
            </div>
            {changelog_html}
        </div>
        '''

    # 각 문서 페이지
    for doc in documents:
        cat_info = CATEGORIES.get(doc["category"], {"name": doc["category"], "icon": "📄"})
        pages_html += f'''
        <div class="page-content" id="page-{doc["id"]}">
            <div class="section-header">
                <h2>{cat_info["icon"]} {doc["title"]}</h2>
            </div>
            {doc["content"]}
        </div>
        '''

    # 최종 HTML 조합 (v2 깔끔한 디자인)
    html_template = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VIRDY 기획 문서</title>
    <style>
        @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.7;
            color: #2c3e50;
            background: #f8f9fa;
        }}

        .container {{
            display: flex;
            min-height: 100vh;
        }}

        /* 좌측 사이드바 */
        .sidebar {{
            width: 280px;
            background: linear-gradient(180deg, #1a252f 0%, #2c3e50 100%);
            color: white;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
            z-index: 100;
        }}

        .sidebar-header {{
            padding: 30px 25px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .sidebar-header h1 {{
            font-size: 23px;
            font-weight: 800;
            color: #3498db;
            margin-bottom: 5px;
        }}

        .sidebar-header .subtitle {{
            font-size: 14px;
            color: #95a5a6;
        }}

        .sidebar-header .meta {{
            margin-top: 15px;
            font-size: 12px;
            color: #7f8c8d;
        }}

        /* 검색창 스타일 */
        .search-container {{
            padding: 15px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }}

        .search-input-wrapper {{
            position: relative;
        }}

        .search-input {{
            width: 100%;
            padding: 12px 15px 12px 40px;
            border: none;
            border-radius: 8px;
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 14px;
            outline: none;
            transition: all 0.2s;
        }}

        .search-input::placeholder {{
            color: #95a5a6;
        }}

        .search-input:focus {{
            background: rgba(255,255,255,0.15);
            box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.5);
        }}

        .search-icon {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: #95a5a6;
            font-size: 16px;
        }}

        .search-clear {{
            position: absolute;
            right: 10px;
            top: 50%;
            transform: translateY(-50%);
            background: none;
            border: none;
            color: #95a5a6;
            cursor: pointer;
            font-size: 16px;
            display: none;
        }}

        .search-clear:hover {{
            color: #fff;
        }}

        /* 검색 결과 스타일 */
        .search-results {{
            max-height: 400px;
            overflow-y: auto;
            margin-top: 10px;
            display: none;
        }}

        .search-results.active {{
            display: block;
        }}

        .search-result-item {{
            padding: 12px 15px;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s;
            margin-bottom: 4px;
        }}

        .search-result-item:hover {{
            background: rgba(52, 152, 219, 0.2);
        }}

        .search-result-title {{
            color: #3498db;
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
        }}

        .search-result-preview {{
            color: #bdc3c7;
            font-size: 12px;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .search-result-preview mark {{
            background: rgba(52, 152, 219, 0.4);
            color: white;
            padding: 0 2px;
            border-radius: 2px;
        }}

        .search-no-results {{
            color: #95a5a6;
            font-size: 13px;
            padding: 15px;
            text-align: center;
        }}

        .search-result-count {{
            color: #7f8c8d;
            font-size: 12px;
            padding: 8px 15px;
            border-bottom: 1px solid rgba(255,255,255,0.1);
            margin-bottom: 5px;
        }}

        .nav-category {{
            padding: 18px 25px 8px;
            font-weight: 700;
            font-size: 13px;
            color: #ecf0f1;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .nav-list {{
            list-style: none;
            padding: 0 15px 15px;
        }}

        .nav-list li {{
            margin: 2px 0;
        }}

        .nav-list a {{
            display: block;
            padding: 10px 15px;
            color: #bdc3c7;
            text-decoration: none;
            border-radius: 8px;
            font-size: 15px;
            transition: all 0.2s ease;
        }}

        .nav-list a:hover {{
            background: rgba(52, 152, 219, 0.2);
            color: #fff;
            padding-left: 20px;
        }}

        .nav-list a.active {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            font-weight: 600;
        }}

        /* 메인 콘텐츠 영역 */
        .main-wrapper {{
            flex: 1;
            margin-left: 280px;
            display: flex;
            justify-content: center;
        }}

        .content-area {{
            display: flex;
            width: 100%;
            max-width: 1200px;
            padding: 40px 30px;
            gap: 30px;
        }}

        .main-content {{
            flex: 1;
            min-width: 0;
            max-width: 850px;
        }}

        /* 우측 TOC */
        .toc-wrapper {{
            width: 220px;
            flex-shrink: 0;
        }}

        .toc {{
            position: sticky;
            top: 30px;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            max-height: calc(100vh - 60px);
            overflow-y: auto;
        }}

        .toc-title {{
            font-size: 14px;
            font-weight: 700;
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
            margin: 6px 0;
        }}

        .toc a {{
            color: #7f8c8d;
            text-decoration: none;
            font-size: 14px;
            display: block;
            padding: 6px 10px;
            border-radius: 6px;
            transition: all 0.2s;
        }}

        .toc a:hover {{
            background: #f8f9fa;
            color: #3498db;
        }}

        /* 페이지 콘텐츠 */
        .page-content {{
            display: none;
            background: white;
            padding: 40px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }}

        .page-content.active {{
            display: block;
        }}

        /* 섹션 헤더 */
        .section-header {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 18px 25px;
            border-radius: 10px;
            margin-bottom: 30px;
        }}

        .section-header h2 {{
            font-size: 21px;
            font-weight: 700;
            margin: 0;
            border: none;
            padding: 0;
            color: white;
        }}

        /* 제목 스타일 */
        h1 {{
            font-size: 29px;
            font-weight: 800;
            margin: 25px 0 15px;
            color: #1a252f;
        }}

        h2 {{
            font-size: 21px;
            font-weight: 700;
            margin: 35px 0 15px;
            color: #2c3e50;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            scroll-margin-top: 20px;
        }}

        h3 {{
            font-size: 18px;
            font-weight: 600;
            margin: 28px 0 12px;
            color: #34495e;
        }}

        h4 {{
            font-size: 16px;
            font-weight: 600;
            margin: 22px 0 10px;
            color: #555;
        }}

        p {{
            margin: 12px 0;
            color: #555;
            font-size: 16px;
        }}

        /* 테이블 */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 15px;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 10px rgba(0,0,0,0.06);
        }}

        th {{
            background: #f8f9fa;
            color: #2c3e50;
            padding: 14px 15px;
            text-align: left;
            font-weight: 600;
            border-bottom: 2px solid #e9ecef;
        }}

        td {{
            padding: 13px 15px;
            border-bottom: 1px solid #e9ecef;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        /* 코드 */
        code {{
            background: #f1f2f6;
            padding: 3px 8px;
            border-radius: 5px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 14px;
            color: #e74c3c;
        }}

        pre {{
            background: #1a252f;
            color: #ecf0f1;
            padding: 20px;
            border-radius: 10px;
            overflow-x: auto;
            margin: 20px 0;
            font-size: 14px;
            line-height: 1.5;
        }}

        pre code {{
            background: none;
            color: inherit;
            padding: 0;
        }}

        /* 리스트 */
        ul, ol {{
            margin: 15px 0;
            padding-left: 25px;
        }}

        li {{
            margin: 10px 0;
            color: #555;
            font-size: 15px;
        }}

        /* 중첩 리스트 */
        ul ul, ol ul {{
            margin: 8px 0;
            padding-left: 22px;
        }}

        ul ul li, ol ul li {{
            margin: 6px 0;
            font-size: 14px;
        }}

        /* 구분선 */
        hr {{
            border: none;
            border-top: 2px solid #e9ecef;
            margin: 35px 0;
        }}

        /* 강조 */
        strong {{
            color: #2c3e50;
            font-weight: 600;
        }}

        em {{
            color: #555;
        }}

        /* 인용구 (info-box 스타일) */
        blockquote {{
            background: #e8f4fd;
            border-left: 4px solid #3498db;
            padding: 18px 22px;
            margin: 20px 0;
            border-radius: 0 10px 10px 0;
            font-size: 15px;
        }}

        blockquote strong {{
            color: #2c3e50;
        }}

        /* 뱃지 스타일 (상태 표시용) */
        .badge {{
            display: inline-block;
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: white;
        }}

        /* 반응형 */
        @media (max-width: 1200px) {{
            .toc-wrapper {{
                display: none;
            }}

            .content-area {{
                justify-content: center;
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

            .content-area {{
                padding: 20px 15px;
            }}

            .page-content {{
                padding: 25px 20px;
            }}
        }}

        /* 스크롤바 스타일 */
        ::-webkit-scrollbar {{
            width: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: #f1f1f1;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #c1c1c1;
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #a1a1a1;
        }}

        /* 프린트 스타일 */
        @media print {{
            .sidebar, .toc-wrapper {{
                display: none;
            }}
            .main-wrapper {{
                margin-left: 0;
            }}
            .page-content {{
                box-shadow: none;
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
                const navLinks = document.querySelectorAll('.nav-list a');
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

        // 검색 기능
        let searchTimeout = null;

        function initSearch() {{
            const searchInput = document.getElementById('search-input');
            const searchClear = document.getElementById('search-clear');
            const searchResults = document.getElementById('search-results');

            if (!searchInput) return;

            searchInput.addEventListener('input', function(e) {{
                const query = e.target.value.trim();

                // 클리어 버튼 표시/숨김
                searchClear.style.display = query.length > 0 ? 'block' : 'none';

                // 디바운스 처리
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {{
                    performSearch(query);
                }}, 200);
            }});

            searchClear.addEventListener('click', function() {{
                searchInput.value = '';
                searchClear.style.display = 'none';
                searchResults.classList.remove('active');
                searchResults.innerHTML = '';
            }});

            // ESC 키로 검색 닫기
            searchInput.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    searchInput.value = '';
                    searchClear.style.display = 'none';
                    searchResults.classList.remove('active');
                    searchResults.innerHTML = '';
                    searchInput.blur();
                }}
            }});
        }}

        function performSearch(query) {{
            const searchResults = document.getElementById('search-results');

            if (query.length < 2) {{
                searchResults.classList.remove('active');
                searchResults.innerHTML = '';
                return;
            }}

            const results = [];
            const queryLower = query.toLowerCase();

            documentData.forEach(doc => {{
                const titleMatch = doc.title.toLowerCase().includes(queryLower);
                const textMatch = doc.searchText && doc.searchText.toLowerCase().includes(queryLower);

                if (titleMatch || textMatch) {{
                    let preview = '';
                    let matchIndex = -1;

                    if (doc.searchText) {{
                        matchIndex = doc.searchText.toLowerCase().indexOf(queryLower);
                        if (matchIndex !== -1) {{
                            // 매칭 위치 주변 텍스트 추출
                            const start = Math.max(0, matchIndex - 40);
                            const end = Math.min(doc.searchText.length, matchIndex + query.length + 80);
                            preview = (start > 0 ? '...' : '') +
                                     doc.searchText.substring(start, end) +
                                     (end < doc.searchText.length ? '...' : '');
                        }}
                    }}

                    results.push({{
                        id: doc.id,
                        title: doc.title,
                        preview: preview,
                        titleMatch: titleMatch,
                        query: query
                    }});
                }}
            }});

            displaySearchResults(results, query);
        }}

        function displaySearchResults(results, query) {{
            const searchResults = document.getElementById('search-results');

            if (results.length === 0) {{
                searchResults.innerHTML = '<div class="search-no-results">검색 결과가 없습니다</div>';
                searchResults.classList.add('active');
                return;
            }}

            let html = `<div class="search-result-count">${{results.length}}개 문서에서 발견</div>`;

            results.forEach(result => {{
                // 검색어 하이라이트
                let highlightedPreview = result.preview;
                if (highlightedPreview) {{
                    const regex = new RegExp(`(${{escapeRegExp(query)}})`, 'gi');
                    highlightedPreview = highlightedPreview.replace(regex, '<mark>$1</mark>');
                }}

                html += `
                    <div class="search-result-item" onclick="goToSearchResult('${{result.id}}', '${{escapeHtml(query)}}')">
                        <div class="search-result-title">${{result.title}}</div>
                        ${{highlightedPreview ? `<div class="search-result-preview">${{highlightedPreview}}</div>` : ''}}
                    </div>
                `;
            }});

            searchResults.innerHTML = html;
            searchResults.classList.add('active');
        }}

        function goToSearchResult(pageId, query) {{
            // 검색창 초기화
            const searchInput = document.getElementById('search-input');
            const searchClear = document.getElementById('search-clear');
            const searchResults = document.getElementById('search-results');

            searchInput.value = '';
            searchClear.style.display = 'none';
            searchResults.classList.remove('active');
            searchResults.innerHTML = '';

            // 해당 페이지로 이동
            showPage(pageId);

            // 페이지 내 검색어 하이라이트 (선택적)
            if (query) {{
                setTimeout(() => {{
                    highlightInPage(query);
                }}, 100);
            }}
        }}

        function highlightInPage(query) {{
            // 기존 하이라이트 제거
            const existingHighlights = document.querySelectorAll('.search-highlight');
            existingHighlights.forEach(el => {{
                const parent = el.parentNode;
                parent.replaceChild(document.createTextNode(el.textContent), el);
                parent.normalize();
            }});

            if (!query || query.length < 2) return;

            const activePage = document.querySelector('.page-content.active');
            if (!activePage) return;

            // 텍스트 노드에서 검색어 찾아 하이라이트
            const walker = document.createTreeWalker(
                activePage,
                NodeFilter.SHOW_TEXT,
                null,
                false
            );

            const textNodes = [];
            while (walker.nextNode()) {{
                if (walker.currentNode.nodeValue.toLowerCase().includes(query.toLowerCase())) {{
                    textNodes.push(walker.currentNode);
                }}
            }}

            textNodes.forEach(node => {{
                const text = node.nodeValue;
                const regex = new RegExp(`(${{escapeRegExp(query)}})`, 'gi');
                if (regex.test(text)) {{
                    const span = document.createElement('span');
                    span.innerHTML = text.replace(regex, '<mark class="search-highlight" style="background: #fff3cd; padding: 1px 3px; border-radius: 3px;">$1</mark>');
                    node.parentNode.replaceChild(span, node);
                }}
            }});

            // 첫 번째 하이라이트로 스크롤
            const firstHighlight = activePage.querySelector('.search-highlight');
            if (firstHighlight) {{
                firstHighlight.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            }}
        }}

        function escapeRegExp(string) {{
            return string.replace(/[.*+?^${{}}()|[\\]\\\\]/g, '\\\\$&');
        }}

        function escapeHtml(text) {{
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }}

        // 페이지 로드 시 초기화
        document.addEventListener('DOMContentLoaded', function() {{
            const firstPageId = documentData.length > 0 ? documentData[0].id : 'updates';
            showPage(firstPageId);
            initSearch();
        }});
    </script>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="sidebar-header">
                <h1>🎬 VIRDY</h1>
                <div class="subtitle">기획 문서 통합본</div>
                <div class="meta">
                    생성일: {datetime.now().strftime('%Y-%m-%d %H:%M')}<br>
                    작성: VIRDY Studio
                </div>
            </div>
            <div class="search-container">
                <div class="search-input-wrapper">
                    <span class="search-icon">🔍</span>
                    <input type="text" id="search-input" class="search-input" placeholder="문서 검색..." autocomplete="off">
                    <button id="search-clear" class="search-clear">✕</button>
                </div>
                <div id="search-results" class="search-results"></div>
            </div>
            <nav>
                {nav_html}
            </nav>
        </aside>

        <div class="main-wrapper">
            <div class="content-area">
                <main class="main-content">
                    {pages_html}
                </main>

                <aside class="toc-wrapper">
                    <div class="toc">
                        <div class="toc-title">📑 이 페이지</div>
                        <div id="toc-content"></div>
                    </div>
                </aside>
            </div>
        </div>
    </div>
</body>
</html>
"""

    # JavaScript 데이터 생성 (검색용 텍스트 포함)
    import json
    doc_data = []
    for doc in documents:
        # HTML 태그 제거하여 순수 텍스트 추출
        plain_text = re.sub(r'<[^>]+>', ' ', doc['content'])
        plain_text = re.sub(r'\s+', ' ', plain_text).strip()
        doc_data.append({
            'id': doc['id'],
            'title': doc['title'],
            'sections': doc['sections'],
            'searchText': plain_text[:10000]  # 검색용 텍스트 (용량 제한)
        })

    # updates와 changelog도 추가 (검색용 텍스트 포함)
    if updates_content:
        updates_plain = re.sub(r'<[^>]+>', ' ', convert_md_to_html(updates_content, add_ids=False))
        updates_plain = re.sub(r'\s+', ' ', updates_plain).strip()
        doc_data.insert(0, {
            'id': 'updates',
            'title': '최근 4주 업데이트',
            'sections': extract_h2_sections(updates_content),
            'searchText': updates_plain[:10000]
        })
    if changelog_content:
        changelog_plain = re.sub(r'<[^>]+>', ' ', convert_md_to_html(changelog_content, add_ids=False))
        changelog_plain = re.sub(r'\s+', ' ', changelog_plain).strip()
        insert_pos = 1 if updates_content else 0
        doc_data.insert(insert_pos, {
            'id': 'changelog',
            'title': '전체 변경 이력',
            'sections': extract_h2_sections(changelog_content),
            'searchText': changelog_plain[:10000]
        })

    html_template = html_template.replace('{documents}', json.dumps(doc_data, ensure_ascii=False))

    # HTML 파일 저장
    output_path = base_dir / 'VIRDY_Onboarding_v2.html'
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)

    print(f"\n[SUCCESS] 생성 완료: {output_path}")
    print(f"[INFO] 총 {len(documents)}개 문서 통합")
    return output_path


if __name__ == '__main__':
    generate_html()
