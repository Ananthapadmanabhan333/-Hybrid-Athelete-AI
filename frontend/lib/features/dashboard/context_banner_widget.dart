import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:flutter_animate/flutter_animate.dart';
import '../../core/app_theme.dart';

enum ContextBannerType { info, warning, success, alert }

class ContextBannerWidget extends StatelessWidget {
  final String message;
  final ContextBannerType type;
  final VoidCallback? onAction;
  final String? actionLabel;

  const ContextBannerWidget({
    super.key,
    required this.message,
    required this.type,
    this.onAction,
    this.actionLabel,
  });

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;
    IconData icon;

    switch (type) {
      case ContextBannerType.warning:
        bg = Colors.orange.withOpacity(0.15);
        fg = Colors.orangeAccent;
        icon = Icons.warning_amber_rounded;
        break;
      case ContextBannerType.alert:
        bg = AppTheme.accentColor.withOpacity(0.15);
        fg = AppTheme.accentColor;
        icon = Icons.error_outline;
        break;
      case ContextBannerType.success:
        bg = AppTheme.successColor.withOpacity(0.15);
        fg = AppTheme.successColor;
        icon = Icons.check_circle_outline;
        break;
      case ContextBannerType.info:
      default:
        bg = AppTheme.primaryColor.withOpacity(0.15);
        fg = AppTheme.primaryColor;
        icon = Icons.info_outline;
        break;
    }

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: fg.withOpacity(0.3)),
      ),
      child: Row(
        children: [
          Icon(icon, color: fg, size: 20),
          const SizedBox(width: 12),
          Expanded(
            child: Text(
              message,
              style: GoogleFonts.inter(
                color: AppTheme.textPrimary,
                fontSize: 13,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
          if (onAction != null && actionLabel != null)
            GestureDetector(
              onTap: onAction,
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                decoration: BoxDecoration(
                  color: fg.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Text(
                  actionLabel!.toUpperCase(),
                  style: GoogleFonts.outfit(
                    color: fg,
                    fontSize: 10,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ),
            ),
        ],
      ),
    ).animate().fadeIn().slideY(begin: -0.5);
  }
}
