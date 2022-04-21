import requests
from bs4 import BeautifulSoup

URL = r"https://examer.ru/ege_po_fizike/teoriya/pryamolinejnoe_dvizhenie_i_dvizhenie_po_okruzhnosti"

def parse_physics(URL=None):
    if URL is not None:
        print("Start parsing!")
        # parse data from url
        request = requests.get(URL)
        soup = BeautifulSoup(request.text, 'html.parser')
        articles = soup.find_all('p')
        articles_list = [x for x in articles if len(x.findChildren('b')) != 0]
        # clear data
        articles_list = [str(x).replace("<b>", "").replace("</b>", "") for x in articles_list]
        articles_list = [str(x).replace("<p>", "").replace("</p>", "") for x in articles_list]
        articles_list = [str(x).replace("$", "").replace("{→}", "").replace("<i>", "").replace("</i>", "").replace(":", ".") for x in articles_list]
        return articles_list
    else:
        pass


def parse_math(URL=None):
    if URL is not None:
        print("Start parsing!")
        request = requests.get(URL)
        soup = BeautifulSoup(request.text, 'html.parser')
        articles = soup.find_all('p')
        articles_list = [x for x in articles if len(x.findChildren('et__note')) != 0]


        print(articles)


if __name__ == "__main__":
    URL = r"https://educon.by/index.php/materials/math/vvodnaja/"
    data = parse_math(URL)
    #print(*data, sep="\n\n")


