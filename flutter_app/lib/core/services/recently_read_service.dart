import 'package:shared_preferences/shared_preferences.dart';

/// Tracks the most recently opened adhkar entries (most-recent-first, capped
/// at 20) so the Adhkar screen's "Recently Read" section can offer a quick
/// resume list. Persisted locally via SharedPreferences — fully offline.
class RecentlyReadService {
  static const _kRecentIds = 'adhkar_recently_read_ids';
  static const _maxEntries = 20;

  Future<List<String>> getRecentIds() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getStringList(_kRecentIds) ?? [];
  }

  Future<void> recordView(String id) async {
    final prefs = await SharedPreferences.getInstance();
    final current = prefs.getStringList(_kRecentIds) ?? [];
    final updated = [id, ...current.where((existing) => existing != id)];
    final capped = updated.length > _maxEntries ? updated.sublist(0, _maxEntries) : updated;
    await prefs.setStringList(_kRecentIds, capped);
  }
}
