from pathlib import Path
import re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Preformatted, Table, TableStyle, KeepTogether
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Circle, Polygon, Path as VectorPath
from reportlab.lib.pagesizes import A4

NAVY=colors.HexColor('#142b35'); GREEN=colors.HexColor('#366958'); PALE=colors.HexColor('#eef4f1'); MUTED=colors.HexColor('#52636a')
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='BodyNote',fontName='Helvetica',fontSize=10,leading=15,textColor=NAVY,spaceAfter=9))
styles.add(ParagraphStyle(name='Lesson',fontName='Helvetica-Bold',fontSize=14,leading=18,textColor=GREEN,spaceBefore=16,spaceAfter=8,keepWithNext=True))
styles.add(ParagraphStyle(name='ChapterName',fontName='Helvetica-Bold',fontSize=24,leading=29,textColor=NAVY,spaceBefore=8,spaceAfter=16,keepWithNext=True))
styles.add(ParagraphStyle(name='SmallNote',fontName='Helvetica',fontSize=8.2,leading=11.5,textColor=MUTED,spaceAfter=7))
styles.add(ParagraphStyle(name='CodeNote',fontName='Courier',fontSize=8.4,leading=12,textColor=NAVY,backColor=PALE,borderPadding=10,spaceBefore=5,spaceAfter=12))
styles.add(ParagraphStyle(name='Question',parent=styles['BodyNote'],leftIndent=18,firstLineIndent=-18,spaceAfter=8))
styles.add(ParagraphStyle(name='CellNote',fontName='Helvetica',fontSize=8.2,leading=11,textColor=NAVY))
styles.add(ParagraphStyle(name='TOCEntry',fontName='Helvetica',fontSize=10,leading=14,leftIndent=0,firstLineIndent=0,spaceBefore=7))

def clean(text):
    text=text.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')
    text=html.escape(text)
    # Add readable, clickable links without reproducing external text.
    text=re.sub(r'(https?://[^\s]+)',lambda m:'<link href="'+m[0].rstrip('.,')+'" color="#366958">'+m[0].rstrip('.,')+'</link>'+('' if m[0][-1] not in '.,' else m[0][-1]),text)
    return text

class Book(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name=='ChapterName':
            text=flowable.getPlainText()
            if text == 'Your study map': return
            key='chapter-'+str(self.page)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(text,key,level=0,closed=False)
            self.notify('TOCEntry',(0,text,self.page,key))

def arrow(d,x1,y1,x2,y2,label=None):
    d.add(Line(x1,y1,x2,y2,strokeColor=GREEN,strokeWidth=1.3))
    if x2>=x1: pts=[x2,y2,x2-6,y2+3,x2-6,y2-3]
    else: pts=[x2,y2,x2+6,y2+3,x2+6,y2-3]
    d.add(Polygon(pts,fillColor=GREEN,strokeColor=GREEN))
    if label:d.add(String((x1+x2)/2,(y1+y2)/2+7,label,fontName='Helvetica',fontSize=8,fillColor=MUTED,textAnchor='middle'))

def diagram(index):
    d=Drawing(480,105)
    if index==3:
        for x,label in [(155,'E'),(325,'O')]:
            d.add(Circle(x,48,23,strokeColor=GREEN,fillColor=PALE,strokeWidth=1.5))
            if label=='E':d.add(Circle(x,48,19,strokeColor=GREEN,fillColor=None))
            d.add(String(x,44,label,textAnchor='middle',fontName='Helvetica-Bold',fontSize=12,fillColor=NAVY))
            d.add(String(x,85,'0: stay',textAnchor='middle',fontSize=8,fillColor=MUTED))
        arrow(d,178,57,302,57,'1: toggle');arrow(d,302,38,178,38)
        arrow(d,95,48,131,48,'start')
        d.add(String(240,8,'Even number of 1s: start in E, accept E.',textAnchor='middle',fontSize=8,fillColor=MUTED))
    elif index==7:
        d.add(Line(55,45,425,45,strokeColor=GREEN,strokeWidth=1.5))
        for x,label,drop in [(170,'2 kOhm','4 V'),(310,'4 kOhm','8 V')]:
            d.add(Rect(x-32,33,64,24,fillColor=PALE,strokeColor=GREEN))
            d.add(String(x,41,label,textAnchor='middle',fontSize=9,fillColor=NAVY))
            d.add(String(x,16,drop,textAnchor='middle',fontSize=8,fillColor=MUTED))
        d.add(String(55,70,'12 V',fontSize=10,fillColor=NAVY))
        d.add(String(410,70,'0 V',fontSize=10,fillColor=NAVY))
        arrow(d,205,82,275,82,'I = 2 mA')
    else:
        labels={1:['Function','Rate of change','Accumulation'],2:['Audience','Evidence','Action'],4:['Ready','Running','Blocked'],5:['Source code','Compiler + linker','Executable'],6:['Defined inputs','Logic / state','Defined outputs']}[index]
        for j,label in enumerate(labels):
            x=15+j*165
            d.add(Rect(x,30,140,45,rx=9,ry=9,fillColor=PALE,strokeColor=GREEN))
            d.add(String(x+70,48,label,textAnchor='middle',fontName='Helvetica-Bold',fontSize=9,fillColor=NAVY))
            if j<2:arrow(d,x+140,52,x+159,52)
        if index==4:
            d.add(String(240,8,'Selected transitions only: dispatch, wait; completion returns blocked work to ready.',textAnchor='middle',fontSize=7.5,fillColor=MUTED))
    return d

def markdown(path,include_h1=True):
    lines=path.read_text().splitlines(); flows=[]; i=0; buffer=[]
    def flush():
        if buffer:
            flows.append(Paragraph(clean(' '.join(buffer)),styles['BodyNote']));buffer.clear()
    while i<len(lines):
        line=lines[i]
        if line.startswith('```'):
            flush(); code=[];i+=1
            while i<len(lines) and not lines[i].startswith('```'):code.append(lines[i]);i+=1
            flows.append(Preformatted('\n'.join(code),styles['CodeNote'],maxLineLength=83,splitChars=' '))
        elif line.startswith('# '):
            flush()
            if include_h1:flows.append(Paragraph(clean(line[2:]),styles['ChapterName']))
        elif line.startswith('## '):
            flush();flows.append(Paragraph(clean(line[3:]),styles['Lesson']))
        elif line.startswith('|'):
            flush();rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.fullmatch(r'[-: ]+',x or '-') for x in cells):rows.append([Paragraph(clean(c),styles['CellNote']) for c in cells])
                i+=1
            i-=1
            if rows:
                widths=[480/len(rows[0])]*len(rows[0]);t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
                t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),PALE),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.6,GREEN),('LINEBELOW',(0,1),(-1,-1),.25,colors.HexColor('#d7e2dc')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]));flows.extend([t,Spacer(1,10)])
        elif re.match(r'^\d+\. ',line):
            flush();flows.append(Paragraph(clean(line),styles['Question']))
        elif line.startswith('- '):
            flush();flows.append(Paragraph('&#8226; '+clean(line[2:]),styles['BodyNote']))
        elif not line.strip():flush()
        else:buffer.append(line)
        i+=1
    flush();return flows

pagew,pageh=A4

def page(canvas,doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#d7e2dc'));canvas.setLineWidth(.5)
    canvas.line(56,43,pagew-56,43)
    canvas.setFont('Helvetica',8);canvas.setFillColor(MUTED)
    canvas.drawString(56,30,'PRIVATUS COSMAS / COMPUTER SCIENCE FOUNDATIONS')
    canvas.drawRightString(pagew-56,30,str(doc.page))
    if doc.page>1:
        canvas.setFont('Helvetica',7);canvas.drawString(56,pageh-28,'SEMESTER ONE / INDEPENDENT STUDY EDITION')
    canvas.restoreState()
