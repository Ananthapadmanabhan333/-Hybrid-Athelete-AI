import 'package:flutter/material.dart';

class HealthStatusSection extends StatelessWidget {
  final List<String> alerts;

  const HealthStatusSection({Key? key, required this.alerts}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          "HEALTH & BIO-STATUS",
          style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.grey, letterSpacing: 1.1),
        ),
        const SizedBox(height: 16),
        if (alerts.isEmpty)
          const Text("Systems optimal. No bio-alerts detected.", style: TextStyle(color: Colors.greenAccent, fontSize: 13))
        else
          ...alerts.map((alert) => Container(
            margin: const EdgeInsets.only(bottom: 8),
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: Colors.redAccent.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(color: Colors.redAccent.withOpacity(0.2)),
            ),
            child: Row(
              children: [
                const Icon(Icons.warning_amber_rounded, color: Colors.redAccent, size: 20),
                const SizedBox(width: 12),
                Expanded(child: Text(alert, style: const TextStyle(color: Colors.white, fontSize: 13))),
              ],
            ),
          )).toList(),
      ],
    );
  }
}
