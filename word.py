from json import dump, load
from bs4 import BeautifulSoup
import bs4
from requests import get
from tqdm import tqdm
from time import sleep

#letter
letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split()

#date changing
def Mdy_ymd(date:str) -> int:
    date = date.split(' ')
    months = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
    }
    year = int(date[-1])
    day = int(date[1])
    try:
        month = int(months[date[0].lower()])
    except Exception:
        month = 0

    # there can be funky years but no funky dates
    if day > 31 or day < 1:
        return 0
    if month < 1 or month > 12:
        return 0

    return ( (year * 10000) + (month * 100) + (day) ) #yyyyymmdd

#retrying requests: sometimes the page request mechanism fails so i had to make it foolproof
def req_page(url, attempts = 100):
    att = attempts #highest number of times it may work
    if not att:
        return 0
    while att:
        try:
            req = get(url, headers=headers)
            return req
        except Exception:
            att -=1
            print(f"\nWARNING: Request dropped, requests left: {att}, waiting for 5 secs")
            sleep(5)
            continue
    if not att:
        return 0

#headers : for specifying a user agent so it doesn't seem as suspicious to the servers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

#every def dataclass
from dataclasses import dataclass

@dataclass
class WordDefinition:
    """Class for sorting the elements of a definition div Tag of Urban Dictionary into a json"""
    originWord: str
    defTag: bs4.element.Tag
      
    def export(self) -> dict:
        #fetching the author's name seperately before clearing the hyperlink element for date collection
        self.authorLink = self.defTag.find('a', attrs={'class':'text-denim dark:text-fluorescent hover:text-limon-lime'})
        self.authorName = self.authorLink.text
        #clearing the authorName
        self.authorLink.clear()
        return {
            'originWord': self.originWord,
            'givenWord': self.defTag.find('h1', attrs={'class':'flex-1'}).text.replace("/r","/n"),
            'meaningWord': self.defTag.find('div', attrs={'class':'meaning mb-4'}).text.replace("/r","/n"),
            'exampleWord': self.defTag.find('div', attrs={'class':'example italic mb-4'}).text.replace("/r","/n"),
            'dateInfoWord': self.defTag.find('div', attrs={'class':'contributor font-bold'}).text.replace("/r","/n")[4:], #funny way but alright
            'authorName': self.authorName,
            'authorLink': self.authorLink['href']
        }

#updates the files
def export_json(word_list, fileName = 'testingTagData.json'):
    #writes all the definitions of the word on this page to the file
        with open(fileName, 'w+') as file:
                dump(word_list, file, indent=4)

if __name__ == "__main__":
    print("Script starting...")

    #all the definitions are stored here
    for letter in letters:
        definitions_result = []

        #load the index file
        with open('wordLinksByLetter.json','r') as file:
            wordIndex = load(file)[letter]
        
        #debugging line
        # pprint(wordIndex) #what happens is, you can only loop through dict.items() but not dict itself
        
        #pagination: with the word definition url
        for (k,v) in tqdm(
                wordIndex.items(), 
                unit= "Words", 
                desc= f"Progress of Letter: {letter.capitalize()}", 
                leave= False
            ):
            url = f"https://www.urbandictionary.com{v}" #the v is the wordLink

            req = req_page(url, attempts=10)
            if req == 0:
                continue

            soup = BeautifulSoup(req.content,'html.parser')
            pagination_div = soup.find_all("a", attrs={"class":"px-3 py-1 rounded-full hover:bg-denim hover:text-white text-light-charcoal"})

            if pagination_div == []:
                last_page_number = 1
            else:
                last_page_number = int(pagination_div[1]['href'].split('=')[-1])

            for i in range(1, last_page_number+1):
                url = f"https://www.urbandictionary.com{v}&page={i}" #url of one page of a wor meaning
                req = req_page(url)
                soup = BeautifulSoup(req.content,'html.parser')

                #pagination: find the last page

                #finding all the definition for the def for each page
                #just find all divs for class: definition bg-white mb-4 shadow-light dark:bg-yankees dark:text-white rounded-md overflow-hidden
                definitions = soup.find_all('div', attrs={'class':'definition bg-white mb-4 shadow-light dark:bg-yankees dark:text-white rounded-md overflow-hidden'})
                
                #for the first element of the definitions
                #I typed camelCase because these are going into a dict which will go into a json

                for definition in definitions:
                    word = WordDefinition(
                        k,
                        definition,
                    )
                    # print(word.export())
                    definitions_result.append(word.export())

        export_json(definitions_result, fileName=f"data/{letter}.json")