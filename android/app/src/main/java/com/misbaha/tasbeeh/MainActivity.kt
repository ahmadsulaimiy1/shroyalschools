package com.misbaha.tasbeeh

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Surface
import androidx.compose.ui.Modifier
import com.misbaha.tasbeeh.theme.MisbahaTheme
import com.misbaha.tasbeeh.ui.counter.CounterScreen
import dagger.hilt.android.AndroidEntryPoint

/**
 * Zero-friction first run: the app opens directly into the Counter tab, no login wall — see
 * /docs/02-DESIGN-SYSTEM.md §4.1. Full bottom-nav (Home/Counter/Library/Journal/Settings) is the
 * next slice of this scaffold; this MVP wires the single highest-priority screen end to end.
 */
@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MisbahaTheme {
                Surface(modifier = Modifier.fillMaxSize()) {
                    CounterScreen()
                }
            }
        }
    }
}
