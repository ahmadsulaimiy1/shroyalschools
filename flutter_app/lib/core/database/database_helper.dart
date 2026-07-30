import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

/// Fully offline local database (except the Qur'an audio cache metadata,
/// which only ever stores where a downloaded recitation file lives on disk).
///
/// Schema:
///  - counter_sessions: one row per counting session (a dhikr + a target count)
///  - dhikr_events: append-only tap ledger (never updated/deleted individually),
///    mirroring the offline-first event-sourcing pattern — see the platform docs
///    at /docs/05-DATABASE-SCHEMA.md for the full-scale cloud-synced version of
///    this same shape.
///  - adhkar (v2): the Phase 2 Adhkar library — see core/models/adhkar_entry.dart
///    for the field-by-field schema this table implements.
///  - quran_bookmarks / quran_favourites / quran_last_read / quran_reads (v3):
///    user-generated Qur'an reading state — the verse text/translation itself
///    is not stored here, it's loaded from the bundled assets/quran/*.json at
///    runtime (see core/database/quran_repository.dart).
///  - quran_bookmarks.label / quran_verse_notes (v4): an optional label on a
///    bookmark (e.g. "For Friday khutbah") and free-text reflection/study
///    notes on any verse, bookmarked or not.
///  - khatm_plan (v5): a single active Khatm (Qur'an-completion) plan --
///    start date + target date, used to compute a daily verse target
///    against the existing quran_reads log.
class DatabaseHelper {
  DatabaseHelper._internal();
  static final DatabaseHelper instance = DatabaseHelper._internal();

  static const int schemaVersion = 5;

  static Database? _database;

  Future<Database> get database async {
    _database ??= await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async {
    final dbPath = await getDatabasesPath();
    final path = join(dbPath, 'misbaha.db');
    return openDatabase(
      path,
      version: schemaVersion,
      onCreate: (db, version) async {
        await _createCounterTables(db);
        await _createAdhkarTable(db);
        await _createQuranTables(db);
        await _createKhatmTable(db);
      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await _createAdhkarTable(db);
        }
        if (oldVersion < 3) {
          await _createQuranTables(db);
        }
        if (oldVersion < 4) {
          // v4 adds an optional label to bookmarks and a free-text
          // reflection-note table -- _createQuranTables is idempotent
          // (IF NOT EXISTS) so it's safe to re-run for the new
          // quran_verse_notes table; the label column needs an explicit
          // ALTER TABLE since SQLite has no "ADD COLUMN IF NOT EXISTS".
          await _createQuranTables(db);
          final columns = await db.rawQuery('PRAGMA table_info(quran_bookmarks)');
          final hasLabel = columns.any((c) => c['name'] == 'label');
          if (!hasLabel) {
            await db.execute('ALTER TABLE quran_bookmarks ADD COLUMN label TEXT');
          }
        }
        if (oldVersion < 5) {
          await _createKhatmTable(db);
        }
      },
    );
  }

  Future<void> _createCounterTables(Database db) async {
    await db.execute('''
      CREATE TABLE counter_sessions (
        id TEXT PRIMARY KEY,
        dhikr_id TEXT,
        target_count INTEGER NOT NULL,
        started_at INTEGER NOT NULL,
        completed_at INTEGER
      )
    ''');
    await db.execute('''
      CREATE TABLE dhikr_events (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL,
        occurred_at INTEGER NOT NULL,
        source TEXT NOT NULL
      )
    ''');
    await db.execute('CREATE INDEX idx_events_session ON dhikr_events (session_id)');
    await db.execute('CREATE INDEX idx_events_occurred_at ON dhikr_events (occurred_at)');
  }

  Future<void> _createAdhkarTable(Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS adhkar (
        id TEXT PRIMARY KEY,
        category TEXT NOT NULL,
        title_ar TEXT NOT NULL,
        title_en TEXT NOT NULL,
        arabic_text TEXT NOT NULL,
        transliteration TEXT NOT NULL,
        translation_en TEXT NOT NULL,
        source_reference TEXT NOT NULL,
        repetition_count INTEGER NOT NULL DEFAULT 1,
        repetition_note TEXT,
        audio_available INTEGER NOT NULL DEFAULT 1,
        favourite INTEGER NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL
      )
    ''');
    await db.execute('CREATE INDEX IF NOT EXISTS idx_adhkar_category ON adhkar (category)');
    await db.execute('CREATE INDEX IF NOT EXISTS idx_adhkar_favourite ON adhkar (favourite)');
  }

  Future<void> _createQuranTables(Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS quran_bookmarks (
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        label TEXT,
        created_at INTEGER NOT NULL,
        PRIMARY KEY (surah, ayah)
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS quran_favourites (
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        created_at INTEGER NOT NULL,
        PRIMARY KEY (surah, ayah)
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS quran_last_read (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        updated_at INTEGER NOT NULL
      )
    ''');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS quran_reads (
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        read_at INTEGER NOT NULL
      )
    ''');
    await db.execute('CREATE INDEX IF NOT EXISTS idx_quran_reads_read_at ON quran_reads (read_at)');
    await db.execute('''
      CREATE TABLE IF NOT EXISTS quran_verse_notes (
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        note TEXT NOT NULL,
        updated_at INTEGER NOT NULL,
        PRIMARY KEY (surah, ayah)
      )
    ''');
  }

  Future<void> _createKhatmTable(Database db) async {
    await db.execute('''
      CREATE TABLE IF NOT EXISTS khatm_plan (
        id INTEGER PRIMARY KEY CHECK (id = 1),
        start_date INTEGER NOT NULL,
        target_date INTEGER NOT NULL,
        created_at INTEGER NOT NULL
      )
    ''');
  }

  Future<void> resetAllData() async {
    final db = await database;
    await db.delete('dhikr_events');
    await db.delete('counter_sessions');
  }
}
