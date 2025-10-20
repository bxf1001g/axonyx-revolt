import 'message.dart';

class AgentResponse {
  final String finalResponse;
  final bool success;
  final List<ToolCall> toolCalls;
  final int iterations;

  AgentResponse({
    required this.finalResponse,
    required this.success,
    required this.toolCalls,
    required this.iterations,
  });

  factory AgentResponse.fromJson(Map<String, dynamic> json) {
    return AgentResponse(
      finalResponse: json['final_response'] ?? '',
      success: json['success'] ?? false,
      toolCalls: (json['tool_calls'] as List?)
              ?.map((tc) => ToolCall.fromJson(tc))
              .toList() ??
          [],
      iterations: json['iterations'] ?? 0,
    );
  }
}
