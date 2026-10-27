// Chạy thử game như học sinh (jsdom): node tools/test_game.js Game.html
// Kiểm tra: làm đúng hết = 10 điểm; làm sai/hết giờ vào danh sách ôn; mọi ảnh/audio nhúng được; không lộ đáp án dạng chữ ở trường dữ liệu.
const fs = require("fs");
const { JSDOM } = require(process.env.JSDOM_PATH || "jsdom");
const file = process.argv[2];
const mode = process.argv[3] || "all";
if (!file) { console.error("Usage: node test_game.js Game.html"); process.exit(2); }
const raw = fs.readFileSync(file, "utf8");
let fails = 0; const ok = (c, m) => { if (!c) { fails++; console.log("✘", m); } };

function boot() {
  const dom = new JSDOM(raw, { runScripts: "dangerously", pretendToBeVisual: true, url: "https://example.test/", beforeParse(w) {
    w.HTMLMediaElement.prototype.play = function () { return Promise.resolve(); };
    w.HTMLMediaElement.prototype.pause = function () {};
    w.Audio = function (src) { const a = w.document.createElement("audio"); a.src = src; return a; };
  }});
  return dom;
}
function run(dom, fn) { return dom.window.eval("(" + fn.toString() + ")()"); }

// ---- 1. Làm đúng toàn bộ
{
  const dom = boot(); const w = dom.window;
  w.document.getElementById("inputStudentName").value = "Test HS";
  w.submitStudentInfo();
  const total = run(dom, () => WORKSHEET.sections.reduce((a, s) => a + s.items.length, 0));
  let n = 0, safety = 0;
  while (safety++ < 500) {
    if (w.document.querySelector(".btn-opt") === null) break;
    const info = run(dom, () => { const it = CUR.items[CUR.itemIdx]; return { idx: it.options.findIndex(o => o.hash === it.ans) }; });
    w.selectChoice(info.idx);
    const eb = w.document.getElementById("explBox").className;
    ok(/correct-theme/.test(eb), `câu ${n + 1}: chọn đáp án đúng nhưng không báo đúng`);
    n++; w.nextItem();
  }
  const txt = w.document.getElementById("dynamicView").textContent;
  ok(n === total, `đã làm ${n}/${total} câu`);
  ok(txt.includes(`${total} / ${total}`) && txt.includes("10.0"), "tổng kết không đạt 10.0 khi đúng hết");
  ok(!/Danh Sách Câu Cần Ôn/.test(txt), "không được có danh sách sai khi đúng hết");
  run(dom, () => { clearTimer(); });
  console.log(`[đúng hết] ${n}/${total} câu, tổng kết OK=${fails === 0}`);
}
// ---- 2. Sai 1 câu mỗi phần + hết giờ 1 câu
{
  const dom = boot(); const w = dom.window;
  w.document.getElementById("inputStudentName").value = "Sai Het";
  w.submitStudentInfo();
  let wrongExpected = 0, safety = 0, first = true;
  while (safety++ < 500 && w.document.querySelector(".btn-opt")) {
    const info = run(dom, () => { const it = CUR.items[CUR.itemIdx]; return { c: it.options.findIndex(o => o.hash === it.ans), n: it.options.length, i: CUR.itemIdx }; });
    if (info.i === 0) {
      if (first) { w.timeOut(); first = false; } else { w.selectChoice((info.c + 1) % info.n); }
      wrongExpected++;
    } else w.selectChoice(info.c);
    w.nextItem();
  }
  const wl = run(dom, () => WRONG_LOG.length);
  ok(wl === wrongExpected, `WRONG_LOG=${wl}, kỳ vọng ${wrongExpected}`);
  const txt = w.document.getElementById("dynamicView").textContent;
  ok(txt.includes(`(${wrongExpected} câu)`), "danh sách ôn lại không hiển thị đúng số câu");
  ok(/Đáp án đúng/.test(txt), "danh sách ôn lại thiếu 'Đáp án đúng'");
  run(dom, () => { clearTimer(); });
  console.log(`[sai/hết giờ] ${wl} câu vào danh sách ôn`);
}
// ---- 3. Media + hiển thị từng phần
{
  const dom = boot(); const w = dom.window;
  w.document.getElementById("inputStudentName").value = "Xem";
  w.submitStudentInfo();
  const rendered = run(dom, () => {
    let c = 0, empty = 0;
    WORKSHEET.sections.forEach((sec, si) => {
      startSection(si, false);
      for (let i = 0; i < CUR.items.length; i++) {
        CUR.itemIdx = i; renderItem(); c++;
        if (!document.querySelector(".prompt-text") || document.querySelectorAll(".btn-opt").length < 2) empty++;
      }
    });
    clearTimer();
    return { c, empty };
  });
  ok(rendered.empty === 0, `${rendered.empty} câu hiển thị thiếu nội dung`);
  const media = run(dom, () => MEDIA);
  let bad = 0;
  const refs = run(dom, () => { const r = []; WORKSHEET.sections.forEach(s => { if (s.audio) r.push(s.audio); if (s.passage && s.passage.img) r.push(s.passage.img); s.items.forEach(i => { if (i.img) r.push(i.img); }); }); return r; });
  refs.forEach(k => { if (!media[k] || !media[k].startsWith("data:")) bad++; });
  ok(bad === 0, `${bad} tham chiếu media không có dữ liệu`);
  console.log(`[media] ${refs.length} tham chiếu, ${Object.keys(media).length} file nhúng`);
}
// ---- 4. Không lộ đáp án
{
  const dom = boot();
  const leaks = run(dom, () => {
    const out = [];
    WORKSHEET.sections.forEach(s => s.items.forEach((it, i) => {
      if ("answer" in it || "explain" in it) out.push(s.id + "#" + (i + 1) + " còn trường plaintext");
      try { const full = atob(it.full); if (full && it.options.length && !full.length) out.push("full rỗng"); } catch (e) { out.push("full không phải base64"); }
    }));
    return out;
  });
  ok(leaks.length === 0, "lộ dữ liệu: " + leaks.slice(0, 3).join("; "));
  console.log(`[bảo mật] trường answer/explain dạng chữ: ${leaks.length ? "CÓ" : "không"} (đáp án đúng chỉ lưu dạng băm)`);
}
console.log(fails ? `\n✘ ${fails} lỗi` : "\n✔ Tất cả kiểm tra đạt");
process.exit(fails ? 1 : 0);
