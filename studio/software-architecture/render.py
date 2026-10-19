from pathlib import Path
import subprocess
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
slug='software-architecture-fieldbook'
dest=ROOT/'tmp/pdfs'/slug;dest.mkdir(parents=True,exist_ok=True)
subprocess.run(['pdftoppm','-scale-to','1000','-png',str(ROOT/'public/archive'/(slug+'.pdf')),str(dest/'page')],check=True)
pages=sorted(dest.glob('page-*.png'));assert len(pages)==84
for offset in range(0,84,12):
 sheet=Image.new('RGB',(1200,1311),'#e4e8e5');draw=ImageDraw.Draw(sheet)
 for j,path in enumerate(pages[offset:offset+12]):
  im=Image.open(path);im.thumbnail((286,405))
  x=j%4*300+7;y=j//4*437+23
  sheet.paste(im,(x,y));draw.text((x,y-17),f'Page {offset+j+1}',fill='#203c46')
 sheet.save(dest/f'sheet-{offset//12+1}.jpg',quality=94)
Image.open(pages[0]).save(ROOT/'public/archive/previews'/(slug+'.webp'),quality=92)
print('Rendered all 84 pages and 7 contact sheets')
