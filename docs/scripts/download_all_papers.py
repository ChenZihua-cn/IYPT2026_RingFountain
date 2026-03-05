#!/usr/bin/env python3
"""
下载所有相关论文
"""

import urllib.request
import os
import ssl

PAPERS_DIR = os.path.join(os.path.dirname(__file__), '..', 'papers')
os.makedirs(PAPERS_DIR, exist_ok=True)

ssl._create_default_https_context = ssl._create_unverified_context

# 扩展论文列表 - 搜索到的相关论文
PAPERS_LIST = [
    # 已确认的论文
    {
        'title': 'Impacting spheres: from liquid drops to elastic beads',
        'arxiv_id': '2510.24855',
        'filename': 'Jana_etal_2025_Impacting_spheres.pdf',
        'note': '最新研究，涉及Wagner和Hertz标度'
    },
    
    # 水冲击相关论文
    {
        'title': 'Water entry of small hydrophobic spheres',
        'arxiv_id': '0804.1385',
        'filename': 'Aristoff_etal_2008_Water_entry_spheres.pdf',
        'note': '经典的水入射研究'
    },
    {
        'title': 'Water entry of spinning spheres',
        'arxiv_id': '1203.2484',
        'filename': 'Truscott_etal_2012_Spinning_spheres.pdf',
        'note': '旋转球体入水'
    },
    {
        'title': 'Cavity formation in the wake of falling objects',
        'arxiv_id': '0908.3043',
        'filename': 'Bergmann_etal_2009_Cavity_formation.pdf',
        'note': '空腔形成动力学'
    },
    {
        'title': 'On the shape of giant soap bubbles',
        'arxiv_id': '1201.1952',
        'filename': 'Cohen_2012_Soap_bubbles.pdf',
        'note': '表面张力相关'
    },
]

def download_arxiv(arxiv_id, filename):
    """从arXiv下载PDF"""
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    filepath = os.path.join(PAPERS_DIR, filename)
    
    # 检查是否已存在
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
    print("IYPT 2026 Ring Fountain - 批量论文下载")
    print("=" * 60)
    
    results = {'downloaded': [], 'exists': [], 'failed': []}
    
    for i, paper in enumerate(PAPERS_LIST, 1):
        print(f"\n[{i}/{len(PAPERS_LIST)}] {paper['title']}")
        print(f"     备注: {paper['note']}")
        
        success, status = download_arxiv(paper['arxiv_id'], paper['filename'])
        results[status].append(paper)
    
    # 统计结果
    print("\n" + "=" * 60)
    print("下载统计")
    print("=" * 60)
    print(f"✅ 新下载: {len(results['downloaded'])}")
    print(f"⏭️  已存在: {len(results['exists'])}")
    print(f"❌ 失败: {len(results['failed'])}")
    
    # 列出所有PDF
    print(f"\n📁 papers目录内容:")
    pdf_files = sorted([f for f in os.listdir(PAPERS_DIR) if f.endswith('.pdf')])
    if pdf_files:
        for f in pdf_files:
            size = os.path.getsize(os.path.join(PAPERS_DIR, f)) / 1024
            print(f"   - {f} ({size:.1f} KB)")
    else:
        print("   (空)")
    
    # 保存下载记录
    log_file = os.path.join(PAPERS_DIR, 'download_log.txt')
    with open(log_file, 'w', encoding='utf-8') as f:
        f.write("IYPT 2026 Ring Fountain - 论文下载记录\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"总论文数: {len(PAPERS_LIST)}\n")
        f.write(f"成功下载: {len(results['downloaded'])}\n")
        f.write(f"已存在: {len(results['exists'])}\n")
        f.write(f"失败: {len(results['failed'])}\n\n")
        
        f.write("论文列表:\n")
        for p in PAPERS_LIST:
            f.write(f"\n- {p['title']}\n")
            f.write(f"  arXiv: {p['arxiv_id']}\n")
            f.write(f"  文件: {p['filename']}\n")
            f.write(f"  备注: {p['note']}\n")
    
    print(f"\n📝 下载记录已保存: download_log.txt")

if __name__ == "__main__":
    main()