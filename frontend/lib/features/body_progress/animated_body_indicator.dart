import 'package:flutter/material.dart';
import '../../core/app_theme.dart';
import 'package:flutter_animate/flutter_animate.dart';

class AnimatedBodyIndicator extends StatelessWidget {
  final double weightStart;
  final double weightEnd;
  final double muscleStart;
  final double muscleEnd;
  final double fatStart;
  final double fatEnd;

  const AnimatedBodyIndicator({
    super.key,
    required this.weightStart,
    required this.weightEnd,
    required this.muscleStart,
    required this.muscleEnd,
    required this.fatStart,
    required this.fatEnd,
  });

  @override
  Widget build(BuildContext context) {
    // Calculate deltas
    double muscleDelta = muscleEnd - muscleStart;
    double fatDelta = fatEnd - fatStart;

    // Normalizing deltas for animation scaling
    // Positive muscle expands shoulders, negative fat shrinks waist
    double shoulderScale = 1.0 + (muscleDelta > 0 ? (muscleDelta / muscleStart) * 2 : 0);
    double waistScale = 1.0 + (fatDelta < 0 ? (fatDelta / fatStart) * 2 : (fatDelta > 0 ? (fatDelta / fatStart) : 0));

    // Clamp scales to prevent extreme distortion
    shoulderScale = shoulderScale.clamp(0.9, 1.3);
    waistScale = waistScale.clamp(0.7, 1.3);

    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: AppTheme.surfaceColor,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.white.withOpacity(0.05)),
      ),
      child: Column(
        children: [
          const Text("BODY COMPOSITION SHIFT", style: TextStyle(color: Colors.grey, fontSize: 12, fontWeight: FontWeight.bold)),
          const SizedBox(height: 24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildMetricColumn("Muscle", muscleDelta >= 0 ? "+${muscleDelta.toStringAsFixed(1)}kg" : "${muscleDelta.toStringAsFixed(1)}kg", Colors.greenAccent),
              
              // The animated body figure
              TweenAnimationBuilder<double>(
                tween: Tween<double>(begin: 0.0, end: 1.0),
                duration: const Duration(milliseconds: 1500),
                curve: Curves.elasticOut,
                builder: (context, value, child) {
                  return CustomPaint(
                    size: const Size(100, 150),
                    painter: BodyPainter(
                      shoulderScale: 1.0 + ((shoulderScale - 1.0) * value),
                      waistScale: 1.0 + ((waistScale - 1.0) * value),
                    ),
                  );
                },
              ),
              
              _buildMetricColumn("Fat", fatDelta <= 0 ? "${fatDelta.toStringAsFixed(1)}kg" : "+${fatDelta.toStringAsFixed(1)}kg", fatDelta <= 0 ? Colors.greenAccent : Colors.redAccent),
            ],
          ),
        ],
      ),
    ).animate().fadeIn(delay: 500.ms).slideY(begin: 0.1);
  }

  Widget _buildMetricColumn(String label, String value, Color color) {
    return Column(
      children: [
        Text(value, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 18)),
        const SizedBox(height: 4),
        Text(label, style: const TextStyle(color: Colors.grey, fontSize: 12)),
      ],
    );
  }
}

class BodyPainter extends CustomPainter {
  final double shoulderScale;
  final double waistScale;

  BodyPainter({required this.shoulderScale, required this.waistScale});

  @override
  void paint(Canvas canvas, Size size) {
    final paint = Paint()
      ..color = AppTheme.primaryColor.withOpacity(0.8)
      ..style = PaintingStyle.fill;
    
    final wireframePaint = Paint()
      ..color = AppTheme.primaryColor
      ..style = PaintingStyle.stroke
      ..strokeWidth = 2.0;

    final double centerX = size.width / 2;
    final double headRadius = size.width * 0.15;
    
    // Head
    canvas.drawCircle(Offset(centerX, headRadius + 5), headRadius, paint);
    
    // Torso Shape
    final Path path = Path();
    
    final double shoulderWidth = (size.width * 0.4) * shoulderScale;
    final double shoulderY = size.height * 0.3;
    final double waistWidth = (size.width * 0.25) * waistScale;
    final double waistY = size.height * 0.8;
    
    path.moveTo(centerX - (headRadius * 0.5), headRadius * 2 + 5); // Neck L
    path.lineTo(centerX + (headRadius * 0.5), headRadius * 2 + 5); // Neck R
    
    path.lineTo(centerX + shoulderWidth, shoulderY); // Shoulder R
    path.lineTo(centerX + waistWidth, waistY); // Waist R
    path.lineTo(centerX - waistWidth, waistY); // Waist L
    path.lineTo(centerX - shoulderWidth, shoulderY); // Shoulder L
    path.close();

    canvas.drawPath(path, paint);
    canvas.drawPath(path, wireframePaint);
  }

  @override
  bool shouldRepaint(covariant BodyPainter oldDelegate) {
    return oldDelegate.shoulderScale != shoulderScale || oldDelegate.waistScale != waistScale;
  }
}
