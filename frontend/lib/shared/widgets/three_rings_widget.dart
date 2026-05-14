import 'dart:math';
import 'package:flutter/material.dart';
import '../../core/app_theme.dart';

class ThreeRingsWidget extends StatelessWidget {
  final double workProgress; // 0.0 to 1.0 (Outer - Red)
  final double trainProgress; // 0.0 to 1.0 (Middle - Green)
  final double recoverProgress; // 0.0 to 1.0 (Inner - Blue/Teal)

  const ThreeRingsWidget({
    super.key,
    required this.workProgress,
    required this.trainProgress,
    required this.recoverProgress,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: 250,
      height: 250,
      child: CustomPaint(
        painter: RingsPainter(
          work: workProgress,
          train: trainProgress,
          recover: recoverProgress,
        ),
        child: const Center(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(Icons.bolt, color: AppTheme.secondaryColor, size: 32),
              Text(
                "READY",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 24,
                  letterSpacing: 1.5,
                  color: Colors.white,
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class RingsPainter extends CustomPainter {
  final double work;
  final double train;
  final double recover;

  RingsPainter({required this.work, required this.train, required this.recover});

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final strokeWidth = 22.0;
    final spacing = 4.0;

    // Radius
    final r1 = (size.width / 2) - (strokeWidth / 2); // Outer
    final r2 = r1 - strokeWidth - spacing; // Middle
    final r3 = r2 - strokeWidth - spacing; // Inner

    // Paint Setup
    final bgPaint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = strokeWidth
      ..strokeCap = StrokeCap.round
      ..color = Colors.grey.withOpacity(0.15);

    // Draw Background Rings
    canvas.drawCircle(center, r1, bgPaint);
    canvas.drawCircle(center, r2, bgPaint);
    canvas.drawCircle(center, r3, bgPaint);

    // Draw Progress Rings
    _drawArc(canvas, center, r1, work, AppTheme.secondaryColor, strokeWidth);
    _drawArc(canvas, center, r2, train, AppTheme.primaryColor, strokeWidth);
    _drawArc(canvas, center, r3, recover, Colors.tealAccent, strokeWidth);
  }

  void _drawArc(Canvas canvas, Offset center, double radius, double progress, Color color, double width) {
    final paint = Paint()
      ..style = PaintingStyle.stroke
      ..strokeWidth = width
      ..strokeCap = StrokeCap.round
      ..color = color;
      
    // Start from top (-pi/2)
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -pi / 2,
      2 * pi * progress,
      false,
      paint,
    );
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
