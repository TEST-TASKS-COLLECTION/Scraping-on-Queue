import requests
from bs4 import BeautifulSoup as bs

import time

def count_words(url, cookie):
    
    print(f"Counting words at: {url}")
    
    time.sleep(2)
    
    start = time.time()
    
    r = requests.get(url)
    
    soup = bs(r.content, "html.parser")
    
    para = " ".join([p.text for p in soup.find_all("p")])
    
    word_count = {}
    word_count = {p.lower().strip(): word_count.get(p.lower().strip(), 0) + 1 for p in para.split()}
    
    end = time.time()
    
    time_elapsed = end - start
    
    print(word_count)
    print(f"Total words: {len(word_count)}")  
    print(f"Time elapsed: {time_elapsed}")
    
    # with open(f"data/task.txt", "w") as f:
    #     f.write(f"Total words is: {len(word_count)}")
    
    return len(word_count)


