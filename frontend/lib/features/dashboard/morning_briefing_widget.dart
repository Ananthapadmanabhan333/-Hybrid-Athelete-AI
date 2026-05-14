import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../core/app_theme.dart';

class MorningBriefingWidget extends StatelessWidget {
  final String userName;
  final int sleepHours;
  final int recoveryScore;
  final String primaryGoal;

  const MorningBriefingWidget({
    super.key,
    required this.userName,
    required this.sleepHours,
    required this.recoveryScore,
    required this.primaryGoal,
  });

  @override
  Widget build(BuildContext context) {
    // Logic to determine daily tone
    String greeting = "Rise & Grind";
    String insight = "You're fully recovered. Push hard today.";
    Color statusColor = AppTheme.successColor;
    IconData statusIcon = Icons.bolt;

    if (recoveryScore < 50) {
      greeting = "Take it Slow";
      insight = "Recovery is low ($recoveryScore%). Focus on mobility.";
      statusColor = AppTheme.accentColor;
      statusIcon = Icons.battery_alert;
    } else if (recoveryScore < 80) {
      greeting = "Steady Pace";
      insight = "Good baseline. maintain consistency.";
      statusColor = AppTheme.primaryColor;
      statusIcon = Icons.battery_charging_full;
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(30),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.5),
            blurRadius: 30,
            offset: const Offset(0, 10),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    DateTime.now().toString().substring(0, 10), // Simple date for MVP
                    style: GoogleFonts.inter(
                      fontSize: 12,
                      fontWeight: FontWeight.w600,
                      letterSpacing: 1.5,
                      color: AppTheme.textSecondary,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    "Good Morning, $userName",
                    style: GoogleFonts.outfit(
                      fontSize: 20, // Slightly smaller than displayMedium for balance
                      fontWeight: FontWeight.w500,
                      color: AppTheme.textPrimary,
                    ),
                  ),
                ],
              ),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: statusColor.withOpacity(0.1),
                  shape: BoxShape.circle,
                  border: Border.all(color: statusColor.withOpacity(0.3)),
                ),
                child: Icon(statusIcon, color: statusColor, size: 24),
              ),
            ],
          ),
          const SizedBox(height: 24),
          const Divider(height: 1, color: Colors.white10),
          const SizedBox(height: 24),
          
          // The "Insight" Section
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.auto_awesome, color: AppTheme.secondaryColor, size: 20),
              const SizedBox(width: 12),
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      greeting,
                      style: GoogleFonts.outfit(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.textPrimary,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      insight,
                      style: GoogleFonts.inter(
                        fontSize: 15,
                        height: 1.5,
                        color: AppTheme.textSecondary,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
    ).animate().fadeIn(duration: 800.ms).slideY(begin: 0.2);
  }
}
