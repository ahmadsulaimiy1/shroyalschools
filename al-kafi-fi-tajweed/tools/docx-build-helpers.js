const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageBreak, TableOfContents, Header, Footer, PageNumber, NumberFormat,
  convertInchesToTwip, Bookmark, BookmarkStart, BookmarkEnd, InternalHyperlink, LevelFormat,
  PositionalTab, PositionalTabAlignment, PositionalTabLeader, PositionalTabRelativeTo,
  PageReference, VerticalAlign, TabStopType, TabStopPosition,
} = require('docx');

// docx-js's `Bookmark` class gives every instance a fresh id generator that
// starts at 1, so bookmarkStart/End ids collide across a multi-bookmark
// document (OOXML requires them unique document-wide). Build bookmark
// start/end pairs manually against one shared counter instead.
let __bookmarkLinkId = 1000;
function bookmarkPair(name) {
  const linkId = __bookmarkLinkId++;
  return { start: new BookmarkStart(name, linkId), end: new BookmarkEnd(linkId) };
}

const HTML_PATH = process.argv[2] || '/home/user/shroyalschools/al-kafi-fi-tajweed/index.html';
const OUT_PATH = process.argv[3] || '/tmp/docxbuild/out.docx';
const LIMIT = process.argv[4] ? parseInt(process.argv[4], 10) : Infinity; // for quick testing

const html = fs.readFileSync(HTML_PATH, 'utf-8');
const $ = cheerio.load(html, { decodeEntities: false });

// ---------- Palette ----------
const C = {
  navy950: '0A1830', navy900: '0D2143', navy800: '152C54', navy700: '1C3866',
  gold700: '8A6A1F', gold600: 'A9812A', gold500: 'C39A3C', gold300: 'E3C780',
  cream050: 'FBF7EE', cream100: 'F6EFDD', cream200: 'EFE4C9',
  ink900: '181410', ink700: '3A3226', ink500: '6B6152',
  rule: 'D9C79A', mistakeBorder: '8C3B2E', white: 'FFFFFF',
};

const FONT_BODY = 'Amiri';
const FONT_DISPLAY = 'Aref Ruqaa';
const FONT_UI = 'Cairo';

let bookmarkCounter = 0;
function bmName(id) {
  if (!id) { bookmarkCounter++; return 'bm_' + bookmarkCounter; }
  return 'bm_' + id.replace(/[^a-zA-Z0-9_]/g, '_');
}

// ---------- Qur'an-aware run splitting ----------
const QURAN_RE = /(﴿[^﴾]*﴾)(\s*\[[^\]]*\])?/g;

function textRunsFor(text, baseOpts) {
  if (!text) return [];
  const runs = [];
  let lastIndex = 0;
  let m;
  QURAN_RE.lastIndex = 0;
  while ((m = QURAN_RE.exec(text)) !== null) {
    if (m.index > lastIndex) {
      const plain = text.slice(lastIndex, m.index);
      if (plain) runs.push(mkRun(plain, baseOpts));
    }
    runs.push(mkRun(m[1], { ...baseOpts, color: C.navy900, size: (baseOpts.size || 24) + 4, font: 'Amiri Quran' }));
    if (m[2]) {
      runs.push(mkRun(m[2], { ...baseOpts, color: C.gold700, bold: true, size: (baseOpts.size || 24) - 6, font: FONT_UI }));
    }
    lastIndex = QURAN_RE.lastIndex;
  }
  if (lastIndex < text.length) {
    const plain = text.slice(lastIndex);
    if (plain) runs.push(mkRun(plain, baseOpts));
  }
  return runs;
}

function mkRun(text, opts = {}) {
  return new TextRun({
    text,
    font: opts.font || FONT_BODY,
    bold: !!opts.bold,
    italics: !!opts.italics,
    color: opts.color || C.ink900,
    size: opts.size || 24, // half-points; 24 = 12pt
    rightToLeft: true,
  });
}

// Walk inline children of an element (text, strong, em, a, br) -> TextRun[]
function inlineRuns(el, baseOpts = {}) {
  const runs = [];
  el.contents().each((_, node) => {
    if (node.type === 'text') {
      runs.push(...textRunsFor(node.data, baseOpts));
    } else if (node.type === 'tag') {
      const $n = $(node);
      if (node.name === 'strong') {
        runs.push(...textRunsFor($n.text(), { ...baseOpts, bold: true, color: baseOpts.color || C.navy900 }));
      } else if (node.name === 'em') {
        runs.push(...textRunsFor($n.text(), { ...baseOpts, italics: true }));
      } else if (node.name === 'a') {
        const hasTerm = $n.find('span.term').length > 0 || $n.hasClass('term');
        if (hasTerm) {
          runs.push(...textRunsFor($n.text(), { ...baseOpts, bold: true, color: C.navy900, underline: true }));
        } else {
          runs.push(...textRunsFor($n.text(), { ...baseOpts, color: baseOpts.color || C.ink900 }));
        }
      } else if (node.name === 'span' && $n.hasClass('term')) {
        runs.push(...textRunsFor($n.text(), { ...baseOpts, bold: true, color: C.navy900 }));
      } else if (node.name === 'span') {
        runs.push(...textRunsFor($n.text(), baseOpts));
      } else {
        runs.push(...textRunsFor($n.text(), baseOpts));
      }
    }
  });
  return runs;
}

function para(runsOrText, opts = {}) {
  const children = Array.isArray(runsOrText) ? runsOrText : textRunsFor(runsOrText, opts);
  return new Paragraph({
    children,
    alignment: opts.align || AlignmentType.JUSTIFIED,
    bidirectional: true,
    spacing: { after: opts.after ?? 160, before: opts.before ?? 0, line: opts.line || 300 },
    border: opts.border,
    shading: opts.shading,
    indent: opts.indent,
  });
}

function headingPara(text, level, id, opts = {}) {
  const { start, end } = bookmarkPair(bmName(id));
  const runs = textRunsFor(text, { bold: true, color: opts.color || C.navy900, size: opts.size || 30, font: FONT_DISPLAY });
  return new Paragraph({
    heading: level,
    children: [start, ...runs, end],
    alignment: AlignmentType.RIGHT,
    bidirectional: true,
    pageBreakBefore: !!opts.pageBreakBefore,
    spacing: { before: opts.before ?? 240, after: opts.after ?? 160 },
    border: opts.border,
  });
}

function pageBreak() {
  return new Paragraph({ children: [new PageBreak()] });
}

// One-cell "boxed" table used for definition/note/mistake/meta/summary/review cards
function boxTable(paragraphs, { fill, borderColor, textColorDefault } = {}) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: { style: BorderStyle.SINGLE, size: 6, color: borderColor || C.gold500 },
      left: { style: BorderStyle.SINGLE, size: 24, color: borderColor || C.gold600 },
      bottom: { style: BorderStyle.SINGLE, size: 6, color: borderColor || C.gold500 },
      right: { style: BorderStyle.SINGLE, size: 6, color: borderColor || C.gold500 },
    },
    rows: [
      new TableRow({
        children: [
          new TableCell({
            shading: { type: ShadingType.CLEAR, fill: fill || C.cream100 },
            margins: { top: 160, bottom: 160, left: 200, right: 200 },
            children: paragraphs,
          }),
        ],
      }),
    ],
  });
}

function labelPara(text, opts = {}) {
  return para(text, { align: AlignmentType.RIGHT, after: 100, ...opts, size: opts.size || 18, });
}

// ---------- Lists ----------
const NUMBERING_CONFIG = {
  config: [
    {
      reference: 'bullet-list',
      levels: [{
        level: 0, format: LevelFormat.BULLET, text: '◆', alignment: AlignmentType.RIGHT,
        style: { paragraph: { indent: { right: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.22) } }, run: { color: C.gold600 } },
      }],
    },
    {
      reference: 'decimal-list',
      levels: [{
        level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.RIGHT,
        style: { paragraph: { indent: { right: convertInchesToTwip(0.3), hanging: convertInchesToTwip(0.22) } }, run: { color: C.navy800, bold: true } },
      }],
    },
  ],
};

function listParagraph(el, ref, opts = {}) {
  const runs = inlineRuns(el, opts);
  return new Paragraph({
    children: runs,
    alignment: AlignmentType.JUSTIFIED,
    bidirectional: true,
    numbering: { reference: ref, level: 0 },
    spacing: { after: 90, line: 300 },
  });
}

// ---------- Tables (kafi-table) ----------
function buildTable($table) {
  const rows = [];
  const $caption = $table.find('caption');
  const headCells = $table.find('thead tr th').toArray();
  const nCols = headCells.length || $table.find('tbody tr').first().find('td').length;
  const colWidth = Math.floor(9026 / nCols); // ~ page content width in dxa / cols

  if (headCells.length) {
    rows.push(new TableRow({
      tableHeader: true,
      children: headCells.map((th) => new TableCell({
        width: { size: colWidth, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: C.navy950 },
        verticalAlign: VerticalAlign.CENTER,
        margins: { top: 100, bottom: 100, left: 120, right: 120 },
        children: [new Paragraph({
          children: inlineRuns($(th), { color: C.gold300, bold: true, size: 20, font: FONT_UI }),
          alignment: AlignmentType.RIGHT, bidirectional: true,
        })],
      })),
    }));
  }

  $table.find('tbody tr').each((i, tr) => {
    const $tds = $(tr).find('td');
    const isFirstColBold = true;
    rows.push(new TableRow({
      children: $tds.toArray().map((td, ci) => new TableCell({
        width: { size: colWidth, type: WidthType.DXA },
        shading: { type: ShadingType.CLEAR, fill: i % 2 === 0 ? C.white : C.cream050 },
        margins: { top: 90, bottom: 90, left: 120, right: 120 },
        children: [new Paragraph({
          children: inlineRuns($(td), { size: 20, bold: (ci === $tds.length - 1) && isFirstColBold, color: (ci === $tds.length - 1) ? C.navy900 : C.ink900 }),
          alignment: AlignmentType.RIGHT, bidirectional: true,
        })],
      })),
    }));
  });

  const out = [];
  if ($caption.length) {
    out.push(para($caption.text(), { align: AlignmentType.RIGHT, before: 120, after: 60, size: 20, bold: true, color: C.navy900 }));
  }
  out.push(new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    rows,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: C.rule },
      left: { style: BorderStyle.SINGLE, size: 4, color: C.rule },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: C.rule },
      right: { style: BorderStyle.SINGLE, size: 4, color: C.rule },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: C.rule },
      insideVertical: { style: BorderStyle.SINGLE, size: 2, color: C.rule },
    },
  }));
  out.push(new Paragraph({ text: '', spacing: { after: 160 } }));
  return out;
}

module.exports = {
  $, C, FONT_BODY, FONT_DISPLAY, FONT_UI, bmName, textRunsFor, mkRun, inlineRuns,
  para, headingPara, pageBreak, boxTable, labelPara, listParagraph, buildTable,
  NUMBERING_CONFIG, HTML_PATH, OUT_PATH, LIMIT,
  docx: require('docx'),
};
