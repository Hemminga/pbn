import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
from pprint import pprint
from xml.etree.ElementTree import parse
import types




if __name__ == '__main__':
    files = [f for f in os.listdir(os.curdir) if os.path.isfile(f)]  # list comprehension version.
    data = []
    for file in files:
        if '.xml' not in file:
            continue
        print(file)
        tree = parse(file)
        root = tree.getroot()
        for reportable_result in root.iter('ReportableSessionResult'):
            result = types.SimpleNamespace()
            xml_player_first = reportable_result.find('PlayerOne')
            result.nbb = xml_player_first.find('LeagueId').text
            result.name = xml_player_first.find('Voornaam').text + \
                          (' ' + xml_player_first.find('Tussenvoegsel').text + ' ' if xml_player_first.find('Tussenvoegsel').text else ' ') + \
                          xml_player_first.find('Achternaam').text
            result.count = reportable_result.find('NumberOfBoards').text
            result.matchpoints = reportable_result.find('AbsoluteResult').text
            result.result = reportable_result.find('Result').text
            data.append(result)
            result = types.SimpleNamespace()
            xml_player_second = reportable_result.find('PlayerTwo')
            result.nbb = xml_player_second.find('LeagueId').text
            result.name = xml_player_second.find('Voornaam').text + \
                          (' ' + xml_player_second.find('Tussenvoegsel').text + ' ' if xml_player_second.find('Tussenvoegsel').text else ' ') + \
                          xml_player_second.find('Achternaam').text
            result.count = reportable_result.find('NumberOfBoards').text
            result.matchpoints = reportable_result.find('AbsoluteResult').text
            result.result = reportable_result.find('Result').text
            data.append(result)
    # pprint(data)
    results = {}
    for mydata in data:
        if mydata.nbb not in results:
            results[mydata.nbb] = {}
        results[mydata.nbb]['nbb'] = mydata.nbb
        results[mydata.nbb]['naam'] = mydata.name
        if 'aantal' not in results[mydata.nbb]:
            results[mydata.nbb]['aantal'] = 0
        results[mydata.nbb]['aantal'] += int(mydata.count)
        if 'totaal' not in results[mydata.nbb]:
            results[mydata.nbb]['totaal'] = 0.0
        results[mydata.nbb]['totaal'] += float(mydata.result) * int(mydata.count)
        if 'reported' not in results[mydata.nbb]:
            results[mydata.nbb]['reported'] = []
        results[mydata.nbb]['reported'].append(mydata.result)
        results[mydata.nbb]['percentage'] = results[mydata.nbb]['totaal'] / results[mydata.nbb]['aantal']
    newlist = []
    max_zittingen = 0
    i = 1
    for result in results:
        if not result or result == '0':
            continue
        if len(results[result]['reported']) > max_zittingen:
            max_zittingen = len(results[result]['reported'])
        newlist.append(results[result])
    results = sorted(newlist, key=lambda x: x['totaal'], reverse=True)
    #pprint(results)
    print(max_zittingen)
    roman_numerals = ['-', 'I', 'II', 'III', 'IV', 'V', 'VI']
    headers = []
    for i in range(max_zittingen):
        headers.append(roman_numerals[i+1])

    # Jinja
    environment = Environment(
        loader=FileSystemLoader("templates/"),
        autoescape=select_autoescape()
    )
    template = environment.get_template("uitslag.txt")
    content = template.render(zittingen=headers, results=results)
    date = datetime.date.today()
    print(date)
    filename = f'{date}_uitslag.html'
    pprint(data)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")