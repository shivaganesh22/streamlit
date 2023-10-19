import streamlit as st
from bs4 import BeautifulSoup
import time
import requests
from pytube import YouTube
import re

def youtube(link):
    yt = YouTube(link)
    n=yt.streams.all()
    for i in n:
        st.write("Type : ",i.mime_type,"Resolution :",i.resolution,"Size (mb)",i.filesize_mb)
        st.link_button("Watch or Download",i.url)
    return n[1].url
def mdisk(url):
    header = {
        'Accept': '*/*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://mdisk.me/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
    	 }
    
    inp = url 
    fxl = inp.split("/")
    cid = fxl[-1]

    URL = f'https://diskuploader.entertainvideo.com/v1/file/cdnurl?param={cid}'
    res = requests.get(url=URL, headers=header).json()
    return res['download'] + '\n\n' + res['source']


###################################################################
def gdrive(url):
    match = re.search(r'([\w-]{25,})', url)
    return f"https://drive.google.com/uc?id={match.group(1)}&export=download"



def mdiskpro(url):

    client = cloudscraper.create_scraper(allow_brotli=False)

    DOMAIN = "https://mdisk.pro"

    ref = "https://m.meclipstudy.in/"

    h = {"referer": ref}

    resp = client.get(url, headers=h)

    soup = BeautifulSoup(resp.content, "html.parser")

    inputs = soup.find_all("input")

    data = {input.get('name'): input.get('value') for input in inputs}

    h = {"x-requested-with": "XMLHttpRequest"}

    time.sleep(8)

    r = client.post(f"{DOMAIN}/links/go", data=data, headers=h)

    try:

        return r.json()['url']

    except:

        return "Something went wrong :("


def shareus(url):

    token = url.split("=")[-1]

    bypassed_url = "https://us-central1-my-apps-server.cloudfunctions.net/r?shortid=" + token

    response = requests.get(bypassed_url).text

    return response
#Gplinks

def GP_links(url: str):
    try:
        # Since only cloudscraper can bypass Cloudflare bot detection
        client = cloudscraper.create_scraper(allow_brotli=False)

        # Visitor ID provided by GPLinks that stores the session
        vid = client.get(url, allow_redirects=False).headers["Location"].split("=")[-1]

        # Convince GPLink that visitor has already visited the 3rd ads page and clicked continue
        client.post(url="https://gplinks.in/track/conversion.php",
                    data={"update": True, "visitor_id": vid, "status": 3})

        # Request to get the final GPLink verification page
        go_url = f"{url}/?{vid}"
        response = client.get(go_url, allow_redirects=False)
        soup = BeautifulSoup(response.content, "html.parser")

        data = {}

        # Find the final GPLink verification page link in the webpage
        go_link_form = soup.find_all(id="go-link")
        for form_elem in go_link_form:
            if form_elem is not None:
                inputs = form_elem.find_all("input")
                for input_elem in inputs:
                    data[input_elem.get('name')] = input_elem.get('value')

        # Final request to get the actual bypassed link
        bypassed_url = client.post(url="https://gplinks.co/links/go",
                                   data=data,
                                   headers={"x-requested-with": "XMLHttpRequest"}
                                   ).json()["url"]
        return bypassed_url
    except Exception as ex:
        print(ex)
        return None



# Streamlit app

st.title("Link Converter")

# Select conversion method

conversion_method = st.selectbox("Select conversion method", ["Youtube","Gdrive","Mdisk Pro", "Shareus", "URL Shortx", "Mdisk.me","GP links"])

# Input URL

url = st.text_input("Enter the URL")

# Convert button

if st.button("Convert"):

    if url:
        if conversion_method=="Gdrive":
            converted_url=gdrive(url)
        elif conversion_method=="Youtube":
            converted_url=youtube(url)
        elif conversion_method == "Mdisk Pro":
            converted_url = mdiskpro(url)

        elif conversion_method == "Shareus":

            converted_url = shareus(url)

        elif conversion_method == "Mdisk.me":
            converted_url = mdisk(url)
        elif conversion_method == "GP links":
            converted_url = GP_links(url)
        st.success("Converted Link:")

        st.markdown(f"[Link 1 ]({converted_url})")
        st.video(converted_url)
        

    else:

        st.warning("Please enter a URL")


