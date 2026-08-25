# -*- coding: utf-8 -*-
"""把 assets/*.svg 渲染为高清透明 PNG（Playwright 无头 Chromium）。

每个器械导出三种：
  png/<name>-standard.png  标准图（写实材质）
  png/<name>-outline.png   轮廓（仅描边）
  png/<name>-keypoints.png 关键点（红点 + 标签，填充变淡）
鼻部参考图只导出 png/<name>.png
"""
import pathlib
from playwright.sync_api import sync_playwright

ROOT = pathlib.Path(__file__).parent
ASSETS = ROOT / "assets"
OUT = ROOT / "png"
OUT.mkdir(exist_ok=True)

SCALE = 3
REFERENCE = {"nose-base-front", "nose-base-profile"}

MODE_JS = """(m) => {
  document.querySelectorAll('.fill').forEach(e => {
    e.style.display = (m === 'outline') ? 'none' : 'block';
    e.style.opacity = (m === 'kp') ? '0.35' : '';
  });
  document.querySelectorAll('.outline').forEach(e => {
    e.style.display = (m === 'outline') ? 'block' : 'none';
  });
  document.querySelectorAll('.kp').forEach(e => {
    e.style.display = (m === 'kp') ? 'block' : 'none';
  });
}"""


def wrap(svg_text: str) -> str:
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<style>html,body{margin:0;background:transparent}</style></head>'
            f'<body>{svg_text}</body></html>')


def main():
    svgs = sorted(ASSETS.glob("*.svg"))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(device_scale_factor=SCALE, viewport={"width": 800, "height": 500})
        page = ctx.new_page()
        for svg in svgs:
            txt = svg.read_text(encoding="utf-8")
            page.set_content(wrap(txt))
            page.wait_for_timeout(60)
            el = page.locator("svg").first
            if svg.stem in REFERENCE:
                el.screenshot(path=str(OUT / f"{svg.stem}.png"), omit_background=True)
                print("ref ", svg.stem)
                continue
            for mode in ("standard", "outline", "kp"):
                if mode != "standard":
                    page.evaluate(MODE_JS, mode)
                el.screenshot(path=str(OUT / f"{svg.stem}-{mode}.png"), omit_background=True)
                print("ok  ", svg.stem, mode)
        browser.close()
    print("done:", len(svgs), "svgs ->", OUT)


if __name__ == "__main__":
    main()
