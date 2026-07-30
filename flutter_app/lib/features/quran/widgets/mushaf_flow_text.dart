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
            textAlign: TextAlign.justify,
            textDirection: TextDirection.rtl,
            text: TextSpan(
              children: [
                TextSpan(
                  text: '${v.arabicText} ',
                  style: TextStyle(fontFamily: 'AmiriQuran', fontSize: baseSize, color: textColor, height: 2.4, letterSpacing: 0.3),
                ),
                WidgetSpan(
                  alignment: PlaceholderAlignment.middle,
                  child: _AyahMarker(number: v.ayah, color: accentColor, textColor: textColor, size: baseSize * 0.62),
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
      padding: const EdgeInsets.symmetric(vertical: 14, horizontal: 12),
      decoration: BoxDecoration(
        border: Border.all(color: accentColor, width: 1.4),
        borderRadius: BorderRadius.circular(4),
      ),
      child: Column(
        children: [
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
        ],
      ),
    );
  }
}

/// A small circular Mushaf-style ayah-end marker (rosette) with the ayah
/// number printed in Arabic-Indic numerals at its centre.
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
      decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: color, width: 1.2)),
      child: Text(
        toArabicIndicDigits(number),
        textDirection: TextDirection.rtl,
        style: TextStyle(fontSize: size * 0.48, color: textColor, fontWeight: FontWeight.w600),
      ),
    );
  }
}
