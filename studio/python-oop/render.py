from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
ROOT = Path(__file__).resolve().parents[2]
DEST = ROOT/'tmp/pdfs/python-oop'
DEST.mkdir(parents=True, exist_ok=True)
subprocess.run(['pdftoppm','-scale-to','1000','-png', str(ROOT/'public/archive/python-oop.pdf'),str(DEST/'page')], check=True)
pages = sorted(DEST.glob('page-*.png'))
assert len(pages) == 80
for offset in range(0,80,16):
    sheet = Image.new('RGB',(1600,2352),'#dce2e2')
    draw = ImageDraw.Draw(sheet)
    for i,path in enumerate(pages[offset:offset+16]):
        im = Image.open(path)
        im.thumbnail((390,552))
        x, y = (i%4)*400+5, (i//4)*588+26
        sheet.paste(im,(x,y))
        draw.text((x,y-20),str(offset+i+1),fill='black')
    sheet.save(DEST/f'sheet-{offset//16+1}.jpg',quality=90)
Image.open(pages[0]).save(ROOT/'public/archive/previews/python-oop.webp',quality=92)
print('Rendered all 80 pages, five contact sheets and archive preview.')
