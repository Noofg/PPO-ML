import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../screens/auth/login_screen.dart';
import '../screens/auth/register_screen.dart';
import '../screens/client/home_screen.dart';
import '../screens/client/AddExpense_screen.dart';
import '../screens/client/AddTransactionScreen.dart';
import '../screens/shareScreens/bottom_navigation.dart';

class AppRouter {
  static final router = GoRouter(
    initialLocation: '/login',
    routes: [
      // 🔹 Login và Register KHÔNG cần bottom navigation
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        builder: (context, state) => const RegisterScreen(),
      ),

      // 🔹 Các route có bottom navigation
      ShellRoute(
        builder: (context, state, child) {
          return BottomNavScreen(child: child);
        },
        routes: [
          GoRoute(
            path: '/home',
            builder: (context, state) => const HomeScreen(),
          ),
          GoRoute(
            path: '/AddExpense',
            builder: (context, state) => const AddExpensePage(),
          ),
          GoRoute(
            path: '/AddTransaction',
            builder: (context, state) => const AddTransactionScreen(),
          ),
        ],
      ),
    ],
  );
}
