from insightlog.lib import filter_data
from insightlog.lib import *
import os



analyzer = InsightLogAnalyzer('nginx', filepath='logs-samples/empty.sample')
analyzer.add_filter('200')
requests = analyzer.get_requests()
print(requests)
