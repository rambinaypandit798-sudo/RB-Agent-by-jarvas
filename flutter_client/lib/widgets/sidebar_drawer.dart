import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../services/rbai_service.dart';
import 'sub_agents_workspace.dart';

class SidebarDrawer extends StatelessWidget {
  final Function(String route) onNavigate;

  const SidebarDrawer({Key? key, required this.onNavigate}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final service = Provider.of<RBAIService>(context);
    final userInitials = service.userName.isNotEmpty
        ? service.userName.split(' ').map((e) => e[0]).take(2).join('').toUpperCase()
        : 'RB';

    return Drawer(
      backgroundColor: Colors.white,
      child: Column(
        children: [
          // User Profile Header
          Container(
            padding: const EdgeInsets.fromLTRB(20, 50, 20, 20),
            color: const Color(0xFFF8FAFC),
            child: Row(
              children: [
                CircleAvatar(
                  radius: 26,
                  backgroundColor: const Color(0xFF1E3A8A),
                  child: Text(
                    userInitials,
                    style: const TextStyle(
                      color: Colors.white,
                      fontWeight: FontWeight.w800,
                      fontSize: 16,
                    ),
                  ),
                ),
                const SizedBox(width: 14),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        service.userName,
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: const TextStyle(
                          color: Color(0xFF0F172A),
                          fontWeight: FontWeight.w800,
                          fontSize: 15,
                        ),
                      ),
                      const SizedBox(height: 2),
                      const Text(
                        "Master User • Autonomous OS",
                        style: TextStyle(
                          color: Color(0xFF64748B),
                          fontSize: 11,
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const Divider(height: 1, color: Color(0xFFE2E8F0)),

          // Navigation Menu Items
          Expanded(
            child: ListView(
              padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 12),
              children: [
                _buildNavItem(context, Icons.home, "Home", () {
                  Navigator.pop(context);
                  onNavigate("home");
                }, isActive: true),
                _buildNavItem(context, Icons.hub, "5 Sub-Agents Workspace", () {
                  Navigator.pop(context);
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const SubAgentsWorkspaceScreen()),
                  );
                }),
                _buildNavItem(context, Icons.language, "Web Research", () {
                  Navigator.pop(context);
                  onNavigate("web");
                }),
                _buildNavItem(context, Icons.code, "Code & GitHub", () {
                  Navigator.pop(context);
                  onNavigate("code");
                }),
                _buildNavItem(context, Icons.folder, "Files & Storage", () {
                  Navigator.pop(context);
                  onNavigate("files");
                }),
                _buildNavItem(context, Icons.note_alt, "Persistent Data Notes", () {
                  Navigator.pop(context);
                  onNavigate("notes");
                }),
                _buildNavItem(context, Icons.chat, "Chats", () {
                  Navigator.pop(context);
                  onNavigate("chats");
                }),
                _buildNavItem(context, Icons.auto_awesome_mosaic, "Projects", () {
                  Navigator.pop(context);
                  onNavigate("projects");
                }),
                _buildNavItem(context, Icons.add_circle, "Skill Add", () {
                  Navigator.pop(context);
                  onNavigate("skills");
                }),
                const Divider(height: 20, color: Color(0xFFE2E8F0)),
                _buildNavItem(context, Icons.settings, "Settings & Accents", () {
                  Navigator.pop(context);
                  onNavigate("settings");
                }),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildNavItem(
    BuildContext context,
    IconData icon,
    String title,
    VoidCallback onTap, {
    bool isActive = false,
  }) {
    return Container(
      margin: const EdgeInsets.only(bottom: 4),
      decoration: BoxDecoration(
        color: isActive ? const Color(0xFFEEF2F6) : Colors.transparent,
        borderRadius: BorderRadius.circular(10),
      ),
      child: ListTile(
        leading: Icon(
          icon,
          color: isActive ? const Color(0xFF0077FE) : const Color(0xFF475569),
          size: 20,
        ),
        title: Text(
          title,
          style: TextStyle(
            color: isActive ? const Color(0xFF0077FE) : const Color(0xFF1E293B),
            fontWeight: isActive ? FontWeight.w700 : FontWeight.w600,
            fontSize: 13,
          ),
        ),
        onTap: onTap,
        dense: true,
        visualDensity: const VisualDensity(vertical: -1),
      ),
    );
  }
}
