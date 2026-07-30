enum DhikrCategory { postSalah, morning, evening, general }

/// A single verified dhikr entry. Text sourced from well-established, uncontroversial
/// adhkar (e.g. Hisn al-Muslim) — not a substitute for scholarly review at production scale.
class Dhikr {
  const Dhikr({
    required this.id,
    required this.category,
    required this.arabicText,
    required this.transliteration,
    required this.translationEn,
    required this.translationAr,
    required this.sourceCitation,
    required this.defaultTarget,
  });

  final String id;
  final DhikrCategory category;
  final String arabicText;
  final String transliteration;
  final String translationEn;
  final String translationAr;
  final String sourceCitation;
  final int defaultTarget;
}

/// Seed content shipped with the app so it is fully usable offline out of the box.
const List<Dhikr> seedAdhkar = [
  Dhikr(
    id: 'subhanallah',
    category: DhikrCategory.postSalah,
    arabicText: 'سُبْحَانَ اللَّهِ',
    transliteration: 'SubhanAllah',
    translationEn: 'Glory be to Allah',
    translationAr: 'تنزيه الله عن كل نقص',
    sourceCitation: 'Sahih Muslim 596',
    defaultTarget: 33,
  ),
  Dhikr(
    id: 'alhamdulillah',
    category: DhikrCategory.postSalah,
    arabicText: 'الْحَمْدُ لِلَّهِ',
    transliteration: 'Alhamdulillah',
    translationEn: 'Praise be to Allah',
    translationAr: 'الثناء على الله',
    sourceCitation: 'Sahih Muslim 596',
    defaultTarget: 33,
  ),
  Dhikr(
    id: 'allahuakbar',
    category: DhikrCategory.postSalah,
    arabicText: 'اللَّهُ أَكْبَرُ',
    transliteration: 'Allahu Akbar',
    translationEn: 'Allah is the Greatest',
    translationAr: 'الله أعظم من كل شيء',
    sourceCitation: 'Sahih Muslim 596',
    defaultTarget: 34,
  ),
  Dhikr(
    id: 'la_ilaha_illallah',
    category: DhikrCategory.general,
    arabicText: 'لَا إِلَٰهَ إِلَّا اللَّهُ',
    transliteration: 'La ilaha illallah',
    translationEn: 'There is no god but Allah',
    translationAr: 'كلمة التوحيد',
    sourceCitation: 'Sunan al-Tirmidhi 3585',
    defaultTarget: 100,
  ),
  Dhikr(
    id: 'astaghfirullah',
    category: DhikrCategory.general,
    arabicText: 'أَسْتَغْفِرُ اللَّهَ',
    transliteration: 'Astaghfirullah',
    translationEn: 'I seek forgiveness from Allah',
    translationAr: 'طلب المغفرة من الله',
    sourceCitation: 'Sahih al-Bukhari 6307',
    defaultTarget: 100,
  ),
  Dhikr(
    id: 'la_hawla',
    category: DhikrCategory.general,
    arabicText: 'لَا حَوْلَ وَلَا قُوَّةَ إِلَّا بِاللَّهِ',
    transliteration: 'La hawla wa la quwwata illa billah',
    translationEn: 'There is no might nor power except with Allah',
    translationAr: 'الاعتراف بالعجز والحول لله وحده',
    sourceCitation: 'Sahih al-Bukhari 6384',
    defaultTarget: 10,
  ),
  Dhikr(
    id: 'subhanallahi_wa_bihamdihi',
    category: DhikrCategory.morning,
    arabicText: 'سُبْحَانَ اللَّهِ وَبِحَمْدِهِ سُبْحَانَ اللَّهِ الْعَظِيمِ',
    transliteration: "SubhanAllahi wa bihamdihi, SubhanAllahil 'Adheem",
    translationEn: 'Glory and praise to Allah, glory to Allah the Magnificent',
    translationAr: 'تسبيح جامع بين التنزيه والحمد',
    sourceCitation: 'Sahih al-Bukhari 6682',
    defaultTarget: 100,
  ),
  Dhikr(
    id: 'salawat',
    category: DhikrCategory.general,
    arabicText: 'اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ',
    transliteration: 'Allahumma salli wa sallim ala Nabiyyina Muhammad',
    translationEn: 'O Allah, send blessings and peace upon our Prophet Muhammad',
    translationAr: 'الصلاة على النبي صلى الله عليه وسلم',
    sourceCitation: 'Traditional salawat',
    defaultTarget: 10,
  ),
  Dhikr(
    id: 'hasbiyallah',
    category: DhikrCategory.evening,
    arabicText: 'حَسْبِيَ اللَّهُ وَنِعْمَ الْوَكِيلُ',
    transliteration: "Hasbiyallahu wa ni'mal wakeel",
    translationEn: 'Allah is sufficient for us, and He is the best disposer of affairs',
    translationAr: 'التوكل الكامل على الله',
    sourceCitation: 'Sunan Abi Dawud 5081',
    defaultTarget: 7,
  ),
  Dhikr(
    id: 'dua_yunus',
    category: DhikrCategory.evening,
    arabicText: 'لَا إِلَٰهَ إِلَّا أَنْتَ سُبْحَانَكَ إِنِّي كُنْتُ مِنَ الظَّالِمِينَ',
    transliteration: "La ilaha illa anta subhanaka inni kuntu minaz-zalimeen",
    translationEn: 'There is no god but You, glory be to You, I was among the wrongdoers',
    translationAr: 'دعاء ذي النون عليه السلام',
    sourceCitation: 'Sunan al-Tirmidhi 3505',
    defaultTarget: 3,
  ),
];
