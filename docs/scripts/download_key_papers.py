#!/usr/bin/env python3
"""
下载关键相关论文
"""

import urllib.request
import os
import ssl

PAPERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'papers')
os.makedirs(PAPERS_DIR, exist_ok=True)

ssl._create_default_https_context = ssl._create_unverified_context

# 关键论文列表 - 从搜索结果中筛选
KEY_PAPERS = [
    {
        'title': 'Dynamics of Water Entry',
        'arxiv_id': '0810.1888',
        'filename': 'Truscott_Aristoff_2008_Dynamics_of_Water_Entry.pdf',
        'note': '水入射动力学经典研究'
    },
    {
        'title': 'Elastocapillary Worthington jets',
        'arxiv_id': '2207.07928',
        'filename': 'Sen_etal_2022_Elastocapillary_Worthington_jets.pdf',
        'note': 'Worthington喷射的最新研究'
    },
    {
        'title': 'Generation and Breakup of Worthington Jets After Cavity Collapse',
        'arxiv_id': '0907.5154',
        'filename': 'Gekle_Gordillo_2009_Worthington_Jets.pdf',
        'note': '空腔坍缩后的Worthington喷射'
    },
]

def download_arxiv(arxiv_id, filename):
    """从arXiv下载PDF"""
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    filepath = os.path.join(PAPERS_DIR, filename)
    
    if os.path.exists(filepath):
        size = os.path.getsize(filepath) / 1024
        print(f"⏭️  已存在: {filename} ({size:.1f} KB)")
        return True, 'exists'
    
    try:
        print(f"📥 下载: {filename}")
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        with urllib.request.urlopen(req, timeout=30) as response:
            with open(filepath, 'wb') as f:
                f.write(response.read())
        
        file_size = os.path.getsize(filepath) / 1024
        print(f"   ✅ 成功 ({file_size:.1f} KB)")
        return True, 'downloaded'
        
    except Exception as e:
        print(f"   ❌ 失败: {e}")
        return False, 'failed'

def main():
    print("=" * 60)
    print("下载关键相关论文")
    print("=" * 60)
    
    results = {'downloaded': [], 'exists': [], 'failed': []}
    
    for i, paper in enumerate(KEY_PAPERS, 1):
        print(f"\n[{i}/{len(KEY_PAPERS)}] {paper['title']}")
        print(f"     备注: {paper['note']}")
        
        success, status = download_arxiv(paper['arxiv_id'], paper['filename'])
        results[status].append(paper)
    
    # 统计
    print("\n" + "=" * 60)
    print("下载统计")
    print("=" * 60)
    print(f"✅ 新下载: {len(results['downloaded'])}")
    print(f"⏭️  已存在: {len(results['exists'])}")
    print(f"❌ 失败: {len(results['failed'])}")
    
    # 列出所有PDF
    print(f"\n📁 papers目录中的PDF文件:")
    pdf_files = sorted([f for f in os.listdir(PAPERS_DIR) if f.endswith('.pdf')])
    for i, f in enumerate(pdf_files, 1):
        size = os.path.getsize(os.path.join(PAPERS_DIR, f)) / 1024
        print(f"   {i}. {f} ({size:.1f} KB)")
    
    print(f"\n总计: {len(pdf_files)} 篇论文")

if __name__ == "__main__":
    main()