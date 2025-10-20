import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:window_manager/window_manager.dart';
import '../providers/agent_provider.dart';
import '../widgets/custom_title_bar.dart';
import '../widgets/message_bubble.dart';
import '../widgets/message_input.dart';
import '../widgets/model_selector.dart';
import '../theme/app_theme.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({super.key});

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> with WindowListener {
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    super.initState();
    windowManager.addListener(this);
    _checkConnection();
  }

  @override
  void dispose() {
    windowManager.removeListener(this);
    _scrollController.dispose();
    super.dispose();
  }

  void _checkConnection() {
    Future.delayed(Duration.zero, () {
      context.read<AgentProvider>().checkConnection();
    });
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      Future.delayed(const Duration(milliseconds: 100), () {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppTheme.backgroundColor,
      body: Column(
        children: [
          // Custom Title Bar (Frameless window controls)
          const CustomTitleBar(),
          
          // Chat Area
          Expanded(
            child: Row(
              children: [
                // Sidebar
                Container(
                  width: 280,
                  decoration: BoxDecoration(
                    color: AppTheme.surfaceColor,
                    border: Border(
                      right: BorderSide(
                        color: Colors.white.withOpacity(0.1),
                        width: 1,
                      ),
                    ),
                  ),
                  child: Column(
                    children: [
                      // Logo/Title
                      Container(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              children: [
                                Container(
                                  width: 40,
                                  height: 40,
                                  decoration: BoxDecoration(
                                    gradient: const LinearGradient(
                                      colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
                                    ),
                                    borderRadius: BorderRadius.circular(12),
                                  ),
                                  child: const Icon(Icons.auto_awesome, color: Colors.white),
                                ),
                                const SizedBox(width: 12),
                                Text(
                                  'Axonyx',
                                  style: Theme.of(context).textTheme.headlineMedium,
                                ),
                              ],
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Revolt Agent',
                              style: Theme.of(context).textTheme.bodySmall,
                            ),
                          ],
                        ),
                      ),
                      
                      const Divider(height: 1),
                      
                      // Model Selector
                      const ModelSelector(),
                      
                      const Divider(height: 1),
                      
                      // Connection Status
                      Consumer<AgentProvider>(
                        builder: (context, provider, child) {
                          return Container(
                            margin: const EdgeInsets.all(16),
                            padding: const EdgeInsets.all(12),
                            decoration: BoxDecoration(
                              color: provider.isConnected
                                  ? AppTheme.successColor.withOpacity(0.1)
                                  : AppTheme.errorColor.withOpacity(0.1),
                              borderRadius: BorderRadius.circular(8),
                              border: Border.all(
                                color: provider.isConnected
                                    ? AppTheme.successColor.withOpacity(0.3)
                                    : AppTheme.errorColor.withOpacity(0.3),
                              ),
                            ),
                            child: Row(
                              children: [
                                Icon(
                                  provider.isConnected ? Icons.check_circle : Icons.error,
                                  color: provider.isConnected
                                      ? AppTheme.successColor
                                      : AppTheme.errorColor,
                                  size: 20,
                                ),
                                const SizedBox(width: 8),
                                Expanded(
                                  child: Text(
                                    provider.isConnected ? 'Connected' : 'Disconnected',
                                    style: TextStyle(
                                      color: provider.isConnected
                                          ? AppTheme.successColor
                                          : AppTheme.errorColor,
                                      fontSize: 12,
                                      fontWeight: FontWeight.w600,
                                    ),
                                  ),
                                ),
                                IconButton(
                                  icon: const Icon(Icons.refresh, size: 16),
                                  onPressed: _checkConnection,
                                  tooltip: 'Refresh connection',
                                ),
                              ],
                            ),
                          );
                        },
                      ),
                      
                      const Spacer(),
                      
                      // Clear Chat Button
                      Padding(
                        padding: const EdgeInsets.all(16),
                        child: SizedBox(
                          width: double.infinity,
                          child: OutlinedButton.icon(
                            icon: const Icon(Icons.delete_outline),
                            label: const Text('Clear Chat'),
                            onPressed: () {
                              context.read<AgentProvider>().clearMessages();
                            },
                            style: OutlinedButton.styleFrom(
                              foregroundColor: AppTheme.textSecondary,
                              side: BorderSide(color: Colors.white.withOpacity(0.1)),
                              padding: const EdgeInsets.symmetric(vertical: 12),
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
                
                // Messages Area
                Expanded(
                  child: Column(
                    children: [
                      // Messages List
                      Expanded(
                        child: Consumer<AgentProvider>(
                          builder: (context, provider, child) {
                            if (provider.messages.isEmpty) {
                              return _buildEmptyState();
                            }
                            
                            WidgetsBinding.instance.addPostFrameCallback((_) {
                              _scrollToBottom();
                            });
                            
                            return ListView.builder(
                              controller: _scrollController,
                              padding: const EdgeInsets.all(24),
                              itemCount: provider.messages.length,
                              itemBuilder: (context, index) {
                                return MessageBubble(
                                  message: provider.messages[index],
                                );
                              },
                            );
                          },
                        ),
                      ),
                      
                      // Loading Indicator
                      Consumer<AgentProvider>(
                        builder: (context, provider, child) {
                          if (!provider.isLoading) return const SizedBox.shrink();
                          
                          return Container(
                            padding: const EdgeInsets.all(16),
                            child: Row(
                              children: [
                                const SizedBox(
                                  width: 20,
                                  height: 20,
                                  child: CircularProgressIndicator(strokeWidth: 2),
                                ),
                                const SizedBox(width: 12),
                                Text(
                                  'Agent is thinking...',
                                  style: Theme.of(context).textTheme.bodySmall,
                                ),
                              ],
                            ),
                          );
                        },
                      ),
                      
                      // Message Input
                      const MessageInput(),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Container(
            width: 100,
            height: 100,
            decoration: BoxDecoration(
              gradient: const LinearGradient(
                colors: [AppTheme.primaryColor, AppTheme.secondaryColor],
              ),
              borderRadius: BorderRadius.circular(24),
            ),
            child: const Icon(Icons.chat_bubble_outline, size: 48, color: Colors.white),
          ),
          const SizedBox(height: 24),
          Text(
            'Welcome to Axonyx Revolt',
            style: Theme.of(context).textTheme.headlineMedium,
          ),
          const SizedBox(height: 8),
          Text(
            'Ask me to automate Windows tasks',
            style: Theme.of(context).textTheme.bodyMedium,
          ),
          const SizedBox(height: 32),
          Wrap(
            spacing: 8,
            runSpacing: 8,
            alignment: WrapAlignment.center,
            children: [
              _suggestionChip('Open Chrome and go to Python.org'),
              _suggestionChip('Take a screenshot of my desktop'),
              _suggestionChip('List all running processes'),
              _suggestionChip('Install an application'),
            ],
          ),
        ],
      ),
    );
  }

  Widget _suggestionChip(String text) {
    return ActionChip(
      label: Text(text),
      onPressed: () {
        // Auto-fill the input (you'll need to implement this)
      },
      backgroundColor: AppTheme.surfaceColor,
      side: BorderSide(color: Colors.white.withOpacity(0.1)),
    );
  }
}
