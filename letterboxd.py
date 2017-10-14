import requests, csv, time, sys, re, codecs, string
from bs4 import BeautifulSoup

def imdb_id_from_lb_uri(lb_uri):
    lb_html = requests.get(lb_uri)
    if 'http://www.imdb.com/title/' in lb_html.text:
        lb_soup = BeautifulSoup(lb_html.text, 'html.parser') 
        imdb_id = lb_soup.find_all(href=re.compile("imdb"))[0].get('href').replace('/maindetails','').replace('http://www.imdb.com/title/','')
        # imdb_url = lb_soup.find_all("a", class_="micro-button track-event") # gets all external URLs for film
    else:
        imdb_id = 'none'
    return imdb_id
    
def imdb_url_from_imdb_id(imdb_id):
    imdb_url = 'http://www.imdb.com/title/' + imdb_id + '/'
    return imdb_url
    
file = 'lb_ratings.csv'
output = [['position','const','created','modified','description','Title','Title type','Directors','You rated','IMDb Rating','Runtime (mins)','Year','Genres','Num. Votes','Release Date (month/day/year)','URL']]
errors = []
position = 0

with open(file) as letterboxd_csv:
    reader = csv.DictReader(letterboxd_csv)
    for row in reader:
        if len(row['Letterboxd URI']) > 28:
            print(row['Letterboxd URI'])
            imdb_id = imdb_id_from_lb_uri(row['Letterboxd URI'])
            if imdb_id != 'none':
                position = position + 1
                imdb_url = imdb_url_from_imdb_id(imdb_id)
                new_row = [position, imdb_id, '', '', '', row['Name'], 'Feature Film', '', float(row['Rating']) * 2, '', '', row['Year'], '', '', '', imdb_url]
                # to do: convert date(s)
                print(new_row)
                output += [new_row]
            else:
                errors += [row]
                
            time.sleep(1)

print('The following rows were not converted:')
print(errors)
        
with open('ratings.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)   
