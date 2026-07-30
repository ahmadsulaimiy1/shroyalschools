#!/usr/bin/env python3
"""Generate the stat-dashboard spread and pull-quote spreads as raw-openxml
markdown fragments, and splice them into the assembled front-matter / body."""

# ---------------------------------------------------------------------------
# 1. "AMIU at a Glance" stat dashboard (2x3 card grid)
# ---------------------------------------------------------------------------

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

STATS = [
    ("11,021", "ACTIVE STUDENTS BY YEAR 10 (2037)"),
    ("$16.7M", "TEN-YEAR CUMULATIVE GROSS REVENUE"),
    ("$0", "DEFICIT IN ANY YEAR, ANY SCENARIO"),
    ("71", "NAMED FOUNDING-DECADE PROGRAMS"),
    ("$5.8M", "TEN-YEAR LIQUIDITY RESERVE"),
    ("$3.3M", "TEN-YEAR WAQF & STAKEHOLDER RESERVE"),
]

def _card(number, label):
    return f'''<w:tc>
      <w:tcPr>
        <w:tcW w:w="4675" w:type="dxa"/>
        <w:tcBorders>
          <w:top w:val="single" w:sz="16" w:space="0" w:color="B08625"/>
          <w:left w:val="single" w:sz="2" w:space="0" w:color="D8DCE5"/>
          <w:bottom w:val="single" w:sz="2" w:space="0" w:color="D8DCE5"/>
          <w:right w:val="single" w:sz="2" w:space="0" w:color="D8DCE5"/>
        </w:tcBorders>
        <w:shd w:val="clear" w:color="auto" w:fill="F6F7FA"/>
        <w:tcMar><w:top w:w="380" w:type="dxa"/><w:left w:w="380" w:type="dxa"/><w:bottom w:w="380" w:type="dxa"/><w:right w:w="380" w:type="dxa"/></w:tcMar>
        <w:vAlign w:val="center"/>
      </w:tcPr>
      <w:p><w:pPr><w:spacing w:before="0" w:after="90"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Bitstream Charter" w:hAnsi="Bitstream Charter"/><w:b/><w:color w:val="122A4E"/><w:sz w:val="52"/></w:rPr><w:t>{esc(number)}</w:t></w:r></w:p>
      <w:p><w:pPr><w:spacing w:before="0" w:after="0"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="5B6372"/><w:sz w:val="15"/><w:spacing w:val="8"/></w:rPr><w:t>{esc(label)}</w:t></w:r></w:p>
    </w:tc>'''

def stat_dashboard_markdown():
    rows = []
    for i in range(0, 6, 2):
        rows.append(f"  <w:tr>\n{_card(*STATS[i])}\n{_card(*STATS[i+1])}\n  </w:tr>")
    rows_xml = "\n".join(rows)
    return f'''```{{=openxml}}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

## AMIU at a Glance {{.unnumbered}}

*The founding-decade record, audited against the adopted Growth Scenario (AMIU-MP-001).*

```{{=openxml}}
<w:tbl>
  <w:tblPr>
    <w:tblW w:w="9350" w:type="dxa"/>
    <w:tblLayout w:type="fixed"/>
    <w:tblBorders>
      <w:top w:val="none" w:sz="0" w:space="0" w:color="auto"/>
      <w:left w:val="none" w:sz="0" w:space="0" w:color="auto"/>
      <w:bottom w:val="none" w:sz="0" w:space="0" w:color="auto"/>
      <w:right w:val="none" w:sz="0" w:space="0" w:color="auto"/>
    </w:tblBorders>
    <w:tblCellSpacing w:w="60" w:type="dxa"/>
  </w:tblPr>
  <w:tblGrid><w:gridCol w:w="4675"/><w:gridCol w:w="4675"/></w:tblGrid>
{rows_xml}
</w:tbl>
```

*Figures reflect the adopted Growth Scenario. Years 11–20 are explicitly directional planning estimates — see Section 1 and Section 40.*

'''

# ---------------------------------------------------------------------------
# 2. Pull-quote spreads — two visual variants for rhythm (navy vs. minimal)
# ---------------------------------------------------------------------------

def quote_spread_navy(quote, attribution):
    quote, attribution = esc(quote), esc(attribution)
    return f'''```{{=openxml}}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:tbl>
  <w:tblPr>
    <w:tblW w:w="9350" w:type="dxa"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="10" w:space="0" w:color="B08625"/>
      <w:bottom w:val="single" w:sz="10" w:space="0" w:color="B08625"/>
    </w:tblBorders>
  </w:tblPr>
  <w:tblGrid><w:gridCol w:w="9350"/></w:tblGrid>
  <w:tr>
    <w:trPr><w:trHeight w:val="8600" w:hRule="atLeast"/><w:cantSplit/></w:trPr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="9350" w:type="dxa"/>
        <w:shd w:val="clear" w:color="auto" w:fill="122A4E"/>
        <w:tcMar><w:top w:w="500" w:type="dxa"/><w:left w:w="900" w:type="dxa"/><w:bottom w:w="500" w:type="dxa"/><w:right w:w="900" w:type="dxa"/></w:tcMar>
        <w:vAlign w:val="center"/>
      </w:tcPr>
      <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="260"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Bitstream Charter" w:hAnsi="Bitstream Charter"/><w:color w:val="B08625"/><w:sz w:val="64"/></w:rPr><w:t>&#8220;</w:t></w:r>
      </w:p>
      <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="320"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Liberation Serif" w:hAnsi="Liberation Serif"/><w:i/><w:color w:val="FFFFFF"/><w:sz w:val="34"/></w:rPr><w:t>{quote}</w:t></w:r>
      </w:p>
      <w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="0"/></w:pPr>
        <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="B08625"/><w:b/><w:sz w:val="16"/><w:spacing w:val="16"/></w:rPr><w:t>{attribution}</w:t></w:r>
      </w:p>
    </w:tc>
  </w:tr>
</w:tbl>
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

'''

def quote_spread_minimal(quote, attribution):
    quote, attribution = esc(quote), esc(attribution)
    return f'''```{{=openxml}}
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
<w:p><w:pPr><w:spacing w:before="3800" w:after="0"/><w:pBdr><w:top w:val="single" w:sz="6" w:space="24" w:color="B08625"/></w:pBdr></w:pPr></w:p>
<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="360"/><w:ind w:left="1000" w:right="1000"/></w:pPr>
  <w:r><w:rPr><w:rFonts w:ascii="Liberation Serif" w:hAnsi="Liberation Serif"/><w:i/><w:color w:val="122A4E"/><w:sz w:val="30"/></w:rPr><w:t>{quote}</w:t></w:r>
</w:p>
<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="0" w:after="0"/></w:pPr>
  <w:r><w:rPr><w:rFonts w:ascii="Liberation Sans" w:hAnsi="Liberation Sans"/><w:color w:val="B08625"/><w:b/><w:sz w:val="16"/><w:spacing w:val="16"/></w:rPr><w:t>{attribution}</w:t></w:r>
</w:p>
<w:p><w:pPr><w:spacing w:before="360" w:after="0"/><w:pBdr><w:bottom w:val="single" w:sz="6" w:space="24" w:color="B08625"/></w:pBdr></w:pPr></w:p>
<w:p><w:r><w:br w:type="page"/></w:r></w:p>
```

'''

if __name__ == "__main__":
    with open("/tmp/stat_dashboard.md", "w", encoding="utf-8") as f:
        f.write(stat_dashboard_markdown())
    with open("/tmp/quote1.md", "w", encoding="utf-8") as f:
        f.write(quote_spread_navy(
            "Financial capacity shall never be a barrier to knowledge.",
            "AMIU MISSION PRINCIPLE · AMIU-MP-001 § 3"))
    with open("/tmp/quote2.md", "w", encoding="utf-8") as f:
        f.write(quote_spread_minimal(
            "A plan for the Tuesday after the promise is made.",
            "THE SUPREME STRATEGIC PLANNING COUNCIL · FOREWORD"))
    with open("/tmp/quote3.md", "w", encoding="utf-8") as f:
        f.write(quote_spread_navy(
            "Every ambition in this Blueprint is priced against a revenue line AMIU has actually adopted — never a revenue line we wished it had.",
            "FOREWORD · THE SUPREME STRATEGIC PLANNING COUNCIL"))
    print("wrote fragments to /tmp")
