"""Build an 84-page illustrated architecture fieldbook and its practice kit."""
from pathlib import Path
from xml.sax.saxutils import escape
import json, math, shutil, zipfile
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from content import CHAPTERS
from references import REFS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'public/archive'
DELIVER=Path('/home/priver/Downloads/output/pdf')
DELIVER.mkdir(parents=True,exist_ok=True)
SLUG='software-architecture-fieldbook'
W,H=595.276,841.89
L,R=73,548
WIDTH=R-L
INK=HexColor('#243C4C');MUTED=HexColor('#61727A');PAPER=HexColor('#FBF8EF')
COLORS=['#245B6A','#32694F','#975533','#61507B']
PARTS=['FOUNDATIONS','SERVICES & EVENTS','DISTRIBUTED WORK','OPERATIONS & EVOLUTION']
for name,file in [('Hand','PatrickHand-Regular.ttf'),('Body','Poppins-Regular.ttf'),('Bold','Poppins-SemiBold.ttf'),('Code','LiberationMono-Regular.ttf')]:
 pdfmetrics.registerFont(TTFont(name,str(ROOT/'studio/fonts'/file)))

class Book:
 def __init__(self):
  self.c=canvas.Canvas(str(OUT/(SLUG+'.pdf')),pagesize=(W,H),pageCompression=1)
  self.c.setTitle('Software Architecture: The Practical Fieldbook')
  self.c.setAuthor('Privatus Cosmas (Priver)')
  self.c.setSubject('Monoliths, microservices, Kafka and real-world system design decisions')
  self.n=0;self.accent=HexColor(COLORS[0]);self.chapter=0
 def page(self,kind,chapter=0,anchor=None):
  if self.n:self.c.showPage()
  self.n+=1;self.chapter=chapter
  self.accent=HexColor(COLORS[min((max(chapter,1)-1)//6,3)])
  c=self.c;c.setFillColor(PAPER);c.rect(0,0,W,H,fill=1,stroke=0)
  c.setStrokeColor(HexColor('#E1E8E6'));c.setLineWidth(.4)
  for y in range(64,781,24):c.line(34,y,W-24,y)
  c.setStrokeColor(HexColor('#D6A49C'));c.setLineWidth(.65);c.line(58,48,58,H-30)
  c.setFillColor(self.accent);c.rect(W-12,642,12,112,fill=1,stroke=0)
  c.setFont('Bold',7.5);c.drawString(L,H-35,'DEPRIVER / SOFTWARE ARCHITECTURE')
  c.setFont('Body',7);c.drawRightString(R,H-35,kind.upper())
  c.setStrokeColor(self.accent);c.line(L,48,R,48)
  c.setFillColor(MUTED);c.setFont('Body',7);c.drawString(L,31,'Privatus Cosmas / Priver · depriver.tech')
  c.drawRightString(R,31,f'{self.n:02d} / 84')
  self.y=H-76
  if anchor:c.bookmarkPage(anchor)
 def p(self,text,size=10.8,leading=17.5,font='Body',color=None,gap=12):
  style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=color or INK)
  obj=Paragraph(escape(text).replace('\n','<br/>'),style)
  _,h=obj.wrap(WIDTH,1000)
  if self.y-h<66:raise ValueError(f'Overflow p{self.n}: {text[:65]} -> {self.y-h}')
  obj.drawOn(self.c,L,self.y-h);self.y-=h+gap
 def h(self,text):self.p(text,30,33,'Hand',self.accent,18)
 def label(self,text):self.p(text,8,12,'Bold',self.accent,7)
 def note(self,title,text):
  self.label(title);self.p(text,10.2,16.7,gap=15)
 def code(self,text,label='TERMINAL'):
  lines=text.splitlines();size=9.1
  maxw=max(pdfmetrics.stringWidth(x,'Code',size) for x in lines)
  size=min(size,size*(WIDTH-24)/maxw) if maxw else size
  assert size>=8,(self.n,size)
  h=30+13*len(lines)
  assert self.y-h>65
  c=self.c;c.setFillColor(HexColor('#EDF1EF'));c.roundRect(L,self.y-h,WIDTH,h,5,fill=1,stroke=0)
  c.setFillColor(self.accent);c.setFont('Bold',7);c.drawString(L+12,self.y-14,label)
  c.setFillColor(INK);c.setFont('Code',size)
  for i,line in enumerate(lines):c.drawString(L+12,self.y-31-i*13,line)
  self.y-=h+16
 def box(self,x,y,w,h,text,fill='#F0E6BD',size=13):
  c=self.c;c.setFillColor(HexColor(fill));c.setStrokeColor(self.accent);c.setLineWidth(.9)
  c.roundRect(x,y,w,h,6,fill=1,stroke=1)
  p=Paragraph(escape(text),ParagraphStyle('box',fontName='Hand',fontSize=size,leading=size+2,textColor=INK,alignment=1))
  _,ph=p.wrap(w-12,h)
  assert ph<h-6,(self.n,text)
  p.drawOn(c,x+6,y+(h-ph)/2)
 def arrow(self,x1,y1,x2,y2,label=None):
  c=self.c;c.setStrokeColor(self.accent);c.setLineWidth(1);c.line(x1,y1,x2,y2)
  a=math.atan2(y2-y1,x2-x1)
  for d in [-.5,.5]:c.line(x2,y2,x2-6*math.cos(a+d),y2-6*math.sin(a+d))
  if label:
   c.setFont('Body',6.5);c.setFillColor(MUTED);c.drawCentredString((x1+x2)/2,(y1+y2)/2+6,label)
 def diagram(self,i,ch):
  y=self.y-108
  if i==10:
   self.box(L,y+29,113,44,'Order committed');self.box(L+155,y+29,120,44,'OrderPlaced')
   self.box(L+325,y+57,150,44,'Notifications');self.box(L+325,y-1,150,44,'Analytics')
   self.arrow(L+113,y+51,L+155,y+51,'publish')
   self.arrow(L+275,y+51,L+325,y+79);self.arrow(L+275,y+51,L+325,y+21)
  elif i==11:
   for j in range(2):
    yy=y+58-j*55
    self.c.setFillColor(self.accent);self.c.setFont('Bold',8);self.c.drawString(L,yy+15,f'P{j}')
    for k in range(4):
     self.box(L+42+k*91,yy,76,35,f'offset {k}',fill='#E7EEE7',size=12)
     if k<3:self.arrow(L+118+k*91,yy+17,L+133+k*91,yy+17)
  elif i==12:
   self.box(L,y+29,120,48,'Topic: P0 / P1 / P2')
   self.box(L+182,y+60,128,40,'Group A: worker 1')
   self.box(L+182,y+3,128,40,'Group A: worker 2')
   self.box(L+344,y+29,131,48,'Group B: all partitions')
   self.arrow(L+120,y+55,L+182,y+80,'P0, P1')
   self.arrow(L+120,y+48,L+182,y+23,'P2')
   # Independent group shown below the assignments, not fed by group A.
   self.arrow(L+60,y+29,L+60,y-15)
   self.arrow(L+60,y-15,L+409,y-15)
   self.arrow(L+409,y-15,L+409,y+29)
  elif i==15:
   self.box(L,y+35,112,44,'Reserved')
   self.box(L+182,y+35,112,44,'Payment result')
   self.box(L+352,y+66,123,40,'Settled: confirm')
   self.box(L+352,y+15,123,40,'Rejected: release')
   self.box(L+172,y-22,132,36,'Unknown: reconcile',fill='#F6E0CC')
   self.arrow(L+112,y+57,L+182,y+57)
   self.arrow(L+294,y+63,L+352,y+86);self.arrow(L+294,y+51,L+352,y+35)
   self.arrow(L+238,y+35,L+238,y+14)
  elif i==5:
   self.box(L,y+30,120,48,'Checkout workflow')
   for j,t in enumerate(['Orders API','Inventory API','Payments API']):
    self.box(L+205+j*88,y+31,80,46,t,size=12)
    self.arrow(L+120,y+54,L+205+j*88,y+54) if j==0 else None
   # Ownership interfaces, not a serial chain.
   self.arrow(L+60,y+30,L+60,y+4);self.arrow(L+60,y+4,L+421,y+4)
   self.arrow(L+333,y+4,L+333,y+31);self.arrow(L+421,y+4,L+421,y+31)
  else:
   bw=104;step=(WIDTH-bw)/3
   for j,text in enumerate(ch['nodes']):
    x=L+j*step;self.box(x,y+25,bw,55,text,size=13)
    if j<3:self.arrow(x+bw,y+52,x+step,y+52)
   if i==14:
    self.c.setStrokeColor(self.accent);self.c.setDash(3,2)
    self.c.roundRect(L-5,y+15,step+bw+10,76,6,fill=0,stroke=1);self.c.setDash()
  self.y=y-38 if i in [12,15] else y-9
  self.p(ch['caption'],9,14,color=MUTED,gap=14)
 def table(self,rows):
  widths=[130,160,WIDTH-290]
  style=ParagraphStyle('cell',fontName='Body',fontSize=9.1,leading=14,textColor=INK)
  data=[[Paragraph(escape(str(s)),style) for s in row] for row in [['CHOICE','WHAT IT HELPS','WHAT IT COSTS']]+rows]
  t=Table(data,colWidths=widths,hAlign='LEFT')
  t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),HexColor('#E1E9E5')),('BACKGROUND',(0,1),(-1,-1),HexColor('#F7F4E9')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),10),('BOTTOMPADDING',(0,0),(-1,-1),10),('LINEBELOW',(0,0),(-1,-1),.45,HexColor('#C3D1CB'))]))
  _,h=t.wrap(WIDTH,1000)
  assert self.y-h>65,(self.n,h)
  t.drawOn(self.c,L,self.y-h);self.y-=h+20
 def reference_links(self,keys):
  self.label('READ FURTHER')
  for key in keys:
   title,url=REFS[key];top=self.y
   self.p(f'[{key}] {title}',8,12,color=MUTED,gap=3)
   self.c.linkURL(url,(L,self.y,R,top),relative=0,thickness=0)
 def cover(self):
  self.page('The practical fieldbook',anchor='cover')
  self.y=H-120;self.label('A NOTEBOOK FOR BUILDING SYSTEMS THAT MAKE SENSE')
  self.p('Software\nArchitecture',53,55,'Hand',self.accent,16)
  self.p('Monoliths, microservices, Kafka\nand the decisions between them.',21,26,'Hand',INK,15)
  self.p('84 pages / 24 chapters / illustrated cases / practical labs',8.5,14,'Bold',self.accent,20)
  y=292
  self.box(L,y+62,142,57,'A clear application',size=19)
  self.box(L+188,y+62,108,57,'Event log',size=19)
  self.box(L+344,y+98,131,48,'Fulfilment',size=17)
  self.box(L+344,y+27,131,48,'Analytics',size=17)
  self.arrow(L+142,y+90,L+188,y+90,'facts')
  self.arrow(L+296,y+95,L+344,y+122)
  self.arrow(L+296,y+85,L+344,y+51)
  self.y=282
  self.p('Start with the problem.\nDraw the boundary. Test the failure.',25,30,'Hand',self.accent,20)
  self.p('PRIVATUS COSMAS / PRIVER',10,16,'Bold',self.accent,5)
  self.p('depriver.tech / First edition / October 2026',9,14,color=MUTED)
 def front(self):
  self.cover()
  self.page('How to use this book',anchor='start');self.h('A practical way to learn')
  self.p('This book is for developers who can build a small application and now want to understand how larger systems are organised. You do not need previous Kafka or cloud experience. Basic Python and SQL help with the optional labs.')
  self.note('THREE PAGES PER CHAPTER','First understand the idea and read its diagram. Next study a concrete case and compare the choices. Finally attempt a design task before reading the worked answer. Several designs can be reasonable; the explanation matters.')
  self.note('REAL-WORLD PROBLEMS, FICTIONAL CASES','Soko Market, the school portal, ticketing service and logistics platform are teaching scenarios. They model common engineering problems, but they are not reports of named companies. All workload figures are illustrative unless explicitly described as a lab result.')
  self.note('WHAT IS TESTED','The companion Python/SQLite lab has 16 passing automated tests. It models crash windows, duplicate handling, offset gaps and saga transitions. It is not a running distributed platform. The optional real Kafka exercise is documented separately and was not executed here.')
  self.note('HOW TO READ THE PICTURES','The small diagrams are conceptual views. Arrows show the relationship described by each caption; they are not complete network or deployment specifications. The Kafka and saga chapters include more specific partition, group and failure-branch sketches.')
  self.p('Use the clickable contents to navigate. Source keys link to official documentation or original authors; the complete bibliography is on pages 83-84. Keep a separate notebook for your own decisions.',size=10,leading=16)
  for start in [0,12]:
   self.page('Contents / '+str(start//12+1),anchor='contents'+str(start));self.h('Your route through the book')
   self.p('Foundations before infrastructure. Decisions before diagrams become deployments.',font='Hand',size=18,leading=23,gap=20)
   for idx in range(start,start+12):
    if idx%6==0:self.label(PARTS[idx//6])
    ch=CHAPTERS[idx];y=self.y
    self.p(f'{idx+1:02d}  {ch["title"]}',10,17,gap=14)
    self.c.setFillColor(self.accent);self.c.setFont('Bold',9)
    self.c.drawRightString(R,y-12,str(6+idx*3))
    self.c.linkRect('',f'ch{idx+1}',(L,self.y,R,y+2),relative=0,thickness=0)
   self.y-=7
   self.p('Glossary 78-79 / Local lab 80 / Kafka lab 81 / Decision template 82 / Sources 83-84',8.8,14)
  self.page('Meet the case',anchor='case');self.h('Soko Market: the journey')
  self.p('A shopper buys a router from a marketplace in Tanzania. The app must accept the order, reserve stock, reconcile payment and arrange fulfilment. A mobile connection can fail at any point. Support still needs to explain what happened.')
  self.label('A FIRST-RELEASE RUNTIME VIEW')
  y=self.y-185
  self.box(L,y+116,108,49,'Shopper browser')
  self.box(L+166,y+116,143,49,'Modular application')
  self.box(L+365,y+116,110,49,'Order database')
  self.box(L+166,y+27,143,49,'Background worker')
  self.box(L+365,y+27,110,49,'Payment provider')
  self.arrow(L+108,y+141,L+166,y+141,'HTTP')
  self.arrow(L+309,y+141,L+365,y+141,'SQL')
  self.arrow(L+237,y+76,L+237,y+116,'module calls')
  self.arrow(L+309,y+51,L+365,y+51,'request / query')
  self.y=y+3
  self.p('The provider is external. Its authenticated callback returns to the application through a separate HTTP route, omitted here for clarity. The worker loads durable work; it is not merely an untracked thread.',9,14,color=MUTED,gap=17)
  self.note('THE INVARIANTS','Stock never becomes negative. A logical payment attempt must not create unintended duplicate charges. A confirmed order has durable evidence. A timeout preserves uncertainty until reconciliation establishes the result.')
  self.note('THE EVOLUTION','Begin with explicit modules and a relational store. Introduce asynchronous delivery when slow or independent work warrants it. Extract a service when ownership, scaling or release evidence justifies the new network boundary.')
  self.p('The book repeatedly asks: what changes, who owns it, and what happens when it fails?',18,24,'Hand',self.accent)
 def chapters(self):
  for i,ch in enumerate(CHAPTERS,1):
   self.page(f'{i:02d} / Understand',i,f'ch{i}')
   self.c.addOutlineEntry(f'{i:02d}. {ch["title"]}',f'ch{i}',level=0,closed=False)
   self.label(PARTS[(i-1)//6]);self.h(ch['title'])
   self.p(ch['goal'],10.6,17,'Bold',gap=16)
   for para in ch['concept']:self.p(para)
   self.diagram(i,ch)
   self.page(f'{i:02d} / In practice',i);self.h('The decision in practice')
   self.label(ch['title'].upper());self.p(ch['case'],11,18,gap=20)
   self.label('COMPARE THE CHOICES');self.table(ch['choices'])
   self.note('FAILURE TO THINK THROUGH',ch['failure'])
   self.reference_links(ch['refs'])
   self.page(f'{i:02d} / Design workshop',i);self.h('Make the decision yourself')
   self.label('YOUR TASK');self.p(ch['task'],11.2,18.5,gap=20)
   self.label('WORKED ANSWER / COMPARE AFTER YOUR ATTEMPT')
   for para in ch['answer']:self.p(para,10.7,17.5)
   self.label('REVIEW YOUR DESIGN')
   for check in ch['checks']:self.p('[  ] '+check,10,16,gap=8)
   self.y-=6;self.p('My assumption to test next:',17,22,'Hand',self.accent,gap=6)
   # Real writing area for the reader, aligned to notebook rules.
   for j in range(2):
    y=self.y-20-j*23
    if y>70:self.c.setStrokeColor(HexColor('#A8BBB7'));self.c.line(L,y,R,y)
 def glossary(self):
  terms=[
  ('ADR','Architecture decision record: context, options, decision, consequences and review trigger.'),
  ('Bounded context','A boundary within which a domain model and its language have a specific meaning. It is not automatically one service.'),
  ('Invariant','A rule that must remain true, such as a stock balance never becoming negative.'),
  ('Monolith','One application deployment unit; it can contain modules and run as multiple instances.'),
  ('Modular monolith','One deployable application with explicit internal ownership and interface boundaries.'),
  ('Microservice','An independently deployable capability with an explicit contract and operational ownership.'),
  ('Port / adapter','An application-facing interface and a technology-specific implementation of that interface.'),
  ('Command / event','A request to perform work / a fact describing work or change that has occurred.'),
  ('Synchronous / asynchronous','The caller waits in the interaction / completion can occur separately and be observed later.'),
  ('Partition / offset','An ordered Kafka log / a position within that partition.'),
  ('Consumer group','A conventional group shares partition assignments and tracks progress independently of other groups.'),
  ('Idempotency','Repeating the same logical operation does not add an unintended extra effect.'),
  ('Outbox','Publication intent stored atomically with local business changes, then delivered by a relay.'),
  ('Saga / compensation','A coordinated sequence of local steps / a business action that addresses an earlier step\'s consequences.'),
  ('Projection / CQRS','A derived read view / separation of command-side and query-side responsibilities or models.'),
  ('Event sourcing','Using a history of domain events as authoritative state, rather than only publishing notifications from CRUD state.'),
  ('Backpressure / bulkhead','A mechanism to slow demand / a capacity boundary that limits the impact of one workload.'),
  ('SLI / SLO','An observed service indicator / the target set for that indicator over a defined window.'),
  ('RTO / RPO','Target time to restore service / acceptable data-loss interval. Both need recovery evidence.'),
  ('Reconciliation','Comparing authoritative records and resolving missing, conflicting or uncertain outcomes.'),
  ]
  for start in [0,10]:
   self.page('Reference / glossary');self.h('The vocabulary, made plain')
   for term,meaning in terms[start:start+10]:
    self.label(term.upper());self.p(meaning,10,16,gap=13)
 def appendices(self):
  self.glossary()
  self.page('Lab / tested local model',anchor='lab');self.h('See the failure, then fix it')
  self.p('Extract the companion ZIP and open its folder in a terminal. The local lab needs Python 3.11-compatible syntax and the standard library only; execution was checked on Python 3.14.7. No credentials or network are required.')
  self.code('python architecture_lab.py\npython -m unittest test_architecture_lab -v')
  self.code('Deliveries: 2; new fulfilments: 1\nNext safe offset: 11\nAfter a payment timeout: payment_unknown','EXPECTED DEMO OUTPUT')
  self.note('FOLLOW THE STATE','place_order commits an order and outbox intent together. relay_once publishes to a simulated transport. Its injected crash leaves the row pending, so retry delivers the same event again. consume commits its identity check and fulfilment effect together.')
  self.note('WHAT TO EXPERIMENT WITH','Open test_architecture_lab.py. Read the producer rollback, publish-crash and consumer rollback tests. Predict the final row counts before running them. Then add a lost-publish-response test and a policy for late settlement after reservation expiry.')
  self.note('THE LIMIT OF THE MODEL','All 16 tests passed locally. The transport is an in-memory list, the relay is single-worker, and saga transitions are pure functions. This does not validate Kafka failover, concurrent relays, network policy, production durability or load handling.')
  self.page('Lab / optional real Kafka');self.h('Observe a real event log')
  self.p('Use the official Apache quickstart to start a disposable local broker. The companion kafka-lab.md contains the complete commands. This exercise was checked against documentation but was not executed in the authoring environment.')
  self.note('1 / CREATE A TOPIC','Create architecture-orders-lab with three partitions. The local exercise uses replication factor one; it cannot demonstrate replicated availability. Describe the topic and confirm the partition count.')
  self.note('2 / PRODUCE WITH KEYS','Send O-42:OrderPlaced, O-42:PaymentSettled and O-43:OrderPlaced with key parsing enabled. Observe where the two O-42 records land under the unchanged keyed partitioning setup. Do not substitute Python\'s built-in hash for Kafka\'s partitioner.')
  self.note('3 / COMPARE CONSUMERS','Run two conventional consumers in architecture-a and inspect their partition assignments. Start architecture-b to observe independent progress. Print keys, partitions and offsets. Do not assume display order across partitions is a total event order.')
  self.note('4 / REPLAY DELIBERATELY','Use a new group identity for the replay exercise. --from-beginning does not override valid existing committed offsets. Before replaying a real consumer, identify which external effects could repeat and how they are controlled.')
  self.reference_links(['KLAB','KCONSUMER'])
  self.p('Record observations separately from expectations. A console demo is evidence about that setup, not proof of an end-to-end production guarantee.',font='Hand',size=18,leading=24)
  self.page('Template / architecture review');self.h('A decision worth keeping')
  self.p('Copy adr-template.md from the practice kit. Use this structure for the capstone or a real project. Keep facts, assumptions and test results distinguishable.')
  items=[('CONTEXT','Who needs what? What workload, team size and constraints are known?'),('INVARIANTS','Which facts must remain true under concurrency and failure?'),('ALTERNATIVES','Compare at least two plausible options with fair benefits and costs.'),('DECISION','Explain why the chosen option fits the present problem.'),('OWNERSHIP','Name data owners, trust boundaries and operational responsibilities.'),('FAILURE & RECOVERY','Trace timeout, duplicate, partial commit, dependency loss and restore.'),('EVIDENCE','Attach test results, measurements and drills. Label untested assumptions.'),('REVIEW TRIGGER','State the observation that would justify changing the decision.')]
  for title,text in items:self.note(title,text)
  self.p('A useful architecture can be explained, tested and revised.',21,26,'Hand',self.accent)
  refs=list(REFS.items())
  for start in [0,12]:
   self.page('Sources / '+str(start//12+1));self.h('Read the original sources')
   self.p('Primary documentation and original authors, checked for this edition in October 2026. Links are clickable. Cases, diagrams and worked answers in this book are original teaching material.',8.7,14,gap=15)
   for key,(title,url) in refs[start:start+12]:
    top=self.y;self.p(f'[{key}] {title}',8.8,13,'Bold',self.accent,gap=2)
    self.p(url,7.8,11.5,color=MUTED,gap=11)
    self.c.linkURL(url,(L,self.y,R,top),relative=0,thickness=0)
 def build(self):
  self.front();self.chapters();self.appendices();assert self.n==84,self.n
  self.c.save();shutil.copy2(OUT/(SLUG+'.pdf'),DELIVER/(SLUG+'.pdf'))

def export_text():
 lines=['# Software Architecture: The Practical Fieldbook','Privatus Cosmas (Priver) / depriver.tech','Fictional teaching scenarios; illustrative workload figures. See README.md for validation limits.']
 for i,ch in enumerate(CHAPTERS,1):
  lines += [f'## {i}. {ch["title"]}',ch['goal'],*ch['concept'],'Concept labels: '+', '.join(ch['nodes']),ch['caption'],'### Case',ch['case'],'### Choices']
  lines += [' | '.join(row) for row in ch['choices']]
  lines += ['### Failure to consider',ch['failure'],'### Task',ch['task'],'### Worked answer',*ch['answer'],'### Checks',*['- '+x for x in ch['checks']]]
  lines += ['References: '+', '.join(f'[{key}]({REFS[key][1]})' for key in ch['refs'])]
 (HERE/'practice/book-text.md').write_text('\n\n'.join(lines)+'\n')

if __name__=='__main__':
 Book().build();export_text()
 with zipfile.ZipFile(OUT/(SLUG+'-practice.zip'),'w',zipfile.ZIP_DEFLATED) as z:
  for path in sorted((HERE/'practice').glob('*')):
   if path.is_file():z.write(path,SLUG+'/'+path.name)
 shutil.copy2(OUT/(SLUG+'-practice.zip'),DELIVER.parent/(SLUG+'-practice.zip'))
 print('Built 84 pages / 24 chapters / practice kit')
