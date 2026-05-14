import 'package:flutter/material.dart';

class AdaptiveStatsCard extends StatelessWidget {
  final double adherence;
  final String status;

  const AdaptiveStatsCard({
    Key? key, 
    required this.adherence, 
    required this.status
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 0,
      color: Colors.blueGrey[900],
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    "Adaptive Plan Status",
                    style: TextStyle(color: Colors.white, fontSize: 16, fontWeight: FontWeight.bold),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    status,
                    style: TextStyle(color: Colors.white.withOpacity(0.7), fontSize: 12),
                  ),
                ],
              ),
            ),
            Column(
              children: [
                Text(
                  "${adherence.toInt()}%",
                  style: const TextStyle(color: Colors.cyanAccent, fontSize: 22, fontWeight: FontWeight.bold),
                ),
                const Text(
                  "Adherence",
                  style: TextStyle(color: Colors.white54, fontSize: 10),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
