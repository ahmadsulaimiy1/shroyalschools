import 'dart:math';

import 'package:sqflite/sqflite.dart';

import 'database_helper.dart';

class DailyCount {
  const DailyCount(this.date, this.count);
  final DateTime date;
  final int count;
}

class CounterRepository {
  CounterRepository(this._db);
  final DatabaseHelper _db;

  final _random = Random();

  String _newId() =>
      '${DateTime.now().microsecondsSinceEpoch}-${_random.nextInt(999999)}';

  Future<String> startSession({required String? dhikrId, required int targetCount}) async {
    final db = await _db.database;
    final id = _newId();
    await db.insert('counter_sessions', {
      'id': id,
      'dhikr_id': dhikrId,
      'target_count': targetCount,
      'started_at': DateTime.now().millisecondsSinceEpoch,
      'completed_at': null,
    });
    return id;
  }

  Future<void> recordTap(String sessionId, {String source = 'tap'}) async {
    final db = await _db.database;
    await db.insert('dhikr_events', {
      'id': _newId(),
      'session_id': sessionId,
      'occurred_at': DateTime.now().millisecondsSinceEpoch,
      'source': source,
    });
  }

  Future<void> completeSession(String sessionId) async {
    final db = await _db.database;
    await db.update(
      'counter_sessions',
      {'completed_at': DateTime.now().millisecondsSinceEpoch},
      where: 'id = ?',
      whereArgs: [sessionId],
    );
  }

  Future<int> countForSession(String sessionId) async {
    final db = await _db.database;
    final result = await db.rawQuery(
      'SELECT COUNT(*) as c FROM dhikr_events WHERE session_id = ?',
      [sessionId],
    );
    return Sqflite.firstIntValue(result) ?? 0;
  }

  Future<int> countSince(DateTime since) async {
    final db = await _db.database;
    final result = await db.rawQuery(
      'SELECT COUNT(*) as c FROM dhikr_events WHERE occurred_at >= ?',
      [since.millisecondsSinceEpoch],
    );
    return Sqflite.firstIntValue(result) ?? 0;
  }

  Future<int> lifetimeCount() async {
    final db = await _db.database;
    final result = await db.rawQuery('SELECT COUNT(*) as c FROM dhikr_events');
    return Sqflite.firstIntValue(result) ?? 0;
  }

  Future<int> sessionCount() async {
    final db = await _db.database;
    final result = await db.rawQuery('SELECT COUNT(*) as c FROM counter_sessions');
    return Sqflite.firstIntValue(result) ?? 0;
  }

  /// Daily totals for the last [days] days (including today), oldest first.
  Future<List<DailyCount>> dailyCounts(int days) async {
    final db = await _db.database;
    final now = DateTime.now();
    final startOfRange = DateTime(now.year, now.month, now.day).subtract(Duration(days: days - 1));

    final rows = await db.rawQuery(
      'SELECT occurred_at FROM dhikr_events WHERE occurred_at >= ?',
      [startOfRange.millisecondsSinceEpoch],
    );

    final buckets = <String, int>{};
    for (var i = 0; i < days; i++) {
      final day = startOfRange.add(Duration(days: i));
      buckets[_dayKey(day)] = 0;
    }
    for (final row in rows) {
      final ts = row['occurred_at'] as int;
      final day = DateTime.fromMillisecondsSinceEpoch(ts);
      final key = _dayKey(DateTime(day.year, day.month, day.day));
      if (buckets.containsKey(key)) {
        buckets[key] = (buckets[key] ?? 0) + 1;
      }
    }

    return List.generate(days, (i) {
      final day = startOfRange.add(Duration(days: i));
      return DailyCount(day, buckets[_dayKey(day)] ?? 0);
    });
  }

  String _dayKey(DateTime d) => '${d.year}-${d.month}-${d.day}';

  Future<void> resetAllData() => _db.resetAllData();
}
