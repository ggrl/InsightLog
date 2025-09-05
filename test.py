from insightlog.lib import InsightLogAnalyzer

analyzer = InsightLogAnalyzer('nginx', filepath='logs-samples/nginx1.sample')
analyzer.add_filter('200')
requests = analyzer.get_requests()
print(requests)