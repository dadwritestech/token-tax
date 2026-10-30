"""Render site/ to PNGs for the README. Needs the site served at BASE (python -m http.server)."""
import sys
from playwright.sync_api import sync_playwright

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8791"
OUT = "docs"

with sync_playwright() as p:
    b = p.chromium.launch()
    for scheme in ("light", "dark"):
        pg = b.new_page(viewport={"width": 1180, "height": 900}, device_scale_factor=2, color_scheme=scheme)
        pg.goto(f"{BASE}/index.html#llama-3" if scheme == "dark" else f"{BASE}/index.html")
        pg.wait_for_timeout(500)
        pg.locator("#hero-card").screenshot(path=f"{OUT}/headline-{scheme}.png")
        if scheme == "light":
            pg.locator(".card").nth(1).screenshot(path=f"{OUT}/bars.png")
            pg.locator(".card").nth(2).screenshot(path=f"{OUT}/heatmap.png")
        pg.close()
    pg = b.new_page(viewport={"width": 1180, "height": 1000}, device_scale_factor=1.5, color_scheme="light")
    pg.goto(f"{BASE}/calculator.html")
    pg.wait_for_function("document.querySelectorAll('#out tr').length > 8", timeout=120000)
    pg.screenshot(path=f"{OUT}/calculator.png", full_page=True)
    b.close()
print("ok")
