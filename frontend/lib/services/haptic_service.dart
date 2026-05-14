import 'package:flutter/services.dart';
import 'package:flutter_vibrate/flutter_vibrate.dart';

class HapticService {
  static final HapticService _instance = HapticService._internal();
  factory HapticService() => _instance;
  HapticService._internal();

  bool _canVibrate = false;

  Future<void> init() async {
    bool canVibrate = await Vibrate.canVibrate;
    _canVibrate = canVibrate;
  }

  void lightImpact() {
    if (_canVibrate) {
      HapticFeedback.lightImpact();
    }
  }

  void mediumImpact() {
    if (_canVibrate) {
      HapticFeedback.mediumImpact();
    }
  }

  void heavyImpact() {
    if (_canVibrate) {
      HapticFeedback.heavyImpact();
    }
  }

  void success() {
    if (_canVibrate) {
      Vibrate.feedback(FeedbackType.success);
    }
  }

  void error() {
    if (_canVibrate) {
      Vibrate.feedback(FeedbackType.error);
    }
  }
  
  void selection() {
    if (_canVibrate) {
      HapticFeedback.selectionClick();
    }
  }
}
