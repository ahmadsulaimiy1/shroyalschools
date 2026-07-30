package com.misbaha.tasbeeh.data.local

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import kotlinx.coroutines.flow.Flow

@Dao
interface DhikrDefinitionDao {
    @Query("SELECT * FROM dhikr_definitions WHERE category = :category")
    fun observeByCategory(category: String): Flow<List<DhikrDefinitionEntity>>

    @Query("SELECT * FROM dhikr_definitions WHERE id = :id")
    suspend fun getById(id: String): DhikrDefinitionEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsertAll(items: List<DhikrDefinitionEntity>)
}

@Dao
interface CounterSessionDao {
    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun upsert(session: CounterSessionEntity)

    @Update
    suspend fun update(session: CounterSessionEntity)

    @Query("SELECT * FROM counter_sessions WHERE id = :id")
    fun observeById(id: String): Flow<CounterSessionEntity?>

    @Query("SELECT * FROM counter_sessions ORDER BY startedAt DESC LIMIT 50")
    fun observeRecent(): Flow<List<CounterSessionEntity>>
}

@Dao
interface DhikrEventDao {
    // The counting ledger is append-only by design — see /docs/04-ANDROID-ARCHITECTURE.md §4
    // (offline-first sync strategy). Events are never updated or deleted, only inserted.
    @Insert(onConflict = OnConflictStrategy.IGNORE)
    suspend fun insert(event: DhikrEventEntity)

    @Query("SELECT COUNT(*) FROM dhikr_events WHERE sessionId = :sessionId")
    fun observeCountForSession(sessionId: String): Flow<Int>

    @Query("SELECT * FROM dhikr_events WHERE syncedAt IS NULL ORDER BY occurredAt ASC LIMIT :limit")
    suspend fun getUnsyncedBatch(limit: Int = 500): List<DhikrEventEntity>

    @Query("UPDATE dhikr_events SET syncedAt = :syncedAt WHERE id IN (:ids)")
    suspend fun markSynced(ids: List<String>, syncedAt: Long)
}
