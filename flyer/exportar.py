"""Exporta flyer-post.html a flyer-post.png (2160 × 2700, el doble de 1080 × 1350 para que se vea nítido).

Uso: python3 exportar.py   (necesita: pip install playwright && playwright install chromium)
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

here = Path(__file__).parent
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=2)
    page.goto((here / "flyer-post.html").resolve().as_uri())
    page.wait_for_timeout(500)
    page.screenshot(path=str(here / "flyer-post.png"))
    browser.close()
print("flyer-post.png listo")
