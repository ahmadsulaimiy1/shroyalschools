package com.misbaha.tasbeeh.ui.counter

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.misbaha.tasbeeh.data.local.DhikrDefinitionDao
import com.misbaha.tasbeeh.data.local.SeedContent
import com.misbaha.tasbeeh.data.repository.CounterRepository
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import javax.inject.Inject

data class CounterUiState(
    val sessionId: String? = null,
    val currentCount: Int = 0,
    val targetCount: Int = 33,
    val dhikrLabelAr: String = "سُبْحَانَ اللَّهِ",
    val dhikrLabelEn: String = "SubhanAllah",
    val isCompleted: Boolean = false,
)

/**
 * Unidirectional data flow ViewModel — single immutable UiState mutated only through intents,
 * per /docs/04-ANDROID-ARCHITECTURE.md §4. Tap handling never performs disk I/O on the calling
 * thread; the repository call is dispatched onto viewModelScope so the UI thread stays free for
 * the <16ms tap-to-feedback budget in /docs/01-PRD.md §6.
 */
@HiltViewModel
class CounterViewModel @Inject constructor(
    private val repository: CounterRepository,
    private val dhikrDefinitionDao: DhikrDefinitionDao,
) : ViewModel() {

    private val _uiState = MutableStateFlow(CounterUiState())
    val uiState: StateFlow<CounterUiState> = _uiState.asStateFlow()

    init {
        viewModelScope.launch {
            // Fixture seed only — production content arrives via the Governance-Board-approved
            // sync API, see /docs/06-API-DOCUMENTATION.md §3 and data/local/SeedContent.kt.
            dhikrDefinitionDao.upsertAll(SeedContent.postSalahTriplet)
            val sessionId = repository.startSession(dhikrDefinitionId = "seed-subhanallah", targetCount = 33)
            _uiState.value = _uiState.value.copy(sessionId = sessionId)
        }
    }

    fun onBeadTapped() {
        val state = _uiState.value
        val sessionId = state.sessionId ?: return
        if (state.isCompleted) return

        val newCount = state.currentCount + 1
        _uiState.value = state.copy(
            currentCount = newCount,
            isCompleted = newCount >= state.targetCount,
        )
        viewModelScope.launch {
            repository.recordTap(sessionId)
        }
    }

    fun onReset() {
        viewModelScope.launch {
            val sessionId = repository.startSession(dhikrDefinitionId = "seed-subhanallah", targetCount = _uiState.value.targetCount)
            _uiState.value = _uiState.value.copy(sessionId = sessionId, currentCount = 0, isCompleted = false)
        }
    }

    fun onTargetSelected(target: Int) {
        _uiState.value = _uiState.value.copy(targetCount = target, isCompleted = _uiState.value.currentCount >= target)
    }
}
