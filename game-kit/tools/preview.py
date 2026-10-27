#!/usr/bin/env python3
"""Chụp màn hình điện thoại (390x844) cho từng phần của game để kiểm tra bố cục bằng mắt.
   python3 tools/preview.py Game.html preview_dir [chỉ_số_phần ...]"""
import sys, os
from playwright.sync_api import sync_playwright
f, out = os.path.abspath(sys.argv[1]), sys.argv[2]
only = [int(x) for x in sys.argv[3:]]
os.makedirs(out, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 390, "height": 844}, device_scale_factor=1)
    errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto("file://" + f)
    pg.screenshot(path=out + "/00_nhap_ten.png")
    pg.fill("#inputStudentName", "Học sinh thử")
    pg.evaluate("submitStudentInfo()")
    pg.evaluate("renderHome()")
    pg.screenshot(path=out + "/01_muc_luc.png", full_page=True)
    n = pg.evaluate("WORKSHEET.sections.length")
    for i in (only or range(n)):
        pg.evaluate("(i)=>{startSection(i,false); clearTimer();}", i)
        pg.screenshot(path=out + "/sec%02d.png" % (i + 1), full_page=True)
    # màn tổng kết (đúng hết)
    pg.evaluate("""()=>{startWorksheet();clearTimer();
      WORKSHEET.sections.forEach((s,si)=>{CUR.secIdx=si;CUR.sec=s;CUR.items=s.items;CUR.correct=s.items.length-(si==0?1:0);CUR.points=s.items.length*130;finishSection&&0;
        SECTION_RESULTS.push({title:s.title,correct:CUR.correct,total:s.items.length,points:CUR.points});});
      WRONG_LOG.push({secTitle:'x',prompt:'1. Ví dụ câu sai',full:'Monday',expl:'Giải thích mẫu'});renderSummary();}""")
    pg.screenshot(path=out + "/99_tong_ket.png", full_page=True)
    b.close()
print("Lỗi JS:", errs if errs else "không")
print("Ảnh trong:", out)
