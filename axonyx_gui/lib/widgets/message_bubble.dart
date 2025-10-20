import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../models/message.dart';
import '../theme/app_theme.dart';

class MessageBubble extends StatelessWidget {
  final Message message;

  const MessageBubble({
    super.key,
    required this.message,
  });

  @override
  Widget build(BuildContext context) {
    if (message.isSystemMessage) {
      return _buildSystemMessage(context);
    }

    if (message.isError) {
      return _buildErrorMessage(context);
    }

    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        mainAxisAlignment:
            message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            _buildAvatar(false),
            const SizedBox(width: 12),
          ],
          Flexible(
            child: Column(
              crossAxisAlignment: message.isUser
                  ? CrossAxisAlignment.end
                  : CrossAxisAlignment.start,
              children: [
                Container(
                  constraints: const BoxConstraints(maxWidth: 600),
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: message.isUser
                        ? AppTheme.userMessageColor
                        : AppTheme.agentMessageColor,
                    borderRadius: BorderRadius.circular(16).copyWith(
                      topLeft: message.isUser
                          ? const Radius.circular(16)
                          : const Radius.circular(4),
                      topRight: message.isUser
                          ? const Radius.circular(4)
                          : const Radius.circular(16),
                    ),
                    border: Border.all(
                      color: Colors.white.withOpacity(0.1),
                    ),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // Message text
                      SelectableText(
                        message.text,
                        style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                              color: AppTheme.textPrimary,
                              height: 1.5,
                            ),
                      ),
                      
                      // Tool calls (if any)
                      if (message.toolCalls != null && message.toolCalls!.isNotEmpty)
                        ..._buildToolCalls(context),
                    ],
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  DateFormat('HH:mm').format(message.timestamp),
                  style: Theme.of(context).textTheme.bodySmall!.copyWith(
                        fontSize: 11,
                      ),
                ),
              ],
            ),
          ),
          if (message.isUser) ...[
            const SizedBox(width: 12),
            _buildAvatar(true),
          ],
        ],
      ),
    );
  }

  Widget _buildAvatar(bool isUser) {
    return Container(
      width: 36,
      height: 36,
      decoration: BoxDecoration(
        gradient: isUser
            ? const LinearGradient(
                colors: [Color(0xFFFF6B6B), Color(0xFFFF8E53)],
              )
            : const LinearGradient(
                colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
              ),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Icon(
        isUser ? Icons.person : Icons.auto_awesome,
        color: Colors.white,
        size: 20,
      ),
    );
  }

  Widget _buildSystemMessage(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Center(
        child: Container(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          decoration: BoxDecoration(
            color: AppTheme.surfaceColor,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: Colors.white.withOpacity(0.1)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                Icons.info_outline,
                size: 16,
                color: AppTheme.secondaryColor,
              ),
              const SizedBox(width: 8),
              Text(
                message.text,
                style: Theme.of(context).textTheme.bodySmall!.copyWith(
                      color: AppTheme.textSecondary,
                    ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildErrorMessage(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Container(
        padding: const EdgeInsets.all(12),
        decoration: BoxDecoration(
          color: AppTheme.errorColor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(12),
          border: Border.all(color: AppTheme.errorColor.withOpacity(0.3)),
        ),
        child: Row(
          children: [
            const Icon(
              Icons.error_outline,
              color: AppTheme.errorColor,
              size: 20,
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Text(
                message.text,
                style: Theme.of(context).textTheme.bodyMedium!.copyWith(
                      color: AppTheme.errorColor,
                    ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  List<Widget> _buildToolCalls(BuildContext context) {
    return [
      const SizedBox(height: 12),
      const Divider(height: 1),
      const SizedBox(height: 12),
      ...message.toolCalls!.map((toolCall) => Padding(
            padding: const EdgeInsets.only(bottom: 8),
            child: Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: Colors.white.withOpacity(0.05),
                borderRadius: BorderRadius.circular(8),
                border: Border.all(
                  color: toolCall.success
                      ? AppTheme.successColor.withOpacity(0.3)
                      : AppTheme.errorColor.withOpacity(0.3),
                ),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Icon(
                        toolCall.success ? Icons.check_circle : Icons.error,
                        size: 16,
                        color: toolCall.success
                            ? AppTheme.successColor
                            : AppTheme.errorColor,
                      ),
                      const SizedBox(width: 8),
                      Text(
                        toolCall.name,
                        style: Theme.of(context).textTheme.bodySmall!.copyWith(
                              fontWeight: FontWeight.w600,
                              color: AppTheme.textPrimary,
                            ),
                      ),
                    ],
                  ),
                  if (toolCall.input.isNotEmpty) ...[
                    const SizedBox(height: 4),
                    Text(
                      'Input: ${toolCall.input.toString()}',
                      style: Theme.of(context).textTheme.bodySmall!.copyWith(
                            fontSize: 11,
                            color: AppTheme.textTertiary,
                          ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ],
              ),
            ),
          )),
    ];
  }
}
