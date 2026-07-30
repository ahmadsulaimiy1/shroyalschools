package com.misbaha.tasbeeh.data.local

/**
 * Minimal offline-available seed matching the sample entries in /docs/05-DATABASE-SCHEMA.md.
 * In production this table is populated by the content-sync API
 * (/docs/06-API-DOCUMENTATION.md §3) and every row passes Governance Board review
 * (/docs/03-BRAND-IDENTITY.md §6) before shipping — this fixture exists only so the app has a
 * working offline-first experience out of the box, and is clearly not a governance-approved feed.
 */
object SeedContent {
    val postSalahTriplet = listOf(
        DhikrDefinitionEntity(
            id = "seed-subhanallah",
            category = "POST_SALAH",
            arabicText = "سُبْحَانَ اللَّهِ",
            transliteration = "SubhanAllah",
            translationEn = "Glory be to Allah",
            sourceCitation = "Sahih Muslim 596 (reference — pending Governance Board sign-off)",
            authenticityGrade = "SAHIH",
            defaultTargetCount = 33,
            contentVersion = 0,
            governanceSignoffId = "unseeded",
        ),
        DhikrDefinitionEntity(
            id = "seed-alhamdulillah",
            category = "POST_SALAH",
            arabicText = "الْحَمْدُ لِلَّهِ",
            transliteration = "Alhamdulillah",
            translationEn = "Praise be to Allah",
            sourceCitation = "Sahih Muslim 596 (reference — pending Governance Board sign-off)",
            authenticityGrade = "SAHIH",
            defaultTargetCount = 33,
            contentVersion = 0,
            governanceSignoffId = "unseeded",
        ),
        DhikrDefinitionEntity(
            id = "seed-allahuakbar",
            category = "POST_SALAH",
            arabicText = "اللَّهُ أَكْبَرُ",
            transliteration = "Allahu Akbar",
            translationEn = "Allah is the Greatest",
            sourceCitation = "Sahih Muslim 596 (reference — pending Governance Board sign-off)",
            authenticityGrade = "SAHIH",
            defaultTargetCount = 34,
            contentVersion = 0,
            governanceSignoffId = "unseeded",
        ),
    )
}
