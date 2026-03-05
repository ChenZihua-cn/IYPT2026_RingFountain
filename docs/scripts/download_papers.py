#!/usr/bin/env python3
"""
论文下载脚本 - 下载IYPT 2026 Ring Fountain相关论文
"""

import os
import sys
import requests
import time

# 配置
PAPERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'papers')
os.makedirs(PAPERS_DIR, exist_ok=True)

# 论文列表：标题, arXiv ID, 下载URL
PAPERS = [
    # 最新相关论文 - Wagner理论应用
    {
        'title': 'Impacting spheres: from liquid drops to elastic beads',
        'arxiv_id': '2510.24855v3',
        'url': 'https://arxiv.org/pdf/2510.24855v3.pdf',
        'filename': 'Jana_etal_2025_Impacting_spheres.pdf'
    },
    # 可添加更多论文
]

def download_paper(url, filename):
    """下载论文PDF文件"""
    try:
        print(f"正在下载: {filename}")
        print(f"URL: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=60)
        
        if response.status_code == 200:
            filepath = os.path.join(PAPERS_DIR, filename)
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            file_size = os.path.getsize(filepath) / 1024
            print(f"✅ 下载成功: {filename} ({file_size:.1f} KB)")
            return True
        else:
            print(f"❌ 下载失败: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 下载出错: {e}")
        return False

def download_from_arxiv(arxiv_id, filename=None):
    """通过arXiv ID下载论文"""
    if filename is None:
        filename = f"{arxiv_id}.pdf"
    
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    return download_paper(url, filename)

def search_arxiv(query, max_results=5):
    """搜索arXiv论文"""
    print(f"\n搜索arXiv: {query}")
    url = f"http://export.arxiv.org/api/query?search_query={query}&max_results={max_results}"
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # 简单解析XML
            content = response.text
            # 提取条目
            entries = []
            lines = content.split('\n')
            for i, line in enumerate(lines):
                if '<entry>' in line:
                    entry = {}
                    # 提取标题
                    for j in range(i, min(i+20, len(lines))):
                        if '<title>' in lines[j] and '</title>' in lines[j]:
                            title = lines[j].replace('<title>', '').replace('</title>', '').strip()
                            # 跳过查询标题
                            if 'arXiv Query' not in title:
                                entry['title'] = title
                        if '<id>' in lines[j] and 'arxiv.org/abs/' in lines[j]:
                            arxiv_id = lines[j].split('/abs/')[-1].replace('</id>', '').strip()
                            entry['arxiv_id'] = arxiv_id
                        if '<summary>' in lines[j]:
                            summary = lines[j].replace('<summary>', '').replace('</summary>', '').strip()
                            entry['summary'] = summary
                    
                    if 'title' in entry and 'arxiv_id' in entry:
                        entries.append(entry)
            
            print(f"找到 {len(entries)} 篇论文:")
            for i, entry in enumerate(entries):
                print(f"\n{i+1}. {entry['title']}")
                print(f"   arXiv: {entry['arxiv_id']}")
                if 'summary' in entry:
                    summary_preview = entry['summary'][:100] + '...' if len(entry['summary']) > 100 else entry['summary']
                    print(f"   摘要: {summary_preview}")
            
            return entries
        else:
            print(f"搜索失败: HTTP {response.status_code}")
            return []
    except Exception as e:
        print(f"搜索出错: {e}")
        return []

def main():
    """主函数"""
    print("=" * 60)
    print("IYPT 2026 Ring Fountain - 论文下载工具")
    print("=" * 60)
    
    # 1. 下载预设论文
    print("\n1. 下载预设论文列表:")
    for paper in PAPERS:
        print(f"\n- {paper['title']}")
        success = download_paper(paper['url'], paper['filename'])
        if not success:
            # 尝试使用arXiv ID下载
            if 'arxiv_id' in paper:
                success = download_from_arxiv(paper['arxiv_id'], paper['filename'])
    
    # 2. 搜索相关论文
    print("\n2. 搜索相关论文:")
    search_queries = [
        'water entry ring fountain',
        'annular object impact water',
        'Worthington jet ring',
        'cavity collapse annular geometry',
    ]
    
    for query in search_queries:
        entries = search_arxiv(query, max_results=3)
        
        # 询问是否下载
        if entries:
            # 暂时只下载第一篇
            entry = entries[0]
            filename = f"{entry['arxiv_id'].replace('/', '_')}.pdf"
            
            download_choice = input(f"\n下载 '{entry['title'][:50]}...'? (y/n): ")
            if download_choice.lower() == 'y':
                download_from_arxiv(entry['arxiv_id'], filename)
        
        time.sleep(2)  # 避免请求过快
    
    # 3. 列出已下载论文
    print("\n3. 已下载论文列表:")
    if os.path.exists(PAPERS_DIR):
        pdf_files = [f for f in os.listdir(PAPERS_DIR) if f.lower().endswith('.pdf')]
        if pdf_files:
            for i, f in enumerate(pdf_files):
                size = os.path.getsize(os.path.join(PAPERS_DIR, f)) / 1024
                print(f"  {i+1}. {f} ({size:.1f} KB)")
        else:
            print("  暂无PDF文件")
    else:
        print("  papers目录不存在")
    
    print("\n✅ 下载完成!")
    print(f"论文保存位置: {PAPERS_DIR}")

if __name__ == "__main__":
    main()