package com.misbaha.tasbeeh.data.local

import androidx.room.Entity
import androidx.room.ForeignKey
import androidx.room.Index
import androidx.room.PrimaryKey

/** Mirrors /docs/05-DATABASE-SCHEMA.md §2 (on-device Room schema). */

@Entity(tableName = "dhikr_definitions")
data class DhikrDefinitionEntity(
    @PrimaryKey val id: String,
    val category: String,
    val arabicText: String,
    val transliteration: String,
    val translationEn: String,
    val sourceCitation: String,
    val authenticityGrade: String,
    val defaultTargetCount: Int,
    val contentVersion: Int,
    val governanceSignoffId: String,
)

@Entity(tableName = "counter_sessions")
data class CounterSessionEntity(
    @PrimaryKey val id: String,
    val dhikrDefinitionId: String?,
    val targetCount: Int,
    val startedAt: Long,
    val completedAt: Long?,
    val contextTag: String?,
)

@Entity(
    tableName = "dhikr_events",
    foreignKeys = [
        ForeignKey(
            entity = CounterSessionEntity::class,
            parentColumns = ["id"],
            childColumns = ["sessionId"],
        ),
    ],
    indices = [Index("sessionId"), Index("syncedAt")],
)
data class DhikrEventEntity(
    @PrimaryKey val id: String,
    val sessionId: String,
    val increment: Int,
    val occurredAt: Long,
    val source: String,
    val syncedAt: Long?,
)
