import sys, asyncio
from playwright.async_api import async_playwright
SRC, OUT = sys.argv[1], sys.argv[2]
HDR = """<div style="width:100%;font-family:Archivo,sans-serif;font-weight:600;font-size:6pt;
 letter-spacing:.18em;text-transform:uppercase;color:#9C8A6E;padding:0 18mm;
 display:flex;justify-content:space-between;align-items:flex-end;margin:0 0 2.4mm;">
 <span>Sultan Hanafi Royal Schools &middot; Academic Board</span>
 <span>Temporary Textbook Adoption Register &middot; 2026/2027</span></div>"""
FTR = """<div style="width:100%;padding:0;margin:3.4mm 0 0;">
 <div style="border-top:.5px solid #E0D2B8;padding-top:2.2mm;display:flex;
  justify-content:space-between;align-items:center;font-family:Archivo,sans-serif;
  font-weight:600;font-size:6pt;letter-spacing:.18em;text-transform:uppercase;color:#9C8A6E;">
  <span>SHRS/ACB/TTA-01</span>
  <span style="font-family:Amiri,serif;font-weight:700;font-size:10pt;color:#2A1C10;
   letter-spacing:0;text-transform:none;"><span class="pageNumber"></span></span>
  <span style="font-family:'Noto Kufi Arabic',sans-serif;font-size:6.4pt;letter-spacing:0;
   text-transform:none;color:#9A8A76;">للاعتماد &mdash; غير معتمدة بعد</span></div></div>"""
async def main():
    async with async_playwright() as p:
        import glob, os
        pin = sorted(glob.glob('/opt/pw-browsers/chromium*/chrome-linux/chrome'))
        kw = {'args': ['--no-sandbox']}
        if pin and os.access(pin[-1], os.X_OK): kw['executable_path'] = pin[-1]
        b = await p.chromium.launch(**kw)
        pg = await b.new_page()
        await pg.goto(f'file://{SRC}', wait_until='networkidle')
        await pg.pdf(path=OUT, format='A4', print_background=True,
                     display_header_footer=True, header_template=HDR, footer_template=FTR,
                     margin={'top':'27mm','bottom':'22mm','left':'18mm','right':'18mm'})
        await b.close()
asyncio.run(main())
print('pdf ok')
