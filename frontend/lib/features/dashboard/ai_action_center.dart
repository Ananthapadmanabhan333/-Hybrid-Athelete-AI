import 'package:flutter/material.dart';

class AIActionCenter extends StatelessWidget {
  final List<String> insights;

  const AIActionCenter({Key? key, required this.insights}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Padding(
          padding: EdgeInsets.symmetric(horizontal: 4.0, vertical: 8.0),
          child: Text(
            "AI ACTION CENTER",
            style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.1, color: Colors.blueGrey),
          ),
        ),
        ...insights.map((insight) => Container(
          margin: const EdgeInsets.only(bottom: 8),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Colors.blue[50],
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: Colors.blue.withOpacity(0.1)),
          ),
          child: Row(
            children: [
              const Icon(Icons.bolt, color: Colors.blue, size: 20),
              const SizedBox(width: 12),
              Expanded(
                child: Text(
                  insight,
                  style: const TextStyle(fontSize: 13, color: Colors.black87),
                ),
              ),
            ],
          ),
        )).toList(),
      ],
    );
  }
}
