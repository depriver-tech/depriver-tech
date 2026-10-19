from pathlib import Path
import subprocess
from PIL import Image,ImageOps,ImageDraw
from concurrent.futures import ThreadPoolExecutor
ROOT=Path(__file__).resolve().parents[2]
DEST=ROOT/'tmp/pdfs/python-series'
slugs=['python-dsa','python-web','python-ai-ml','python-backend','python-automation']
def render(slug):
 folder=DEST/slug;folder.mkdir(parents=True,exist_ok=True)
 subprocess.run(['pdftoppm','-scale-to','850','-png',str(ROOT/'public/archive'/f'{slug}.pdf'),str(folder/'page')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
 pages=sorted(folder.glob('page-*.png'))
 assert len(pages)==64
 for offset in range(0,64,16):
  sheet=Image.new('RGB',(1000,1516),'#e8e8e8');draw=ImageDraw.Draw(sheet)
  for j,path in enumerate(pages[offset:offset+16]):
   im=Image.open(path);im.thumbnail((238,337))
   x=(j%4)*250+6;y=(j//4)*379+24
   sheet.paste(im,(x,y));draw.text((x,y-18),str(offset+j+1),fill='black')
  sheet.save(DEST/f'{slug}-sheet-{offset//16+1}.jpg',quality=92)
 cover=Image.open(pages[0]);cover.save(ROOT/'public/archive/previews'/f'{slug}.webp',quality=90)
 return slug
with ThreadPoolExecutor(max_workers=3) as pool:
 for slug in pool.map(render,slugs):print(slug, 'rendered',flush=True)
