import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class StatisticsScreen extends StatelessWidget {
  const StatisticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Thống kê chi tiêu')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            const Text(
              "Tổng chi tiêu theo danh mục",
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 20),
            Expanded(
              child: PieChart(
                PieChartData(
                  sections: [
                    PieChartSectionData(
                      color: Colors.blue,
                      value: 40,
                      title: 'Ăn uống\n40%',
                      radius: 60,
                    ),
                    PieChartSectionData(
                      color: Colors.green,
                      value: 25,
                      title: 'Giải trí\n25%',
                      radius: 60,
                    ),
                    PieChartSectionData(
                      color: Colors.orange,
                      value: 20,
                      title: 'Thời trang\n20%',
                      radius: 60,
                    ),
                    PieChartSectionData(
                      color: Colors.purple,
                      value: 15,
                      title: 'Khác\n15%',
                      radius: 60,
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              icon: const Icon(Icons.refresh),
              label: const Text("Làm mới dữ liệu"),
              onPressed: () {
                // TODO: gọi lại API hoặc cập nhật dữ liệu
              },
            ),
          ],
        ),
      ),
    );
  }
}
