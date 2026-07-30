package com.misbaha.tasbeeh.theme

import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable

private val LightColors = lightColorScheme(
    primary = MisbahaColors.PrimaryLight,
    secondary = MisbahaColors.Gold,
    background = MisbahaColors.SurfaceLight,
    surface = MisbahaColors.SurfaceElevatedLight,
    onPrimary = MisbahaColors.SurfaceElevatedLight,
    onBackground = MisbahaColors.TextPrimaryLight,
    onSurface = MisbahaColors.TextPrimaryLight,
    onSurfaceVariant = MisbahaColors.TextSecondaryLight,
    error = MisbahaColors.ErrorLight,
)

// "Night Dhikr" theme — see /docs/03-BRAND-IDENTITY.md §3
private val DarkColors = darkColorScheme(
    primary = MisbahaColors.PrimaryDark,
    secondary = MisbahaColors.GoldDark,
    background = MisbahaColors.SurfaceDark,
    surface = MisbahaColors.SurfaceElevatedDark,
    onPrimary = MisbahaColors.SurfaceDark,
    onBackground = MisbahaColors.TextPrimaryDark,
    onSurface = MisbahaColors.TextPrimaryDark,
    onSurfaceVariant = MisbahaColors.TextSecondaryDark,
    error = MisbahaColors.ErrorDark,
)

@Composable
fun MisbahaTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    val colorScheme = if (darkTheme) DarkColors else LightColors
    MaterialTheme(
        colorScheme = colorScheme,
        typography = MisbahaTypography,
        shapes = MisbahaShapes,
        content = content,
    )
}
