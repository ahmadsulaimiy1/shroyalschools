import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../../core/localization/app_localizations.dart';
import '../../core/services/hijri_calendar_service.dart';
import '../../core/theme/app_colors.dart';
import '../quran/widgets/mushaf_flow_text.dart' show toArabicIndicDigits;

enum _CalendarView { month, agenda }

/// Hijri & Gregorian calendar centre: a Gregorian month grid with each day's
/// Hijri equivalent shown underneath (computed on-device, see
/// core/services/hijri_calendar_service.dart), plus an agenda view of
/// upcoming Islamic dates for the current Hijri year.
class IslamicCalendarScreen extends StatefulWidget {
  const IslamicCalendarScreen({super.key});

  @override
  State<IslamicCalendarScreen> createState() => _IslamicCalendarScreenState();
}

class _IslamicCalendarScreenState extends State<IslamicCalendarScreen> {
  static const _service = HijriCalendarService();

  _CalendarView _view = _CalendarView.month;
  late DateTime _visibleMonth;
  final _today = DateTime.now();

  @override
  void initState() {
    super.initState();
    _visibleMonth = DateTime(_today.year, _today.month);
  }

  void _changeMonth(int delta) {
    setState(() => _visibleMonth = DateTime(_visibleMonth.year, _visibleMonth.month + delta));
  }

  String _eventName(String Function(String) t, IslamicEvent e) => t('calendar_event_${e.key}');

  @override
  Widget build(BuildContext context) {
    final t = context.loc.t;
    final isArabic = context.loc.locale.languageCode == 'ar';
    final theme = Theme.of(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(t('calendar_title')),
        actions: [
          IconButton(
            icon: Icon(_view == _CalendarView.month ? Icons.event_note_outlined : Icons.calendar_month_outlined),
            tooltip: t('calendar_toggle_view'),
            onPressed: () => setState(() => _view = _view == _CalendarView.month ? _CalendarView.agenda : _CalendarView.month),
          ),
        ],
      ),
      body: _view == _CalendarView.month
          ? _MonthView(
              visibleMonth: _visibleMonth,
              today: _today,
              service: _service,
              isArabic: isArabic,
              theme: theme,
              t: t,
              onPrev: () => _changeMonth(-1),
              onNext: () => _changeMonth(1),
            )
          : _AgendaView(service: _service, from: _today, isArabic: isArabic, theme: theme, t: t, eventName: _eventName),
    );
  }
}

class _MonthView extends StatelessWidget {
  const _MonthView({
    required this.visibleMonth,
    required this.today,
    required this.service,
    required this.isArabic,
    required this.theme,
    required this.t,
    required this.onPrev,
    required this.onNext,
  });

  final DateTime visibleMonth;
  final DateTime today;
  final HijriCalendarService service;
  final bool isArabic;
  final ThemeData theme;
  final String Function(String) t;
  final VoidCallback onPrev;
  final VoidCallback onNext;

  static const _weekdayLabels = ['S', 'M', 'T', 'W', 'T', 'F', 'S'];

  @override
  Widget build(BuildContext context) {
    final firstOfMonth = DateTime(visibleMonth.year, visibleMonth.month, 1);
    final daysInMonth = DateTime(visibleMonth.year, visibleMonth.month + 1, 0).day;
    final leadingBlanks = firstOfMonth.weekday % 7; // DateTime.weekday: Mon=1..Sun=7 -> Sun=0

    final hijriFirst = service.toHijri(firstOfMonth);
    final monthNames = isArabic ? hijriMonthNamesAr : hijriMonthNamesEn;

    return Column(
      children: [
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 12),
          child: Row(
            children: [
              IconButton(icon: const Icon(Icons.chevron_left), onPressed: onPrev),
              Expanded(
                child: Column(
                  children: [
                    Text(DateFormat.yMMMM().format(visibleMonth), style: theme.textTheme.titleMedium),
                    Text(
                      '${monthNames[hijriFirst.month - 1]} ${hijriFirst.year} AH',
                      style: theme.textTheme.bodySmall?.copyWith(color: AppColors.gold),
                    ),
                  ],
                ),
              ),
              IconButton(icon: const Icon(Icons.chevron_right), onPressed: onNext),
            ],
          ),
        ),
        Row(
          children: _weekdayLabels
              .map((d) => Expanded(child: Center(child: Text(d, style: theme.textTheme.labelSmall))))
              .toList(),
        ),
        const Divider(height: 1),
        Expanded(
          child: GridView.builder(
            padding: const EdgeInsets.all(8),
            gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 7, childAspectRatio: 0.75),
            itemCount: leadingBlanks + daysInMonth,
            itemBuilder: (context, i) {
              if (i < leadingBlanks) return const SizedBox.shrink();
              final day = i - leadingBlanks + 1;
              final date = DateTime(visibleMonth.year, visibleMonth.month, day);
              final hijri = service.toHijri(date);
              final isToday = date.year == today.year && date.month == today.month && date.day == today.day;
              final isEventDay = islamicEvents.any((e) => e.hijriMonth == hijri.month && e.hijriDay == hijri.day);

              return Container(
                margin: const EdgeInsets.all(2),
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: isToday ? AppColors.navy : null,
                ),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      '$day',
                      style: theme.textTheme.bodyMedium?.copyWith(
                        color: isToday ? Colors.white : null,
                        fontWeight: isToday ? FontWeight.w700 : FontWeight.w400,
                      ),
                    ),
                    Text(
                      isArabic ? toArabicIndicDigits(hijri.day) : '${hijri.day}',
                      style: theme.textTheme.labelSmall?.copyWith(
                        color: isToday ? AppColors.gold : theme.colorScheme.onSurfaceVariant,
                      ),
                    ),
                    if (isEventDay)
                      Container(
                        width: 4,
                        height: 4,
                        margin: const EdgeInsets.only(top: 1),
                        decoration: BoxDecoration(shape: BoxShape.circle, color: isToday ? AppColors.gold : AppColors.primaryLight),
                      ),
                  ],
                ),
              );
            },
          ),
        ),
        Padding(
          padding: const EdgeInsets.all(12),
          child: Text(
            t('calendar_disclaimer'),
            style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
            textAlign: TextAlign.center,
          ),
        ),
      ],
    );
  }
}

class _AgendaView extends StatelessWidget {
  const _AgendaView({
    required this.service,
    required this.from,
    required this.isArabic,
    required this.theme,
    required this.t,
    required this.eventName,
  });

  final HijriCalendarService service;
  final DateTime from;
  final bool isArabic;
  final ThemeData theme;
  final String Function(String) t;
  final String Function(String Function(String), IslamicEvent) eventName;

  @override
  Widget build(BuildContext context) {
    final upcoming = service.upcomingEvents(from);
    final monthNames = isArabic ? hijriMonthNamesAr : hijriMonthNamesEn;

    return ListView.builder(
      padding: const EdgeInsets.all(16),
      itemCount: upcoming.length + 1,
      itemBuilder: (context, i) {
        if (i == upcoming.length) {
          return Padding(
            padding: const EdgeInsets.symmetric(vertical: 12),
            child: Text(
              t('calendar_disclaimer'),
              style: theme.textTheme.bodySmall?.copyWith(color: theme.colorScheme.onSurfaceVariant),
              textAlign: TextAlign.center,
            ),
          );
        }
        final item = upcoming[i];
        return Card(
          child: ListTile(
            leading: const Icon(Icons.event_outlined, color: AppColors.gold),
            title: Text(eventName(t, item.event)),
            subtitle: Text('${monthNames[item.event.hijriMonth - 1]} ${item.event.hijriDay}, ${item.hijriYear} AH'),
            trailing: Text(DateFormat.yMMMd().format(item.gregorianDate)),
          ),
        );
      },
    );
  }
}
