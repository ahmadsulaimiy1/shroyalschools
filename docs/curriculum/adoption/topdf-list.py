import sys, asyncio, glob, os
from playwright.async_api import async_playwright
SRC, OUT = sys.argv[1], sys.argv[2]
HDR = """<div style="width:100%;font-family:Archivo,sans-serif;font-weight:600;font-size:6pt;
 letter-spacing:.2em;text-transform:uppercase;color:#A08E72;padding:0 18mm;
 display:flex;justify-content:space-between;align-items:flex-end;margin:0 0 2.6mm;">
 <span>Sultan Hanafi Royal Schools</span>
 <span>Textbook List &middot; 2026 / 2027</span></div>"""
FTR = """<div style="width:100%;padding:0;margin:3.6mm 0 0;">
 <div style="border-top:.5px solid #DFCFB3;padding-top:2.2mm;display:flex;
  justify-content:space-between;align-items:center;font-family:Archivo,sans-serif;
  font-weight:600;font-size:6pt;letter-spacing:.2em;text-transform:uppercase;color:#A08E72;">
  <span>Registrar&rsquo;s Office</span>
  <span style="font-family:Amiri,serif;font-weight:700;font-size:10.4pt;color:#2A1C10;
   letter-spacing:0;text-transform:none;"><span class="pageNumber"></span></span>
  <span style="font-family:'Noto Kufi Arabic',sans-serif;font-size:6.6pt;letter-spacing:0;
   text-transform:none;color:#9C8B74;">قائمة الكتب الدراسية</span></div></div>"""
async def main():
    async with async_playwright() as p:
        pin = sorted(glob.glob('/opt/pw-browsers/chromium*/chrome-linux/chrome'))
        kw = {'args': ['--no-sandbox']}
        if pin and os.access(pin[-1], os.X_OK): kw['executable_path'] = pin[-1]
        b = await p.chromium.launch(**kw); pg = await b.new_page()
        await pg.goto(f'file://{SRC}', wait_until='networkidle')
        await pg.pdf(path=OUT, format='A4', print_background=True,
                     display_header_footer=True, header_template=HDR, footer_template=FTR,
                     margin={'top':'26mm','bottom':'22mm','left':'17mm','right':'17mm'})
        await b.close()
asyncio.run(main())
print('pdf ok')
