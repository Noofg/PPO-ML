import 'package:flutter/material.dart';

class AddTransactionScreen extends StatefulWidget {
  const AddTransactionScreen({super.key});

  @override
  State<AddTransactionScreen> createState() => _AddTransactionScreenState();
}

class _AddTransactionScreenState extends State<AddTransactionScreen> {
  final TextEditingController amountController = TextEditingController();
  final TextEditingController noteController = TextEditingController();
  DateTime selectedDate = DateTime.now();
  String? selectedCategory;

  final List<String> categories = [
    'Ăn uống',
    'Thời trang',
    'Giải trí',
    'Đi lại',
    'Học tập',
    'Khác'
  ];

  void _pickDate() async {
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: selectedDate,
      firstDate: DateTime(2023),
      lastDate: DateTime(2100),
    );
    if (picked != null) {
      setState(() => selectedDate = picked);
    }
  }

  void _addCategory() {
    showDialog(
      context: context,
      builder: (context) {
        final TextEditingController newCategoryController = TextEditingController();
        return AlertDialog(
          title: const Text("Thêm danh mục"),
          content: TextField(
            controller: newCategoryController,
            decoration: const InputDecoration(hintText: "Tên danh mục"),
          ),
          actions: [
            TextButton(
              child: const Text("Hủy"),
              onPressed: () => Navigator.pop(context),
            ),
            ElevatedButton(
              child: const Text("Thêm"),
              onPressed: () {
                setState(() {
                  categories.add(newCategoryController.text);
                  selectedCategory = newCategoryController.text;
                });
                Navigator.pop(context);
              },
            ),
          ],
        );
      },
    );
  }

  void _saveTransaction() {
    final amount = amountController.text;
    final note = noteController.text;
    final category = selectedCategory;

    if (amount.isEmpty || category == null) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Vui lòng nhập đầy đủ thông tin')),
      );
      return;
    }

    // TODO: Gửi dữ liệu lên backend hoặc lưu vào local
    print("Đã lưu: $amount | $category | $note | $selectedDate");

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Đã lưu giao dịch')),
    );

    // Xóa form
    amountController.clear();
    noteController.clear();
    setState(() {
      selectedCategory = null;
      selectedDate = DateTime.now();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("Thêm Giao Dịch")),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: amountController,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: "Số tiền",
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              decoration: const InputDecoration(
                labelText: "Danh mục",
                border: OutlineInputBorder(),
              ),
              value: selectedCategory,
              onChanged: (value) => setState(() => selectedCategory = value),
              items: categories
                  .map((cat) => DropdownMenuItem(value: cat, child: Text(cat)))
                  .toList(),
            ),
            TextButton.icon(
              onPressed: _addCategory,
              icon: const Icon(Icons.add),
              label: const Text("Thêm danh mục"),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: noteController,
              decoration: const InputDecoration(
                labelText: "Ghi chú (tuỳ chọn)",
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: Text("Ngày: ${selectedDate.toLocal()}".split(' ')[0]),
                ),
                ElevatedButton(
                  onPressed: _pickDate,
                  child: const Text("Chọn ngày"),
                ),
              ],
            ),
            const Spacer(),
            ElevatedButton.icon(
              onPressed: _saveTransaction,
              icon: const Icon(Icons.save),
              label: const Text("Lưu giao dịch"),
              style: ElevatedButton.styleFrom(minimumSize: const Size.fromHeight(50)),
            ),
          ],
        ),
      ),
    );
  }
}
