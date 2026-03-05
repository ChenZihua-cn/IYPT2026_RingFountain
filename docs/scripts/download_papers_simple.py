#!/usr/bin/env python3
"""
简化版论文下载脚本
"""

import urllib.request
import os
import ssl

PAPERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'papers')
os.makedirs(PAPERS_DIR, exist_ok=True)

# 禁用SSL验证（某些网络环境需要）
ssl._create_default_https_context = ssl._create_unverified_context

# 论文列表
PAPERS_TO_DOWNLOAD = [
    {
        'title': 'Impacting spheres: from liquid drops to elastic beads',
        'arxiv_id': '2510.24855',
        'filename': 'Jana_etal_2025_Impacting_spheres.pdf'
    },
]

def download_arxiv(arxiv_id, filename):
    """从arXiv下载PDF"""
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    filepath = os.path.join(PAPERS_DIR, filename)
    
    try:
        print(f"下载: {filename}")
        print(f"URL: {url}")
        
        # 添加headers
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        file_size = os.path.getsize(filepath) / 1024
        print(f"✅ 成功: {filename} ({file_size:.1f} KB)\n")
        return True
        
    except Exception as e:
        print(f"❌ 失败: {e}\n")
        return False

def main():
    print("=" * 50)
    print("论文下载工具")
    print("=" * 50)
    
    downloaded = []
    failed = []
    
    for paper in PAPERS_TO_DOWNLOAD:
        success = download_arxiv(paper['arxiv_id'], paper['filename'])
        if success:
            downloaded.append(paper['filename'])
        else:
            failed.append(paper['filename'])
    
    # 显示结果
    print("\n" + "=" * 50)
    print("下载结果:")
    print("=" * 50)
    
    if downloaded:
        print(f"\n✅ 成功 ({len(downloaded)}):")
        for f in downloaded:
            print(f"  - {f}")
    
    if failed:
        print(f"\n❌ 失败 ({len(failed)}):")
        for f in failed:
            print(f"  - {f}")
    
    # 列出所有PDF
    print(f"\n📁 papers目录内容:")
    pdf_files = [f for f in os.listdir(PAPERS_DIR) if f.endswith('.pdf')]
    if pdf_files:
        for f in pdf_files:
            size = os.path.getsize(os.path.join(PAPERS_DIR, f)) / 1024
            print(f"  - {f} ({size:.1f} KB)")
    else:
        print("  (空)")

if __name__ == "__main__":
    main()