import 'package:flutter/material.dart';

import '../models/dhikr.dart';

/// Shared "what is the Counter screen currently counting" state, so the Home and
/// Adhkar screens can hand off a specific dhikr to the Counter tab without a
/// full route push (matches the one-tap flows in the product's user journeys).
class ActiveDhikrController extends ChangeNotifier {
  Dhikr? _dhikr;
  int _customTarget = 33;

  /// null = freeform counting (no specific dhikr text shown).
  Dhikr? get dhikr => _dhikr;
  int get target => _dhikr?.defaultTarget ?? _customTarget;

  void select(Dhikr dhikr) {
    _dhikr = dhikr;
    notifyListeners();
  }

  void clearToFreeform() {
    _dhikr = null;
    notifyListeners();
  }

  void setCustomTarget(int value) {
    _customTarget = value;
    notifyListeners();
  }
}
