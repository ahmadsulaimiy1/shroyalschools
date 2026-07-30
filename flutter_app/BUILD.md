# Build, Package & Publish — Misbaha (Flutter)

## 0. Fastest path: let CI build the APK for you

Every push to this repo that touches `flutter_app/` triggers
`.github/workflows/build-flutter-apk.yml`, which builds a real release APK/AAB on a
GitHub-hosted runner (full Android SDK + internet access) and:
- uploads them as workflow artifacts (Actions tab → latest run → Artifacts), and
- publishes/updates a GitHub Release tagged **`latest-apk`** with `app-release.apk` and
  `app-release.aab` attached — the easiest way to just download and install the app.

You can also trigger it manually: **Actions → Build Misbaha APK → Run workflow**.

## 1. Prerequisites (local build)

- Flutter SDK ≥ 3.24 (`flutter --version`)
- Android SDK + a JDK 17 (Android Studio's bundled JDK works)
- `flutter doctor` shows no blocking issues for Android

## 2. First-time setup

```bash
cd flutter_app
flutter pub get
dart run flutter_launcher_icons     # generates mipmap/adaptive launcher icons from assets/icon/
```

`android/local.properties` is generated automatically by Flutter tooling on first
`flutter pub get` / `flutter build` — do not hand-create or commit it.

## 3. Build a debug APK (fastest, for testing on a device)

```bash
flutter build apk --debug
# output: build/app/outputs/flutter-apk/app-debug.apk
```

## 4. Build a release APK

```bash
flutter build apk --release
# output: build/app/outputs/flutter-apk/app-release.apk
```

Smaller, per-device APKs (recommended if distributing directly rather than via Play,
since a fat APK bundles all ABIs):

```bash
flutter build apk --release --split-per-abi
# outputs: app-armeabi-v7a-release.apk, app-arm64-v8a-release.apk, app-x86_64-release.apk
```

Install directly on a connected device: `flutter install` or
`adb install build/app/outputs/flutter-apk/app-release.apk`.

> **Note:** the release build type currently signs with the Android **debug key**
> (`android/app/build.gradle.kts` → `signingConfig = signingConfigs.getByName("debug")`) specifically so
> `flutter build apk --release` works immediately with zero setup. This is fine for
> sideloading/testing. **Before publishing to Google Play you must switch to a real
> release keystore** — see §6.

## 5. Build an Android App Bundle (AAB) — required for Google Play

```bash
flutter build appbundle --release
# output: build/app/outputs/bundle/release/app-release.aab
```

## 6. Set up a real release signing key (required before Play Store upload)

```bash
keytool -genkey -v -keystore ~/misbaha-release.jks \
  -keyalg RSA -keysize 2048 -validity 10000 -alias misbaha
```

Create `android/key.properties` (gitignored — never commit real signing secrets):

```properties
storePassword=<your keystore password>
keyPassword=<your key password>
keyAlias=misbaha
storeFile=/absolute/path/to/misbaha-release.jks
```

Edit `android/app/build.gradle.kts`:

```kotlin
import java.util.Properties

val keystoreProperties = Properties()
val keystorePropertiesFile = rootProject.file("key.properties")
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(keystorePropertiesFile.inputStream())
}

android {
    signingConfigs {
        create("release") {
            keyAlias = keystoreProperties["keyAlias"] as String?
            keyPassword = keystoreProperties["keyPassword"] as String?
            storeFile = keystoreProperties["storeFile"]?.let { file(it) }
            storePassword = keystoreProperties["storePassword"] as String?
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.getByName("release")   // was: getByName("debug")
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
}
```

Then rebuild: `flutter build appbundle --release`.

## 7. Publish to Google Play

1. Create a developer account at [play.google.com/console](https://play.google.com/console) (one-time $25 fee).
2. **Create app** → fill app name (Misbaha), default language (Arabic or English),
   app/game type, free/paid.
3. **Store listing**: short/full description, screenshots (phone + tablet, in both
   Arabic and English — see `/docs/12-STORE-PUBLISHING-PACKAGE.md` in the repo root
   for copy and asset specs), feature graphic, app icon (auto-pulled from the AAB).
4. **App content** section: complete the Data safety form (this app collects **no**
   data — everything is local/offline, see `about_privacy` string), content rating
   questionnaire, target audience, ads declaration (none), government apps
   declaration (no).
5. **Production → Create new release**: upload `app-release.aab`, add release notes.
6. Roll out to **Internal testing** first, verify install + core flows on a real
   device, then promote the same release to **Closed testing** → **Production**.
7. Play Console review typically takes a few hours to a few days for a new app.

## 8. Quick QA checklist before any release

- [ ] `flutter analyze` — no errors
- [ ] `flutter test` — all green
- [ ] Fresh install: Splash → Home → Counter tap works, count persists after app kill/reopen
- [ ] Toggle language to Arabic in Settings — full RTL mirroring, no clipped text
- [ ] Toggle dark mode — both themes readable, no invisible text
- [ ] Toggle Volume Button Counter on, press a volume key on a real device — count increments, no volume UI popup
- [ ] Reset Counter and Reset All Data both prompt for confirmation before acting
- [ ] Airplane mode on — every screen still fully functional (offline-first)
