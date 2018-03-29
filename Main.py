
import urllib.request as urllib2
import urllib
from bs4 import BeautifulSoup

field_dictionary = {}
table_dictionary = {}
example = ['bkpf', 'bseg']
for i in example:
    url = "http://www.leanx.eu/en/sap/table/{}.html".format(i)
    table_dictionary[i] = []
    page=urllib.request.Request(url,headers={'User-Agent': 'Mozilla/5.0'})
    infile=urllib.request.urlopen(page).read()
    data = infile.decode('ISO-8859-1') # Read the content as string decoded with ISO-8859-1

    soup = BeautifulSoup(data, "html.parser")
    table = soup.find("table")

    for div in table.find_all("div"):
        div.decompose()

    datasets = []
    for row in table.find_all("tr", {'class':'info'}):
        dataset = []
        for td in row.find_all("td")[:2]:
            dataset.append(td.get_text())
        if dataset[0] not in field_dictionary:
            field_dictionary[dataset[0]] = {'description': dataset[1], 'table_pk': [i], 'table_npk': []}
        else:
            field_dictionary[dataset[0]]['table_pk'].append(i)
        dataset.append(1)
        table_dictionary[i].append(dataset)
        row.decompose()

    for row in table.find_all("tr")[1:]:
        dataset = []
        for td in row.find_all("td")[:2]:
            dataset.append(td.get_text())
        if dataset[0] not in field_dictionary:
            field_dictionary[dataset[0]] = {'description': dataset[1], 'table_pk': [], 'table_npk': [i]}
        else:
            field_dictionary[dataset[0]]['table_npk'].append(i)
        dataset.append(0)
        table_dictionary[i].append(dataset)
        row.decompose()

print(field_dictionary['MANDT'])