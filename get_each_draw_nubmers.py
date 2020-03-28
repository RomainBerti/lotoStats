import requests
from html2csv import Converter

url = 'https://loteries.lotoquebec.com/fr/loteries/lotto-max?annee=2019&widget=resultats-anterieurs&noProduit=223#res'

years = range(2020, 2008, -1)

# response = requests.get(url)

converter = Converter()
# output = converter.convert(response.text)


def format_seven_numbers_with_bonus(numbers_string):
    seven_numbers, bonus = numbers_string.strip(')').split('(')
    seven_numbers_formatted = ','.join([seven_numbers[i: i + 2] for i in range(0, len(seven_numbers), 2)])
    return f'{seven_numbers_formatted},{bonus}'


with open('loto_table.csv', 'w') as file:
    file.writelines('Date,Number1,Number2,Number3,Number4,Number5,Number6,Number7,Bonus Number\n')
    url_pre, url_post = url.split('2019')
    for year in years:
        request_url = f'{url_pre}{year}{url_post}'
        response = requests.get(request_url)
        output = converter.convert(response.text)
        for csv_string, _ in output:
            for string in csv_string.split('\r\n'):
                if 'Date' in string:
                    continue
                try:
                    date, numbers = string.split(',')
                except ValueError:
                    continue
                if 'Tirage Principal' in numbers:
                    formatted_numbers_without_maxmillions = numbers.split('Maxmillions')[0].strip('Tirage Principal')
                    formatted_numbers = format_seven_numbers_with_bonus(formatted_numbers_without_maxmillions)
                else:
                    formatted_numbers = format_seven_numbers_with_bonus(numbers)
                string = f'{date},{formatted_numbers}'
                file.writelines(f'{string}\r\n')
