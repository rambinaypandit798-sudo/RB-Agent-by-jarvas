import 'dart:convert';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:speech_to_text/speech_to_text.dart' as stt;
import 'package:flutter_tts/flutter_tts.dart';
import '../models/message.dart';

enum AssistantState { idle, listening, thinking, speaking }

class RBAIService extends ChangeNotifier {
  String baseUrl = "http://127.0.0.1:8765";
  AssistantState _state = AssistantState.idle;
  bool isConnected = false;
  Map<String, dynamic> deviceStatus = {};

  final List<ChatMessage> _messages = [];
  List<ChatMessage> get messages => List.unmodifiable(_messages);
  AssistantState get state => _state;

  // Speech & Voice
  late stt.SpeechToText _speech;
  late FlutterTts _tts;
  bool _speechEnabled = false;
  String _lastHeardWords = "";

  RBAIService() {
    _speech = stt.SpeechToText();
    _tts = FlutterTts();
    _initVoice();
    checkConnection();
  }

  void setBaseUrl(String url) {
    baseUrl = url;
    checkConnection();
    notifyListeners();
  }

  void _setState(AssistantState newState) {
    _state = newState;
    notifyListeners();
  }

  Future<void> _initVoice() async {
    try {
      _speechEnabled = await _speech.initialize(
        onError: (err) => debugPrint('[RB.AI STT Error]: $err'),
        onStatus: (status) => debugPrint('[RB.AI STT Status]: $status'),
      );
      await _tts.setLanguage("en-US");
      await _tts.setPitch(1.0);
      await _tts.setSpeechRate(0.5);
    } catch (e) {
      debugPrint('[RB.AI Voice Init]: $e');
    }
  }

  Future<bool> checkConnection() async {
    try {
      final res = await http.get(Uri.parse('$baseUrl/api/status')).timeout(const Duration(seconds: 4));
      if (res.statusCode == 200) {
        isConnected = true;
        deviceStatus = json.decode(res.body);
        notifyListeners();
        return true;
      }
    } catch (_) {
      isConnected = false;
      notifyListeners();
    }
    return false;
  }

  // Wake Phrase "Hey RB" continuous listener
  void startListeningForWakeWord() async {
    if (!_speechEnabled) {
      await _initVoice();
    }

    _setState(AssistantState.listening);
    await _speech.listen(
      onResult: (result) {
        _lastHeardWords = result.recognizedWords;
        final lower = _lastHeardWords.toLowerCase();

        // Check wake phrase
        if (lower.contains("hey rb") || lower.contains("rb")) {
          debugPrint("Wake word detected in: $_lastHeardWords");
          _speech.stop();
          sendPrompt(_lastHeardWords, isVoice: true);
        }
      },
      listenFor: const Duration(seconds: 30),
      pauseFor: const Duration(seconds: 4),
      listenOptions: stt.SpeechListenOptions(partialResults: true),
    );
  }

  void stopListening() {
    _speech.stop();
    _setState(AssistantState.idle);
  }

  Future<void> speak(String text) async {
    _setState(AssistantState.speaking);
    await _tts.speak(text);
    _setState(AssistantState.idle);
  }

  Future<void> sendPrompt(String text, {Uint8List? imageBytes, bool isVoice = false}) async {
    if (text.trim().isEmpty && imageBytes == null) return;

    // Add user message
    _messages.add(ChatMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      role: MessageRole.user,
      text: text,
      imageBytes: imageBytes,
    ));
    notifyListeners();

    _setState(AssistantState.thinking);

    try {
      final Map<String, dynamic> payload = {
        "text": text,
        "is_voice": isVoice,
      };

      if (imageBytes != null) {
        payload["image"] = base64Encode(imageBytes);
      }

      final res = await http.post(
        Uri.parse('$baseUrl/api/chat'),
        headers: {"Content-Type": "application/json"},
        body: json.encode(payload),
      ).timeout(const Duration(seconds: 35));

      if (res.statusCode == 200) {
        final data = json.decode(res.body);
        final replyText = data['response'] ?? '(No response)';
        final toolCalls = data['tool_calls'] as List<dynamic>?;

        _messages.add(ChatMessage(
          id: (DateTime.now().millisecondsSinceEpoch + 1).toString(),
          role: MessageRole.assistant,
          text: replyText,
          toolCalls: toolCalls,
        ));

        if (isVoice) {
          speak(replyText);
        } else {
          _setState(AssistantState.idle);
        }
      } else {
        _messages.add(ChatMessage(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          role: MessageRole.system,
          text: "Server Error: ${res.statusCode}",
        ));
        _setState(AssistantState.idle);
      }
    } catch (e) {
      _messages.add(ChatMessage(
        id: DateTime.now().millisecondsSinceEpoch.toString(),
        role: MessageRole.system,
        text: "Connection failed: Could not reach RB.AI on $baseUrl ($e)",
      ));
      _setState(AssistantState.idle);
    }
  }

  Future<void> executeQuickAction(String action, [Map<String, dynamic>? args]) async {
    try {
      final res = await http.post(
        Uri.parse('$baseUrl/api/action'),
        headers: {"Content-Type": "application/json"},
        body: json.encode({"action": action, "args": args ?? {}}),
      );
      if (res.statusCode == 200) {
        checkConnection();
      }
    } catch (e) {
      debugPrint('[Action Error]: $e');
    }
  }
}
