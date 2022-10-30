from bs4 import BeautifulSoup
from requests import get
from pprint import pprint

#headers : for specifying a user agent so it doesn't seem as suspicious to the servers
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}

if __name__ == "__main__":
    url = "https://www.urbandictionary.com/browse.php?character=W&page=579"
    req = get(url, headers=headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    ul_section = soup.find('ul', attrs={'class':'mt-3 columns-2 md:columns-3'})
    words_a_li_ul = ul_section.find_all('a', attrs={'class':'py-1 block text-denim dark:text-white break-all hover:text-limon-lime hover:underline'})
    pprint(words_a_li_ul)