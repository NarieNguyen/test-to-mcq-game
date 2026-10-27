import os, json, subprocess, glob, re, shutil
from PIL import Image

# Thư mục chứa file audio/PDF gốc người dùng gửi (tự động thích ứng cả Windows và Linux)
def _get_src_dir():
    if os.environ.get('SRC'):
        return os.environ['SRC'].rstrip('/\\') + '/'
    if os.path.exists('/mnt/user-data/attachments/'):
        return '/mnt/user-data/attachments/'
    return './'

A = _get_src_dir()
WORK = os.environ.get('WORK', './work').rstrip('/\\') + '/'

class Unit:
    def __init__(s, n):
        s.n = n
        s.dir = WORK + 'u%d/' % n
        os.makedirs(s.dir + 'media', exist_ok=True)
        s.cache = {}

    def crop(s, page, box, name):
        """box theo toạ độ ảnh 100dpi (827x1170); lưu webp vào media/"""
        path = s.dir + 'hi/p-%d.png' % page
        if not os.path.exists(path):
            path = s.dir + 'pages/p-%d.png' % page
        im = Image.open(path).convert('RGB')
        x0, y0, x1, y1 = [int(v * 2) for v in box]
        im.crop((x0, y0, x1, y1)).save(s.dir + 'media/%s.webp' % name, 'WEBP', quality=85)
        return 'media/%s.webp' % name

    def audio(s, pat, name):
        """
        Tìm và nạp audio MP3 chuẩn nhẹ.
        Tự động tìm kiếm file trong thư mục nguồn và thư mục hiện tại.
        Nếu file là WAV và không có ffmpeg, tự động tìm file MP3 tương ứng để tránh phình dung lượng.
        """
        matches = glob.glob(A + pat)
        if not matches:
            matches = glob.glob(pat)
        if not matches:
            # Tìm rộng hơn theo basename
            base_pat = os.path.basename(pat)
            matches = glob.glob('**/' + base_pat, recursive=True)
            
        if not matches:
            raise FileNotFoundError("Không tìm thấy file audio khớp với mẫu: %s" % pat)
            
        f = matches[0]
        out = s.dir + 'media/%s.mp3' % name
        
        # Nếu đã là MP3 và không cần convert hoặc không có ffmpeg
        if f.lower().endswith('.mp3'):
            shutil.copyfile(f, out)
            return 'media/%s.mp3' % name
            
        # Nếu là WAV, ưu tiên dùng ffmpeg nén sang 64k mono
        if shutil.which('ffmpeg'):
            subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f, '-ac', '1', '-b:a', '64k', out], check=True)
            return 'media/%s.mp3' % name
        else:
            # Không có ffmpeg trên Windows: tìm xem có file MP3 cùng tên hoặc liên quan không
            alt_mp3 = os.path.splitext(f)[0] + '.mp3'
            if os.path.exists(alt_mp3):
                shutil.copyfile(alt_mp3, out)
                return 'media/%s.mp3' % name
            # Kiểm tra trong thư mục gốc
            cand_mp3s = glob.glob(f"*{os.path.basename(os.path.splitext(f)[0])}*.mp3")
            if cand_mp3s:
                shutil.copyfile(cand_mp3s[0], out)
                return 'media/%s.mp3' % name
            
            # Cảnh báo nghiêm trọng nếu buộc phải copy WAV
            print(f"⚠️ CẢNH BÁO: Không có ffmpeg và không thấy file MP3 thay thế cho {f}. File WAV có thể làm game nặng > 3MB!")
            wav_out = s.dir + 'media/%s.wav' % name
            shutil.copyfile(f, wav_out)
            return 'media/%s.wav' % name

    def save(s, game):
        json.dump(game, open(s.dir + 'game.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
        n = sum(len(x['items']) for x in game['sections'])
        print('✔ game.json đã lưu:', len(game['sections']), 'phần,', n, 'câu')

def Q(prompt, options, answer, explain, img=None, audioAt=None):
    d = {'prompt': prompt, 'options': options, 'answer': answer, 'explain': explain}
    if img: d['img'] = img
    if audioAt is not None: d['audioAt'] = audioAt
    return d

_k = [0]
def place(correct, wrongs):
    """Chèn đáp án đúng luân phiên vị trí A, B, C, D để phân bố đều ~25%."""
    opts = list(wrongs)
    n = len(opts) + 1
    pos = _k[0] % n
    _k[0] += 1
    opts.insert(pos, correct)
    return opts

def _grid(self, page, boxes, name, cols=3, w=420):
    path = self.dir + 'hi/p-%d.png' % page
    if not os.path.exists(path):
        path = self.dir + 'pages/p-%d.png' % page
    im = Image.open(path).convert('RGB')
    tiles = []
    for b in boxes:
        t = im.crop(tuple(int(v * 2) for v in b))
        t = t.resize((w, round(t.height * w / t.width)))
        tiles.append(t)
    rows = [tiles[i:i + cols] for i in range(0, len(tiles), cols)]
    H = sum(max(t.height for t in r) for r in rows) + 8 * (len(rows) + 1)
    W = cols * w + 8 * (cols + 1)
    sh = Image.new('RGB', (W, H), 'white')
    y = 8
    for r in rows:
        x = 8
        for t in r:
            sh.paste(t, (x, y))
            x += w + 8
        y += max(t.height for t in r) + 8
    sh.save(self.dir + 'media/%s.webp' % name, 'WEBP', quality=85)
    return 'media/%s.webp' % name

Unit.grid = _grid

def _quad(self, page, y0, y1, x0, x1, name):
    q = (x1 - x0) / 4.0
    return self.grid(page, [(x0 + i * q, y0, x0 + (i + 1) * q, y1) for i in range(4)], name, cols=2, w=420)

Unit.quad = _quad
