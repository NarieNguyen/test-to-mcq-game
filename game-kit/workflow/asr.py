import subprocess,wave,sys,glob
from pocketsphinx import Decoder, get_model_path
import os
A=os.environ.get('SRC','/mnt/user-data/attachments/')
mp=get_model_path()
def run(pat,out):
    f=glob.glob(A+pat)[0]
    subprocess.run(['ffmpeg','-y','-v','error','-i',f,'-ar','16000','-ac','1',out])
    d=Decoder(hmm=mp+'/en-us/en-us',lm=mp+'/en-us/en-us.lm.bin',dict=mp+'/en-us/cmudict-en-us.dict',loglevel='FATAL')
    d.start_utt(); w=wave.open(out)
    while True:
        b=w.readframes(4000)
        if not b: break
        d.process_raw(b,False,False)
    d.end_utt()
    segs=[(s.start_frame/100,s.word) for s in d.seg() if not s.word.startswith('<') and not s.word.startswith('[')]
    # gom theo quãng lặng >0.9s
    lines=[];cur=[];last=None
    for t,wd in segs:
        if last is not None and t-last>1.0: lines.append(cur);cur=[]
        cur.append((t,wd)); last=t
    if cur: lines.append(cur)
    print('##',pat)
    for l in lines: print('  %5.1fs  %s'%(l[0][0],' '.join(w for _,w in l)))
for p in sys.argv[1:]: run(p,'/tmp/_a.wav')
