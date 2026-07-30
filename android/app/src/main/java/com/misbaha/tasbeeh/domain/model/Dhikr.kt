package com.misbaha.tasbeeh.domain.model

/**
 * Platform-agnostic domain model — lives in a pure-Kotlin package deliberately so it can be
 * lifted into a shared `core-domain`/`core-model` module for the Kotlin Multiplatform / iOS
 * push described in /docs/04-ANDROID-ARCHITECTURE.md §1 without modification.
 */
data class DhikrDefinition(
    val id: String,
    val category: DhikrCategory,
    val arabicText: String,
    val transliteration: String,
    val translationEn: String,
    val sourceCitation: String,
    val authenticityGrade: AuthenticityGrade,
    val defaultTargetCount: Int,
)

enum class DhikrCategory {
    POST_SALAH, MORNING, EVENING, TRAVEL, RUQYAH, SLEEP, FREEFORM
}

enum class AuthenticityGrade {
    QURAN, SAHIH, HASAN, DAIF_REFERENCE_ONLY
}

data class CounterSession(
    val id: String,
    val dhikr: DhikrDefinition?,
    val targetCount: Int,
    val currentCount: Int,
    val startedAtEpochMs: Long,
    val completedAtEpochMs: Long?,
)
