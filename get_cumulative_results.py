import requests
from html2csv import Converter
from random import choices

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
    table = all_time_num_order[0].strip().split('\r\n')
    table = [line.split(',') for line in table]
    total = sum(int(element[1]) for element in table[2:-1])
    probability_list = [float(str(int(line[1])/total)[:6]) for line in table if line[0].isdigit()]
    table = '\r\n'.join([','.join(line + [f'{str(int(line[1])/total)[:6]}']) if line[0].isdigit() else ','.join(line)
                         for line in table])
    file.writelines(table)

with open('loto_table_freq_order.csv', 'w') as file:
    for csv_string in all_time_freq_order:
        file.writelines(csv_string)
'''
total = 0
twod_array = []
lines_of_strings = all_time_num_order[0].split('\n')
for line in lines_of_strings:
    try:
        list_of_elem = [int(x) for x in line.strip('\r').split(',')]
        twod_array.append(list_of_elem)
        total += list_of_elem[1]
    except ValueError:
        twod_array.append([x for x in line.strip('\r').split(',')])

column_of_prob = [line[1]/total for line in twod_array if isinstance(line[0], int)]
'''
list_of_draws = []
while len(list_of_draws) < 6:
    new_draw = choices(range(1, 50), probability_list)
    if new_draw not in list_of_draws:
        list_of_draws.append(str(new_draw))

print(list_of_draws)
