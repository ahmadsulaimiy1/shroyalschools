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
class DatabaseHelper {
  DatabaseHelper._internal();
  static final DatabaseHelper instance = DatabaseHelper._internal();

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
      version: 1,
      onCreate: (db, version) async {
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
      },
    );
  }

  Future<void> resetAllData() async {
    final db = await database;
    await db.delete('dhikr_events');
    await db.delete('counter_sessions');
  }
}
