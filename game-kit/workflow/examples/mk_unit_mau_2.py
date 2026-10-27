from common import *
import random
u=Unit(10)
au4=u.audio('*Part_4_U10.mp3','part4'); au5=u.audio('*Part_5_U10.wav','part5')
def distract(pool,ans,k,seed):
    w=[x for x in pool if x!=ans]; random.Random(seed).shuffle(w); return w[:k]
def mc(prefix,qs,imgf=None,**kw):
    pass
sec=[]
# P1
g1=u.crop(1,(300,205,795,478),'p1_grid')
P1=[('play chess','A','chơi cờ vua'),('play volleyball','B','chơi bóng chuyền'),('play basketball','C','chơi bóng rổ'),('play badminton','D','chơi cầu lông'),('play football','E','chơi bóng đá')]
items=[Q('%d. “%s” – nối với bức tranh nào?'%(i+1,t),place(a,distract('ABCDE',a,3,i)),a,'“%s” = %s → tranh %s.'%(t,d,a),img=g1) for i,(t,a,d) in enumerate(P1)]
sec.append({'id':'part1','icon':'🖼️','title':'Part 1. Vocabulary – Look and match.','desc':'Nối hoạt động với bức tranh','items':items})
# P2
rows=[(545,655),(658,765),(770,877),(882,990),(995,1108)]
P2=[(['play chess','play basketball','play badminton','school bag'],'school bag','Ba mục kia là hoạt động giờ ra chơi (play …); school bag là đồ dùng học tập.'),
    (['ruler','chat with my friends','play football','play volleyball'],'ruler','Ba mục kia là hoạt động giờ ra chơi; ruler là đồ dùng học tập.'),
    (['play table tennis','pencil case','play badminton','play word puzzles'],'pencil case','Ba mục kia là hoạt động giờ ra chơi; pencil case là đồ dùng học tập.'),
    (['play basketball','play chess','play football','book'],'book','Ba mục kia là hoạt động giờ ra chơi; book là đồ vật.'),
    (['chat with my friends','play volleyball','play table tennis','classroom'],'classroom','Ba mục kia là hoạt động giờ ra chơi; classroom là nơi chốn.')]
items=[Q('%d. Chọn từ/cụm từ khác loại:'%(i+1),place(a,[x for x in w if x!=a]),a,e,img=u.quad(1,rows[i][0],rows[i][1],30,795,'p2_%d'%(i+1))) for i,(w,a,e) in enumerate(P2)]
sec.append({'id':'part2','icon':'🔍','title':'Part 2. Vocabulary – Circle the odd one out.','desc':'Tìm từ khác loại','items':items})
# P3
bank=['chess','basketball','volleyball','badminton','table tennis','word puzzles']
r3=[(316,438),(450,572),(584,706),(719,842),(853,977),(990,1113)]
P3=['chess','basketball','volleyball','badminton','table tennis','word puzzles']
items=[Q('%d. I play ____ at break time.'%(i+1),place(a,distract(bank,a,3,10+i)),a,'Nhìn tranh: play %s.'%a,img=u.crop(2,(585,r3[i][0],782,r3[i][1]),'p3_%d'%(i+1))) for i,a in enumerate(P3)]
sec.append({'id':'part3','icon':'✍️','title':'Part 3. Vocabulary – Look and complete.','desc':'Điền từ đúng với tranh','wordBank':bank,'items':items})
# P4
b4=[(180,335),(350,505),(518,672),(680,825)]
P4=[('What does Ben do at break time?',['a (chơi cờ vua)','b (chơi bóng đá)','c (giải ô chữ)'],'b (chơi bóng đá)','Bài nghe: “Do you play chess at break time? – No. I play football with Nam at break time.” → b.',3),
    ('What does Mai do at break time?',['a (chơi cầu lông)','b (chơi bóng rổ)','c (trò chuyện)'],'a (chơi cầu lông)','Bài nghe: “Do you play basketball at break time? – No, I don’t. … I play badminton with Lucy.” → a.',14),
    ('What does he do at break time?',['a (chơi bóng bàn)','b (chơi bóng chuyền)','c (chơi bóng rổ)'],'b (chơi bóng chuyền)','Bài nghe: “I play volleyball at break time.” → b.',30),
    ('What do the two boys do at break time?',['a (trò chuyện)','b (chơi cờ vua)','c (chơi bóng đá)'],'b (chơi cờ vua)','Bài nghe: “Are they playing football? – No, they aren’t. They play chess at break time.” → b.',37)]
items=[Q('%d. Nghe và chọn: %s'%(i+1,q),o,a,e,img=u.crop(3,(30,b4[i][0],790,b4[i][1]),'p4_%d'%(i+1)),audioAt=t) for i,(q,o,a,e,t) in enumerate(P4)]
sec.append({'id':'part4','icon':'🎧','title':'Part 4. Listening – Listen and tick.','desc':'Nghe và chọn tranh đúng','audio':au4,'markLabel':'Nhảy đến câu:','audioMarks':[{'label':'Câu %d'%(i+1),'t':P4[i][4]} for i in range(4)],'items':items})
# P5
g5=u.crop(3,(35,880,790,1115),'p5_grid')
P5=[('Lucy chơi cầu lông ở sân trường','4'),('Ben thích hoạt động yên tĩnh, chơi cờ vua','1'),('Nam đá bóng với bạn gần khung thành','3'),('Mai giải ô chữ trong sách bài tập','5'),('Hai bạn nam chơi bóng bàn','6'),('Anna chơi bóng chuyền gần lưới','2')]
at5=[4,15,23,30,36,43]
items=[Q('%d. Nghe và đánh số: nội dung thứ %d trong bài nghe ứng với tranh nào?'%(i+1,i+1),place('Tranh '+p,['Tranh '+x for x in distract('123456',p,3,30+i)]),'Tranh '+p,'Thứ %d trong bài nghe: %s → tranh %s.'%(i+1,t,p),img=g5,audioAt=at5[i]) for i,(t,p) in enumerate(P5)]
sec.append({'id':'part5','icon':'🔢','title':'Part 5. Listening – Listen and number.','desc':'Nghe và đánh số thứ tự tranh (tranh đánh số 1–6 từ trái sang phải, hàng trên rồi hàng dưới)','audio':au5,'markLabel':'Nhảy đến số:','audioMarks':[{'label':'Số %d'%(i+1),'t':at5[i]} for i in range(6)],'items':items})
# P6
ys=[(213,380),(390,557),(567,735),(744,910),(920,1087)]
g6=u.grid(4,[(475,a,788,b) for a,b in ys],'p6_pics')
P6=[('I play chess at break time.','A','chơi cờ vua'),('I play table tennis with my friend.','C','chơi bóng bàn'),('We chat with our friends.','B','trò chuyện cùng bạn'),('I play volleyball.','D','chơi bóng chuyền'),('I do word puzzles.','E','giải ô chữ')]
items=[Q('%d. “%s” – nối với tranh nào?'%(i+1,t),place(a,distract('ABCDE',a,3,50+i)),a,'Câu này nói về việc %s → tranh %s.'%(d,a),img=g6) for i,(t,a,d) in enumerate(P6)]
sec.append({'id':'part6','icon':'🔗','title':'Part 6. Reading – Read and match.','desc':'Đọc câu và nối với tranh','items':items})
# P7
P7=[('A: What do you do at break time?  B: ____',['I play badminton.','Yes, I do.','It’s football.'],'I play badminton.','“What do you do…?” → I play + hoạt động.'),
    ('A: Do you play chess at break time?  B: ____',['I play basketball.','No, I don’t.','They chat with friends.'],'No, I don’t.','“Do you…?” → Yes, I do. / No, I don’t.'),
    ('A: What does she do at break time?  B: ____',['She plays basketball.','Yes, she does.','I play volleyball.'],'She plays basketball.','“What does she do…?” → She plays + hoạt động.'),
    ('A: Do they chat with their friends?  B: ____',['No, it isn’t.','Yes, they do.','He plays chess.'],'Yes, they do.','“Do they…?” → Yes, they do. / No, they don’t.'),
    ('A: Does he play football?  B: ____',['Yes, he does.','I’m fine.','It’s a ruler.'],'Yes, he does.','“Does he…?” → Yes, he does. / No, he doesn’t.')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e) for i,(q,o,a,e) in enumerate(P7)]
sec.append({'id':'part7','icon':'💬','title':'Part 7. Reading – Read and choose the correct answer.','desc':'Chọn câu trả lời đúng','items':items})
# P8
txt=['Hello. My name’s Nam. I am in class 3A. At break time, I play football with Ben. Lucy plays badminton with Mai. Minh likes table tennis. After that, we chat with our friends under a tree. We are happy at school.']
P8=[('Is Nam in class 4A?',['No, he isn’t.','Yes, he is.','Yes, he does.'],'No, he isn’t.','Nam học lớp 3A, không phải 4A.'),
    ('Who does Nam play football with?',['Ben','Minh','Mai'],'Ben','“I play football with Ben.”'),
    ('Who plays badminton?',['Lucy and Mai','Nam and Ben','Minh'],'Lucy and Mai','“Lucy plays badminton with Mai.”'),
    ('What does Minh like?',['Table tennis','Badminton','Football'],'Table tennis','“Minh likes table tennis.”'),
    ('Where do the children chat?',['Under a tree.','In the classroom.','Near the goal.'],'Under a tree.','“We chat with our friends under a tree.”')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e) for i,(q,o,a,e) in enumerate(P8)]
sec.append({'id':'part8','icon':'📖','title':'Part 8. Reading – Read the text and answer.','desc':'Đọc đoạn văn và trả lời','passage':{'kind':'reading','header':'ĐỌC ĐOẠN VĂN CỦA NAM:','img':u.crop(5,(310,580,808,918),'p8_pics'),'paragraphs':txt},'items':items})
# P9
P9=[('What ____ you do at break time?',['do','are'],'do','What do you do…? – dùng trợ động từ do.'),('I ____ chess at break time.',['play','plays'],'play','Chủ ngữ I → play.'),('She ____ badminton at break time.',['plays','play'],'plays','Chủ ngữ she (ngôi thứ ba số ít) → plays.'),('____ he play football at break time?',['Does','Do'],'Does','Chủ ngữ he → Does.'),('Yes, he ____.',['does','do'],'does','Trả lời Does he…? → Yes, he does.'),('They ____ with their friends.',['chat','chats'],'chat','Chủ ngữ they → chat.')]
items=[Q('%d. %s'%(i+1,q),o,a,e) for i,(q,o,a,e) in enumerate(P9)]
sec.append({'id':'part9','icon':'✅','title':'Part 9. Grammar – Choose and complete.','desc':'Chọn từ đúng để hoàn thành câu','items':items})
# P10
bx=[(28,287),(293,525),(540,790)]; by=[(435,622),(630,820)]
P10=[('I play ____.',['chess','football','volleyball'],'chess','Tranh chơi cờ vua.'),
     ('They ____ with their friends.',['chat','chats','play'],'chat','Tranh các bạn trò chuyện; chủ ngữ They → chat.'),
     ('He ____ football.',['plays','play','does'],'plays','Chủ ngữ He → plays.'),
     ('I ____ volleyball.',['play','plays','chat'],'play','Chủ ngữ I → play.'),
     ('Do you ____ table tennis?',['play','plays','chat'],'play','Sau Do you → động từ nguyên mẫu play.'),
     ('She plays ____.',['word puzzles','table tennis','chess'],'word puzzles','Tranh bạn nữ giải ô chữ → word puzzles.')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e,img=u.crop(6,(bx[i%3][0],by[i//3][0],bx[i%3][1],by[i//3][1]),'p10_%d'%(i+1))) for i,(q,o,a,e) in enumerate(P10)]
sec.append({'id':'part10','icon':'🖍️','title':'Part 10. Grammar – Look and complete.','desc':'Nhìn tranh và hoàn thành câu','items':items})
# P11
P11=[('at break time / What / do / you / do / ?','What do you do at break time?',['What you do do at break time?','Do you what do at break time?','What do do you at break time?']),
     ('play badminton / Does / Mai / at break time / ?','Does Mai play badminton at break time?',['Mai does play badminton at break time?','Does play Mai badminton at break time?','Does Mai badminton play at break time?']),
     ('chat with / I / my friends / after that / .','After that, I chat with my friends.',['I after that chat with my friends.','After that, chat I with my friends.','After that, I my friends chat with.']),
     ('No, / doesn’t / he / . / He plays chess / .','No, he doesn’t. He plays chess.',['No, doesn’t he. He plays chess.','He no doesn’t. He plays chess.','No, he doesn’t. Plays he chess.']),
     ('table tennis / Ben and Nam / play / together / .','Ben and Nam play table tennis together.',['Ben and Nam table tennis play together.','Table tennis Ben and Nam play together.','Ben and Nam plays table tennis together.'])]
items=[Q('%d. Sắp xếp: %s'%(i+1,q),place(a,w),a,'Câu đúng: “%s”'%a) for i,(q,a,w) in enumerate(P11)]
sec.append({'id':'part11','icon':'🔀','title':'Part 11. Writing – Put the words in order.','desc':'Sắp xếp từ thành câu','items':items})
# P12
i12=u.crop(7,(25,142,810,715),'p12_pic')
P12=[('How many children can you see in the picture?',['Eleven.','Nine.','Twelve.'],'Eleven.','Đếm: 2 bạn đá bóng, 2 bạn chơi cầu lông, 2 bạn chơi bóng bàn, 2 bạn chơi cờ, 3 bạn ngồi ghế đá = 11.'),
     ('What are the two boys on the left doing?',['They are playing football.','They are playing chess.','They are chatting.'],'They are playing football.','Hai bạn nam bên trái đang đá bóng gần khung thành.'),
     ('Which game are the two girls in the middle playing?',['Badminton.','Volleyball.','Table tennis.'],'Badminton.','Hai bạn nữ ở giữa cầm vợt, có lưới và quả cầu → cầu lông.'),
     ('What are the two children at the wooden table in front doing?',['They are playing chess.','They are playing table tennis.','They are doing word puzzles.'],'They are playing chess.','Hai bạn ở bàn gỗ phía trước đang chơi cờ vua.'),
     ('Where are the three children sitting, and what are they doing?',['On a bench under the tree, chatting.','In the classroom, playing chess.','Near the net, playing badminton.'],'On a bench under the tree, chatting.','Ba bạn ngồi trên ghế đá dưới gốc cây và đang trò chuyện.'),
     ('Are the boy and the girl at the table playing chess?',['Yes, they are.','No, they aren’t.','Yes, they do.'],'Yes, they are.','Bạn nam và bạn nữ ở bàn đang chơi cờ vua.')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e,img=i12) for i,(q,o,a,e) in enumerate(P12)]
sec.append({'id':'part12','icon':'🗣️','title':'Part 12. Speaking – Look at the picture and answer the questions.','desc':'Nhìn tranh và trả lời','items':items})
u.save({'id':'gs3_u10','title':'GLOBAL SUCCESS - UNIT 10: BREAK TIME ACTIVITIES','badge':'Luyện Thi · Global Success','tag':'Global Success 3 · Unit 10','champTitle':'Thần Đồng Tiếng Anh','sections':sec})
