"""
Captures high-resolution, pixel-perfect screenshots of the live React frontend.
Runs against the running Vite dev server on http://localhost:5173.
"""

from pathlib import Path
from playwright.sync_api import sync_playwright

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

PAGES_TO_CAPTURE = [
    ("react_overview.png", "http://localhost:5173/"),
    ("react_recommend.png", "http://localhost:5173/recommend"),
    ("react_yield.png", "http://localhost:5173/yield"),
    ("react_advisory.png", "http://localhost:5173/advisory"),
    ("react_financials.png", "http://localhost:5173/financials"),
    ("react_market.png", "http://localhost:5173/market"),
]


def capture_all():
    print("Launching Chrome via Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(executable_path=CHROME_PATH, headless=True)
        context = browser.new_context(
            viewport={"width": 1400, "height": 850},
            device_scale_factor=2,  # Retina high DPI for publication print
        )
        page = context.new_page()

        for filename, url in PAGES_TO_CAPTURE:
            print(f"Navigating to {url}...")
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(2000)  # Wait for animations and charts
                out_path = DOCS_DIR / filename
                page.screenshot(path=str(out_path))
                print(f" Saved: {out_path}")
            except Exception as e:
                print(f" Failed to capture {url}: {e}")

        browser.close()
    print("Screenshot capture complete!")


if __name__ == "__main__":
    capture_all()
