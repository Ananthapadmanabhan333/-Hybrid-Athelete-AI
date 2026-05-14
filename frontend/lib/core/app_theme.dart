import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

class AppTheme {
  // Cyberpunk Zen Palette
  static const Color backgroundColor = Color(0xFF050505); // Deepest Black
  static const Color surfaceColor = Color(0xFF121212); // Soft Black
  static const Color primaryColor = Color(0xFF00F0FF); // Cyan Neon
  static const Color secondaryColor = Color(0xFF7000FF); // Electric Purple
  static const Color accentColor = Color(0xFFFF003C); // Runner Red
  static const Color successColor = Color(0xFF00FF94); // Matrix Green
  
  static const Color textPrimary = Color(0xFFFFFFFF);
  static const Color textSecondary = Color(0xFFB3B3B3);

  static ThemeData get darkTheme {
    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      scaffoldBackgroundColor: backgroundColor,
      primaryColor: primaryColor,
      colorScheme: const ColorScheme.dark(
        primary: primaryColor,
        secondary: secondaryColor,
        surface: surfaceColor,
        error: accentColor,
        surfaceContainerHighest: Color(0xFF1E1E1E),
      ),
      
      // Typography
      textTheme: TextTheme(
        displayLarge: GoogleFonts.outfit(
          fontSize: 32, 
          fontWeight: FontWeight.bold, 
          color: textPrimary,
          letterSpacing: -1.0,
        ),
        displayMedium: GoogleFonts.outfit(
          fontSize: 24, 
          fontWeight: FontWeight.w600, 
          color: textPrimary,
          letterSpacing: -0.5,
        ),
        titleLarge: GoogleFonts.outfit(
          fontSize: 20, 
          fontWeight: FontWeight.bold, 
          color: textPrimary,
        ),
        bodyLarge: GoogleFonts.inter(
          fontSize: 16, 
          color: textPrimary,
        ),
        bodyMedium: GoogleFonts.inter(
          fontSize: 14, 
          color: textSecondary,
          height: 1.5,
        ),
      ),
      
      // Component Themes
      // cardTheme: CardTheme(
      //   color: surfaceColor,
      //   elevation: 0,
      //   shape: RoundedRectangleBorder(
      //     borderRadius: BorderRadius.circular(24),
      //     side: BorderSide(color: Colors.white.withOpacity(0.05)),
      //   ),
      // ),
      
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          foregroundColor: Colors.black,
          elevation: 0,
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
          shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
          textStyle: GoogleFonts.outfit(fontWeight: FontWeight.bold, fontSize: 16),
        ),
      ),

      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: surfaceColor,
        contentPadding: const EdgeInsets.all(20),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide.none,
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: BorderSide(color: Colors.white.withOpacity(0.1)),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(16),
          borderSide: const BorderSide(color: primaryColor),
        ),
      ),
    );
  }
}
