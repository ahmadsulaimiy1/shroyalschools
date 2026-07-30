package com.misbaha.tasbeeh.data.repository

import com.misbaha.tasbeeh.data.local.CounterSessionDao
import com.misbaha.tasbeeh.data.local.CounterSessionEntity
import com.misbaha.tasbeeh.data.local.DhikrEventDao
import com.misbaha.tasbeeh.data.local.DhikrEventEntity
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.combine
import java.util.UUID
import javax.inject.Inject

/**
 * Room is the single source of truth (offline-first repository pattern) — see
 * /docs/04-ANDROID-ARCHITECTURE.md §4. The counter tap path never touches the network directly.
 */
class CounterRepository @Inject constructor(
    private val sessionDao: CounterSessionDao,
    private val eventDao: DhikrEventDao,
) {
    suspend fun startSession(dhikrDefinitionId: String?, targetCount: Int, contextTag: String? = null): String {
        val sessionId = UUID.randomUUID().toString()
        sessionDao.upsert(
            CounterSessionEntity(
                id = sessionId,
                dhikrDefinitionId = dhikrDefinitionId,
                targetCount = targetCount,
                startedAt = System.currentTimeMillis(),
                completedAt = null,
                contextTag = contextTag,
            ),
        )
        return sessionId
    }

    suspend fun recordTap(sessionId: String, source: String = "tap") {
        eventDao.insert(
            DhikrEventEntity(
                id = UUID.randomUUID().toString(),
                sessionId = sessionId,
                increment = 1,
                occurredAt = System.currentTimeMillis(),
                source = source,
                syncedAt = null,
            ),
        )
    }

    suspend fun completeSession(session: CounterSessionEntity) {
        sessionDao.update(session.copy(completedAt = System.currentTimeMillis()))
    }

    fun observeSessionProgress(sessionId: String): Flow<Pair<CounterSessionEntity?, Int>> =
        combine(sessionDao.observeById(sessionId), eventDao.observeCountForSession(sessionId)) { session, count ->
            session to count
        }
}
