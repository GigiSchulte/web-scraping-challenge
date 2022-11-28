#imports
from splinter import Browser
from bs4 import BeautifulSoup as soup
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

#scrape all function
def scrape_all():
    #splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = scrape_news(browser) #get info from page

    marsData = {
        "newsTitle": news_title,
        "newsParagraph": news_paragraph,
        "featuredImage": scrape_feature_image(browser),
        "facts": scrape_facts_page(browser),
        "hemispheres": scrape_hemispheres(browser),
        "lastUpdated": dt.datetime.now()
    }

    browser.quit()

    return marsData #show output

#scrape the mars news page
def scrape_news(browser):
    #visit site
    url = 'https://redplanetscience.com/' 
    browser.visit(url)

    #page load delay
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #convert to soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')
    slide_elem = news_soup.select_one('div.list_text')

    news_title = slide_elem.find('div', class_='content_title').get_text() #grab title
    news_p = slide_elem.find('div', class_='article_teaser_body').get_text() #grab paragrach for headline
    return news_title, news_p

#scrape through the featured image page
def scrape_feature_image(browser):
    #visit url
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    #find and click image button
    full_image_link = browser.find_by_tag('button')[1]
    full_image_link.click()

    #parse html
    html = browser.html
    img_soup = soup(html, 'html.parser')

    img_url_rel = img_soup.find('img', class_='fancybox-image').get('src') #grab image

    img_url = f'https://spaceimages-mars.com/{img_url_rel}' #use base to create absolute url

    return img_url


#scrape through the facts page
def scrape_facts_page(browser):
    #visit url
    url = 'https://galaxyfacts-mars.com/'
    browser.visit(url)

     #parse html
    html = browser.html
    fact_soup = soup(html, 'html.parser')

    #find location
    factsLocation = fact_soup.find('div', class_="diagram mt-4")
    factTable = factsLocation.find('table') #grabs html code for fact table

    #empty string
    facts = ""

    #addt to empty string
    facts += str(factTable)
    return facts


#scrape through the hemispheres pages
def scrape_hemispheres(browser):
    #visit url
    url = "https://marshemispheres.com/"
    browser.visit(url)

    hemisphere_image_urls = [] #list to hold images and titles

    #create loop
    for i in range(4):
        #holds hemisphers info
        hemisphereInfo = {}
    
        #loop through each pic base on a -> product-item -> img
        browser.find_by_css('a.product-item img')[i].click()
    
        #find sample image tag and bring back href for each image
        sample = browser.links.find_by_text('Sample').first
        hemisphereInfo["img_url"]=sample['href']
    
        #get hemi titles
        hemisphereInfo['title'] = browser.find_by_css('h2.title').text
    
        #append hemis to object list
        hemisphere_image_urls.append(hemisphereInfo)
    
        browser.back()

    return hemisphere_image_urls


#set up as a flask app
if __name__=="__main__":
    print(scrape_all())