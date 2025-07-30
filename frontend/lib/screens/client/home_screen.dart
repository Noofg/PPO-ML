import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F6FA),
      appBar: AppBar(
        title: const Text("FINACEPRO", style: TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.deepPurple,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: SingleChildScrollView(
          child: Column(
            children: [
              // Tổng quan
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: const [
                  _StatCard(title: "Tổng số dư", amount: "50.000.000₫", color: Colors.green),
                  _StatCard(title: "Thu nhập", amount: "10.000.000₫", color: Colors.blue),
                  _StatCard(title: "Chi tiêu", amount: "5.000.000₫", color: Colors.red),
                ],
              ),
              const SizedBox(height: 24),
              // Biểu đồ
              Container(
                width: double.infinity,
                height: 250,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 8)],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text("Biểu đồ chi tiêu hàng tháng", style: TextStyle(fontWeight: FontWeight.bold)),
                    SizedBox(height: 16),
                    Expanded(child: SpendingChart()),
                  ],
                ),
              ),
              const SizedBox(height: 24),
              // Giao dịch gần đây
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.white,
                  borderRadius: BorderRadius.circular(16),
                  boxShadow: [BoxShadow(color: Colors.black12, blurRadius: 8)],
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: const [
                    Text("Giao dịch gần đây", style: TextStyle(fontWeight: FontWeight.bold)),
                    SizedBox(height: 12),
                    _TransactionItem(title: "Ăn uống", amount: "-120.000₫", date: "16/07/2025", color: Colors.red),
                    _TransactionItem(title: "Lương tháng", amount: "+10.000.000₫", date: "01/07/2025", color: Colors.green),
                    _TransactionItem(title: "Mua sắm", amount: "-1.500.000₫", date: "12/07/2025", color: Colors.orange),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _StatCard extends StatelessWidget {
  final String title;
  final String amount;
  final Color color;

  const _StatCard({
    required this.title,
    required this.amount,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 8),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: color.withOpacity(0.1),
          borderRadius: BorderRadius.circular(16),
        ),
        child: Column(
          children: [
            Text(title, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500)),
            const SizedBox(height: 8),
            Text(amount, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
          ],
        ),
      ),
    );
  }
}

class _TransactionItem extends StatelessWidget {
  final String title;
  final String amount;
  final String date;
  final Color color;

  const _TransactionItem({
    required this.title,
    required this.amount,
    required this.date,
    required this.color,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(vertical: 4),
      leading: CircleAvatar(backgroundColor: color.withOpacity(0.2), child: Icon(Icons.attach_money, color: color)),
      title: Text(title),
      subtitle: Text(date),
      trailing: Text(amount, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
    );
  }
}

class SpendingChart extends StatelessWidget {
  const SpendingChart({super.key});

  @override
  Widget build(BuildContext context) {
    return LineChart(
      LineChartData(
        gridData: FlGridData(show: false),
        titlesData: FlTitlesData(show: true),
        borderData: FlBorderData(show: false),
        lineBarsData: [
          LineChartBarData(
            spots: const [
              FlSpot(0, 1),
              FlSpot(1, 1.5),
              FlSpot(2, 1.4),
              FlSpot(3, 3),
              FlSpot(4, 2),
              FlSpot(5, 2.2),
              FlSpot(6, 1.8),
            ],
            isCurved: true,
            barWidth: 3,
            color: Colors.deepPurple,
            dotData: FlDotData(show: false),
          )
        ],
      ),
    );
  }
}
