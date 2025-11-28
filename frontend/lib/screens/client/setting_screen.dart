import 'package:flutter/material.dart';

class SettingScreen extends StatelessWidget {
  const SettingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Cài đặt"),
        backgroundColor: Colors.deepPurple,
        foregroundColor: Colors.white,
        elevation: 2,
      ),
      body: ListView(
        children: [
          const SizedBox(height: 20),
          const _SectionTitle(title: 'Tài khoản'),
          _SettingTile(
            icon: Icons.person,
            title: 'Hồ sơ cá nhân',
            onTap: () {},
          ),
          _SettingTile(
            icon: Icons.lock,
            title: 'Bảo mật & Mật khẩu',
            onTap: () {},
          ),
          const Divider(),

          const _SectionTitle(title: 'Tùy chọn'),
          _SettingTile(
            icon: Icons.notifications,
            title: 'Thông báo',
            onTap: () {},
          ),
          _SettingTile(
            icon: Icons.palette,
            title: 'Giao diện & Chủ đề',
            onTap: () {},
          ),
          const Divider(),

          const _SectionTitle(title: 'Khác'),
          _SettingTile(
            icon: Icons.info_outline,
            title: 'Giới thiệu ứng dụng',
            onTap: () {},
          ),
          _SettingTile(
            icon: Icons.logout,
            title: 'Đăng xuất',
            iconColor: Colors.red,
            onTap: () {
              // TODO: Thêm logic đăng xuất
              showDialog(
                context: context,
                builder: (_) => AlertDialog(
                  title: const Text('Xác nhận'),
                  content: const Text('Bạn có chắc chắn muốn đăng xuất?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Hủy'),
                    ),
                    TextButton(
                      onPressed: () {
                        Navigator.pop(context);
                        // Thêm logic chuyển sang màn hình đăng nhập nếu cần
                      },
                      child: const Text('Đăng xuất'),
                    ),
                  ],
                ),
              );
            },
          ),
        ],
      ),
    );
  }
}

class _SettingTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final VoidCallback onTap;
  final Color? iconColor;

  const _SettingTile({
    required this.icon,
    required this.title,
    required this.onTap,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Icon(icon, color: iconColor ?? Colors.deepPurple),
      title: Text(title),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: onTap,
    );
  }
}

class _SectionTitle extends StatelessWidget {
  final String title;
  const _SectionTitle({required this.title});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Text(title.toUpperCase(),
          style: TextStyle(
              color: Colors.grey[600], fontWeight: FontWeight.bold)),
    );
  }
}
