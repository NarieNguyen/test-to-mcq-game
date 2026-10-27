import sys,subprocess,os
from PIL import Image
u,secs=sys.argv[1],[int(x) for x in sys.argv[2:]]
P=os.environ.get('WORK','./work')+'/prev%s/'%u
subprocess.run(['python3','-I',os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','tools','preview.py'),os.environ.get('WORK','./work')+'/out_U%s.html'%u,P]+[str(i-1) for i in secs],check=True,capture_output=True)
ims=[Image.open(P+'sec%02d.png'%i) for i in secs]
h=min(1250,max(i.height for i in ims)); W=sum(i.width for i in ims)
s=Image.new('RGB',(W,h),'white'); x=0
for i in ims: s.paste(i.crop((0,0,i.width,min(i.height,h))),(x,0)); x+=i.width
s.save(P+'sheet.png'); print(P+'sheet.png')
