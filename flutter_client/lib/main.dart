import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'services/rbai_service.dart';
import 'screens/home_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => RBAIService()),
      ],
      child: const RBAssistantApp(),
    ),
  );
}

class RBAssistantApp extends StatelessWidget {
  const RBAssistantApp({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RB.AI Assistant',
      debugShowCheckedModeBanner: false,
      theme: ThemeData.dark().copyWith(
        scaffoldBackgroundColor: const Color(0xFF090E17),
        primaryColor: const Color(0xFF00E5FF),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF00E5FF),
          secondary: Color(0xFFBD00FF),
          surface: Color(0xFF131D2E),
        ),
      ),
      home: const HomeScreen(),
    );
  }
}
