import sys, asyncio
from playwright.async_api import async_playwright
SRC, OUT = sys.argv[1], sys.argv[2]
RANGES = sys.argv[3] if len(sys.argv)>3 else ''
NOFURN = len(sys.argv)>4
HDR = """<div style="width:100%;font-family:Archivo,'Helvetica Neue',sans-serif;
 font-weight:600;font-size:6.1pt;letter-spacing:.19em;text-transform:uppercase;
 color:#9C8A6E;padding:0 19mm;display:flex;justify-content:space-between;
 align-items:flex-end;margin:0 0 2.4mm;">
 <span>Sultan Hanafi Royal Schools &middot; School of Islamic and Arabic Studies</span>
 <span>The Curriculum Handbook</span></div>"""
FTR = """<div style="width:100%;padding:0;margin:3.4mm 0 0;">
 <div style="border-top:.5px solid #E0D2B8;padding-top:2.2mm;display:flex;
  justify-content:space-between;align-items:center;
  font-family:Archivo,'Helvetica Neue',sans-serif;font-weight:600;font-size:6.1pt;
  letter-spacing:.19em;text-transform:uppercase;color:#9C8A6E;">
  <span>GACAIS</span>
  <span style="font-family:Amiri,serif;font-weight:700;font-size:10pt;color:#2A1C10;
   letter-spacing:0;text-transform:none;"><span class="pageNumber"></span></span>
  <span style="font-family:'Noto Kufi Arabic',sans-serif;font-size:6.6pt;letter-spacing:0;
   text-transform:none;color:#9A8A76;">&#x648;&#x62B;&#x64A;&#x642;&#x629; &#x639;&#x645;&#x644; &mdash; &#x63A;&#x64A;&#x631; &#x645;&#x639;&#x62A;&#x645;&#x62F;&#x629;</span></div></div>"""
async def main():
    async with async_playwright() as p:
        import glob, os
        pin = sorted(glob.glob('/opt/pw-browsers/chromium*/chrome-linux/chrome'))
        kw = {'args': ['--no-sandbox']}
        if pin and os.access(pin[-1], os.X_OK):
            kw['executable_path'] = pin[-1]
        b = await p.chromium.launch(**kw)
        pg = await b.new_page()
        await pg.goto(f'file://{SRC}', wait_until='networkidle')
        await pg.pdf(path=OUT, format='A4', print_background=True,
                     display_header_footer=not NOFURN, header_template=HDR, footer_template=FTR,
                     margin=({'top':'0','bottom':'0','left':'0','right':'0'} if NOFURN else
                             {'top':'29mm','bottom':'23mm','left':'19mm','right':'19mm'}),
                     page_ranges=RANGES)
        await b.close()
asyncio.run(main())
print('pdf ok')
