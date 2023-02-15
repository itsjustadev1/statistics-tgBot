from requests import get
import bs4


def countUsers(idChannel):
    url = "https://tlgrm.ru/channels/@"
    r = get(url + idChannel)
    text = r.text

    soup = bs4.BeautifulSoup(text, "html.parser")
    a = soup.select(".channel-header__subscribers")
    if a[0]:
        usersCounter = int(a[0].text)
    else:
        print("can't find subscribers information")
    b = soup.select(".channel-header__title")
    if b[0]:
        nameChannel = b[0].text.strip()
    else:
        print("can't find name for channel")

    return usersCounter, nameChannel
