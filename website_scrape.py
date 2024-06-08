import requests
from bs4 import BeautifulSoup
import re
import traceback

def scrape_website(site):
    linkedin = []
    token_limit = 16385
    sites = []
    text_content = ""
    metadata = {}  # Dictionary to store metadata
    print("finding for site ",site )
    try:
        hdr = {'User-Agent': 'Mozilla/5.0'}
        req = requests.get(site, headers=hdr)
        soup = BeautifulSoup(req.content, 'html.parser')
        
        # Extract metadata
        title = soup.title.string if soup.title else ""
        meta_tags = soup.find_all('meta')
        description = ""
        keywords = ""
        text_content += f"title :{title} \n"
        for tag in meta_tags:
            if tag.get('name') == 'description':
                description = tag.get('content')
                text_content += f"description : {description}"

            elif tag.get('name') == 'keywords':
                keywords = tag.get('content')
                text_content += f"keywords : {keywords}"

        # Store metadata in dictionary
        links = soup.body.find_all('a')
        text_content += soup.get_text()
        pattern = r'[^a-zA-Z0-9\s]'
        text_content = re.sub(pattern, '', text_content)
        urls = [link.get('href') for link in links if link.get('href') is not None]
        done = 0    

        for link in urls:
            if "linkedin" in link:
                linkedin.append(link)
        
            if link.startswith('/'):
                link = site.replace('/','') + link
            if site in link and link not in sites:
                print("Going through ", link , " Now")  
                done += 1
                print("Done with ",done*100/len(urls),'%')
                try:
                    sites.append(link)
                    req = requests.get(link, headers=hdr)
                    soup = BeautifulSoup(req.content, 'html.parser')
                    links = soup.body.find_all('a') 
                    if len(text_content)/4 > token_limit:
                        print("Token Limit exceeds, breaking loop now")
                        break
                    links = [link.get("href") for link in soup.find_all('a') if link.get("href")]  # Extract all href attributes from <a> tags
                    links_text = ' '.join(links)  # Concatenate all links into a single string

                    text_content += re.sub(r'\s+', ' ', soup.get_text() + links_text)
                    text_content = re.sub(pattern, '', text_content)
                except Exception as e:
                    traceback.print_exc() 
                
    except Exception as e:
        print(e)
        # st.error(f"Error while processing the website: {e}")
    return linkedin, text_content[:token_limit*4]

