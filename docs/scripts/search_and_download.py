#!/usr/bin/env python3
"""
搜索并下载更多相关论文
"""

import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import os
import ssl

PAPERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'papers')
os.makedirs(PAPERS_DIR, exist_ok=True)

ssl._create_default_https_context = ssl._create_unverified_context

# 搜索关键词
SEARCH_QUERIES = [
    'water entry',
    'cavity collapse',
    'Worthington jet',
    'impact water',
    'bubble dynamics',
]

def search_arxiv(query, max_results=5):
    """搜索arXiv论文"""
    encoded_query = urllib.parse.quote(query)
    url = f"http://export.arxiv.org/api/query?search_query=all:{encoded_query}&max_results={max_results}&sortBy=relevance"
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            data = response.read()
        
        # 解析XML
        root = ET.fromstring(data)
        
        # 定义命名空间
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'arxiv': 'http://arxiv.org/schemas/atom'
        }
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            title = entry.find('atom:title', ns).text.strip()
            summary = entry.find('atom:summary', ns).text.strip()
            
            # 获取arXiv ID
            id_elem = entry.find('atom:id', ns)
            arxiv_url = id_elem.text.strip()
            arxiv_id = arxiv_url.split('/abs/')[-1]
            
            # 获取作者
            authors = []
            for author in entry.findall('atom:author', ns):
                name = author.find('atom:name', ns).text
                authors.append(name)
            
            papers.append({
                'title': title,
                'arxiv_id': arxiv_id,
                'authors': authors,
                'summary': summary[:200] + '...' if len(summary) > 200 else summary
            })
        
        return papers
        
    except Exception as e:
        print(f"搜索出错: {e}")
        return []

def download_paper(arxiv_id, filename):
    """下载论文"""
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    filepath = os.path.join(PAPERS_DIR, filename)
    
    if os.path.exists(filepath):
        return True, 'exists'
    
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        return True, 'downloaded'
    except:
        return False, 'failed'

def main():
    print("=" * 60)
    print("arXiv论文搜索工具")
    print("=" * 60)
    
    all_papers = []
    
    for query in SEARCH_QUERIES:
        print(f"\n搜索: '{query}'")
        papers = search_arxiv(query, max_results=3)
        
        if papers:
            print(f"  找到 {len(papers)} 篇论文")
            for i, p in enumerate(papers, 1):
                print(f"\n  [{i}] {p['title']}")
                print(f"      作者: {', '.join(p['authors'][:2])}{'...' if len(p['authors']) > 2 else ''}")
                print(f"      arXiv: {p['arxiv_id']}")
            all_papers.extend(papers)
        else:
            print("  未找到论文")
    
    # 去重
    seen_ids = set()
    unique_papers = []
    for p in all_papers:
        if p['arxiv_id'] not in seen_ids:
            seen_ids.add(p['arxiv_id'])
            unique_papers.append(p)
    
    print(f"\n{'='*60}")
    print(f"共找到 {len(unique_papers)} 篇不重复论文")
    print("="*60)
    
    # 保存搜索结果
    search_results_file = os.path.join(PAPERS_DIR, 'search_results.txt')
    with open(search_results_file, 'w', encoding='utf-8') as f:
        f.write("arXiv搜索结果\n")
        f.write("=" * 60 + "\n\n")
        
        for p in unique_papers:
            f.write(f"标题: {p['title']}\n")
            f.write(f"作者: {', '.join(p['authors'])}\n")
            f.write(f"arXiv: {p['arxiv_id']}\n")
            f.write(f"URL: https://arxiv.org/abs/{p['arxiv_id']}\n")
            f.write(f"摘要: {p['summary']}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"\n📝 搜索结果已保存: search_results.txt")
    print(f"   位置: {search_results_file}")

if __name__ == "__main__":
    main()