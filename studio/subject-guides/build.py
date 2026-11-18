"""Build original subject/session notes, seven PDFs and the editable companion archive.
Run with a Python environment containing reportlab and pypdf.
"""
from pathlib import Path
import json, re, zipfile
from pypdf import PdfReader
from session_enrichment import EXTRAS
from renderer import *
styles['BodyNote'].leading=13
styles['BodyNote'].spaceAfter=6
styles['Lesson'].fontSize=12
styles['Lesson'].leading=15
styles['Lesson'].spaceBefore=11
styles['Lesson'].spaceAfter=6
styles['ChapterName'].fontSize=22
styles['ChapterName'].leading=26
SOURCE=Path(__file__).resolve().parent
REPO=SOURCE.parents[1]
PUBLIC=REPO/'public/guides/subjects'
CONTENT=REPO/'src/content/study'
PUBLIC.mkdir(parents=True,exist_ok=True)
CONTENT.mkdir(parents=True,exist_ok=True)
modules=[]
for idx,path in enumerate(sorted((SOURCE/'notes').glob('*.md'))):
    text=path.read_text()
    code,title=text.splitlines()[0][2:].split(' | ',1)
    slug=path.stem[3:]
    sections=re.split(r'^## Lesson (\d+) \| (.+)\n',text,flags=re.M)
    assert len(sections)==25 and len(EXTRAS[idx])==8
    intro=sections[0].split('## Learning outcomes and route\n',1)[1].strip()
    intro=intro.replace('Lessons 1-8','Sessions 1-8').replace('eight lessons','eight sessions')
    final=sections[-1]
    practice_start=final.index('\n## Practice set')
    sections[-1]=final[:practice_start]
    appendix=final[practice_start:].strip()
    resource=appendix.split('## Mastery checkpoint and further study',1)[-1].strip()
    folder=PUBLIC/slug
    folder.mkdir(exist_ok=True)
    session_meta=[]
    session_bodies=[]
    for i in range(8):
        number=int(sections[1+i*3]); heading=sections[2+i*3]
        notes=sections[3+i*3].strip()
        objective,extension,task,answer=EXTRAS[idx][i]
        prerequisite='Recall the key definition and one example from the previous session before continuing.' if i else 'Read the module preparation notes and identify any prerequisite you need to revise.'
        body=f'''# Session {number:02d} | {heading}

## What you should be able to do
{objective}

## Preparation and session plan
{prerequisite} Allow about 75 minutes, including an independent attempt and correction. This is a proposed study session, not a university timetable.

## Core notes and worked example
{notes}

## Reasoning in more depth
{extension}

## Independent task | Attempt before reading the answer
{task}

## Worked answer and marking points
{answer}

## Review and progression
Explain the objective from memory. Change one task input and justify the new answer. Record a correction and retry after a day and a week.
'''
        front={'title':heading,'module':slug,'code':code,'number':number,'objective':objective}
        # JSON is valid YAML for each scalar and avoids quoting ambiguities.
        fm='---\n'+'\n'.join(k+': '+json.dumps(v) for k,v in front.items())+'\n---\n'
        content_dir=CONTENT/slug;content_dir.mkdir(exist_ok=True)
        # Page layout supplies the single h1; content starts at its first section.
        (content_dir/f'session-{number:02d}.md').write_text(fm+body.split('\n',1)[1])
        (folder/f'session-{number:02d}.md').write_text(body)
        session_meta.append({'number':number,'title':heading,'objective':objective,'href':f'/study/{slug}/session-{number:02d}/'})
        session_bodies.append(body)
    scope='Original independent foundation notes. Module names follow the supplied MUST Prospectus 2025/2026; these sessions are not lecturer-issued outlines or a claim of complete current examination coverage. Check sequence and depth against current teaching. Edition: 18 November 2026.'
    module_md=f'# {code} | {title}\n\n{scope}\n\n## Module route and preparation\n{intro}\n\n## Session map\n'+'\n'.join(f'{s["number"]}. {s["title"]}' for s in session_meta)+'\n\n'+'\n\n'.join(session_bodies)+'\n\n'+appendix+'\n'
    (folder/'notes.md').write_text(module_md)
    # Render separate subject book. Page breaks establish a clear session boundary.
    flows=[Spacer(1,30),Paragraph('PRIVATUS COSMAS / SUBJECT STUDY GUIDES',styles['SmallNote']),Spacer(1,28),Paragraph(clean(title),styles['ChapterName']),Paragraph(clean(code+' / SEMESTER ONE'),styles['Lesson']),Spacer(1,18),Paragraph('Eight guided sessions, original worked examples, session tasks and answers, plus a twelve-question module practice set.',styles['BodyNote']),diagram(idx+1),Spacer(1,20),Paragraph(clean(scope),styles['SmallNote']),PageBreak(),Paragraph('Your study map',styles['ChapterName'])]
    toc=TableOfContents();toc.levelStyles=[styles['TOCEntry']];flows += [toc,Spacer(1,15),Paragraph('Module route and preparation',styles['Lesson']),Paragraph(clean(intro),styles['BodyNote']),PageBreak()]
    for i in range(8):
        session_path=folder/f'session-{i+1:02d}.md'
        flows.extend(markdown(session_path));flows.append(PageBreak())
    appendix_path=folder/'.appendix.md';appendix_path.write_text('# Module practice and further study\n\n'+appendix)
    flows.extend(markdown(appendix_path));appendix_path.unlink()
    pdf=folder/f'{slug}.pdf'
    doc=Book(str(pdf),pagesize=A4,rightMargin=56,leftMargin=56,topMargin=50,bottomMargin=58,title=title+' - Independent Session Notes',author='Privatus Cosmas',subject=code+' / eight independent foundation sessions')
    doc.multiBuild(flows,onFirstPage=page,onLaterPages=page)
    reader=PdfReader(pdf);assert all(p.extract_text().strip() for p in reader.pages)
    modules.append({'slug':slug,'code':code,'title':title,'description':intro.split('\n')[0],'sessions':session_meta,'pages':len(reader.pages),'pdf':f'/guides/subjects/{slug}/{slug}.pdf','notes':f'/guides/subjects/{slug}/notes.md','resources':resource})
(CONTENT.parent.parent/'data/subjects.json').write_text(json.dumps(modules,indent=2)+'\n')
(PUBLIC/'README.md').write_text('# Semester-one subject guides\n\nSeven separate foundation guides; eight independent study sessions each. Read in order, attempt tasks before answers, then complete each module practice set. The numbered sessions are a proposed self-study sequence, not official lecture dates. Match this edition to your current lecturer outlines.\n\n'+ '\n'.join(f'- {m["code"]}: {m["title"]} ({m["pages"]} pages)' for m in modules)+'\n\nRead online: https://depriver.tech/study/\n')
with zipfile.ZipFile(PUBLIC/'semester-one-subject-guides.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted(PUBLIC.rglob('*')):
        if p.is_file() and p.suffix in ('.pdf','.md'):
            z.write(p,'semester-one-subject-guides/'+str(p.relative_to(PUBLIC)))
print(json.dumps([{'subject':m['title'],'pages':m['pages'],'sessions':len(m['sessions'])} for m in modules],indent=2))
