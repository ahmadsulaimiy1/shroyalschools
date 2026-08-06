import 'package:flutter/material.dart';

import '../../../core/localization/app_localizations.dart';
import '../../../core/models/quran_chapter.dart';
import '../../../core/models/quran_verse.dart';

/// Converts a non-negative integer to Eastern Arabic-Indic numerals
/// (٠١٢٣٤٥٦٧٨٩), as printed in a real Mushaf.
String toArabicIndicDigits(int n) {
  const western = '0123456789';
  const eastern = ['٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'];
  return n.toString().split('').map((c) {
    final i = western.indexOf(c);
    return i == -1 ? c : eastern[i];
  }).join();
}

/// Renders a continuous Mushaf-style flow of Arabic verse text: no per-verse
/// cards, verses run together as a single justified paragraph broken only by
/// small ornamental ayah-end markers, with a surah header banner + Bismillah
/// wherever a new surah begins within [verses]. This is deliberately
/// Arabic-only (a real Mushaf page carries no interlinear translation) --
/// Reading Mode A/B/C governs the card view; this widget is what "Madani
/// Mushaf Mode" switches to instead.
class MushafFlowText extends StatelessWidget {
  const MushafFlowText({
    super.key,
    required this.verses,
    required this.chapters,
    required this.textColor,
    required this.accentColor,
    this.fontScale = 1.0,
    this.onVerseTap,
  });

  final List<QuranVerse> verses;

  /// Chapter metadata keyed by surah number, used to print each surah's
  /// header banner (Arabic name + Bismillah) wherever a new surah starts.
  final Map<int, QuranChapter> chapters;
  final Color textColor;
  final Color accentColor;
  final double fontScale;
  final ValueChanged<QuranVerse>? onVerseTap;

  static const _bismillah = 'بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ';

  @override
  Widget build(BuildContext context) {
    final baseSize = 22.0 * fontScale;
    final children = <Widget>[];
    int? lastSurah;

    for (final v in verses) {
      if (v.surah != lastSurah) {
        final chapter = chapters[v.surah];
        if (chapter != null) {
          children.add(_SurahHeader(chapter: chapter, accentColor: accentColor, textColor: textColor));
          // At-Tawbah (9) traditionally omits the Bismillah; al-Fatiha's
          // first verse already *is* the Bismillah, so it isn't repeated.
          if (v.surah != 9 && v.surah != 1) {
            children.add(
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 12),
                child: Text(
                  _bismillah,
                  textAlign: TextAlign.center,
                  textDirection: TextDirection.rtl,
                  style: TextStyle(fontFamily: 'AmiriQuran', fontSize: baseSize * 0.95, color: textColor, height: 2.0),
                ),
              ),
            );
          }
        }
        lastSurah = v.surah;
      }

      children.add(
        GestureDetector(
          onTap: onVerseTap == null ? null : () => onVerseTap!(v),
          child: RichText(
            // Not TextAlign.justify: Flutter's justify only stretches
            // inter-word spacing, which is not how a real Mushaf justifies
            // Arabic (proper Quranic justification elongates letters via
            // kashida/tatweel, encoded directly into page-specific glyphs --
            // see the pending King Fahd Mushaf page-layout import). Naive
            // word-spacing justification on a cursive script reads as
            // unnaturally gappy, so right-alignment is the honest choice
            // until that data is in.
            textAlign: TextAlign.right,
            textDirection: TextDirection.rtl,
            text: TextSpan(
              children: [
                TextSpan(
                  text: '${v.arabicText} ',
                  // Arabic is a cursive/joining script -- any non-zero
                  // letterSpacing inserts a gap after every shaped glyph
                  // cluster, which visually breaks letter joining. Never
                  // apply letterSpacing to Arabic text.
                  style: TextStyle(fontFamily: 'AmiriQuran', fontSize: baseSize, color: textColor, height: 2.4, letterSpacing: 0.0),
                ),
                WidgetSpan(
                  alignment: PlaceholderAlignment.middle,
                  child: _AyahMarker(number: v.ayah, color: accentColor, textColor: textColor, size: baseSize * 0.62),
                ),
                if (v.isSajdah)
                  WidgetSpan(
                    alignment: PlaceholderAlignment.middle,
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 3),
                      child: _SajdahMarker(color: accentColor, size: baseSize * 0.62),
                    ),
                  ),
                const TextSpan(text: '  '),
              ],
            ),
          ),
        ),
      );
    }

    return Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: children);
  }
}

class _SurahHeader extends StatelessWidget {
  const _SurahHeader({required this.chapter, required this.accentColor, required this.textColor});
  final QuranChapter chapter;
  final Color accentColor;
  final Color textColor;

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: const EdgeInsets.only(top: 20, bottom: 4),
      padding: const EdgeInsets.all(3),
      decoration: BoxDecoration(border: Border.all(color: accentColor, width: 1), borderRadius: BorderRadius.circular(6)),
      child: Container(
        padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 12),
        decoration: BoxDecoration(
          border: Border.all(color: accentColor, width: 1.4),
          borderRadius: BorderRadius.circular(3),
        ),
        child: Column(
          children: [
            _CornerFlourish(color: accentColor),
            const SizedBox(height: 6),
            Text(
              chapter.nameArabic,
              textDirection: TextDirection.rtl,
              style: TextStyle(fontFamily: 'AmiriQuran', fontSize: 26, color: accentColor, fontWeight: FontWeight.w600),
            ),
            const SizedBox(height: 4),
            Text(
              '${chapter.nameTransliteration} · ${chapter.revelationType == 'meccan' ? context.loc.t('quran_meccan') : context.loc.t('quran_medinan')}',
              style: TextStyle(fontSize: 12, color: textColor.withOpacity(0.65), letterSpacing: 0.5),
            ),
            const SizedBox(height: 6),
            _CornerFlourish(color: accentColor),
          ],
        ),
      ),
    );
  }
}

/// A small diamond-and-dots flourish, the kind of restrained ornament used
/// above/below a real Mushaf's surah-header banner -- deliberately simple
/// (a handful of shapes, no image assets) to keep with this app's dignity-
/// over-decoration design brief.
class _CornerFlourish extends StatelessWidget {
  const _CornerFlourish({required this.color});
  final Color color;

  @override
  Widget build(BuildContext context) {
    Widget dot() => Container(width: 4, height: 4, decoration: BoxDecoration(shape: BoxShape.circle, color: color));
    Widget diamond() => Transform.rotate(
          angle: 0.785398, // 45 degrees
          child: Container(width: 7, height: 7, color: color),
        );
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [dot(), const SizedBox(width: 6), diamond(), const SizedBox(width: 6), dot()],
    );
  }
}

/// The traditional printed-Mushaf sajdah (prostration) mark -- a small
/// domed/pointed outline enclosing the ۩ glyph itself, matching how this
/// symbol is set apart from the ordinary ayah-end rosette in real Mushafs.
/// Shown only on the 15 verses whose bundled Arabic text already carries
/// this mark (see [QuranVerse.isSajdah]).
class _SajdahMarker extends StatelessWidget {
  const _SajdahMarker({required this.color, required this.size});
  final Color color;
  final double size;

  @override
  Widget build(BuildContext context) {
    return Tooltip(
      message: context.loc.t('quran_sajdah_verse'),
      child: Container(
        width: size,
        height: size,
        alignment: Alignment.center,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          border: Border.all(color: color, width: 1.2),
        ),
        child: Text(
          '۩',
          textDirection: TextDirection.rtl,
          style: TextStyle(fontFamily: 'AmiriQuran', fontSize: size * 0.7, color: color, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }
}

/// A double-ring circular Mushaf-style ayah-end marker (rosette) with the
/// ayah number printed in Arabic-Indic numerals at its centre.
class _AyahMarker extends StatelessWidget {
  const _AyahMarker({required this.number, required this.color, required this.textColor, required this.size});
  final int number;
  final Color color;
  final Color textColor;
  final double size;

  @override
  Widget build(BuildContext context) {
    return Container(
      width: size,
      height: size,
      alignment: Alignment.center,
      padding: const EdgeInsets.all(1.5),
      decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: color, width: 1)),
      child: Container(
        alignment: Alignment.center,
        decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: color, width: 1)),
        child: Text(
          toArabicIndicDigits(number),
          textDirection: TextDirection.rtl,
          style: TextStyle(fontSize: size * 0.42, color: textColor, fontWeight: FontWeight.w600),
        ),
      ),
    );
  }
}
