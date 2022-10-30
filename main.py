from json import dumps, load
from bs4 import BeautifulSoup
from requests import get
from tqdm import trange
from pprint import pprint
from playsound import playsound
from time import sleep

#headers : for specifying a user agent so it doesn't seem as suspicious to the servers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

#list of letters
letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")

#page-number-info: key-value pair info of page numbers that reside on the index page
with open('letterPageNumbers.json', 'r') as file:
    page_num_info = load(file)

#word_list: list of words according to the letters
word_list = {}

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
            sleep(20)
            att -=1
            continue

if __name__ == "__main__":
    # url : to be for-looped
    for letter in letters:
        letter_words = {}
        for i in trange(1,page_num_info[letter.capitalize()] + 1):
            if i%300 == 0:
                sleep(10)
            elif i%100 == 0:
                sleep(5)
            url = f"https://www.urbandictionary.com/browse.php?character={letter.capitalize()}&page={i}"
            req = req_page(url)
            if req == 0: #i don't want some failed fetching job ruin my program
                continue
            soup = BeautifulSoup(req.content,'html.parser')
            ul_section = soup.find('ul', attrs={'class':'mt-3 columns-2 md:columns-3'})
            words_a_li_ul = ul_section.find_all("a", attrs={"class":"py-1 block text-denim dark:text-white break-all hover:text-limon-lime hover:underline"})
            # letter_words += {a.text:a['href'] for a in words_a_li_ul}
            letter_words.update({a.text:a['href'] for a in words_a_li_ul})
        word_list[letter] = letter_words
        pprint(letter_words)

    # checking if things are alright
    # pprint(page_num_info['A'])
    pprint(word_list)
    
    #writing the word list into json
    with open('wordLinksByLetter.json', 'w+') as file:
        file.write(dumps(word_list, indent=4, sort_keys=True))
    
    #playsound: play songs as an inication of completion
    playsound('valley.mp3')