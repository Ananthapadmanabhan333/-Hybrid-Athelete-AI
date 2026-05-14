import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../../../core/constants.dart';
import '../../../core/app_theme.dart';
import '../../../services/auth_service.dart';

class NutritionChatWindow extends StatefulWidget {
  const NutritionChatWindow({super.key});

  @override
  State<NutritionChatWindow> createState() => _NutritionChatWindowState();
}

class _NutritionChatWindowState extends State<NutritionChatWindow> {
  final TextEditingController _controller = TextEditingController();
  final List<Map<String, dynamic>> _messages = [];
  bool _isLoading = false;
  final ScrollController _scrollController = ScrollController();
  final AuthService _authService = AuthService();

  @override
  void initState() {
    super.initState();
    _messages.add({"text": "Hello! I am your AI Nutrition Coach. Based on your active log trends, how can I help you optimize your diet today?", "isMe": false});
  }

  Future<void> _sendMessage() async {
    if (_controller.text.isEmpty) return;

    final userText = _controller.text;
    setState(() {
      _messages.add({"text": userText, "isMe": true});
      _isLoading = true;
    });
    _controller.clear();
    _scrollToBottom();

    try {
      final token = await _authService.getToken();
      
      // format history mapping isMe to is_user boolean for backend
      List<Map<String, dynamic>> history = _messages.sublist(1).map((m) => {
        "text": m["text"],
        "is_user": m["isMe"]
      }).toList();

      final response = await http.post(
        Uri.parse('${AppConstants.apiBaseUrl}/agents/nutrition/chat'),
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer $token"
        },
        body: jsonEncode({
          "query": userText,
          "history": history
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _messages.add({"text": data['response']['message'], "isMe": false});
        });
      } else {
        setState(() {
          _messages.add({"text": "I'm having trouble analyzing your request. Check your connection or try logging a meal first.", "isMe": false});
        });
      }
    } catch (e) {
      setState(() {
        _messages.add({"text": "Connection issue. Please try again.", "isMe": false});
      });
    }

    setState(() {
      _isLoading = false;
    });
    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("AI Nutritionist")),
      body: Column(
        children: [
          Expanded(
             child: ListView.builder(
              controller: _scrollController,
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length + (_isLoading ? 1 : 0),
              itemBuilder: (context, index) {
                if (index == _messages.length) {
                  return const Align(
                    alignment: Alignment.centerLeft,
                    child: Padding(
                      padding: EdgeInsets.all(8.0),
                      child: Text("Nutritionist is typing...", style: TextStyle(color: Colors.grey, fontStyle: FontStyle.italic)),
                    ),
                  );
                }
                return _buildMessageBubble(_messages[index]["text"], _messages[index]["isMe"]);
              },
            ),
          ),
          Container(
            padding: const EdgeInsets.all(16),
            color: AppTheme.surfaceColor,
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    style: const TextStyle(color: Colors.white),
                    decoration: InputDecoration(
                      hintText: "Ask about macros, meals, timing...",
                      filled: true,
                      fillColor: Colors.black12,
                      border: OutlineInputBorder(borderRadius: BorderRadius.circular(24), borderSide: BorderSide.none),
                      contentPadding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                CircleAvatar(
                  backgroundColor: AppTheme.primaryColor,
                  child: IconButton(
                    icon: const Icon(Icons.send, color: Colors.black),
                    onPressed: _sendMessage,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildMessageBubble(String text, bool isMe) {
    return Align(
      alignment: isMe ? Alignment.centerRight : Alignment.centerLeft,
      child: Container(
        margin: const EdgeInsets.symmetric(vertical: 4),
        padding: const EdgeInsets.all(16),
        constraints: BoxConstraints(maxWidth: MediaQuery.of(context).size.width * 0.75),
        decoration: BoxDecoration(
          color: isMe ? AppTheme.primaryColor : AppTheme.surfaceColor,
          borderRadius: BorderRadius.only(
            topLeft: const Radius.circular(16),
            topRight: const Radius.circular(16),
            bottomLeft: isMe ? const Radius.circular(16) : const Radius.circular(0),
            bottomRight: isMe ? const Radius.circular(0) : const Radius.circular(16),
          ),
        ),
        child: Text(text, style: TextStyle(fontSize: 16, color: isMe ? Colors.black : Colors.white, height: 1.4)),
      ),
    );
  }
}
