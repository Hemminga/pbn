import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pprint import pprint
import model
import view


if __name__ == '__main__':
    pbn = input("Give a PBN string: ")
    # DEBUG
    if pbn == '':
        pbn = "N:Q974.KJ.QJ43.QJ8 J82.AQT4.875.K64 AT65.8532.962.A7 K3.976.AKT.T9532"
    data = model.process_pbn_input(pbn)
    # pprint(data)

    environment = Environment(
        loader=FileSystemLoader("templates/"),
        autoescape=select_autoescape()
    )
    template = environment.get_template("draad.txt")
    content = template.render(hands=data.hands)
    date = datetime.date.today()
    print(date)
    filename = f'{date}_draad.html'
    pprint(data)
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
    # pprint(data)
