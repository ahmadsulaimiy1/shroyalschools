package com.misbaha.tasbeeh

import android.view.KeyEvent
import io.flutter.embedding.android.FlutterActivity
import io.flutter.embedding.engine.FlutterEngine
import io.flutter.plugin.common.MethodChannel

/**
 * Adds hardware volume-button counting on top of the standard Flutter host activity.
 * When enabled (toggled from the in-app Settings screen via the MethodChannel below),
 * volume key presses are consumed here — incrementing the dhikr counter instead of
 * changing the media volume — and forwarded to Dart.
 */
class MainActivity : FlutterActivity() {

    private val channelName = "com.misbaha.tasbeeh/volume_buttons"
    private var methodChannel: MethodChannel? = null
    private var volumeButtonCountingEnabled = false

    override fun configureFlutterEngine(flutterEngine: FlutterEngine) {
        super.configureFlutterEngine(flutterEngine)

        methodChannel = MethodChannel(flutterEngine.dartExecutor.binaryMessenger, channelName).apply {
            setMethodCallHandler { call, result ->
                when (call.method) {
                    "setEnabled" -> {
                        volumeButtonCountingEnabled = call.argument<Boolean>("enabled") ?: false
                        result.success(null)
                    }
                    else -> result.notImplemented()
                }
            }
        }
    }

    override fun onKeyDown(keyCode: Int, event: KeyEvent): Boolean {
        if (volumeButtonCountingEnabled &&
            (keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN)
        ) {
            methodChannel?.invokeMethod("onVolumeButtonPressed", null)
            return true // consume the event so the system volume UI does not appear
        }
        return super.onKeyDown(keyCode, event)
    }

    override fun onKeyUp(keyCode: Int, event: KeyEvent): Boolean {
        if (volumeButtonCountingEnabled &&
            (keyCode == KeyEvent.KEYCODE_VOLUME_UP || keyCode == KeyEvent.KEYCODE_VOLUME_DOWN)
        ) {
            return true // also consume the matching key-up so no residual volume toast/action fires
        }
        return super.onKeyUp(keyCode, event)
    }
}
