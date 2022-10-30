from json import dumps
from bs4 import BeautifulSoup
from requests import get
from tqdm import tqdm
from pprint import pprint

#headers : for specifying a user agent so it doesn't seem as suspicious to the servers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

#list of letters
letters = "a b c d e f g h i j k l m n o p q r s t u v w x y z".split(" ")

#page-number-info: key-value pair info of page numbers that reside on the index page
page_num_info = {} #todo to be pickled/jsoned

if __name__ == "__main__":

    #url : to be for-looped
    for letter in tqdm(letters):
        url = f"https://www.urbandictionary.com/browse.php?character={letter.capitalize()}"
        req = get(url, headers=headers)
        soup = BeautifulSoup(req.content,'html.parser')
        pagination_div = soup.find_all("a", attrs={"class":"px-3 py-1 rounded-full hover:bg-denim hover:text-white text-light-charcoal"})
        last_page_number = int(pagination_div[1]['href'][29:])
        page_num_info[letter.capitalize()] = last_page_number
    
    #checking if things are alright
    pprint(page_num_info)

    #pickle that numbers
    with open("letterPageNumbers.json", "w+") as file:
        file.write(dumps(page_num_info, sort_keys=True, indent=4))
        print("! Writing JSON file Complete")