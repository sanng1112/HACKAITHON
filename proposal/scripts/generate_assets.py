#!/usr/bin/env python3
"""Generate all GovOne image assets: architecture diagram, wireframes, user flows."""
import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def get_font(size, bold=False):
    try: return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)
    except: return ImageFont.load_default()


def create_architecture_diagram():
    W, H = 1600, 1000
    img = Image.new('RGB', (W, H), 'white')
    draw = ImageDraw.Draw(img)
    COLORS = {'user': ('#4CAF50','#E8F5E9'),'ai': ('#2196F3','#E3F2FD'),'process': ('#FF9800','#FFF3E0'),'data': ('#9C27B0','#F3E5F5')}
    f_title = get_font(24, bold=True); f_layer = get_font(16, bold=True); f_item = get_font(13)
    draw.text((W//2-250, 15), 'KIẾN TRÚC TỔNG THỂ GOVONE', fill='#0066CC', font=f_title)
    layers = [
        (80,100,1440,150,'TẦNG 1 — USER LAYER','user',[
            'Kiosk Touchscreen\n(Voice-first)','Web App\n(React/Next.js)','Mobile App\n(React Native)']),
        (80,280,1440,300,'TẦNG 2 — AI CORE (VNPT APIs)','ai',[
            'SmartVoice\nSTT / TTS','Smartbot\nNLP / Intent','SmartReader\nOCR / Doc AI','eKYC\nOCR/Compare/Liveness','SmartVision\nClassification/Face/Sentiment']),
        (80,610,1440,140,'TẦNG 3 — PROCESSING LAYER','process',[
            'Voice Gateway\n+ Load Balancer','Intent Engine\n+ Dialog Manager','Document Processor\n+ Rules Engine','Sentiment Analyzer\n+ Report Generator']),
        (80,780,1440,140,'TẦNG 4 — DATA LAYER','data',[
            'PostgreSQL\n(Giao dịch + Hồ sơ)','Redis\n(Cache + Session)','MinIO / S3\n(Scan gốc)','Knowledge Base\n(Thủ tục HC)'])]
    for x,y,w,h,title,key,items in layers:
        bg,border = COLORS[key]
        draw.rounded_rectangle([x,y,x+w,y+h], radius=10, fill=bg, outline=border, width=2)
        draw.rounded_rectangle([x,y,x+w,y+35], radius=10, fill=border)
        draw.rectangle([x,y+20,x+w,y+35], fill=border)
        draw.text((x+15,y+8), title, fill='white', font=f_layer)
        n = len(items)
        for i,item in enumerate(items):
            ix = x+15+i*min(280,(w-30)//n); iy = y+50; iw = min(270,(w-30)//n-10)
            ih = 90 if key=='ai' else 70
            draw.rounded_rectangle([ix,iy,ix+iw,iy+ih], radius=6, fill='white', outline=border, width=1)
            for li,line in enumerate(item.split('\n')):
                lb = draw.textbbox((0,0),line,font=f_item); lw = lb[2]-lb[0]
                draw.text((ix+(iw-lw)//2, iy+8+li*18), line, fill='#333333', font=f_item)
        if key != 'data':
            ay = y+h; draw.line([(W//2,ay),(W//2,ay+20)], fill="#666", width=2)
            draw.polygon([(W//2-8,ay+20),(W//2+8,ay+20),(W//2,ay+30)], fill="#666")
    img.save(os.path.join(ASSETS_DIR,'architecture-diagram.png')); print('✅ Architecture diagram done')


def create_wireframe_kiosk():
    W,H = 800,1000
    img = Image.new('RGB',(W,H),'#F5F5F5'); draw = ImageDraw.Draw(img)
    BLUE='#2196F3'; DARK='#0066CC'
    draw.rounded_rectangle([10,10,790,990], radius=15, fill='white', outline=BLUE, width=3)
    draw.text((250,30),'GIAO DIỆN KIOSK VOICE-FIRST',fill=DARK,font=get_font(18,bold=True))
    draw.rounded_rectangle([30,70,770,115], radius=6, fill=DARK)
    draw.text((280,82),'UBND PHƯỜNG [TÊN PHƯỜNG]',fill='white',font=get_font(14,bold=True))
    cx,cy=400,230; draw.ellipse([cx-60,cy-60,cx+60,cy+60],fill='#E3F2FD',outline=BLUE,width=3)
    draw.rounded_rectangle([370,210,430,230], radius=4, fill=DARK)
    draw.polygon([(370,210),(370,230),(350,220)],fill=DARK)
    draw.arc([380,195,400,225],0,180,fill=DARK,width=2); draw.arc([385,190,405,230],0,180,fill=DARK,width=2)
    draw.text((230,320),'Xin chào! Bác cần hỗ trợ gì ạ?',fill='#333',font=get_font(18,bold=True))
    draw.rounded_rectangle([250,370,550,390], radius=4, fill='#E8F5E9')
    draw.text((270,374),'🔴 Đang nghe... Hãy nói yêu cầu',fill='#333',font=get_font(13))
    for lbl,bx,by,clr in [('Tra cứu thủ tục',40,440,BLUE),('Khai báo hồ sơ',280,440,BLUE),('Hướng dẫn',520,440,'#FF9800')]:
        draw.rounded_rectangle([bx,by,bx+220,by+55],radius=8,fill=clr); draw.text((bx+20,by+15),lbl,fill='white',font=get_font(14,bold=True))
    draw.rounded_rectangle([40,540,760,680], radius=6, fill='#F9F9F9', outline='#DDD')
    draw.text((50,555),'Trợ lý ảo GovOne:',fill=DARK,font=get_font(13,bold=True))
    for i,line in enumerate(['🤖 Bác vui lòng đưa CCCD vào khay scan ạ.','👤 (Bác A đưa CCCD vào scan)','🤖 Cảm ơn bác. Hệ thống đang xác thực...']):
        draw.text((50,590+i*30),line,fill='#333',font=get_font(12))
    draw.rounded_rectangle([200,720,600,770],radius=25,fill='#2196F3')
    draw.text((260,738),'👆 Chạm để nói hoặc nói "GovOne"',fill='white',font=get_font(13,bold=True))
    for i,lbl in enumerate(['Giấy xác nhận HNT','Đăng ký thường trú','Sao y bản chính','Xác nhận thu nhập']):
        bx=50+i*185; draw.rounded_rectangle([bx,810,bx+165,850],radius=6,fill='white',outline='#CCC')
        draw.text((bx+10,823),lbl,fill='#666',font=get_font(11))
    img.save(os.path.join(ASSETS_DIR,'wireframe-kiosk.png')); print('✅ Wireframe Kiosk done')

def create_wireframe_scan():
    W,H=800,920; img=Image.new('RGB',(W,H),'#F5F5F5'); draw=ImageDraw.Draw(img)
    BLUE='#2196F3'; DARK='#0066CC'
    draw.rounded_rectangle([5,5,795,915],radius=10,fill='white',outline=BLUE,width=2)
    draw.text((250,20),'MÀN HÌNH SCAN OCR — CÁN BỘ',fill=DARK,font=get_font(16,bold=True))
    draw.rounded_rectangle([30,55,770,200],radius=8,fill='#F0F0F0',outline='#CCC')
    draw.text((320,110),'📄 Khu vực nạp hồ sơ',fill='#999',font=get_font(14))
    draw.rounded_rectangle([200,145,600,175],radius=4,fill=DARK); draw.text((250,150),'Kéo thả file hoặc chọn máy scan',fill='white',font=get_font(11))
    for i,(l,cl) in enumerate([('Scan từ máy',BLUE),('Tải file lên',BLUE),('Scan ống','#FF9800')]):
        draw.rounded_rectangle([40+i*250,220,240+i*250,260],radius=6,fill=cl); draw.text((50+i*250,230),l,fill='white',font=get_font(13,bold=True))
    draw.rounded_rectangle([30,290,770,390],radius=6,fill='#F9F9F9',outline='#DDD')
    for i,s in enumerate(['Loại giấy tờ: Tự động phát hiện','Độ phân giải: 300 DPI','Định dạng đầu ra: JSON + PDF/A']):
        draw.text((50,310+i*28),s,fill='#666',font=get_font(11))
    draw.rounded_rectangle([30,420,770,600],radius=6,fill='#F0F0F0',outline='#DDD')
    draw.text((350,500),'📄 Preview bản scan',fill='#999',font=get_font(13))
    draw.rounded_rectangle([30,630,770,780],radius=6,fill='white',outline='#DDD')
    draw.text((40,640),'Kết quả OCR trích xuất:',fill=DARK,font=get_font(13,bold=True))
    for i,(l,v) in enumerate([('Họ tên:','Nguyễn Văn A'),('CCCD:','079201000123'),('Ngày sinh:','15/06/1961')]):
        draw.text((50,670+i*30),l,fill='#333',font=get_font(11,bold=True)); draw.text((160,670+i*30),v,fill='#4CAF50',font=get_font(11))
    for i,(l,cl) in enumerate([('✅ Xử lý OCR','#4CAF50'),('💾 Lưu nháp','#FF9800'),('❌ Hủy','#F44336')]):
        draw.rounded_rectangle([40+i*250,810,240+i*250,860],radius=6,fill=cl); draw.text((50+i*250,825),l,fill='white',font=get_font(13,bold=True))
    img.save(os.path.join(ASSETS_DIR,'wireframe-scan.png')); print('✅ Wireframe Scan done')

def create_wireframe_dashboard():
    W,H=1600,1000; img=Image.new('RGB',(W,H),'#F5F5F5'); draw=ImageDraw.Draw(img)
    BLUE='#2196F3'; DARK='#0066CC'
    draw.text((W//2-250,10),'WIREFRAME DASHBOARD CÁN BỘ',fill=DARK,font=get_font(22,bold=True))
    draw.rectangle([10,50,100,990],fill='#1A237E')
    for i,ic in enumerate(['☰','📊','📁','📋','⚙','🔍']): draw.text((40,70+i*100),ic,fill='white',font=get_font(20))
    bx,by,bw,bh=130,60,1440,920
    draw.rounded_rectangle([bx,by,bx+bw,by+bh],radius=10,fill='white',outline='#DDD')
    draw.rounded_rectangle([bx+15,by+15,bx+bw-15,by+60],radius=6,fill=DARK)
    draw.text((bx+180,by+28),'DASHBOARD QUẢN LÝ HỒ SƠ — GOVONE',fill='white',font=get_font(16,bold=True))
    for i,(v,l,clr) in enumerate([('1,234','Tổng GD','#E3F2FD'),('89','Đang XL','#FFF3E0'),('1,145','Hoàn thành','#E8F5E9'),('12','Cảnh báo','#FFEBEE'),('95%','Hài lòng','#E8F5E9')]):
        kx=bx+30+i*275; draw.rounded_rectangle([kx,by+80,kx+260,by+140],radius=8,fill=clr,outline=BLUE)
        draw.text((kx+15,by+88),v,fill=DARK,font=get_font(22,bold=True)); draw.text((kx+15,by+118),l,fill='#666',font=get_font(12))
    draw.rounded_rectangle([bx+30,by+170,bx+700,by+370],radius=6,fill='#F9F9F9',outline='#DDD')
    draw.text((bx+280,by+260),'📈 Biểu đồ xu hướng (7 ngày)',fill='#999',font=get_font(14))
    draw.rounded_rectangle([bx+730,by+170,bx+bw-15,by+370],radius=6,fill='white',outline='#DDD')
    draw.text((bx+900,by+180),'📋 Hồ sơ gần đây',fill=DARK,font=get_font(13,bold=True))
    for i,h in enumerate(['STT','Họ tên','Loại hồ sơ','Ngày','Trạng thái','Kết quả']):
        draw.text((bx+750+i*100,by+210),h,fill=DARK,font=get_font(11,bold=True))
    for ri,row in enumerate([['1','Nguyễn Văn A','Xác nhận HNT','12/06','✅ Hoàn thành','Khop'],['2','Trần Thị B','Đăng ký TT','12/06','⚠️ Cảnh báo','Sai địa chỉ'],['3','Lê Văn C','Sao y BC','11/06','✅ Hoàn thành','Khop'],['4','Phạm Thị D','Xác nhận TN','11/06','❌ Lỗi','Thiếu giấy'],['5','Hoàng Văn E','CCCD','10/06','✅ Hoàn thành','Khop']]):
        ry=by+245+ri*30; draw.line([(bx+740,ry),(bx+bw-20,ry)],fill='#EEE')
        for ci,val in enumerate(row): draw.text((bx+750+ci*100,ry+4),val,fill='#333',font=get_font(10))
    draw.rounded_rectangle([bx+30,by+400,bx+bw-15,by+580],radius=6,fill='#FFFDE7',outline='#FF9800')
    draw.text((bx+50,by+415),'⚠️ Chi tiết cảnh báo (2 hồ sơ)',fill='#FF9800',font=get_font(14,bold=True))
    for i,w in enumerate(['• Hồ sơ #1024: Họ tên không khớp (Nguyễn Văn A ≠ Nguyễn Văn Ấ)','• Hồ sơ #1025: Địa chỉ không khớp (123 Lê Lợi ≠ 124 Lê Lợi)']):
        draw.text((bx+50,by+455+i*30),w,fill='#333',font=get_font(11))
    img.save(os.path.join(ASSETS_DIR,'wireframe-dashboard.png')); print('✅ Wireframe Dashboard done')

def create_user_flow_citizen():
    W,H=1400,900; img=Image.new('RGB',(W,H),'white'); draw=ImageDraw.Draw(img)
    f_title=get_font(22,bold=True); f_step=get_font(14,bold=True); f_label=get_font(12)
    draw.text((W//2-250,15),'LUỒNG NGƯỜI DÂN (CITIZEN) — VOICE-FIRST',fill='#0066CC',font=f_title)
    nodes=[(700,80,'Bắt đầu','#4CAF50',False),(700,200,'Camera phát hiện\n→ Phát giọng chào','#2196F3',False),(700,320,'Người dân nói yêu cầu\n→ STT → Smartbot','#2196F3',False),(400,450,'Cần giấy tờ?','#FF9800',True),(1000,450,'TTS trả lời\nkết quả','#2196F3',False),(400,580,'Hướng dẫn đưa CCCD\n→ Scan → OCR → eKYC','#2196F3',False),(700,700,'Xác nhận thông tin\n→ Sentiment AI','#2196F3',False),(700,820,'Kết thúc.\nLog phiên giao dịch','#4CAF50',False)]
    for x,y,text,color,isd in nodes:
        lines=text.split('\n'); ml=max(draw.textbbox((0,0),l,font=f_step)[2] for l in lines); th=len(lines)*22; bw=max(ml+50,180); bh=max(th+40,70)
        if isd: pts=[(x,y-bh//2),(x+bw//2,y),(x,y+bh//2),(x-bw//2,y)]; draw.polygon(pts,fill='white',outline=color,width=2)
        else: draw.rounded_rectangle([x-bw//2,y-bh//2,x+bw//2,y+bh//2],radius=12,fill='white',outline=color,width=2)
        for li,line in enumerate(lines): lb=draw.textbbox((0,0),line,font=f_step); lw=lb[2]-lb[0]; draw.text((x-lw//2,y-th//2+li*22),line,fill='#333',font=f_step)
    for (x1,y1),(x2,y2) in [((700,115),(700,165)),((700,235),(700,285)),((700,355),(530,415)),((400,485),(400,545)),((400,615),(700,665)),((700,735),(700,790)),((830,415),(960,440))]:
        draw.line([(x1,y1),(x2,y2)],fill='#666',width=2); mx,my=(x1+x2)//2,(y1+y2)//2; draw.polygon([(mx-5,my-5),(mx+5,my+5),(mx-5,my+5)],fill='#666')
    draw.text((450,445),'Có',fill='#FF9800',font=f_label); draw.text((870,430),'Không',fill='#4CAF50',font=f_label)
    img.save(os.path.join(ASSETS_DIR,'user-flow-citizen.png')); print('✅ User flow (Citizen) done')

def create_user_flow_officer():
    W,H=1400,600; img=Image.new('RGB',(W,H),'white'); draw=ImageDraw.Draw(img)
    f_title=get_font(22,bold=True); f_step=get_font(14,bold=True)
    draw.text((W//2-200,15),'LUỒNG CÁN BỘ (OFFICER) — OCR PIPELINE',fill='#0066CC',font=f_title)
    steps=[(100,200,'Nạp hồ sơ\n(Scan/Upload)','#4CAF50'),(330,200,'Phân loại\n(SmartVision)','#2196F3'),(560,200,'OCR & Bóc tách\n(SmartReader)','#2196F3'),(790,200,'Đối chiếu CSDL\n(eKYC)','#FF9800'),(1020,200,'Kiểm tra & Duyệt\n(Dashboard)','#FF9800'),(1250,200,'Xuất dữ liệu\n(PostgreSQL/\nMinIO)','#9C27B0')]
    for x,y,text,color in steps:
        lines=text.split('\n'); ml=max(draw.textbbox((0,0),l,font=f_step)[2] for l in lines); th=len(lines)*22; bw=170; bh=80
        draw.rounded_rectangle([x-bw//2,y-bh//2,x+bw//2,y+bh//2],radius=10,fill='white',outline=color,width=2)
        for li,line in enumerate(lines): lb=draw.textbbox((0,0),line,font=f_step); lw=lb[2]-lb[0]; draw.text((x-lw//2,y-th//2+li*22),line,fill='#333',font=f_step)
    for i in range(len(steps)-1):
        x1,y1=steps[i][0]+85,steps[i][1]; x2,y2=steps[i+1][0]-85,steps[i+1][1]; draw.line([(x1,y1),(x2,y2)],fill='#666',width=2)
        draw.polygon([(x2-8,y2-5),(x2+2,y2),(x2-8,y2+5)],fill='#666')
    img.save(os.path.join(ASSETS_DIR,'user-flow-officer.png')); print('✅ User flow (Officer) done')

if __name__ == '__main__':
    os.makedirs(ASSETS_DIR, exist_ok=True)
    create_architecture_diagram()
    create_wireframe_kiosk()
    create_wireframe_scan()
    create_wireframe_dashboard()
    create_user_flow_citizen()
    create_user_flow_officer()
    print('🎯 All GovOne assets generated!')
