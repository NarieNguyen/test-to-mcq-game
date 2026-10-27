from common import *
import random
u=Unit(8)
au4=u.audio('*Part_4_U8.mp3','part4'); au5=u.audio('*Part_5_U8.wav','part5')
def distract(pool,ans,k,seed):
    w=[x for x in pool if x!=ans]; random.Random(seed).shuffle(w); return w[:k]
sec=[]
# P1
g1=u.crop(1,(410,218,770,600),'p1_grid')
P1=[('school bag','A','cặp sách xanh lá'),('pen','B','bút mực'),('notebook','C','vở xoắn xanh'),('eraser','D','cục tẩy'),('ruler','E','thước kẻ')]
items=[Q('%d. “%s” – nối với bức tranh nào?'%(i+1,t),place(a,distract('ABCDE',a,3,i)),a,'“%s” ứng với tranh %s (%s).'%(t,a,d),img=g1) for i,(t,a,d) in enumerate(P1)]
sec.append({'id':'part1','icon':'🖼️','title':'Part 1. Vocabulary – Look and match.','desc':'Nối từ với đồ vật','items':items})
# P2
rows=[(652,742),(748,838),(845,932),(938,1022),(1025,1118)]
P2=[(['swimming','ruler','book','pen'],'swimming','Ruler, book, pen là đồ dùng học tập; swimming là môn thể thao/hoạt động.'),
    (['school bag','pencil case','eraser','playground'],'playground','School bag, pencil case, eraser là đồ dùng học tập; playground là nơi chốn.'),
    (['notebook','pencil','teacher','ruler'],'teacher','Notebook, pencil, ruler là đồ dùng học tập; teacher là người.'),
    (['pen','pencil','school bag','nose'],'nose','Pen, pencil, school bag là đồ dùng học tập; nose là bộ phận cơ thể.'),
    (['Do you have a pen?','Yes, I do.','No, I don’t.','Sit down, please.'],'Sit down, please.','Ba câu kia là hỏi–đáp về việc có đồ vật hay không; Sit down, please là khẩu lệnh trong lớp.')]
items=[Q('%d. Chọn từ/câu khác loại:'%(i+1),w,a,e,img=u.quad(1,rows[i][0],rows[i][1],80,785,'p2_%d'%(i+1))) for i,(w,a,e) in enumerate(P2)]
sec.append({'id':'part2','icon':'🔍','title':'Part 2. Vocabulary – Circle the odd one out.','desc':'Tìm từ khác loại','items':items})
# P3
bank=['pen','ruler','book','school bag','pencil','pencil case']
r3=[(307,423),(437,553),(566,688),(701,823),(837,955),(969,1095)]
P3=[('I have a ____.','pen'),('I have a ____.','book'),('This is my ____.','school bag'),('I have a ____.','ruler'),('This is my ____.','pencil case'),('I have a ____.','pencil')]
items=[Q('%d. %s'%(i+1,t),place(a,distract(bank,a,3,10+i)),a,'Nhìn tranh: %s'%a,img=u.crop(2,(500,r3[i][0],755,r3[i][1]),'p3_%d'%(i+1))) for i,(t,a) in enumerate(P3)]
sec.append({'id':'part3','icon':'✍️','title':'Part 3. Vocabulary – Look and complete.','desc':'Điền từ đúng với tranh','wordBank':bank,'items':items})
# P4
b4=[(180,330),(350,500),(520,640),(655,775)]
P4=[('What does Ben have?',['a (cục tẩy)','b (thước kẻ vàng)','c (vở xanh)'],'b (thước kẻ vàng)','Bài nghe: “Do you have a ruler? – No, I don’t. I have a yellow ruler.” → Ben có thước kẻ vàng (b).',3),
    ('What does Lucy have?',['a (bút mực)','b (thước kẻ)','c (vở)'],'a (bút mực)','Bài nghe: “I have a pen.” → Lucy có bút mực (a).',9),
    ('Do you have a notebook?',['a (Yes, I do.)','b (No, I don’t.)','c (I don’t know.)'],'a (Yes, I do.)','Bài nghe: “Do you have a notebook? – Yes, I do.” → a.',14),
    ('What is in Mai’s school bag?',['a (vở)','b (hộp bút)','c (bút chì và cục tẩy)'],'c (bút chì và cục tẩy)','Bài nghe: “Is there a notebook in it? – No. I have a pencil and an eraser in my school bag.” → c.',25)]
items=[Q('%d. Nghe và chọn: %s'%(i+1,q),o,a,e,img=u.crop(3,(30,b4[i][0],790,b4[i][1]),'p4_%d'%(i+1)),audioAt=t) for i,(q,o,a,e,t) in enumerate(P4)]
sec.append({'id':'part4','icon':'🎧','title':'Part 4. Listening – Listen and tick.','desc':'Nghe và chọn tranh đúng','audio':au4,'markLabel':'Nhảy đến câu:','audioMarks':[{'label':'Câu %d'%(i+1),'t':P4[i][4]} for i in range(4)],'items':items})
# P5
g5=u.crop(3,(45,848,785,1105),'p5_grid')
P5=[('pencil màu vàng','4'),('cặp sách xanh lá','1'),('hộp bút','6'),('vở xanh','3'),('bút mực đen','2'),('cục tẩy đỏ–xanh','5')]
at5=[4,11,19,27,33,42]
items=[Q('%d. Nghe và đánh số: nội dung thứ %d trong bài nghe ứng với tranh nào?'%(i+1,i+1),place('Tranh '+p,['Tranh '+x for x in distract('123456',p,3,30+i)]),'Tranh '+p,'Thứ %d trong bài nghe nói về %s → tranh %s.'%(i+1,t,p),img=g5,audioAt=at5[i]) for i,(t,p) in enumerate(P5)]
sec.append({'id':'part5','icon':'🔢','title':'Part 5. Listening – Listen and number.','desc':'Nghe và đánh số thứ tự tranh','audio':au5,'markLabel':'Nhảy đến số:','audioMarks':[{'label':'Số %d'%(i+1),'t':at5[i]} for i in range(6)],'items':items})
# P6
g6=u.grid(4,[(535,205,783,372),(535,388,783,553),(535,570,783,735),(535,750,783,915),(535,932,783,1098)],'p6_pics')
P6=[('I have a pen.','D'),('Do you have an eraser? – No, I don’t. I have a ruler.','A'),('This is my school bag.','C'),('Do you have a notebook? – Yes, I do.','B'),('I have a pencil case.','E')]
items=[Q('%d. “%s” – nối với tranh nào?'%(i+1,t),place(a,distract('ABCDE',a,3,50+i)),a,'Câu này khớp với tranh %s.'%a,img=g6) for i,(t,a) in enumerate(P6)]
sec.append({'id':'part6','icon':'🔗','title':'Part 6. Reading – Read and match.','desc':'Đọc câu và nối với tranh','items':items})
# P7
P7=[('A: Do you have a notebook?  B: ____',['It’s green.','Yes, I do.','I have two pens.'],'Yes, I do.','“Do you have…?” → Yes, I do. / No, I don’t.'),
    ('A: What do you have?  B: ____',['No, I don’t.','Open your book.','I have a ruler.'],'I have a ruler.','“What do you have?” → I have + đồ vật.'),
    ('A: Do you have a pencil case?  B: ____',['No, I don’t.','Yes, I am.','This is my book.'],'No, I don’t.','Trả lời Do you have…? bằng No, I don’t.'),
    ('A: Is this your school bag?  B: ____',['I have a pen.','No, I can’t.','Yes, it is.'],'Yes, it is.','“Is this…?” → Yes, it is.'),
    ('A: Do you have a pen?  B: ____',['It’s a bag.','No, I don’t. I have a pencil.','Thank you.'],'No, I don’t. I have a pencil.','Trả lời Do you have a pen? bằng No, I don’t + nói mình có gì.')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e) for i,(q,o,a,e) in enumerate(P7)]
sec.append({'id':'part7','icon':'💬','title':'Part 7. Reading – Read and choose the correct answer.','desc':'Chọn câu trả lời đúng','items':items})
# P8
txt=['Hello. My name’s Ben. I am in class 3A. I have a blue school bag. In my school bag, I have a book, two notebooks, a pencil case, three pencils and a ruler. My friend Mai has a pink school bag. She has an eraser and a pen. We like our school things.']
P8=[('Who is speaking?',['Ben','Mai','Nam'],'Ben','“My name’s Ben.”'),
    ('What colour is Ben’s school bag?',['It’s blue.','It’s pink.','It’s green.'],'It’s blue.','“I have a blue school bag.”'),
    ('What does Ben have in his school bag?',['A book, two notebooks, a pencil case, three pencils and a ruler.','An eraser and a pen.','A pink school bag.'],'A book, two notebooks, a pencil case, three pencils and a ruler.','Liệt kê trong bài: “a book, two notebooks, a pencil case, three pencils and a ruler”.'),
    ('Who has a pink school bag?',['Ben','Mai','Lucy'],'Mai','“My friend Mai has a pink school bag.”'),
    ('Does Mai have a pen?',['Yes, she does.','No, she doesn’t.','Yes, I do.'],'Yes, she does.','“She has an eraser and a pen.”')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e) for i,(q,o,a,e) in enumerate(P8)]
sec.append({'id':'part8','icon':'📖','title':'Part 8. Reading – Read the text and answer.','desc':'Đọc đoạn văn và trả lời','passage':{'kind':'reading','header':'ĐỌC ĐOẠN VĂN CỦA BEN:','img':u.crop(5,(327,610,790,968),'p8_pics'),'paragraphs':txt},'items':items})
# P9
P9=[('I ____ a pen.',['have','has'],'have','Chủ ngữ I → have.'),('Do you ____ a notebook?',['has','have'],'have','Sau Do you → have.'),('Yes, I ____.',['do','am'],'do','Trả lời Do you have…? → Yes, I do.'),('No, I ____.',['doesn’t','don’t'],'don’t','Chủ ngữ I → don’t.'),('I have ____ eraser.',['an','a'],'an','Eraser bắt đầu bằng nguyên âm → an.'),('This is my school ____.',['bags','bag'],'bag','“This is my…” + danh từ số ít → bag.')]
items=[Q('%d. %s'%(i+1,q),o,a,e) for i,(q,o,a,e) in enumerate(P9)]
sec.append({'id':'part9','icon':'✅','title':'Part 9. Grammar – Choose and complete.','desc':'Chọn từ đúng để hoàn thành câu','items':items})
# P10
bx=[(40,283),(300,532),(548,785)]; by=[(482,668),(686,868)]
P10=[('I have a ____.',['pen','pencil','ruler'],'pen','Tranh cây bút mực.'),
     ('This ____.',['is my notebook','are my notebooks','have my notebook'],'is my notebook','Tranh một quyển vở → This is my notebook.'),
     ('Do ____?',['you have a ruler','you have a pen','you have a notebook'],'you have a ruler','Tranh thước kẻ → Do you have a ruler?'),
     ('Do ____?  (Yes, I do.)',['you have a pencil','you have a ruler','you have an eraser'],'you have a pencil','Tranh bút chì, trả lời “Yes, I do.” → Do you have a pencil?'),
     ('Do ____?  (No, I don’t.)',['you have an eraser','you have a pen','you have a pencil case'],'you have an eraser','Tranh cục tẩy, trả lời “No, I don’t.” → Do you have an eraser?'),
     ('This ____.',['is my pencil case','are my pencil cases','have my pencil case'],'is my pencil case','Tranh hộp bút → This is my pencil case.')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e,img=u.crop(6,(bx[i%3][0],by[i//3][0],bx[i%3][1],by[i//3][1]),'p10_%d'%(i+1))) for i,(q,o,a,e) in enumerate(P10)]
sec.append({'id':'part10','icon':'🖍️','title':'Part 10. Grammar – Look and complete.','desc':'Nhìn tranh và hoàn thành câu','items':items})
# P11
P11=[('have / I / a / pen / .','I have a pen.',['Have I a pen.','I a have pen.','Pen I have a.']),
     ('do / you / have / a / book / ?','Do you have a book?',['You do have a book?','Do have you a book?','Do you a have book?']),
     ('in / your / What’s / school bag / ?','What’s in your school bag?',['What’s your in school bag?','In your what’s school bag?','What’s school bag in your?']),
     ('don’t / No / I / .','No, I don’t.',['I no don’t.','Don’t no I.','No, don’t I.']),
     ('is / my / This / school bag / .','This is my school bag.',['Is this my school bag.','This my is school bag.','My this is school bag.'])]
items=[Q('%d. Sắp xếp: %s'%(i+1,q),place(a,w),a,'Câu đúng: “%s”'%a) for i,(q,a,w) in enumerate(P11)]
sec.append({'id':'part11','icon':'🔀','title':'Part 11. Writing – Put the words in order.','desc':'Sắp xếp từ thành câu','items':items})
# P12
i12=u.crop(7,(42,162,788,745),'p12_pic')
P12=[('How many students are in the picture?',['Six.','Four.','Eight.'],'Six.','Đếm trong tranh có 6 bạn học sinh.'),
     ('Are there two rulers on the desks?',['Yes, there are.','No, there aren’t.','Yes, I do.'],'Yes, there are.','Trên các bàn có hai cây thước (một ở bàn giữa, một ở bàn bên phải).'),
     ('What does the girl with the book have?',['She has a book.','She has a school bag.','She has a ruler.'],'She has a book.','Bạn nữ ngồi bên trái đang cầm quyển sách bìa xanh lá.'),
     ('What’s on the desk on the left?',['A notebook, an eraser and a pen.','A pencil case and a ruler.','A school bag.'],'A notebook, an eraser and a pen.','Bàn bên trái có một quyển vở vàng, một cục tẩy và một cây bút mực.'),
     ('What is the boy asking?',['Do you have a ruler?','Do you have a pen?','What colour is it?'],'Do you have a ruler?','Bong bóng thoại của bạn nam: “Do you have a ruler?”'),
     ('Are the children happy?',['Yes, they are.','No, they aren’t.','Yes, I do.'],'Yes, they are.','Các bạn đều đang cười.')]
items=[Q('%d. %s'%(i+1,q),place(a,[x for x in o if x!=a]),a,e,img=i12) for i,(q,o,a,e) in enumerate(P12)]
sec.append({'id':'part12','icon':'🗣️','title':'Part 12. Speaking – Look at the picture and answer the questions.','desc':'Nhìn tranh và trả lời','items':items})
u.save({'id':'gs3_u8','title':'GLOBAL SUCCESS - UNIT 8: MY SCHOOL THINGS','badge':'Luyện Thi · Global Success','tag':'Global Success 3 · Unit 8','champTitle':'Thần Đồng Tiếng Anh','sections':sec})
