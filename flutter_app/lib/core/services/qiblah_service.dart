import 'dart:math' as math;

/// Great-circle initial bearing (in degrees, 0-360, 0 = true north) from a
/// device's position to the Kaaba, using the standard spherical bearing
/// formula. Coordinates for the Kaaba (21.4225 N, 39.8262 E) are the
/// commonly-cited reference figure used across independent Qiblah-finder
/// tools and mapping services -- cross-checked against multiple sources
/// (variance between sources is a few thousandths of a degree, i.e. a few
/// tens of metres, which does not meaningfully change the bearing at
/// intercontinental distances).
class QiblahService {
  static const double kaabaLatitude = 21.4225;
  static const double kaabaLongitude = 39.8262;

  static double _toRadians(double degrees) => degrees * math.pi / 180.0;
  static double _toDegrees(double radians) => radians * 180.0 / math.pi;

  /// Bearing (degrees from true north, clockwise, 0-360) pointing from
  /// [latitude]/[longitude] toward the Kaaba.
  static double bearingTo(double latitude, double longitude) {
    final phi1 = _toRadians(latitude);
    final phi2 = _toRadians(kaabaLatitude);
    final deltaLambda = _toRadians(kaabaLongitude - longitude);

    final y = math.sin(deltaLambda) * math.cos(phi2);
    final x = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(deltaLambda);
    final theta = math.atan2(y, x);
    return (_toDegrees(theta) + 360) % 360;
  }

  /// Great-circle distance in kilometres, for display context (e.g. "4,800
  /// km to Makkah") -- uses the same spherical model as [bearingTo].
  static double distanceKm(double latitude, double longitude) {
    const earthRadiusKm = 6371.0;
    final phi1 = _toRadians(latitude);
    final phi2 = _toRadians(kaabaLatitude);
    final deltaPhi = _toRadians(kaabaLatitude - latitude);
    final deltaLambda = _toRadians(kaabaLongitude - longitude);

    final a = math.sin(deltaPhi / 2) * math.sin(deltaPhi / 2) +
        math.cos(phi1) * math.cos(phi2) * math.sin(deltaLambda / 2) * math.sin(deltaLambda / 2);
    final c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a));
    return earthRadiusKm * c;
  }
}
