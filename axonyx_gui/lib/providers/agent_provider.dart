import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import '../models/message.dart';
import '../models/agent_response.dart';

class AgentProvider with ChangeNotifier {
  final List<Message> _messages = [];
  bool _isLoading = false;
  String _selectedModel = 'claude-3-5-haiku-20241022';
  String _backendUrl = 'http://localhost:8000';
  bool _isConnected = false;

  List<Message> get messages => _messages;
  bool get isLoading => _isLoading;
  String get selectedModel => _selectedModel;
  bool get isConnected => _isConnected;

  // Available models
  final List<Map<String, String>> availableModels = [
    {
      'id': 'claude-3-5-haiku-20241022',
      'name': 'Haiku 3.5',
      'description': 'Fast & Cheap ⚡',
    },
    {
      'id': 'claude-3-7-sonnet-20250219',
      'name': 'Sonnet 3.7',
      'description': 'Balanced 🎯',
    },
    {
      'id': 'claude-opus-4-20250514',
      'name': 'Opus 4',
      'description': 'Most Powerful 🚀',
    },
  ];

  // Set backend URL
  void setBackendUrl(String url) {
    _backendUrl = url;
    notifyListeners();
  }

  // Change model
  Future<void> changeModel(String modelId) async {
    _selectedModel = modelId;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('$_backendUrl/set-model'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({'model': modelId}),
      );

      if (response.statusCode == 200) {
        _addSystemMessage('Model changed to ${_getModelName(modelId)}');
      }
    } catch (e) {
      debugPrint('Error changing model: $e');
    }
  }

  String _getModelName(String modelId) {
    return availableModels.firstWhere(
      (m) => m['id'] == modelId,
      orElse: () => {'name': 'Unknown'},
    )['name']!;
  }

  // Check backend connection
  Future<void> checkConnection() async {
    try {
      final response = await http.get(Uri.parse('$_backendUrl/health'));
      _isConnected = response.statusCode == 200;
    } catch (e) {
      _isConnected = false;
      debugPrint('Backend connection error: $e');
    }
    notifyListeners();
  }

  // Send message to agent
  Future<void> sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    // Add user message
    final userMessage = Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: text,
      isUser: true,
      timestamp: DateTime.now(),
    );
    _messages.add(userMessage);
    notifyListeners();

    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.post(
        Uri.parse('$_backendUrl/execute'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'task': text,
          'model': _selectedModel,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final agentResponse = AgentResponse.fromJson(data);

        // Add agent response
        final agentMessage = Message(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          text: agentResponse.finalResponse,
          isUser: false,
          timestamp: DateTime.now(),
          toolCalls: agentResponse.toolCalls,
          success: agentResponse.success,
        );
        _messages.add(agentMessage);
      } else {
        _addErrorMessage('Error: ${response.statusCode}');
      }
    } catch (e) {
      _addErrorMessage('Connection error: ${e.toString()}');
    }

    _isLoading = false;
    notifyListeners();
  }

  void _addSystemMessage(String text) {
    _messages.add(Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: text,
      isUser: false,
      timestamp: DateTime.now(),
      isSystemMessage: true,
    ));
    notifyListeners();
  }

  void _addErrorMessage(String text) {
    _messages.add(Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      text: text,
      isUser: false,
      timestamp: DateTime.now(),
      isError: true,
    ));
    notifyListeners();
  }

  void clearMessages() {
    _messages.clear();
    notifyListeners();
  }
}
