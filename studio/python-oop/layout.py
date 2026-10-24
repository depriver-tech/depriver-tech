"""Notebook renderer adapted from the existing depriver.tech Python series."""
import importlib, json, re, shutil, zipfile
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, Color, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
OUT=ROOT/'public/archive'
DELIVER=Path('/home/priver/Downloads/output/pdf')
DELIVER.mkdir(parents=True,exist_ok=True)
for name,file in [('Hand','PatrickHand-Regular.ttf'),('Body','Poppins-Regular.ttf'),('Bold','Poppins-SemiBold.ttf'),('Code','LiberationMono-Regular.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(ROOT/'studio/fonts'/file)))
W,H=595.276,841.89
LEFT,RIGHT=78,548
WIDTH=RIGHT-LEFT
INK=HexColor('#203A50'); MUTED=HexColor('#596976'); PAPER=HexColor('#FBF7ED')
MANIFEST=[]

class Notebook:
    def __init__(self,book):
        self.b=book; self.n=0; self.accent=HexColor(book['color'])
        self.path=OUT/(book['slug']+'.pdf')
        self.c=canvas.Canvas(str(self.path),pagesize=(W,H),pageCompression=1)
        self.c.setTitle(book['title']+' | The practical notebook')
        self.c.setAuthor('Privatus Cosmas (Priver) · depriver.tech')
        self.c.setSubject('24 guided lessons, worked examples, practice and explained answers')
    def page(self,kind,chapter=None):
        if self.n: self.c.showPage()
        self.n+=1; c=self.c
        c.setFillColor(PAPER); c.rect(0,0,W,H,fill=1,stroke=0)
        c.setStrokeColor(HexColor('#DFE7E8')); c.setLineWidth(.45)
        for y in range(58,775,23):c.line(38,y,W-27,y)
        c.setStrokeColor(HexColor('#DCAAA2')); c.setLineWidth(.7); c.line(62,48,62,H-40)
        c.setFillColor(self.accent); c.roundRect(W-18,660,25,90,4,fill=1,stroke=0)
        c.setFont('Bold',8); c.setFillColor(self.accent)
        c.drawString(LEFT,H-37,'DEPRIVER / PYTHON FIELD NOTES')
        c.setFont('Body',7.5);c.drawRightString(RIGHT,H-37,kind.upper())
        c.setStrokeColor(self.accent);c.line(LEFT,48,RIGHT,48)
        c.setFont('Body',7);c.setFillColor(MUTED);c.drawString(LEFT,32,self.b['title']+' / Privatus Cosmas')
        c.drawRightString(RIGHT,32,f'{self.n:02d} / 80')
        self.y=H-80
        if chapter:
            c.bookmarkPage(chapter)
    def text(self,text,size=10.2,leading=16.7,font='Body',color=INK,space=12):
        style=ParagraphStyle('p',fontName=font,fontSize=size,leading=leading,textColor=color)
        p=Paragraph(escape(text).replace('\n','<br/>'),style)
        _,height=p.wrap(WIDTH,1000)
        if self.y-height<65:raise ValueError(f'Overflow {self.b["slug"]} page{self.n}: {text[:60]} ({self.y-height})')
        p.drawOn(self.c,LEFT,self.y-height);self.y-=height+space
    def heading(self,text):self.text(text,size=29,leading=32,font='Hand',color=self.accent,space=18)
    def label(self,text):self.text(text,size=8,leading=12,font='Bold',color=self.accent,space=7)
    def code(self,code,label):
        lines=code.splitlines();size=9.0
        longest=max(pdfmetrics.stringWidth(line,'Code',size) for line in lines)
        if longest>WIDTH-24:size*= (WIDTH-24)/longest
        if size<7.8:raise ValueError(f'Code too small: {size} {self.n}')
        lead=12.5; height=30+lead*len(lines)
        if self.y-height<65:raise ValueError(f'Code overflow {self.n}')
        c=self.c;c.setFillColor(HexColor('#EEF1EF'));c.setStrokeColor(HexColor('#CBD6D4'))
        c.roundRect(LEFT-2,self.y-height,WIDTH+4,height,5,fill=1,stroke=1)
        c.setFont('Bold',7);c.setFillColor(self.accent);c.drawString(LEFT+10,self.y-14,label)
        c.setFont('Code',size);c.setFillColor(INK)
        for i,line in enumerate(lines):c.drawString(LEFT+10,self.y-31-i*lead,line)
        self.y-=height+14
    def callout(self,title,text):
        self.label(title);self.text(text,size=9.4,leading=15,space=12)
    def cover(self):
        self.page('Beginner to advanced')
        self.y=H-123
        self.text('THE PRACTICAL NOTEBOOK',9,14,'Bold',self.accent,22)
        self.text(self.b['title'],42,47,'Hand',self.accent,18)
        self.text(self.b['subtitle'],16,24,'Hand',INK,26)
        self.text('80 pages  /  24 guided lessons  /  48 code files',9,15,'Bold',self.accent,24)
        c=self.c
        # A compact, topic-specific learning diagram, drawn as ink on paper.
        labels={'python-oop':['OBJECTS','CONTRACTS','DESIGN','TESTS'], 'python-dsa':['INPUT','STRUCTURE','ALGORITHM','RESULT'],
        'python-web':['BROWSER','REQUEST','PYTHON','PAGE'],
        'python-backend':['CLIENT','API','SERVICE','DATA'],
        'python-ai-ml':['DATA','MODEL','EVALUATE','IMPROVE'],
        'python-automation':['PLAN','PREVIEW','RUN','VERIFY']}[self.b['slug']]
        y=366;boxw=99
        for i,label in enumerate(labels):
            x=LEFT+i*121
            c.setFillColor(HexColor('#F2E3AD'));c.setStrokeColor(self.accent)
            c.roundRect(x,y,boxw,46,7,fill=1,stroke=1)
            c.setFillColor(self.accent);c.setFont('Hand',16);c.drawCentredString(x+boxw/2,y+16,label)
            if i<3:
                c.line(x+boxw+3,y+23,x+117,y+23);c.line(x+113,y+27,x+117,y+23);c.line(x+113,y+19,x+117,y+23)
        self.y=318
        self.text('Understand it. Try it. Explain it.',23,28,'Hand',self.accent,18)
        self.text(self.b['intro'],10.2,17,space=20)
        self.text('PRIVATUS COSMAS / PRIVER',9,15,'Bold',self.accent,5)
        self.text('depriver.tech  ·  First edition / October 2026',8.5,14,space=0)
    def contents(self):
        self.page('Your route');self.heading('Your 24-lesson route')
        self.text('Work in order, or use this clickable map to revisit a topic. Each lesson has a learn page, a practice page and an explained solution.',space=18)
        for i,l in enumerate(self.b['lessons'],1):
            page=4+(i-1)*3; y=self.y
            c=self.c;c.setFillColor(self.accent);c.setFont('Bold',9);c.drawString(LEFT,y-11,f'{i:02d}')
            c.setFillColor(INK);c.setFont('Body',9.2);c.drawString(LEFT+29,y-11,l['title'])
            c.setFont('Body',8.5);c.drawRightString(RIGHT,y-11,str(page))
            c.linkRect('',f'lesson{i}',(LEFT,y-20,RIGHT,y+2),relative=0,thickness=0)
            self.y-=21
        self.y-=10;self.text('Setup and study method · 3     References and study aids · 76-80',8.5,14)
    def setup(self):
        self.page('Start here');self.heading('Make this book yours')
        self.label('BEFORE YOU START');self.text(self.b['prerequisite'])
        self.label('YOUR WORKSPACE');self.text(self.b['setup'])
        self.code(self.b['install'],'TERMINAL / FOLLOW THE COMMANDS FOR THIS BOOK')
        self.label('A SIMPLE STUDY RHYTHM')
        self.text('1. Read: predict what the example will do before running it.\n2. Practise: write your answer using the acceptance cases.\n3. Compare: read the solution, explain the difference, then extend it.',space=14)
        self.text('The companion ZIP contains lesson_01_example.py through lesson_24_example.py and matching solution files. Run them from the extracted folder; lesson 24 uses capstone.py. Most successful checks are silent; a traceback means a check failed.',size=9.7,leading=16)
        self.callout('READABLE NOTES, PRECISE CODE','Handwritten headings keep the notebook feel; body text and code use clear fonts. Copy runnable code from the ZIP to preserve indentation. The PDF is searchable and its contents links are clickable.')
    def lessons(self):
        for i,l in enumerate(self.b['lessons'],1):
            self.page(f'{i:02d} / Learn',f'lesson{i}');self.heading(l['title'])
            self.label('THE GOAL');self.text(l['goal'],font='Bold',size=10,leading=16,space=12)
            self.text(l['concept'])
            self.code(l['code'],f'lesson_{i:02d}_example.py')
            self.text(l['explain'],size=9.5,leading=15)
            self.callout('WATCH FOR THIS',l['pitfall'])
            self.page(f'{i:02d} / Practise');self.heading('Your turn: '+l['title'])
            self.label('THE CHALLENGE');self.text(l['task'],size=11,leading=18,space=20)
            self.label('ACCEPTANCE CHECKS')
            for case in l['cases']:self.text('[  ]  '+case,size=10,leading=17,space=8)
            self.y-=6;self.callout('A NUDGE, IF YOU NEED ONE',l['hint'])
            self.label('TRACE BEFORE YOU CODE')
            c=self.c;top=self.y;rh=32;cw=WIDTH/3
            c.setFillColor(HexColor('#E8ECE6'));c.rect(LEFT,top-27,WIDTH,27,fill=1,stroke=0)
            c.setStrokeColor(HexColor('#AABDBB'));c.setLineWidth(.6)
            for j in range(5):c.line(LEFT,top-27-j*rh,RIGHT,top-27-j*rh)
            for j in range(4):c.line(LEFT+j*cw,top,LEFT+j*cw,top-27-4*rh)
            c.setFillColor(self.accent);c.setFont('Bold',7.5)
            for j,t in enumerate(['INPUT / STATE','PREDICTED RESULT','ACTUAL / WHY']):c.drawString(LEFT+j*cw+7,top-17,t)
            self.y=top-27-4*rh-22
            self.label('EXPLAIN YOUR APPROACH')
            self.text('Write the steps in plain language. Include one edge case and why your approach handles it.',size=9.5,leading=15)
            self.text('Try the task before turning the page. Your first attempt is part of the lesson.',font='Hand',size=16,leading=21)
            self.page(f'{i:02d} / Solution');self.heading('One clear solution')
            self.label(l['title'].upper())
            self.code(l['solution'],f'lesson_{i:02d}_solution.py')
            self.label('WHY IT WORKS');self.text(l['answer'],size=10.2,leading=17)
            self.callout('TAKE IT FURTHER',l['extension'])
            self.label('CHECK YOUR UNDERSTANDING')
            self.text('Can you explain the important decision in this solution? Change one input and predict the result. Add an assertion for that case, then run the file again.',size=9.5,leading=16)
    def references(self):
        self.page('Keep learning');self.heading('Sources & next steps')
        self.text('Use these official references when you need the full API contract or a deeper explanation. Documentation can evolve; check the version used by your own environment.',size=10,leading=17)
        for title,url in self.b['refs']:
            before=self.y;self.text(title,10,15,'Bold',self.accent,3);self.text(url,8,13,space=13)
            self.c.linkURL(url,(LEFT,self.y,RIGHT,before),relative=0,thickness=0)
        self.callout('WHAT THE CHECKS ESTABLISH','All 48 companion scripts were executed independently during preparation. Their assertions check the small fixtures shown here. They do not establish production readiness, security under attack, browser accessibility or performance at scale.')
        self.callout('YOUR NEXT PROJECT','Choose a small problem you can explain. Write its inputs, outputs and success checks. Build a minimal version, test one failure path, and ask another learner to follow your README. Record what you would improve next.')
        self.text('Keep your notes. Keep experimenting.',23,28,'Hand',self.accent)
    def finish(self):
        self.cover();self.contents();self.setup();self.lessons();self.references()
        assert self.n==80
        self.c.save();shutil.copy2(self.path,DELIVER/self.path.name)

def companions(b):
    folder=HERE/'generated'/b['slug'];folder.mkdir(parents=True,exist_ok=True)
    md=[f"# {b['title']}",b['intro'],'## Setup',b['setup'],'```sh',b['install'],'```']
    for i,l in enumerate(b['lessons'],1):
        for kind,key in [('example','code'),('solution','solution')]:
            (folder/f'lesson_{i:02d}_{kind}.py').write_text(f'# {b["title"]}: {l["title"]}\n'+l[key]+'\n')
        md.extend([f'## {i}. {l["title"]}',l['goal'],l['concept'],'```python',l['code'],'```',l['explain'],'### Practice',l['task'],*['- '+x for x in l['cases']],'Hint: '+l['hint'],'### Solution','```python',l['solution'],'```',l['answer'],'Watch for: '+l['pitfall'],'Extension: '+l['extension']])
    (folder/'lesson.md').write_text('\n\n'.join(md)+'\n')
    (folder/'README.md').write_text(f'''# {b['title']} - practice files

By Privatus Cosmas (Priver), depriver.tech. Companion to the 80-page notebook.

## Setup

{b['setup']}

```sh
{b['install']}
```

Create a virtual environment before installing third-party packages:

```sh
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1
```

There are 24 example scripts and 24 matching solutions. Run each file on its own.
Most successful checks print nothing; a failed assertion produces a traceback.
Read the lesson before its solution. lesson.md provides the complete text.

These are local educational fixtures. No live service credentials are needed.
Tests establish the demonstrated examples, not production readiness. Browser,
network, deployment and security review remain separate work for a real app.

## Official references

'''+ '\n'.join(f'- [{t}]({u})' for t,u in b['refs'])+'\n')
    with zipfile.ZipFile(OUT/(b['slug']+'-practice.zip'),'w',zipfile.ZIP_DEFLATED) as z:
        for file in sorted(folder.iterdir()):z.write(file,b['slug']+'/'+file.name)

