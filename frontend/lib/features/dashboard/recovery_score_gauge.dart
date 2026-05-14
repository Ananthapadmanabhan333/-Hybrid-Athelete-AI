import 'package:flutter/material.dart';

class RecoveryScoreGauge extends StatelessWidget {
  final double score; // 0 to 100

  const RecoveryScoreGauge({Key? key, required this.score}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    Color gaugeColor = score > 70 ? Colors.greenAccent : (score > 40 ? Colors.orangeAccent : Colors.redAccent);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.black.withOpacity(0.05),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: gaugeColor.withOpacity(0.3)),
      ),
      child: Column(
        children: [
          const Text(
            "RECOVERY",
            style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, letterSpacing: 1.2),
          ),
          const SizedBox(height: 12),
          Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                height: 80,
                width: 80,
                child: CircularProgressIndicator(
                  value: score / 100,
                  strokeWidth: 8,
                  backgroundColor: Colors.grey[200],
                  valueColor: AlwaysStoppedAnimation<Color>(gaugeColor),
                ),
              ),
              Text(
                "${score.toInt()}",
                style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
            ],
          ),
        ],
      ),
    );
  }
}
