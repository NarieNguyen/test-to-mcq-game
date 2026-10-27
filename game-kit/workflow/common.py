import os,json,subprocess,glob,re
from PIL import Image
# Thư mục chứa file audio/PDF gốc người dùng gửi (đặt qua biến môi trường SRC hoặc sửa tại đây)
A=os.environ.get('SRC','/mnt/user-data/attachments/')
WORK=os.environ.get('WORK','./work')+'/'
class Unit:
    def __init__(s,n): s.n=n; s.dir=WORK+'u%d/'%n; os.makedirs(s.dir+'media',exist_ok=True); s.cache={}
    def crop(s,page,box,name):
        """box theo toạ độ ảnh 100dpi (827x1170); lưu webp vào media/"""
        im=Image.open(s.dir+'hi/p-%d.png'%page).convert('RGB')
        x0,y0,x1,y1=[int(v*2) for v in box]
        im.crop((x0,y0,x1,y1)).save(s.dir+'media/%s.webp'%name,'WEBP',quality=85)
        return 'media/%s.webp'%name
    def audio(s,pat,name):
        f=glob.glob(A+pat)[0]; out=s.dir+'media/%s.mp3'%name
        subprocess.run(['ffmpeg','-y','-v','error','-i',f,'-ac','1','-b:a','64k',out],check=True); return 'media/%s.mp3'%name
    def save(s,game):
        json.dump(game,open(s.dir+'game.json','w',encoding='utf8'),ensure_ascii=False,indent=1)
        n=sum(len(x['items']) for x in game['sections']); print('game.json:',len(game['sections']),'phần',n,'câu')
def Q(prompt,options,answer,explain,img=None,audioAt=None):
    d={'prompt':prompt,'options':options,'answer':answer,'explain':explain}
    if img: d['img']=img
    if audioAt is not None: d['audioAt']=audioAt
    return d

_k=[0]
def place(correct,wrongs):
    """Chèn đáp án đúng luân phiên vị trí A,B,C,D (để phân bố đều)."""
    opts=list(wrongs); n=len(opts)+1
    pos=_k[0]%n; _k[0]+=1
    opts.insert(pos,correct); return opts

def _grid(self,page,boxes,name,cols=3,w=420):
    im=Image.open(self.dir+'hi/p-%d.png'%page).convert('RGB'); tiles=[]
    for b in boxes:
        t=im.crop(tuple(int(v*2) for v in b)); t=t.resize((w,round(t.height*w/t.width))); tiles.append(t)
    rows=[tiles[i:i+cols] for i in range(0,len(tiles),cols)]
    H=sum(max(t.height for t in r) for r in rows)+8*(len(rows)+1); W=cols*w+8*(cols+1)
    sh=Image.new('RGB',(W,H),'white'); y=8
    for r in rows:
        x=8
        for t in r: sh.paste(t,(x,y)); x+=w+8
        y+=max(t.height for t in r)+8
    sh.save(self.dir+'media/%s.webp'%name,'WEBP',quality=85); return 'media/%s.webp'%name
Unit.grid=_grid

def _quad(self,page,y0,y1,x0,x1,name):
    q=(x1-x0)/4.0
    return self.grid(page,[(x0+i*q,y0,x0+(i+1)*q,y1) for i in range(4)],name,cols=2,w=420)
Unit.quad=_quad
