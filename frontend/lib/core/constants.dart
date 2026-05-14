import 'package:flutter/foundation.dart';

class AppConstants {
  static const String appName = 'Hybrid Athlete AI';
  static const String _envApiUrl = String.fromEnvironment('API_URL', defaultValue: '');
  
  static String get apiBaseUrl {
    if (_envApiUrl.isNotEmpty) {
      return _envApiUrl;
    }

    if (kIsWeb) {
      return 'http://localhost:8000/api/v1';
    } else if (defaultTargetPlatform == TargetPlatform.android) {
      return 'http://10.0.2.2:8000/api/v1'; // Android Emulator
    } else {
      return 'http://localhost:8000/api/v1'; // iOS, Windows, macOS, Linux
    }
  }
}
