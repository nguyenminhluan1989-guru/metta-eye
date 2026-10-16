# Usage: python3 -I cutpose.py raw/  -> poses/luan-XX.png (raw files named 01.jpg ... 20.png)
import sys, os, re
from rembg import remove, new_session
from PIL import Image
src = sys.argv[1]; out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'poses')
s = new_session('isnet-general-use')
for f in sorted(os.listdir(src)):
    m = re.match(r'(\d{1,2})', f)
    if not m: continue
    code = m.group(1).zfill(2)
    im = Image.open(os.path.join(src, f)).convert('RGB')
    cut = remove(im, session=s, alpha_matting=True)
    bb = cut.getchannel('A').point(lambda a: 255 if a > 20 else 0).getbbox()
    cut = cut.crop(bb)
    # normalise: 1254px tall like luan.png, keep aspect
    r = 1254 / cut.height
    cut = cut.resize((round(cut.width * r), 1254), Image.LANCZOS)
    cut.save(os.path.join(out, f'luan-{code}.png')); print('ok', code, cut.size)
