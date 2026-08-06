/// Catalog of Android notification channels used by the worship reminder
/// system. Each reminder *kind* gets its own channel (rather than sharing a
/// handful of generic channels) so a user can mute, re-tone, or silence one
/// specific reminder type from Android's own per-channel notification
/// settings without affecting the others -- e.g. muting "Missed Prayer"
/// while keeping the Adhan itself on.
class NotificationChannel {
  const NotificationChannel({required this.id, required this.nameKey, required this.descriptionKey});
  final String id;

  /// Localisation keys, resolved at channel-creation time.
  final String nameKey;
  final String descriptionKey;
}

class NotificationChannels {
  NotificationChannels._();

  static const prayerAdhan = NotificationChannel(
    id: 'prayer_adhan',
    nameKey: 'notif_channel_prayer_adhan',
    descriptionKey: 'notif_channel_prayer_adhan_desc',
  );
  static const prayerEarly = NotificationChannel(
    id: 'prayer_early',
    nameKey: 'notif_channel_prayer_early',
    descriptionKey: 'notif_channel_prayer_early_desc',
  );
  static const prayerIqamah = NotificationChannel(
    id: 'prayer_iqamah',
    nameKey: 'notif_channel_prayer_iqamah',
    descriptionKey: 'notif_channel_prayer_iqamah_desc',
  );
  static const prayerMissed = NotificationChannel(
    id: 'prayer_missed',
    nameKey: 'notif_channel_prayer_missed',
    descriptionKey: 'notif_channel_prayer_missed_desc',
  );
  static const friday = NotificationChannel(
    id: 'friday_jumuah',
    nameKey: 'notif_channel_friday',
    descriptionKey: 'notif_channel_friday_desc',
  );
  static const tahajjudGentle = NotificationChannel(
    id: 'tahajjud_gentle',
    nameKey: 'notif_channel_tahajjud_gentle',
    descriptionKey: 'notif_channel_tahajjud_gentle_desc',
  );
  static const tahajjudStrong = NotificationChannel(
    id: 'tahajjud_strong',
    nameKey: 'notif_channel_tahajjud_strong',
    descriptionKey: 'notif_channel_tahajjud_strong_desc',
  );
  static const quranReading = NotificationChannel(
    id: 'quran_reading',
    nameKey: 'notif_channel_quran_reading',
    descriptionKey: 'notif_channel_quran_reading_desc',
  );
  static const quranKhatm = NotificationChannel(
    id: 'quran_khatm',
    nameKey: 'notif_channel_quran_khatm',
    descriptionKey: 'notif_channel_quran_khatm_desc',
  );
  static const quranMemorisation = NotificationChannel(
    id: 'quran_memorisation',
    nameKey: 'notif_channel_quran_memorisation',
    descriptionKey: 'notif_channel_quran_memorisation_desc',
  );
  static const adhkarMorning = NotificationChannel(
    id: 'adhkar_morning',
    nameKey: 'notif_channel_adhkar_morning',
    descriptionKey: 'notif_channel_adhkar_morning_desc',
  );
  static const adhkarEvening = NotificationChannel(
    id: 'adhkar_evening',
    nameKey: 'notif_channel_adhkar_evening',
    descriptionKey: 'notif_channel_adhkar_evening_desc',
  );
  static const adhkarSleep = NotificationChannel(
    id: 'adhkar_sleep',
    nameKey: 'notif_channel_adhkar_sleep',
    descriptionKey: 'notif_channel_adhkar_sleep_desc',
  );
  static const adhkarTravel = NotificationChannel(
    id: 'adhkar_travel',
    nameKey: 'notif_channel_adhkar_travel',
    descriptionKey: 'notif_channel_adhkar_travel_desc',
  );

  static const all = [
    prayerAdhan,
    prayerEarly,
    prayerIqamah,
    prayerMissed,
    friday,
    tahajjudGentle,
    tahajjudStrong,
    quranReading,
    quranKhatm,
    quranMemorisation,
    adhkarMorning,
    adhkarEvening,
    adhkarSleep,
    adhkarTravel,
  ];
}
