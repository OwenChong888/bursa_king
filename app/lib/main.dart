import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:syncfusion_flutter_charts/charts.dart';

// 1. Markdown support makes the AI response look much better
// Run: flutter pub add flutter_markdown
// import 'package:flutter_markdown/flutter_markdown.dart'; 

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Bursa Sentinel',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Bursa Sentinel | Track B'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _tickerController = TextEditingController();
  String _analysisResult = "Enter a Bursa ticker (e.g., 1155.KL) to start.";
  bool _isLoading = false;
  List<StockChartData> _chartDataList = [];

  Future<void> _runSwarmAnalysis() async {
    final ticker = _tickerController.text.trim().toUpperCase();
    if (ticker.isEmpty) return;

    setState(() {
      _isLoading = true;
      _chartDataList = []; 
      _analysisResult = "Gathering Market Intelligence...";
    });

    try {
      // Use localhost for Web, 10.0.2.2 for Android Emulator
      final response = await http.post(
        Uri.parse('http://localhost:8000/analyze?ticker=$ticker'),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        
        setState(() {
          // Update Text Analysis with null check
          _analysisResult = data['analysis'] ?? "No intelligence report generated.";
          
          // Parse Historical Data for Chart
          if (data['history'] != null) {
            final List<dynamic> history = data['history'];
            _chartDataList = history.map((e) {
              return StockChartData(
                DateTime.parse(e['date']),
                (e['open'] as num).toDouble(),
                (e['high'] as num).toDouble(),
                (e['low'] as num).toDouble(),
                (e['close'] as num).toDouble(),
              );
            }).toList();
          }
        });
      } else {
        setState(() {
          _analysisResult = "⚠️ Server Error: ${response.statusCode}";
        });
      }
    } catch (e) {
      setState(() {
        _analysisResult = "❌ Connection Failed: Is server.py running?\n$e";
      });
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.blueGrey[900],
        elevation: 4,
        title: Text(widget.title, style: const TextStyle(color: Colors.white, fontSize: 18)),
        actions: [
          if (_isLoading)
            const Padding(
              padding: EdgeInsets.symmetric(horizontal: 16.0),
              child: Center(child: SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))),
            )
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // SEARCH SECTION
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _tickerController,
                    onSubmitted: (_) => _runSwarmAnalysis(),
                    decoration: const InputDecoration(
                      labelText: "Bursa Ticker",
                      hintText: "1155.KL",
                      prefixIcon: Icon(Icons.show_chart),
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 10),
                IconButton.filled(
                  onPressed: _isLoading ? null : _runSwarmAnalysis,
                  icon: const Icon(Icons.analytics_outlined),
                  padding: const EdgeInsets.all(15),
                )
              ],
            ),
            
            const SizedBox(height: 20),

            // CHART SECTION
            if (_chartDataList.isNotEmpty) 
              Card(
                elevation: 2,
                child: Padding(
                  padding: const EdgeInsets.all(8.0),
                  child: SizedBox(
                    height: 280,
                    child: SfCartesianChart(
                      title: ChartTitle(text: '${_tickerController.text.toUpperCase()} 30-Day Trend', textStyle: const TextStyle(fontSize: 12)),
                      trackballBehavior: TrackballBehavior(
                        enable: true,
                        activationMode: ActivationMode.singleTap,
                        tooltipSettings: const InteractiveTooltip(enable: true, format: 'point.x : point.y'),
                      ),
                      primaryXAxis: DateTimeAxis(),
                      series: <CandleSeries<StockChartData, DateTime>>[
                        CandleSeries<StockChartData, DateTime>(
                          dataSource: _chartDataList,
                          xValueMapper: (StockChartData data, _) => data.x,
                          lowValueMapper: (StockChartData data, _) => data.low,
                          highValueMapper: (StockChartData data, _) => data.high,
                          openValueMapper: (StockChartData data, _) => data.open,
                          closeValueMapper: (StockChartData data, _) => data.close,
                          enableSolidCandles: true,
                          bearColor: Colors.redAccent,
                          bullColor: Colors.greenAccent,
                        ),
                      ],
                    ),
                  ),
                ),
              ),

            const SizedBox(height: 20),
            const Text("AGENT INTELLIGENCE REPORT", style: TextStyle(fontWeight: FontWeight.bold, letterSpacing: 1.2, color: Colors.blueGrey)),
            const Divider(),
            
            // REPORT SECTION
            Expanded(
              child: Container(
                padding: const EdgeInsets.all(16),
                decoration: BoxDecoration(
                  color: Colors.grey[50],
                  borderRadius: BorderRadius.circular(12),
                  border: Border.all(color: Colors.grey[300]!),
                ),
                child: SingleChildScrollView(
                  child: Text(
                    _analysisResult,
                    style: const TextStyle(fontSize: 15, height: 1.5, fontFamily: 'Georgia'),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class StockChartData {
  StockChartData(this.x, this.open, this.high, this.low, this.close);
  final DateTime x;
  final double open;
  final double high;
  final double low;
  final double close;
}