#!/usr/bin/env python3
"""Generate all image assets for AutoCheck proposal."""
from PIL import Image, ImageDraw, ImageFont
import os

AD = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
FB = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FR = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'


def gf(sz, b=False):
    try:
        return ImageFont.truetype(FB if b else FR, sz)
    except:
        return ImageFont.load_default()


def arch():
    W, H = 1600, 800
    img = Image.new('RGB', (W, H), 'white')
    d = ImageDraw.Draw(img)
    cl = {'input':('#4CAF50','#E8F5E9'),'ai':('#2196F3','#E3F2FD'),'output':('#9C27B0','#F3E5F5')}
    d.text((W//2-180,15), 'KIEN TRUC TONG THE AUTOCHECK', fill='#0066CC', font=gf(22,True))
    ly = [
        (80,100,1440,150,'TANG 1 - INPUT','input',['May Scan thuong','May Scan ong ADF','Upload PDF/JPEG','Camera chup']),
        (80,300,1440,220,'TANG 2 - AI PROCESSING (VNPT)','ai',
         ['SmartReader OCR','SmartReader Doc AI','SmartVision','eKYC Compare','eKYC Liveness','AI Rules']),
        (80,570,1440,120,'TANG 3 - OUTPUT & STORAGE','output',['PostgreSQL','MinIO/S3','Redis Cache']),
    ]
    for x,y,w,h,tt,key,items in ly:
        bg,bo = cl[key]
        d.rounded_rectangle([x,y,x+w,y+h], radius=10, fill=bg, outline=bo, width=2)
        d.rounded_rectangle([x,y,x+w,y+35], radius=10, fill=bo)
        d.rectangle([x,y+20,x+w,y+35], fill=bo)
        d.text((x+15,y+8), tt, fill='white', font=gf(16,True))
        n = len(items)
        for i,item in enumerate(items):
            ix = x+20+i*(min(200,(w-40)//n-8))
            iy = y+50; iw = min(195,(w-40)//n-8)
            d.rounded_rectangle([ix,iy,ix+iw,iy+65], radius=6, fill='white', outline=bo, width=1)
            tb = d.textbbox((0,0),item,font=gf(13))
            d.text((ix+(iw-(tb[2]-tb[0]))//2,iy+12), item, fill='#333', font=gf(13))
    for yp in [250,520]:
        d.line([(W//2,yp),(W//2,yp+30)], fill='#666', width=2)
        d.polygon([(W//2-8,yp+30),(W//2+8,yp+30),(W//2,yp+40)], fill='#666')
    img.save(os.path.join(AD,'architecture-diagram.png'))
    print('Architecture diagram done')



def flow():
    W,H = 1400,900
    img = Image.new('RGB', (W,H), 'white')
    d = ImageDraw.Draw(img)
    d.text((W//2-250,15), 'LUONG XU LY HO SO AUTOCHECK', fill='#0066CC', font=gf(22,True))
    nodes = [
        (700,80,'Can bo nap ho so','#4CAF50',0),(400,200,'Scan tai lieu','#2196F3',0),(1000,200,'Upload file so','#2196F3',0),
        (700,320,'SmartVision:\nPhan loai','#FF9800',0),(700,440,'SmartReader:\nOCR','#2196F3',0),
        (400,560,'Doi chieu CSDL\neKYC','#FF9800',1),(1000,560,'AI Rules:\nKiem tra','#FF9800',1),
        (700,700,'Dashboard:\nKiem tra','#2196F3',0),(700,820,'Xuat du lieu\n+ Luu goc','#4CAF50',0),
    ]
    for x,y,text,color,isd in nodes:
        lines = text.split('\n')
        ml = max(d.textbbox((0,0),l,font=gf(14,True))[2] for l in lines)
        th = len(lines)*22; bw = max(ml+50,180); bh = max(th+40,70)
        if isd:
            pts = [(x,y-bh//2),(x+bw//2,y),(x,y+bh//2),(x-bw//2,y)]
            d.polygon(pts, fill='white', outline=color, width=2)
        else:
            d.rounded_rectangle([x-bw//2,y-bh//2,x+bw//2,y+bh//2], radius=12, fill='white', outline=color, width=2)
        for li,line in enumerate(lines):
            lb = d.textbbox((0,0),line,font=gf(14,True))
            d.text((x-(lb[2]-lb[0])//2, y-th//2+li*22), line, fill='#333', font=gf(14,True))
    arrs = [((700,115),(520,165)),((700,115),(880,165)),((400,235),(700,285)),((1000,235),(700,285)),
            ((700,355),(700,405)),((700,475),(520,528)),((700,475),(880,528)),((400,595),(700,665)),
            ((1000,595),(700,665)),((700,735),(700,785))]
    for (x1,y1),(x2,y2) in arrs:
        d.line([(x1,y1),(x2,y2)], fill='#666', width=2)
    img.save(os.path.join(AD,'user-flow.png'))
    print('User flow done')


def wf():
    W,H = 1600,1000
    img = Image.new('RGB', (W,H), '#F5F5F5')
    d = ImageDraw.Draw(img)
    BL='#2196F3'; DB='#0066CC'
    d.text((W//2-200,10), 'WIREFRAME GIAO DIEN AUTOCHECK', fill=DB, font=gf(22,True))
    # Dashboard screen
    x1,y1,sw,sh = 30,50,760,920
    d.rounded_rectangle([x1,y1,x1+sw,y1+sh], radius=10, fill='white', outline=BL, width=2)
    d.text((x1+200,y1+15), 'DASHBOARD KIEM TRA & XAC THUC', fill=DB, font=gf(18,True))
    for i,(v,l) in enumerate([('1,234','Da xu ly'),('12','Canh bao'),('3','Loi'),('98.5%','Chinh xac')]):
        sx = x1+20+i*180
        d.rounded_rectangle([sx,y1+60,sx+170,y1+110], radius=6, fill='#E3F2FD', outline=BL)
        d.text((sx+10,y1+67), v, fill=DB, font=gf(18,True))
        d.text((sx+10,y1+92), l, fill='#666', font=gf(10))
    hdrs = ['STT','Loai ho so','Ngay','Trang thai','Ket qua']; cw=[40,150,120,120,120]; cx=x1+20
    d.rounded_rectangle([cx,y1+140,cx+sw-40,y1+175], radius=4, fill=DB)
    for i,h in enumerate(hdrs):
        d.text((cx+10+sum(cw[:i]),y1+150), h, fill='white', font=gf(12,True))
    rows = [['1','CCCD','10/06','Da XN','Khop'],['2','So ho khau','10/06','Canh bao','Sai dia chi'],
            ['3','Giay khai sinh','10/06','Da XN','Khop'],['4','Bang TN','09/06','Loi','Thieu'],
            ['5','CCCD','09/06','Da XN','Khop']]
    for ri,row in enumerate(rows):
        ry=y1+185+ri*30; d.line([(cx,ry+28),(cx+sw-40,ry+28)], fill='#EEE')
        for ci,val in enumerate(row):
            d.text((cx+10+sum(cw[:ci]),ry+4), val, fill='#333', font=gf(10))
    d.rounded_rectangle([cx,y1+340,cx+sw-40,y1+520], radius=6, fill='#FFFDE7', outline='#FF9800')
    d.text((cx+15,y1+350), 'Chi tiet canh bao', fill='#FF9800', font=gf(13,True))
    for i,w in enumerate(['Ho ten: A != B','Dia chi: 123 != 124']):
        d.text((cx+15,y1+390+i*25), w, fill='#333', font=gf(10))
    img.save(os.path.join(AD,'wireframe-validation-dashboard.png'))
    print('Wireframe dashboard done')
    # Scan screen
    img2 = Image.new('RGB', (800,920), '#F5F5F5')
    d2 = ImageDraw.Draw(img2)
    d2.rounded_rectangle([5,5,795,915], radius=10, fill='white', outline=BL, width=2)
    d2.text((250,20), 'MAN HINH SCAN HO SO', fill=DB, font=gf(16,True))
    d2.rounded_rectangle([30,55,770,250], radius=8, fill='#F0F0F0', outline='#CCC')
    d2.text((300,130), 'Khu vuc scan', fill='#999', font=gf(14))
    d2.rectangle([150,160,650,180], fill=DB)
    d2.text((200,162), 'Keo tha file hoac scan truc tiep', fill='white', font=gf(10))
    for i,(l,cl) in enumerate([('Scan tu may',BL),('Tai file len',BL),('Scan ong','#FF9800')]):
        d2.rounded_rectangle([40+i*240,280,260+i*240,320], radius=6, fill=cl)
        d2.text((50+i*240,290), l, fill='white', font=gf(13,True))
    d2.rounded_rectangle([30,350,770,450], radius=6, fill='#F9F9F9', outline='#DDD')
    for i,s in enumerate(['Loai giay to: Tu dong phat hien','Do phan giai: 300 DPI','Dinh dang: JSON + PDF/A']):
        d2.text((50,370+i*25), s, fill='#666', font=gf(10))
    d2.rounded_rectangle([30,480,770,650], radius=6, fill='#F0F0F0', outline='#DDD')
    d2.text((300,550), 'Preview ban scan', fill='#999', font=gf(12))
    for i,(l,cl) in enumerate([('Xu ly OCR','#4CAF50'),('Luu nhap','#FF9800'),('Huy','#F44336')]):
        d2.rounded_rectangle([40+i*240,680,260+i*240,720], radius=6, fill=cl)
        d2.text((50+i*240,690), l, fill='white', font=gf(13,True))
    img2.save(os.path.join(AD,'wireframe-scan-interface.png'))
    print('Wireframe scan interface done')


if __name__ == '__main__':
    os.makedirs(AD, exist_ok=True)
    arch(); flow(); wf()
    print('All AutoCheck assets generated!')
