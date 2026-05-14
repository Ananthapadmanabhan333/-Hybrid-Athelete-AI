
import 'package:flutter/material.dart';

class MedicalDashboard extends StatelessWidget {
  const MedicalDashboard({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Medical AI')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.upload_file),
              label: const Text("Upload Lab Report"),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: () {},
              icon: const Icon(Icons.note_add),
              label: const Text("Log Symptoms"),
            ),
          ],
        ),
      ),
    );
  }
}
