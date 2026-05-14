import 'dart:math' as math;
import 'package:flutter/material.dart';
import '../../../core/app_theme.dart';
import 'package:flutter_animate/flutter_animate.dart';

/// Animated strength progress bar that fills based on volume lifted vs target.
class StrengthProgressBar extends StatelessWidget {
  final String label;
  final double value;  // current volume (kg)
  final double max;    // target volume (kg)
  final Color color;

  const StrengthProgressBar({
    super.key,
    required this.label,
    required this.value,
    required this.max,
    this.color = Colors.orangeAccent,
  });

  @override
  Widget build(BuildContext context) {
    final progress = (value / max).clamp(0.0, 1.0);
    final pct = (progress * 100).toInt();

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 13)),
              Text("$pct%", style: TextStyle(color: color, fontWeight: FontWeight.bold)),
            ],
          ),
          const SizedBox(height: 6),
          Stack(
            children: [
              Container(
                height: 10,
                decoration: BoxDecoration(
                  color: Colors.white10,
                  borderRadius: BorderRadius.circular(5),
                ),
              ),
              TweenAnimationBuilder<double>(
                tween: Tween(begin: 0, end: progress),
                duration: const Duration(milliseconds: 1200),
                curve: Curves.easeOutCubic,
                builder: (context, val, _) => FractionallySizedBox(
                  widthFactor: val,
                  child: Container(
                    height: 10,
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [color.withOpacity(0.6), color],
                      ),
                      borderRadius: BorderRadius.circular(5),
                      boxShadow: [BoxShadow(color: color.withOpacity(0.4), blurRadius: 6, spreadRadius: 1)],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }
}

/// Pulsating cardio heartbeat visual showing zone intensity.
class CardioHeartbeatVisual extends StatefulWidget {
  final double load;    // 0.0 to 1.0 (e.g. avg_hr / max_hr)
  final String zone;   // "Zone 1" .. "Zone 5"

  const CardioHeartbeatVisual({super.key, required this.load, required this.zone});

  @override
  State<CardioHeartbeatVisual> createState() => _CardioHeartbeatVisualState();
}

class _CardioHeartbeatVisualState extends State<CardioHeartbeatVisual> with SingleTickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    // Pulse speed reflects cardio intensity
    final durationMs = (1500 - (widget.load * 700)).clamp(400.0, 1500.0).toInt();
    _pulseController = AnimationController(vsync: this, duration: Duration(milliseconds: durationMs))
      ..repeat(reverse: true);
    _pulseAnimation = Tween<double>(begin: 0.9, end: 1.15).animate(
      CurvedAnimation(parent: _pulseController, curve: Curves.easeInOut),
    );
  }

  Color _zoneColor() {
    switch (widget.zone) {
      case 'Zone 1': return Colors.blue;
      case 'Zone 2': return Colors.green;
      case 'Zone 3': return Colors.yellow;
      case 'Zone 4': return Colors.orange;
      case 'Zone 5': return Colors.red;
      default: return AppTheme.primaryColor;
    }
  }

  @override
  Widget build(BuildContext context) {
    final c = _zoneColor();
    return Row(
      children: [
        AnimatedBuilder(
          animation: _pulseAnimation,
          builder: (_, __) => Transform.scale(
            scale: _pulseAnimation.value,
            child: Icon(Icons.favorite, color: c, size: 36),
          ),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(widget.zone, style: TextStyle(color: c, fontWeight: FontWeight.bold, fontSize: 16)),
              const SizedBox(height: 4),
              LinearProgressIndicator(
                value: widget.load,
                backgroundColor: Colors.white10,
                valueColor: AlwaysStoppedAnimation(c),
                minHeight: 6,
                borderRadius: BorderRadius.circular(3),
              ),
              const SizedBox(height: 4),
              Text("Cardiovascular Load: ${(widget.load * 100).toInt()}%", style: const TextStyle(color: Colors.grey, fontSize: 11)),
            ],
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }
}

/// Boxing power velocity gauge using a radial custom painter.
class BoxingVelocityGauge extends StatelessWidget {
  final double power; // 0.0 to 1.0

  const BoxingVelocityGauge({super.key, required this.power});

  @override
  Widget build(BuildContext context) {
    final Color gaugeColor = power > 0.7 ? Colors.redAccent : power > 0.4 ? Colors.orangeAccent : Colors.greenAccent;
    return Column(
      children: [
        TweenAnimationBuilder<double>(
          tween: Tween(begin: 0, end: power),
          duration: const Duration(milliseconds: 1400),
          curve: Curves.elasticOut,
          builder: (context, val, _) => CustomPaint(
            size: const Size(140, 80),
            painter: _GaugePainter(val, gaugeColor),
          ),
        ),
        const SizedBox(height: 8),
        Text(
          "PUNCH POWER: ${(power * 100).toInt()}%",
          style: TextStyle(color: gaugeColor, fontWeight: FontWeight.bold, letterSpacing: 1.5, fontSize: 13),
        ),
      ],
    );
  }
}

class _GaugePainter extends CustomPainter {
  final double value; // 0.0 to 1.0
  final Color color;

  _GaugePainter(this.value, this.color);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height);
    final radius = size.width / 2;
    const startAngle = 3.14159; // pi (left)
    const sweepAngle = 3.14159; // half circle

    // Track
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      startAngle, sweepAngle, false,
      Paint()..color = Colors.white12..style = PaintingStyle.stroke..strokeWidth = 12..strokeCap = StrokeCap.round,
    );

    // Filled arc
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      startAngle, sweepAngle * value, false,
      Paint()..color = color..style = PaintingStyle.stroke..strokeWidth = 12..strokeCap = StrokeCap.round
        ..maskFilter = MaskFilter.blur(BlurStyle.normal, 4),
    );

    // Needle dot
    final angle = startAngle + sweepAngle * value;
    final needleX = center.dx + radius * math.cos(angle);
    final needleY = center.dy + radius * math.sin(angle);
    canvas.drawCircle(Offset(needleX, needleY), 7, Paint()..color = color);
  }

  @override
  bool shouldRepaint(covariant _GaugePainter old) => old.value != value;
}
