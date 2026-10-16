import 'dart:typed_data';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:image_picker/image_picker.dart';
import '../services/rbai_service.dart';
import '../widgets/voice_visualizer.dart';
import '../widgets/chat_view.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _textController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final ImagePicker _picker = ImagePicker();
  Uint8List? _selectedImageBytes;
  bool _isTorchOn = false;

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

  void _handleSend(RBAIService service) {
    final text = _textController.text.trim();
    if (text.isEmpty && _selectedImageBytes == null) return;

    service.sendPrompt(
      text,
      imageBytes: _selectedImageBytes,
      isVoice: false,
    );

    _textController.clear();
    setState(() {
      _selectedImageBytes = null;
    });
    _scrollToBottom();
  }

  Future<void> _pickImage() async {
    final XFile? photo = await _picker.pickImage(
      source: ImageSource.camera,
      maxWidth: 1024,
      imageQuality: 80,
    );
    if (photo != null) {
      final bytes = await photo.readAsBytes();
      setState(() {
        _selectedImageBytes = bytes;
      });
    }
  }

  void _showSettingsDialog(RBAIService service) {
    final urlController = TextEditingController(text: service.baseUrl);
    showDialog(
      context: context,
      builder: (ctx) => AlertDialog(
        backgroundColor: const Color(0xFF131D2E),
        title: const Text("RB.AI Backend Settings", style: TextStyle(color: Colors.white)),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              "Configure connection to RB.AI Python core running in Termux:",
              style: TextStyle(color: Colors.white70, fontSize: 13),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: urlController,
              style: const TextStyle(color: Colors.white),
              decoration: const InputDecoration(
                labelText: "Server URL",
                labelStyle: TextStyle(color: Colors.cyanAccent),
                hintText: "http://127.0.0.1:8765",
                enabledBorder: UnderlineInputBorder(borderSide: BorderSide(color: Colors.white30)),
              ),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(ctx),
            child: const Text("Cancel"),
          ),
          ElevatedButton(
            onPressed: () {
              service.setBaseUrl(urlController.text.trim());
              Navigator.pop(ctx);
            },
            child: const Text("Connect"),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final service = Provider.of<RBAIService>(context);

    return Scaffold(
      backgroundColor: const Color(0xFF090E17),
      appBar: AppBar(
        backgroundColor: const Color(0xFF0E1726),
        elevation: 0,
        title: Row(
          children: [
            const Icon(Icons.auto_awesome, color: Color(0xFF00E5FF), size: 22),
            const SizedBox(width: 8),
            const Text(
              "RB.AI",
              style: TextStyle(
                fontWeight: FontWeight.bold,
                letterSpacing: 1.2,
                color: Colors.white,
              ),
            ),
            const SizedBox(width: 8),
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
              decoration: BoxDecoration(
                color: (service.isConnected ? Colors.green : Colors.orange).withOpacity(0.2),
                borderRadius: BorderRadius.circular(10),
                border: Border.all(
                  color: service.isConnected ? Colors.green : Colors.orange,
                  width: 1,
                ),
              ),
              child: Text(
                service.isConnected ? "TERMUX READY" : "OFFLINE",
                style: TextStyle(
                  color: service.isConnected ? Colors.greenAccent : Colors.orangeAccent,
                  fontSize: 10,
                  fontWeight: FontWeight.bold,
                ),
              ),
            ),
          ],
        ),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings, color: Colors.white70),
            onPressed: () => _showSettingsDialog(service),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Top Section: Voice Visualizer Orb
            Container(
              padding: const EdgeInsets.symmetric(vertical: 20),
              decoration: const BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [Color(0xFF0E1726), Color(0xFF090E17)],
                ),
              ),
              child: Center(
                child: VoiceVisualizerOrb(
                  state: service.state,
                  onTap: () {
                    if (service.state == AssistantState.listening) {
                      service.stopListening();
                    } else {
                      service.startListeningForWakeWord();
                    }
                  },
                ),
              ),
            ),

            // Quick Automation Action Bar
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              child: SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    _buildQuickAction(
                      icon: _isTorchOn ? Icons.flash_on : Icons.flash_off,
                      label: "Torch",
                      color: _isTorchOn ? Colors.amber : Colors.blueGrey,
                      onTap: () {
                        setState(() => _isTorchOn = !_isTorchOn);
                        service.executeQuickAction("torch", {"enabled": _isTorchOn});
                      },
                    ),
                    const SizedBox(width: 10),
                    _buildQuickAction(
                      icon: Icons.battery_charging_full,
                      label: "Battery",
                      color: Colors.greenAccent,
                      onTap: () {
                        service.sendPrompt("Hey RB, what is my device battery status and health?");
                      },
                    ),
                    const SizedBox(width: 10),
                    _buildQuickAction(
                      icon: Icons.notifications_active,
                      label: "Notify",
                      color: Colors.purpleAccent,
                      onTap: () {
                        service.executeQuickAction("notify", {
                          "title": "RB.AI System",
                          "content": "RB.AI assistant is active and synchronized!"
                        });
                      },
                    ),
                    const SizedBox(width: 10),
                    _buildQuickAction(
                      icon: Icons.terminal,
                      label: "Termux Info",
                      color: Colors.cyanAccent,
                      onTap: () {
                        service.sendPrompt("Hey RB, provide a system summary of my Termux environment.");
                      },
                    ),
                  ],
                ),
              ),
            ),

            const Divider(color: Colors.white10, height: 1),

            // Chat View / History
            Expanded(
              child: ChatView(
                messages: service.messages,
                scrollController: _scrollController,
              ),
            ),

            // Image Preview if captured
            if (_selectedImageBytes != null)
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                color: const Color(0xFF131D2E),
                child: Row(
                  children: [
                    ClipRRect(
                      borderRadius: BorderRadius.circular(6),
                      child: Image.memory(_selectedImageBytes!, width: 48, height: 48, fit: BoxFit.cover),
                    ),
                    const SizedBox(width: 10),
                    const Text("Vision snapshot ready", style: TextStyle(color: Colors.white70, fontSize: 12)),
                    const Spacer(),
                    IconButton(
                      icon: const Icon(Icons.close, color: Colors.white60, size: 20),
                      onPressed: () => setState(() => _selectedImageBytes = null),
                    )
                  ],
                ),
              ),

            // Bottom Input Bar
            Container(
              padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
              decoration: const BoxDecoration(
                color: Color(0xFF0E1726),
                border: Border(top: BorderSide(color: Colors.white12, width: 0.8)),
              ),
              child: Row(
                children: [
                  IconButton(
                    icon: const Icon(Icons.camera_alt, color: Color(0xFF00E5FF)),
                    onPressed: _pickImage,
                  ),
                  Expanded(
                    child: TextField(
                      controller: _textController,
                      style: const TextStyle(color: Colors.white),
                      decoration: const InputDecoration(
                        hintText: "Ask RB.AI or command Termux...",
                        hintStyle: TextStyle(color: Colors.white38),
                        border: InputBorder.none,
                      ),
                      onSubmitted: (_) => _handleSend(service),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.send, color: Color(0xFF00E5FF)),
                    onPressed: () => _handleSend(service),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildQuickAction({
    required IconData icon,
    required String label,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: color.withOpacity(0.12),
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: color.withOpacity(0.4), width: 1),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 16, color: color),
            const SizedBox(width: 6),
            Text(label, style: TextStyle(color: color, fontSize: 12, fontWeight: FontWeight.w600)),
          ],
        ),
      ),
    );
  }
}
