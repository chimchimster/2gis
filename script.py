import re
from requests_html import HTMLSession
import pandas as pd

# session = HTMLSession()
# response = session.get('https://2gis.ru/firm/70000001061816441')
#
# findCharAndNumber = re.findall(r'"type":"phone","value":"\+7\d+', response.text).pop()
# findNumber = re.findall(r'\d+', findCharAndNumber)
#
# findCharTitle = re.findall(r'<title>.*</title>', response.text)
# findCharEmail = re.findall(r'"type":"email","text":".*?"', response.text)
# findEmail = re.findall(r'"text":".*@.*"', findCharEmail.pop())
#
# response2 = session.get('https://2gis.ru/moscow/search/%D1%81%D0%BA%D0%BB%D0%B0%D0%B4/geo/')
#
# ids = re.findall(r'"data":\[([^]]+)\]', response2.text)
#
# response3 = session.get('https://2gis.ru/moscow/search/%D1%81%D0%BA%D0%BB%D0%B0%D0%B4/page/2/geo')


class IdsCollector:
    paginate_link = 'https://2gis.ru/moscow/search/фабрики/page/'

    def __init__(self, paginate_number):
        self.session = HTMLSession()
        self.paginate_number = paginate_number

    def collect_ids(self):

        for i in range(1, self.paginate_number + 1):
            response = self.session.get(f'{self.paginate_link}{i}/geo')

            ids = re.findall(r'"data":\[([^]]+)\]', response.text)

            with open('ids.txt', 'a') as file:
                for id in ids:
                    res = id.replace('"', '')
                    r = res.split(',')
                    for _ in r:
                        file.write(_ + '\n')


# i = IdsCollector(25)
# i.collect_ids()

class CollectData:

    link = 'https://2gis.ru/firm/'

    def __init__(self):
        self.session = HTMLSession()

    def find_full_data(self):
        with open('ids.txt', 'r') as file:
            data = [d.strip() for d in file.readlines()]

            for dt in data:
                response = self.session.get(f'{self.link}{dt}')

                findNumber, findCharTitle, findEmail = '', '', ''

                findCharAndNumber = re.findall(r'"type":"phone","value":"\+7\d+', response.text)
                if findCharAndNumber:
                    findCharAndNumber = findCharAndNumber.pop()

                    findNumber = re.findall(r'\d+', findCharAndNumber)

                findCharTitle = re.findall(r'<title>.*</title>', response.text)

                if findCharTitle:
                    findCharTitle = findCharTitle.pop()

                findCharEmail = re.findall(r'"type":"email","text":".*?"', response.text)

                if findCharEmail:
                    findCharEmail = findCharEmail.pop()

                    findEmail = re.findall(r'"text":".*@.*"', findCharEmail)

                with open('result.txt', 'a') as file:

                    file.write(f'{findCharTitle, findEmail, findNumber}' + '\n')


# c = CollectData()
# c.find_full_data()

# with open('result.txt', 'r') as file:
#     res = [r.replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace("<title>", '').replace("</title>", "").replace("['", '').replace('text":"', '').replace("']", '').replace("['", '').replace("'])", '').strip() for r in file.readlines()]
#
#     for rs in res:
#         with open('companies-sklad.txt', 'a') as file:
#             file.write(rs + '\n')


with open('companies-sklad.txt', 'r') as file:
    # res = [r.replace('2ГИС', ':').strip() for r in file.readlines()]

    res = [r.strip().split('2ГИС') for r in file.readlines()]

    res = [[r[0]] + r[1].split(',') for r in res]
    res = [r for r in res if r != '']
    new = []
    for r in res:
        new.append(r[:3] + [r[3].replace("'", '').replace(' ', '')])
    new = [n for n in new if n[3] != '']
    print(new)
    df = pd.DataFrame(new, columns=['title', 'empty', 'email', 'number'])

    df.to_excel('companies.xlsx')