class Message {
  final String id;
  final String text;
  final bool isUser;
  final DateTime timestamp;
  final List<ToolCall>? toolCalls;
  final bool success;
  final bool isSystemMessage;
  final bool isError;

  Message({
    required this.id,
    required this.text,
    required this.isUser,
    required this.timestamp,
    this.toolCalls,
    this.success = true,
    this.isSystemMessage = false,
    this.isError = false,
  });
}

class ToolCall {
  final String name;
  final Map<String, dynamic> input;
  final Map<String, dynamic> result;
  final bool success;

  ToolCall({
    required this.name,
    required this.input,
    required this.result,
    required this.success,
  });

  factory ToolCall.fromJson(Map<String, dynamic> json) {
    return ToolCall(
      name: json['name'] ?? '',
      input: json['input'] ?? {},
      result: json['result'] ?? {},
      success: json['success'] ?? false,
    );
  }
}
