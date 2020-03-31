import requests
from html2csv import Converter

url = 'https://loteries.espacejeux.com/en/lotteries/lotto-max?outil=statistiques-223#res'

response = requests.get(url)

converter = Converter()
output = converter.convert(response.text)

all_time_num_order = ''
all_time_freq_order = ''

for table in output:
    if 'Numeric OrderSince the start' in table[0]:
        all_time_num_order = table
    if 'Frequency OrderSince the start' in table[0]:
        all_time_freq_order = table

with open('loto_table_num_order.csv', 'w') as file:
    for csv_string in all_time_num_order:
        file.writelines(csv_string)

with open('loto_table_freq_order.csv', 'w') as file:
    for csv_string in all_time_freq_order:
        file.writelines(csv_string)
