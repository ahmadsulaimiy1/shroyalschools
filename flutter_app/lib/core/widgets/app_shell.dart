import 'package:flutter/material.dart';

import '../../features/adhkar/adhkar_screen.dart';
import '../../features/counter/counter_screen.dart';
import '../../features/home/home_screen.dart';
import '../../features/quran/quran_screen.dart';
import '../../features/settings/settings_screen.dart';
import '../../features/statistics/statistics_screen.dart';
import '../localization/app_localizations.dart';

/// Root navigation shell: Home / Counter / Qur'an / Adhkar / Statistics /
/// Settings. About is reached from Settings, not a top-level tab.
class AppShell extends StatefulWidget {
  const AppShell({super.key, this.initialIndex = 0});

  final int initialIndex;

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  late int _index = widget.initialIndex;

  final _screens = const [
    HomeScreen(),
    CounterScreen(),
    QuranScreen(),
    AdhkarScreen(),
    StatisticsScreen(),
    SettingsScreen(),
  ];

  void goToCounter() => setState(() => _index = 1);
  void goToQuran() => setState(() => _index = 2);

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    return AppShellScope(
      goToCounter: goToCounter,
      goToQuran: goToQuran,
      child: Scaffold(
        body: IndexedStack(index: _index, children: _screens),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _index,
          onDestinationSelected: (i) => setState(() => _index = i),
          destinations: [
            NavigationDestination(icon: const Icon(Icons.home_outlined), selectedIcon: const Icon(Icons.home), label: t('nav_home')),
            NavigationDestination(icon: const Icon(Icons.fingerprint_outlined), selectedIcon: const Icon(Icons.fingerprint), label: t('nav_counter')),
            NavigationDestination(icon: const Icon(Icons.menu_book_outlined), selectedIcon: const Icon(Icons.menu_book), label: t('nav_quran')),
            NavigationDestination(icon: const Icon(Icons.auto_stories_outlined), selectedIcon: const Icon(Icons.auto_stories), label: t('nav_adhkar')),
            NavigationDestination(icon: const Icon(Icons.bar_chart_outlined), selectedIcon: const Icon(Icons.bar_chart), label: t('nav_statistics')),
            NavigationDestination(icon: const Icon(Icons.settings_outlined), selectedIcon: const Icon(Icons.settings), label: t('nav_settings')),
          ],
        ),
      ),
    );
  }
}

/// Lets any descendant screen (e.g. Home's "Start Counting"/"Continue Reading"
/// cards) jump straight to the Counter or Qur'an tab without a full route push.
class AppShellScope extends InheritedWidget {
  const AppShellScope({super.key, required this.goToCounter, required this.goToQuran, required super.child});

  final VoidCallback goToCounter;
  final VoidCallback goToQuran;

  static AppShellScope? maybeOf(BuildContext context) =>
      context.dependOnInheritedWidgetOfExactType<AppShellScope>();

  @override
  bool updateShouldNotify(AppShellScope oldWidget) => false;
}
