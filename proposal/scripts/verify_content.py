#!/usr/bin/env python3
import os
from docx import Document

def verify():
    project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    doc_path = os.path.join(project_dir, 'proposal.docx')
    pdf_path = os.path.join(project_dir, 'proposal.pdf')
    assets_dir = os.path.join(project_dir, 'assets')
    print('='*60); print('GOVONE PROPOSAL VERIFICATION'); print('='*60)
    
    if not os.path.isfile(doc_path): print(f'❌ proposal.docx not found'); return False
    print(f'✅ proposal.docx ({os.path.getsize(doc_path)/1024:.1f} KB)')
    if os.path.isfile(pdf_path): print(f'✅ proposal.pdf ({os.path.getsize(pdf_path)/1024:.1f} KB)')
    else: print('⚠️ proposal.pdf not found')
    
    doc = Document(doc_path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    print(f'\n📊 Statistics: Paragraphs: {len(doc.paragraphs)}, Tables: {len(doc.tables)}')
    
    print(f'\n📋 Sections Check:')
    all_ok = True
    for keyword, name in [('ĐẶT VẤN ĐỀ','1. Đặt vấn đề'),('GIẢI PHÁP','2. Giải pháp'),('THIẾT KẾ','3. Thiết kế'),('KHẢ THI','4. Tính khả thi'),('ĐỔI MỚI','5. Đổi mới'),('TÁC ĐỘNG','6. Tác động'),('KẾT LUẬN','7. Kết luận')]:
        found = any(keyword.upper() in t.upper() for t in paragraphs)
        if not found: all_ok = False
        print(f'   {"✅" if found else "❌"} Section {name}')
    
    print(f'\n🔍 Key Content Check:')
    for name, keyword in [('Tên "GovOne"','GOVONE'),('Đề tài 6','ĐỀ TÀI 6'),('SmartVoice','SMARTVOICE'),('SmartReader','SMARTREADER'),('eKYC','EKYC'),('SmartVision','SMARTVISION'),('Pain-point PP1','PP1'),('TAM-SAM-SOM','TAM'),('Basic/Pro/Enterprise','BASIC'),('MVP 7 ngày','7 NGÀY'),('Header footer','GOVONE — ĐỘI THI')]:
        found = any(keyword.upper() in t.upper() for t in paragraphs)
        if not found: all_ok = False
        print(f'   {"✅" if found else "❌"} {name}')
    
    print(f'\n🖼️ Assets Check:')
    for asset in ['logo-govone.png','architecture-diagram.png','user-flow-citizen.png','user-flow-officer.png','wireframe-kiosk.png','wireframe-scan.png','wireframe-dashboard.png']:
        path = os.path.join(assets_dir, asset)
        if os.path.isfile(path): print(f'   ✅ {asset} ({os.path.getsize(path)/1024:.1f} KB)')
        else: print(f'   ❌ {asset} MISSING'); all_ok = False
    
    print(f'\n{"="*60}')
    if all_ok: print('🎯 VERIFICATION PASSED! All content complete.')
    else: print('⚠️ VERIFICATION PARTIAL — Some items need attention.')
    return all_ok

if __name__ == '__main__':
    verify()
