const {
  $, C, FONT_BODY, FONT_DISPLAY, FONT_UI, bmName, textRunsFor, mkRun, inlineRuns,
  para, headingPara, pageBreak, boxTable, labelPara, listParagraph, buildTable,
  NUMBERING_CONFIG, HTML_PATH, OUT_PATH, LIMIT, HEADER_TITLE, docx,
} = require('./docx-build-helpers.js');

const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle,
  PageBreak, TableOfContents, Header, Footer, PageNumber, NumberFormat,
  convertInchesToTwip, Bookmark, LevelFormat, ImageRun,
  PositionalTab, PositionalTabAlignment, PositionalTabLeader, PositionalTabRelativeTo,
  PageReference, VerticalAlign, TabStopType, TabStopPosition,
} = docx;

// pull a base64 data-URI <img> out of an element and turn it into a centered
// ImageRun paragraph; returns [] if no image is present (never throws on missing art)
function crestImageParagraph($img, sizePx) {
  const src = $img.attr('src') || '';
  const m = /^data:image\/(png|jpe?g);base64,(.+)$/.exec(src);
  if (!m) return [];
  const buffer = Buffer.from(m[2], 'base64');
  return [new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 160 },
    children: [new ImageRun({ data: buffer, transformation: { width: sizePx, height: sizePx }, type: m[1] === 'png' ? 'png' : 'jpg' })],
  })];
}

const body = [];
const push = (...items) => { items.flat().filter(Boolean).forEach(i => body.push(i)); };

// track headings we bookmark, in order, for the manual analytical index
const indexEntries = []; // {text, bookmarkId}
let collectIndex = true; // turned off once we leave the numbered Babs/appendices (glossary reuses .section-title for its own grouping headers, which aren't real index targets)
let tocInserted = false;

function buildTocBlock() {
  return [
    headingPara('فهرس المحتويات', HeadingLevel.HEADING_1, 'native_toc', { size: 32, pageBreakBefore: true, before: 0, after: 160 }),
    para('(اضغط بزر الماوس الأيمن على الفهرس ثم اختر "تحديث الحقل" لضبط أرقام الصفحات عند فتح المستند لأول مرة)', { align: AlignmentType.RIGHT, italics: true, color: C.ink500, size: 16, after: 200 }),
    new TableOfContents('فهرس المحتويات', { hyperlink: true, headingStyleRange: '1-3' }),
    pageBreak(),
  ];
}

// ============================================================
// COVER
// ============================================================
function renderCover($sec) {
  const out = [];
  out.push(new Paragraph({ text: '', spacing: { after: 600 } }));
  const bismillah = $sec.find('.bismillah').first().text().trim();
  if (bismillah) out.push(para(bismillah, { align: AlignmentType.CENTER, size: 30, color: C.navy900, font: 'Amiri Quran', after: 500 }));
  out.push(new Paragraph({
    children: textRunsFor($sec.find('h1').first().text(), { size: 68, bold: true, color: C.navy950, font: FONT_DISPLAY }),
    alignment: AlignmentType.CENTER, bidirectional: true, spacing: { after: 400 },
  }));
  const subtitleGold = $sec.find('.subtitle-gold').text().trim();
  if (subtitleGold) out.push(para(subtitleGold, { align: AlignmentType.CENTER, size: 24, bold: true, color: C.gold700, after: 260 }));
  const subtitle = $sec.find('.subtitle').text().trim();
  if (subtitle) out.push(para(subtitle, { align: AlignmentType.CENTER, size: 22, color: C.ink700, after: 500 }));
  out.push(para('۞', { align: AlignmentType.CENTER, size: 28, color: C.gold500, after: 500,
    border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.gold500, space: 12 }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.gold500, space: 12 } } }));

  // each .credits block (author, then editor if present) rendered by its own
  // role/epithet/name/credential class markers - never by sibling position
  $sec.find('.credits').each((_, block) => {
    const $b = $(block);
    const role = $b.find('.role').text().trim();
    const epithet = $b.find('.epithet').text().trim();
    const name = $b.find('.name').text().trim();
    const isEditor = ($b.attr('class') || '').includes('editor-credits');
    if (role) out.push(para(role, { align: AlignmentType.CENTER, size: 18, color: C.gold700, after: 60 }));
    if (epithet) out.push(para(epithet, { align: AlignmentType.CENTER, size: 16, italics: true, color: C.ink500, after: 40 }));
    if (name) out.push(para(name, { align: AlignmentType.CENTER, size: isEditor ? 24 : 30, bold: true, color: C.navy950, after: isEditor ? 100 : 340 }));
    $b.find('.credential').each((__, cred) => {
      const t = $(cred).text().trim();
      if (t) out.push(para(t, { align: AlignmentType.CENTER, size: 15, italics: true, color: C.ink500, after: 60 }));
    });
    if (isEditor) out.push(new Paragraph({ text: '', spacing: { after: 200 } }));
  });

  const seriesLine = $sec.find('.series-line').text().trim();
  if (seriesLine) out.push(para(seriesLine, { align: AlignmentType.CENTER, size: 15, color: C.ink500, after: 200 }));
  const editionBadge = $sec.find('.edition-badge').text().trim();
  if (editionBadge) out.push(para(editionBadge, { align: AlignmentType.CENTER, size: 18, bold: true, color: C.gold700, after: 260 }));
  out.push(...crestImageParagraph($sec.find('.crest-badge img').first(), 70));
  const pubAr = $sec.find('.pub-name-ar').text().trim();
  if (pubAr) out.push(para(pubAr, { align: AlignmentType.CENTER, size: 19, bold: true, color: C.gold700, after: 40 }));
  const pubEn = $sec.find('.pub-name-en').text().trim();
  if (pubEn) out.push(para(pubEn, { align: AlignmentType.CENTER, size: 16, color: C.ink500, after: 200 }));
  const footerLine = $sec.find('.footer-line').text().trim();
  if (footerLine) out.push(para(footerLine, { align: AlignmentType.CENTER, size: 18, color: C.ink500, after: 200 }));
  out.push(pageBreak());
  return out;
}

function renderHalfTitle($sec) {
  const out = [];
  out.push(new Paragraph({ text: '', spacing: { after: 1200 } }));
  const bismillah = $sec.find('.bismillah').text().trim();
  if (bismillah) out.push(para(bismillah, { align: AlignmentType.CENTER, size: 26, color: C.navy900, font: 'Amiri Quran', after: 400 }));
  out.push(new Paragraph({
    children: textRunsFor($sec.find('h1').text(), { size: 52, bold: true, color: C.navy950, font: FONT_DISPLAY }),
    alignment: AlignmentType.CENTER, bidirectional: true, spacing: { after: 300 },
  }));
  $sec.find('.tagline').each((i, t) => {
    const text = $(t).text().trim();
    if (text) out.push(para(text, { align: AlignmentType.CENTER, size: 20, color: C.gold700, after: i === 0 ? 100 : 0 }));
  });
  out.push(pageBreak());
  return out;
}

// ============================================================
// BACK COVER
// ============================================================
function renderBackCover($sec) {
  const out = [];
  out.push(new Paragraph({ text: '', spacing: { after: 400 } }));
  out.push(para($sec.find('.bc-kicker').text(), { align: AlignmentType.CENTER, size: 16, color: C.gold600, bold: true, after: 300 }));
  out.push(new Paragraph({
    children: textRunsFor($sec.find('.bc-title').text(), { size: 34, bold: true, color: C.navy950, font: FONT_DISPLAY }),
    alignment: AlignmentType.CENTER, bidirectional: true, spacing: { after: 300 },
  }));
  out.push(para($sec.find('.bc-description').text(), { align: AlignmentType.JUSTIFIED, size: 20, color: C.ink700, after: 400 }));
  out.push(para('۞', { align: AlignmentType.CENTER, size: 22, color: C.gold500, after: 400 }));
  const bioLabel = $sec.find('.bc-bio-block .bc-label').text().trim();
  const bioClone = $sec.find('.bc-bio-block').clone();
  bioClone.find('.bc-label').remove();
  const bioText = bioClone.text().trim();
  if (bioLabel) out.push(para(bioLabel, { align: AlignmentType.RIGHT, size: 16, color: C.gold700, bold: true, after: 80 }));
  if (bioText) out.push(para(bioText, { align: AlignmentType.JUSTIFIED, size: 18, color: C.ink700, after: 400 }));

  const editorLabel = $sec.find('.bc-editor .bc-label').text().trim();
  const editorClone = $sec.find('.bc-editor').clone();
  editorClone.find('.bc-label').remove();
  const editorText = editorClone.text().trim();
  if (editorLabel) out.push(para(editorLabel, { align: AlignmentType.RIGHT, size: 16, color: C.gold700, bold: true, after: 80 }));
  if (editorText) out.push(para(editorText, { align: AlignmentType.JUSTIFIED, size: 18, color: C.ink700, after: 400 }));

  const seriesAbout = $sec.find('.bc-series-about').text().trim();
  if (seriesAbout) out.push(para(seriesAbout, { align: AlignmentType.CENTER, size: 16, italics: true, color: C.ink500, after: 400 }));

  $sec.find('.bc-meta .row').each((_, row) => {
    const $row = $(row);
    const k = $row.find('.k').text().trim();
    const vClone = $row.clone();
    vClone.find('.k').remove();
    const v = vClone.text().trim();
    out.push(para(`${k}: ${v}`, { align: AlignmentType.RIGHT, size: 18, color: C.ink700, after: 120 }));
  });
  const isbnText = $sec.find('.bc-isbn-box .isbn-text').text().replace(/\s+/g, ' ').trim();
  if (isbnText) out.push(para(isbnText, { align: AlignmentType.CENTER, size: 16, italics: true, color: C.ink500, after: 300 }));
  out.push(...crestImageParagraph($sec.find('.bc-mark .crest-badge img').first(), 56));
  const markLabel = $sec.find('.bc-mark').clone();
  markLabel.find('.crest-badge').remove();
  const markText = markLabel.text().replace(/\s+/g, ' ').trim();
  if (markText) out.push(para(markText, { align: AlignmentType.CENTER, size: 18, bold: true, color: C.gold700, after: 200 }));
  return out;
}

function renderColophon($sec, $footer) {
  const out = [];
  out.push(new Paragraph({ text: '', spacing: { after: 800 } }));
  out.push(para($sec.find('.bismillah').text(), { align: AlignmentType.CENTER, size: 22, color: C.gold700, font: 'Amiri Quran', after: 300 }));
  out.push(new Paragraph({
    children: textRunsFor($sec.find('h2').text(), { size: 36, bold: true, color: C.navy950, font: FONT_DISPLAY }),
    alignment: AlignmentType.CENTER, bidirectional: true, spacing: { after: 260 },
  }));
  out.push(para($sec.find('p').text(), { align: AlignmentType.CENTER, size: 20, color: C.ink700, after: 400 }));
  if ($footer && $footer.length) {
    out.push(para($footer.text().trim(), { align: AlignmentType.CENTER, size: 16, color: C.ink500 }));
  }
  return out;
}

// ============================================================
// generic field-list (publisher info) -> mini table
// ============================================================
function renderFieldList($fl) {
  const rows = [];
  $fl.find('li').each((_, li) => {
    const $li = $(li);
    const k = $li.find('.k').text();
    const v = $li.find('.v').text();
    rows.push(new TableRow({
      children: [
        new TableCell({
          width: { size: 2600, type: WidthType.DXA }, shading: { type: ShadingType.CLEAR, fill: C.cream100 },
          margins: { top: 90, bottom: 90, left: 120, right: 120 },
          children: [para(k, { align: AlignmentType.RIGHT, bold: true, color: C.gold700, size: 20, after: 0 })],
        }),
        new TableCell({
          width: { size: 6400, type: WidthType.DXA },
          margins: { top: 90, bottom: 90, left: 120, right: 120 },
          children: [para(v, { align: AlignmentType.RIGHT, color: C.ink700, size: 20, after: 0 })],
        }),
      ],
    }));
  });
  return [new Table({
    width: { size: 100, type: WidthType.PERCENTAGE }, rows,
    borders: {
      top: { style: BorderStyle.SINGLE, size: 4, color: C.rule }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.rule },
      left: { style: BorderStyle.SINGLE, size: 4, color: C.rule }, right: { style: BorderStyle.SINGLE, size: 4, color: C.rule },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 2, color: C.rule }, insideVertical: { style: BorderStyle.NONE },
    },
  }), new Paragraph({ text: '', spacing: { after: 160 } })];
}

// ============================================================
// Generic content-node renderer (recursive)
// ============================================================
function renderNode(el) {
  const $el = $(el);
  const tag = el.tagName || el.name;
  const cls = ($el.attr('class') || '');

  if (tag === 'h2' && cls.includes('chapter-title')) {
    const id = $el.closest('article').attr('id');
    const text = $el.text().trim();
    if (collectIndex && id) indexEntries.push({ text, id });
    return [headingPara(text, HeadingLevel.HEADING_2, id, { size: 28, before: 320, after: 140 })];
  }
  if (tag === 'h2') { // front-matter page titles
    const id = $el.closest('section').attr('id');
    return [headingPara($el.text().trim(), HeadingLevel.HEADING_1, id, { size: 32, pageBreakBefore: true, before: 0, after: 200 })];
  }
  if (tag === 'h3' && cls.includes('section-title')) {
    const id = $el.closest('*[id]').attr('id');
    const text = $el.text().trim();
    if (collectIndex && id) indexEntries.push({ text, id });
    return [headingPara(text, HeadingLevel.HEADING_3, id, { size: 23, color: C.gold700, before: 260, after: 120 })];
  }
  if (tag === 'h3') {
    return [headingPara($el.text().trim(), HeadingLevel.HEADING_3, null, { size: 23, before: 260, after: 120 })];
  }
  if (tag === 'h4') {
    return [para($el.text().trim(), { align: AlignmentType.RIGHT, bold: true, color: C.navy800, size: 22, before: 200, after: 100 })];
  }
  if (tag === 'p') {
    return [para(inlineRuns($el, { size: 22 }), { after: 140 })];
  }
  if (tag === 'ul' && cls.includes('field-list')) {
    return renderFieldList($el);
  }
  if (tag === 'ul') {
    if ($el.parent().hasClass('toc') || $el.closest('.toc').length) return [];
    return $el.children('li').toArray().map(li => listParagraph($(li), 'bullet-list', { size: 22 }));
  }
  if (tag === 'ol') {
    return $el.children('li').toArray().map(li => listParagraph($(li), 'decimal-list', { size: 22 }));
  }
  if (tag === 'div' && cls.includes('table-wrap')) {
    return buildTable($el.find('table').first());
  }
  if (tag === 'div' && cls.split(/\s+/).includes('definition')) {
    const inner = $el.children('p').toArray().map(p => para(inlineRuns($(p), { size: 22 }), { after: 80 }));
    return [boxTable(inner, { fill: C.cream100, borderColor: C.navy800 }), new Paragraph({ text: '', spacing: { after: 140 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('note')) {
    const title = $el.find('.note-title').text().trim();
    const rest = $el.children().not('.note-title').toArray().flatMap(c => renderInner($(c)));
    const inner = [labelPara(title, { bold: true, color: C.gold700, size: 18 }), ...rest];
    return [boxTable(inner, { fill: C.white, borderColor: C.gold600 }), new Paragraph({ text: '', spacing: { after: 140 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('mistake')) {
    const title = $el.find('.mistake-title').text().trim();
    const ps = $el.children('p').not('.mistake-title').toArray().map(p => para(inlineRuns($(p), { size: 22 }), { after: 0 }));
    const inner = [labelPara(title, { bold: true, color: C.mistakeBorder, size: 18 }), ...ps];
    return [boxTable(inner, { fill: C.cream050, borderColor: C.mistakeBorder }), new Paragraph({ text: '', spacing: { after: 140 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('examples')) {
    const title = $el.find('.examples-title').text().trim();
    const items = $el.find('li').toArray().map(li => listParagraph($(li), 'bullet-list', { size: 21, color: C.ink700 }));
    return [labelPara(title, { bold: true, color: C.navy800, size: 19 }), ...items, new Paragraph({ text: '', spacing: { after: 100 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('meta-card')) {
    const title = $el.find('h3').text().trim();
    const items = $el.find('li').toArray().map(li => listParagraph($(li), 'bullet-list', { size: 21, color: C.cream100 }));
    const inner = [labelPara(title, { bold: true, color: C.gold300, size: 17 }), ...items];
    return [boxTable(inner, { fill: C.navy950, borderColor: C.navy950 }), new Paragraph({ text: '', spacing: { after: 160 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('summary-card')) {
    const title = $el.find('h3').text().trim();
    const ps = $el.find('p').toArray().map(p => para(inlineRuns($(p), { size: 22 }), { after: 0 }));
    const inner = [labelPara(title, { bold: true, color: C.navy900, size: 18 }), ...ps];
    return [boxTable(inner, { fill: C.cream100, borderColor: C.gold300 }), new Paragraph({ text: '', spacing: { after: 160 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('review-card')) {
    const title = $el.find('h3').text().trim();
    const items = $el.find('li').toArray().map(li => listParagraph($(li), 'decimal-list', { size: 22 }));
    const inner = [labelPara(title, { bold: true, color: C.gold700, size: 18 }), ...items];
    return [boxTable(inner, { fill: C.white, borderColor: C.navy700 }), new Paragraph({ text: '', spacing: { after: 160 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('checkpoint')) {
    const inner = [para(inlineRuns($el, { size: 21, bold: true, color: '241A05' }), { align: AlignmentType.RIGHT, after: 0 })];
    return [boxTable(inner, { fill: C.gold500, borderColor: C.gold600 }), new Paragraph({ text: '', spacing: { after: 200 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('ruling')) {
    return [para(inlineRuns($el, { size: 21, bold: true, color: C.navy900 }),
      { align: AlignmentType.RIGHT, after: 140, shading: { type: ShadingType.CLEAR, fill: C.cream200 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('matn')) {
    return [para(inlineRuns($el, { size: 24, color: C.navy950, font: FONT_BODY }),
      { align: AlignmentType.CENTER, after: 160, before: 60,
        border: { top: { style: BorderStyle.SINGLE, size: 4, color: C.gold500, space: 8 }, bottom: { style: BorderStyle.SINGLE, size: 4, color: C.gold500, space: 8 } },
        shading: { type: ShadingType.CLEAR, fill: C.cream100 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('small-note')) {
    const inner = [para(inlineRuns($el, { size: 18, italics: true, color: C.ink500 }), { after: 0 })];
    return [boxTable(inner, { fill: C.cream200, borderColor: C.gold500 }), new Paragraph({ text: '', spacing: { after: 140 } })];
  }
  if (tag === 'div' && cls.split(/\s+/).includes('pref-signoff')) {
    const out = [new Paragraph({ text: '', spacing: { after: 60 },
      border: { top: { style: BorderStyle.DASHED, size: 4, color: C.rule || 'D9C79A', space: 8 } } })];
    const date = $el.find('.date').text().trim();
    const signee = $el.find('.signee').text().trim();
    const org = $el.find('.org').text().trim();
    const loc = $el.find('.loc').text().trim();
    if (date) out.push(para(date, { align: AlignmentType.CENTER, size: 18, color: C.ink500, after: 80 }));
    if (signee) out.push(new Paragraph({
      children: textRunsFor(signee, { size: 26, bold: true, color: C.navy900, font: FONT_DISPLAY }),
      alignment: AlignmentType.CENTER, bidirectional: true, spacing: { after: org ? 40 : 140 },
    }));
    if (org) out.push(para(org, { align: AlignmentType.CENTER, size: 20, bold: true, color: C.gold700, after: 20 }));
    if (loc) out.push(para(loc, { align: AlignmentType.CENTER, size: 19, color: C.ink500, after: 160 }));
    return out;
  }
  if (tag === 'div' && cls.includes('field-list')) {
    return renderFieldList($el);
  }
  if (tag === 'ul' && cls.includes('field-list')) {
    return renderFieldList($el);
  }
  if (tag === 'article') {
    return renderInner($el);
  }
  if (tag === 'div' && (cls.includes('content') || cls.includes('page-pad'))) {
    return renderInner($el);
  }
  // fall back: recurse into children
  return renderInner($el);
}

function renderInner($el) {
  const out = [];
  $el.children().each((_, c) => { out.push(...renderNode(c)); });
  return out;
}

// ============================================================
// MAIN WALK over <body> children in document order
// ============================================================
const bodyChildren = $('body').children().toArray();
let count = 0;
for (const el of bodyChildren) {
  if (count >= LIMIT) break;
  const $el = $(el);
  const tag = el.tagName;
  const id = $el.attr('id');
  const cls = ($el.attr('class') || '');

  if (tag === 'nav' || tag === 'script') continue;
  if (tag === 'footer') continue; // folded into colophon

  if (cls.includes('back-cover')) { push(renderBackCover($el)); count++; continue; }
  if (cls.includes('cover')) { push(renderCover($el)); count++; continue; }
  if (cls.includes('half-title')) { push(renderHalfTitle($el)); count++; continue; }
  if (cls.includes('colophon')) { push(renderColophon($el, $('footer.book-footer'))); count++; continue; }
  if (cls.includes('part-opener')) {
    const kicker = $el.find('.kicker').text().trim();
    const title = $el.find('h2').text().trim();
    const desc = $el.find('.part-desc').text().trim();
    push(headingPara(`${kicker} — ${title}`, HeadingLevel.HEADING_1, id, { size: 34, pageBreakBefore: true, before: 0, after: 160, color: C.navy950 }));
    if (desc) push(para(desc, { align: AlignmentType.RIGHT, italics: true, color: C.ink500, size: 20, after: 260 }));
    count++;
    continue;
  }
  if (id === 'toc') { count++; continue; } // replaced by native TOC field, inserted just before مقدمة المؤلف
  if (id === 'index') { count++; continue; } // replaced by generated analytical index at the end

  if (cls.includes('page')) {
    if (id && id.startsWith('muqaddimah') && !tocInserted) { push(buildTocBlock()); tocInserted = true; }
    if (id === 'glossary') collectIndex = false;
    push(renderInner($el));
    count++;
    continue;
  }
  // anything else at top level
  push(renderNode(el));
  count++;
}

// ============================================================
// Assemble final document: title pages -> native TOC (inserted inline
// above, right before مقدمة المؤلف) -> body -> native index
// ============================================================
if (!tocInserted) {
  // fallback: no `id^=muqaddimah` page found — insert right after the cover/half-title block
  const insertAt = Math.min(2, body.length);
  body.splice(insertAt, 0, ...buildTocBlock());
}
const finalBody = body;

// ---------- Native analytical index (auto page numbers via PAGEREF) ----------
const indexBlock = [];
indexBlock.push(headingPara('الفهرس التحليلي', HeadingLevel.HEADING_1, 'native_index', { size: 32, pageBreakBefore: true, before: 0, after: 200 }));
for (const entry of indexEntries) {
  if (!entry.id) continue;
  const bm = bmName(entry.id);
  indexBlock.push(new Paragraph({
    bidirectional: true,
    alignment: AlignmentType.RIGHT,
    spacing: { after: 110 },
    children: [
      ...textRunsFor(entry.text, { size: 22, color: C.ink700 }),
      new TextRun({ rightToLeft: true, children: [new PositionalTab({ alignment: PositionalTabAlignment.LEFT, leader: PositionalTabLeader.DOT, relativeTo: PositionalTabRelativeTo.MARGIN })] }),
      new PageReference(bm, { font: FONT_UI, size: 20, bold: true, color: C.gold700 }),
    ],
  }));
}
finalBody.push(...indexBlock);

// ============================================================
// Build Document
// ============================================================
const docTitle = $('title').text().trim() || 'كتاب';
const docDescription = $('meta[name="description"]').attr('content') || '';
const docCreator = ($('.cover .credits .name').first().text() || '').trim() || 'مؤلف';

const doc = new Document({
  creator: docCreator,
  title: docTitle,
  description: docDescription,
  features: { updateFields: true },
  numbering: NUMBERING_CONFIG,
  styles: {
    default: {
      document: { run: { font: FONT_BODY, size: 22, color: C.ink900, rightToLeft: true }, paragraph: { spacing: { line: 300 } } },
    },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT_DISPLAY, size: 32, bold: true, color: C.navy950, rightToLeft: true },
        paragraph: { alignment: AlignmentType.RIGHT, spacing: { before: 240, after: 160 } } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT_DISPLAY, size: 28, bold: true, color: C.navy900, rightToLeft: true },
        paragraph: { alignment: AlignmentType.RIGHT, spacing: { before: 300, after: 140 }, border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: C.gold500, space: 4 } } } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT_UI, size: 23, bold: true, color: C.gold700, rightToLeft: true },
        paragraph: { alignment: AlignmentType.RIGHT, spacing: { before: 260, after: 120 } } },
    ],
  },
  sections: [
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4 in twips
          margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 },
        },
        rtlGutter: true,
      },
      headers: {
        default: new Header({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER, bidirectional: true,
            children: [mkRun(HEADER_TITLE, { size: 16, color: C.ink500, font: FONT_UI })],
          })],
        }),
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER, bidirectional: true,
            children: [new TextRun({ children: [PageNumber.CURRENT], font: FONT_UI, size: 18, color: C.gold700 })],
          })],
        }),
      },
      children: finalBody,
    },
  ],
});

Packer.toBuffer(doc).then((buf) => {
  require('fs').writeFileSync(OUT_PATH, buf);
  console.log('Wrote', OUT_PATH, buf.length, 'bytes. body blocks:', finalBody.length, 'indexEntries:', indexEntries.length);
});
