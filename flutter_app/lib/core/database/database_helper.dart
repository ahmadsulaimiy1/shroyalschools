import 'package:path/path.dart';
import 'package:sqflite/sqflite.dart';

/// Fully offline local database. No network calls anywhere in this app.
///
/// Schema:
///  - counter_sessions: one row per counting session (a dhikr + a target count)
///  - dhikr_events: append-only tap ledger (never updated/deleted individually),
///    mirroring the offline-first event-sourcing pattern — see the platform docs
///    at /docs/05-DATABASE-SCHEMA.md for the full-scale cloud-synced version of
///    this same shape.
///  - adhkar (v2): the Phase 2 Adhkar library — see core/models/adhkar_entry.dart
///    for the field-by-field schema this table implements.
class DatabaseHelper {
  DatabaseHelper._internal();
  static final DatabaseHelper instance = DatabaseHelper._internal();

  static const int schemaVersion = 2;

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
      },
      onUpgrade: (db, oldVersion, newVersion) async {
        if (oldVersion < 2) {
          await _createAdhkarTable(db);
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

  Future<void> resetAllData() async {
    final db = await database;
    await db.delete('dhikr_events');
    await db.delete('counter_sessions');
  }
}
