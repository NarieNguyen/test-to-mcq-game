#!/usr/bin/env python3
"""
build_game.py — dựng 1 file game HTML (mở offline, chấm điểm tự động) từ game.json + thư mục media.

Cách dùng:
  python3 tools/build_game.py game.json -o Game_TenBai.html
  python3 tools/build_game.py --suggest-marks media/part4.mp3     # gợi ý mốc thời gian trong audio

game.json viết ở dạng ĐỌC ĐƯỢC (đáp án là chữ thường). Script này lo: kiểm tra lỗi, băm đáp án,
mã hoá lời giải, nén ảnh, nhúng ảnh/audio, ghép vào engine/engine.html. Không sửa engine bằng tay.
Thoát với mã khác 0 nếu có LỖI (không được giao file khi còn lỗi).
"""
import argparse, base64, hashlib, html, io, json, os, re, shutil, subprocess, sys, unicodedata

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")

HERE = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(HERE, "..", "engine", "engine.html")
ANS_SALT = "wtg_v2_2026"          # PHẢI trùng với engine.html
M32 = 0xFFFFFFFF
ERR, WARN = [], []


# ---------- băm đáp án: bản Python của normalize()/cyrb53() trong engine ----------
def normalize(s):
    s = unicodedata.normalize("NFC", str(s or "")).strip().lower()
    s = s.replace("`", "'").replace("\u2019", "'")
    out = []
    for ch in s:
        cat = unicodedata.category(ch)
        out.append(ch if cat[0] in "LN" else " ")
    return " ".join("".join(out).split())


def _imul(a, b):
    return (a * b) & M32


def cyrb53(s, seed=0):
    h1 = (0xDEADBEEF ^ seed) & M32
    h2 = (0x41C6CE57 ^ seed) & M32
    # JS duyệt theo UTF-16 code unit
    units = s.encode("utf-16-le")
    for i in range(0, len(units), 2):
        ch = units[i] | (units[i + 1] << 8)
        h1 = _imul(h1 ^ ch, 2654435761)
        h2 = _imul(h2 ^ ch, 1597334677)
    h1 = _imul(h1 ^ (h1 >> 16), 2246822507) ^ _imul(h2 ^ (h2 >> 13), 3266489909)
    h2 = _imul(h2 ^ (h2 >> 16), 2246822507) ^ _imul(h1 ^ (h1 >> 13), 3266489909)
    h1 &= M32
    h2 &= M32
    return 4294967296 * (2097151 & h2) + h1


def hash_ans(val):
    return format(cyrb53(ANS_SALT + normalize(val)), "x")


def b64(s):
    return base64.b64encode(str(s).encode("utf-8")).decode("ascii")


# ---------- làm sạch văn bản: chỉ cho phép <b> <i> <u> <br> ----------
def clean(s):
    s = html.escape(str(s if s is not None else ""), quote=False)
    return re.sub(r"&lt;(/?)(b|i|u|br)\s*/?&gt;", lambda m: "<%s%s>" % (m.group(1), m.group(2)), s)


def plain(s):
    return re.sub(r"<[^>]+>", "", str(s))


# ---------- media ----------
class Media:
    def __init__(self, base, optimize=True):
        self.base, self.optimize = base, optimize
        self.map, self.by_digest, self.info = {}, {}, {}

    def add(self, rel, where, kind):
        if not rel:
            return None
        path = os.path.join(self.base, rel)
        if not os.path.isfile(path):
            ERR.append("%s: không thấy file %s" % (where, rel))
            return None
        raw = open(path, "rb").read()
        ext = os.path.splitext(rel)[1].lower()
        if kind == "image":
            raw, mime = self._image(raw, ext, where)
        else:
            raw, mime = self._audio(path, raw, ext, where)
        digest = hashlib.md5(raw).hexdigest()
        if digest not in self.by_digest:
            key = "m%d" % (len(self.map) + 1)
            self.by_digest[digest] = key
            self.map[key] = "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))
            self.info[key] = (rel, len(raw))
        return self.by_digest[digest]

    def _image(self, raw, ext, where):
        mimes = {".webp": "image/webp", ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif"}
        if ext not in mimes:
            ERR.append("%s: định dạng ảnh không hỗ trợ (%s)" % (where, ext))
            return raw, "image/png"
        if not self.optimize or ext == ".gif":
            return raw, mimes[ext]
        try:
            from PIL import Image
            im = Image.open(io.BytesIO(raw))
            if ext == ".webp" and im.width <= 1000 and len(raw) < 250_000:
                return raw, "image/webp"
            if im.width > 900:
                im = im.resize((900, round(im.height * 900 / im.width)), Image.LANCZOS)
            buf = io.BytesIO()
            im.convert("RGBA" if im.mode in ("RGBA", "LA", "P") else "RGB").save(buf, "WEBP", quality=82, method=6)
            return buf.getvalue(), "image/webp"
        except Exception as e:  # không có PIL -> giữ nguyên
            WARN.append("%s: không nén được ảnh (%s), giữ nguyên" % (where, e))
            return raw, mimes[ext]

    def _audio(self, path, raw, ext, where):
        if ext == ".mp3":
            return raw, "audio/mpeg"
        if ext == ".wav":
            if shutil.which("ffmpeg"):
                r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-b:a", "64k", "-f", "mp3", "-"], capture_output=True)
                if r.returncode == 0 and r.stdout:
                    return r.stdout, "audio/mpeg"
            return raw, "audio/wav"
        if shutil.which("ffmpeg"):
            r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-b:a", "64k", "-f", "mp3", "-"], capture_output=True)
            if r.returncode == 0 and r.stdout:
                return r.stdout, "audio/mpeg"
        ERR.append("%s: audio %s không phải mp3/wav và không có ffmpeg để đổi" % (where, ext))
        return raw, "audio/mpeg"


def audio_duration(path):
    try:
        import miniaudio
        return round(float(miniaudio.get_file_info(path).duration), 1)
    except Exception:
        pass
    if shutil.which("ffprobe"):
        r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True)
        try:
            return round(float(r.stdout.strip()), 1)
        except ValueError:
            pass
    if not os.path.exists(path):
        return 0
    if path.lower().endswith(".wav"):
        try:
            import wave
            with wave.open(path, "rb") as w:
                return round(w.getnframes() / float(w.getframerate()), 1)
        except Exception:
            pass
    if path.lower().endswith(".mp3"):
        try:
            import struct
            with open(path, "rb") as f:
                data = f.read()
            pos = 0
            while pos < len(data) - 4:
                if data[pos] == 0xff and (data[pos+1] & 0xe0) == 0xe0:
                    header = struct.unpack(">I", data[pos:pos+4])[0]
                    bitrate_idx = (header >> 12) & 0xf
                    bitrates = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320, 0]
                    br = bitrates[bitrate_idx]
                    if br > 0:
                        return round(len(data) * 8 / (br * 1000), 1)
                pos += 1
        except Exception:
            pass
    return 0


def suggest_marks(path):
    if not shutil.which("ffmpeg"):
        sys.exit("Cần ffmpeg để gợi ý mốc.")
    r = subprocess.run(["ffmpeg", "-i", path, "-af", "silencedetect=noise=-35dB:d=1.2", "-f", "null", "-"], capture_output=True, text=True)
    ends = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r.stderr)]
    print("Duration: %ss" % audio_duration(path))
    print("Các điểm giọng đọc bắt đầu lại sau quãng lặng ≥1.2s (ứng viên cho audioMarks/audioAt, 0 luôn là đầu bài):")
    print("  t = 0")
    for t in ends:
        print("  t = %.0f" % t)
    print("→ Nghe lại để đặt nhãn đúng (Câu 1, Câu 2... hoặc tên người nói). Không đoán nếu không chắc.")


# ---------- dựng ----------
def build(cfg_path, out_path, optimize):
    base = os.path.dirname(os.path.abspath(cfg_path))
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    media = Media(base, optimize)

    for k in ("id", "title", "sections"):
        if not cfg.get(k):
            ERR.append("game.json thiếu trường bắt buộc: %s" % k)
    if ERR:
        return None
    if not re.fullmatch(r"[a-z0-9_]+", cfg["id"]):
        ERR.append("id chỉ gồm chữ thường/số/gạch dưới (vd ta4_u3)")

    settings = {"secondsPerQuestion": 90, "basePoints": 100, "maxSpeedBonus": 50}
    settings.update(cfg.get("settings") or {})
    out = {
        "id": cfg["id"], "title": clean(cfg["title"]), "badge": clean(cfg.get("badge", "")),
        "tag": clean(cfg.get("tag", "")), "mascot": clean(cfg.get("mascot", "Cú Giáo Sư")),
        "champTitle": clean(cfg.get("champTitle", "Thần Đồng")), "settings": settings, "sections": [],
    }

    seen_ids, total, positions = set(), 0, []
    for si, sec in enumerate(cfg["sections"]):
        sid = sec.get("id") or "part%d" % (si + 1)
        W = "Phần %s" % sid
        if sid in seen_ids:
            ERR.append("%s: id phần bị trùng" % W)
        seen_ids.add(sid)
        if not sec.get("title"):
            ERR.append("%s: thiếu title" % W)
        o = {"id": sid, "icon": sec.get("icon", "📝"), "title": clean(sec.get("title", "")), "desc": clean(sec.get("desc", "")), "items": []}
        if sec.get("wordBank"):
            o["wordBank"] = [clean(w) for w in sec["wordBank"]]
        if sec.get("imgStyle"):
            o["imgStyle"] = sec["imgStyle"]
        dur = 0
        if sec.get("audio"):
            o["audio"] = media.add(sec["audio"], W + " audio", "audio")
            dur = audio_duration(os.path.join(base, sec["audio"]))
            o["duration"] = dur
            if sec.get("markLabel"):
                o["markLabel"] = clean(sec["markLabel"])
            marks = sec.get("audioMarks") or []
            for m in marks:
                if dur and not (0 <= m["t"] <= dur):
                    ERR.append("%s: mốc '%s' t=%s vượt độ dài audio %ss" % (W, m["label"], m["t"], dur))
            o["audioMarks"] = [{"label": clean(m["label"]), "t": m["t"]} for m in marks]

        ps = sec.get("passage")
        if ps:
            kind = ps.get("kind")
            if kind not in ("reading", "blanks", "dialogue"):
                ERR.append("%s: passage.kind phải là reading | blanks | dialogue" % W)
            p = {"kind": kind, "header": clean(ps.get("header", "")), "theme": ps.get("theme", "amber" if kind == "reading" else "blue")}
            if ps.get("img"):
                p["img"] = media.add(ps["img"], W + " passage.img", "image")
            if kind in ("reading", "blanks"):
                if not ps.get("paragraphs"):
                    ERR.append("%s: passage thiếu paragraphs" % W)
                p["paragraphs"] = [clean(x) for x in ps.get("paragraphs", [])]
            if kind == "blanks":
                nums = sorted(int(n) for n in re.findall(r"\{(\d+)\}", " ".join(ps.get("paragraphs", []))))
                n_items = len(sec.get("items", []))
                if nums != list(range(1, n_items + 1)):
                    ERR.append("%s: các chỗ trống {n} trong đoạn văn (%s) phải đúng là 1..%d (bằng số câu hỏi)" % (W, nums, n_items))
                if ps.get("note"):
                    p["note"] = clean(ps["note"])
            if kind == "dialogue":
                if not ps.get("lines"):
                    ERR.append("%s: passage thiếu lines" % W)
                p["lines"] = [{"who": clean(l["who"]), "text": clean(l["text"])} for l in ps.get("lines", [])]
            o["passage"] = p

        if not sec.get("items"):
            ERR.append("%s: không có câu hỏi" % W)
        for ii, it in enumerate(sec.get("items", [])):
            Q = "%s câu %d" % (W, ii + 1)
            opts = it.get("options") or []
            if not it.get("prompt"):
                ERR.append("%s: thiếu prompt" % Q)
            if not (2 <= len(opts) <= 4):
                ERR.append("%s: cần 2–4 đáp án (hiện %d)" % (Q, len(opts)))
            hashes = [hash_ans(plain(x)) for x in opts]
            if len(set(hashes)) != len(hashes):
                ERR.append("%s: có 2 đáp án trùng nhau sau chuẩn hoá (khác nhau chỉ ở dấu câu/hoa thường?)" % Q)
            ah = hash_ans(plain(it.get("answer", "")))
            if ah not in hashes:
                ERR.append("%s: answer %r không khớp đáp án nào trong options" % (Q, it.get("answer")))
                continue
            if not it.get("explain"):
                WARN.append("%s: thiếu explain (lời giải)" % Q)
            positions.append(hashes.index(ah))
            item = {
                "prompt": clean(it.get("prompt", "")), "img": media.add(it.get("img"), Q + " img", "image") if it.get("img") else None,
                "options": [{"text": clean(x), "hash": h} for x, h in zip(opts, hashes)],
                "ans": ah, "full": b64(clean(it.get("fullAnswer", it["answer"]))), "e": b64(clean(it.get("explain", ""))),
            }
            if it.get("audioAt") is not None:
                if not sec.get("audio"):
                    ERR.append("%s: có audioAt nhưng phần không có audio" % Q)
                elif dur and it["audioAt"] > dur:
                    ERR.append("%s: audioAt=%s vượt độ dài audio %ss" % (Q, it["audioAt"], dur))
                item["audioAt"] = it["audioAt"]
            o["items"].append(item)
        total += len(o["items"])
        out["sections"].append(o)

    out["totalQuestions"] = total
    if positions:
        top = max(positions.count(i) for i in range(4))
        if len(positions) >= 12 and top / len(positions) > 0.5:
            WARN.append("Vị trí đáp án đúng lệch (>50%% cùng 1 vị trí) — xáo lại options")
    if ERR:
        return None

    def js(o):
        return json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")

    eng = open(ENGINE, encoding="utf-8").read()
    badge = out["badge"]
    repl = {"__PAGE_TITLE__": plain(out["title"]), "__BADGE__": badge, "__HEADER_TITLE__": out["title"],
            "/*__WORKSHEET__*/null": js(out), "/*__MEDIA__*/{}": js(media.map)}
    for k, v in repl.items():
        if k not in eng:
            sys.exit("engine.html thiếu placeholder %s" % k)
        eng = eng.replace(k, v)
    open(out_path, "w", encoding="utf-8").write(eng)

    sz = os.path.getsize(out_path)
    if sz > 3_000_000:
        WARN.append("File game nặng %.1f MB (> 3.0 MB). Hãy kiểm tra xem có file audio WAV thô nào chưa được nén sang MP3 không!" % (sz / 1e6))

    print("✔ %s — %d phần, %d câu, %d file media, %.1f MB" % (out_path, len(out["sections"]), total, len(media.map), sz / 1e6))
    return out_path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config", nargs="?")
    ap.add_argument("-o", "--out")
    ap.add_argument("--no-optimize", action="store_true", help="không nén/đổi ảnh")
    ap.add_argument("--suggest-marks", metavar="AUDIO")
    a = ap.parse_args()
    if a.suggest_marks:
        return suggest_marks(a.suggest_marks)
    if not a.config:
        ap.error("thiếu game.json")
    out = a.out or "Game_" + re.sub(r"\W+", "_", os.path.splitext(os.path.basename(a.config))[0]) + ".html"
    res = build(a.config, out, not a.no_optimize)
    for w in WARN:
        print("⚠", w)
    for e in ERR:
        print("✘", e)
    if not res:
        sys.exit(1)


if __name__ == "__main__":
    main()
