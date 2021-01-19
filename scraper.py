from bs4 import BeautifulSoup
import requests
import time


def searchLinks(keyword):

    list_of_page = []
    links = []

    for i in range(17):
        url = "https://hewlett.org/wp/wp-admin/admin-ajax.php"

        data = {
        "action": "update_results",
        "engine": "grant",
        "listing_type": "/grants/",
        "keyword": keyword,
        "sort": "date",
        "current_page": i+1
        }

        response = requests.post(url, data=data)
        dictionary = response.json()
        articles = dictionary["articles"]
        list_of_page.extend(articles["page"])

        time.sleep(3)


    for j in list_of_page:
        links.append(j["url"])


    with open('urls.txt', 'w') as file:
        for link in links:
            file.write(link + '\n')


def concatenationString(listData):

    string = ""

    for index in range(len(listData)):
        if listData[index] != None:
            if index == 1 or index == 0 or index == 7: #cas où peut avoir de virgules
                string += listData[index].text.strip().replace(",", "")
                string += ","
            elif index == 8:
                string += listData[index]['href']
                string += ","
            elif index == 9:
                string += listData[index].text.strip().replace(",", " ")
                string += ","
            else:
                string += listData[index].text.strip() #cas général
                string += ","
        else:  # si il n'y a pas de info on n'ajoute qu'un "espace"
            string += " "
            string += ","

    return string

# Recupere les titles de chaque nouvelle sur la page.
def getNews(list_News):

    str = ""
    for item in list_News:
        str += item.find('a').text.strip().replace(",", " ")
        str += ","

    return str

# Recupere les données desirées sur la page et sauvegarde dans un fichier cvs.
def getInfos():

    with open('urls.txt', 'r') as file:
        with open('projets.csv', 'w') as outFile:
            outFile.write('Title,Amount,Program,Date,Term,Type of Support,Strategies,Overview,About the Grantee Website,About the Grantee Address, News1, News2, News3 \n')
            for row in file:
                url = row.strip()
                response = requests.get(url)
                if response.ok:

                    #on sauvegarde chaque champ desire dans une variable
                    soup = BeautifulSoup(response.text, 'html.parser')
                    print(soup)
                    title = soup.find('title')
                    amount = soup.find('div', 'highlights-value')
                    program = amount.find_next('div', 'highlights-value')
                    date = program.find_next('div', 'highlights-value')
                    term = date.find_next('div', 'highlights-value')
                    typeOfSupport = term.find_next('div', 'highlights-value')
                    strategies = typeOfSupport.find_next('div', 'highlights-value')
                    overview = soup.find('div', 'grant-overview')
                    aboutGranteeSite = soup.find('div', 'aboutgrantee-extra').find('a')
                    aboutGranteeAdresse = soup.find('div', 'aboutgrantee-address')
                    list_News = soup.find_all('div', 'aboutgrantee-info')

                    # on ajoute les variables dans une liste
                    items = []
                    items.append(title)
                    items.append(amount)
                    items.append(program)
                    items.append(date)
                    items.append(term)
                    items.append(typeOfSupport)
                    items.append(strategies)
                    items.append(overview)
                    items.append(aboutGranteeSite)
                    items.append(aboutGranteeAdresse)

                    news = getNews(list_News) #recupere les nouvelles
                    string = concatenationString(items)
                    outFile.write(string + news + '\n')
                    print(string + news + '\n')

                time.sleep(3)



if __name__ == "__main__":

    while True:

        print("1. Search")
        print("2. Extract data")
        print("3. Quit")
        answerUser = int(input("Choose the number of the desired option: "))


        if answerUser == 1:
            keyWord = (input("Enter the search keyword: "))
            searchLinks(keyWord)

        elif answerUser == 2:
            getInfos()

        else:
            break





