# Chris12902
# 26 July 2020
# Catalog Cleaner: Searches through 24 pages of catalog clothes and removes all duplicate items, then provides a list of all original IDs.

from urllib.request import Request, urlopen
import re
thumbnails = []
ids = []
total_ids = 0
total_copies = 0
pages_to_search = 24

url = "https://search.roblox.com/catalog/json?Category=3"
def buildUrl(url):
    ItemTypes = int(input("Which clothes would you like to search for?\n1. shirts\n2. pants\n3. t-shirts\n4. all\nInput a number: "))
    if ItemTypes == 1:
        url = url + "&Subcategory=12"
    elif ItemTypes == 2:
        url = url + "&Subcategory=14"
    elif ItemTypes == 3:
        url = url + "&Subcategory=13"
    else:
        url = url + "&Subcategory=3"
    SortType = int(input("Which sort type would you like to use?\n1. relevance\n2. best selling\n3. most favorited\n4. recently updated\n5. price (low to high)\n6. price (high to low)\nInput a number: "))
    if SortType == 2:
        url = url + "&SortType=2"
    elif SortType == 3:
        url = url + "&SortType=1"
    elif SortType == 4:
        url = url + "&SortType=3"
    elif SortType == 5:
        url = url + "&SortType=4"
    elif SortType == 6:
        url = url + "&SortType=5"
    if SortType == 2 or SortType == 3:
        SortType = int(input("\n1. all time\n2. past week\n3. past day\nInput a number: "))
        if SortType == 1:
            url = url + "&SortAggregation=5"
        elif SortType == 2:
            url = url + "&SortAggregation=3"
        else:
            url = url + "&SortAggregation=1"
    Keyword = input("Enter the phrase you would like to search for: ").replace("&","%26").replace(" ","%20")
    url = url + "&Keyword="+Keyword
    return url
def PageSearch(pagenumber, url):
    global total_copies, total_ids, ids, thumbnails
    req = Request(url + "&PageNumber="+str(pagenumber))
    webpage = str(urlopen(req).read().decode('utf-8').encode('unicode-escape'))
    # gets item IDs, which is important for determining item age.
    pattern = re.compile('"AssetId":(.+?),')
    found_ids = re.findall(pattern,webpage)
    total_ids = total_ids + len(found_ids)
    # Gets thumbnails, which is important for removing duplicates.
    pattern = re.compile(',"ThumbnailUrl":"(.+?)",')
    found_thumbs = re.findall(pattern,webpage)
    for i in range(0,len(found_thumbs)):
        try:
            for e in range(i+1,len(found_thumbs)):
                if found_thumbs[i] == found_thumbs[e]:
                    total_copies = total_copies + 1
                    if found_ids[i] > found_ids[e]:
                        found_ids.pop(e)
                        found_thumbs.pop(e)
                    else:
                        found_ids.pop(i)
                        found_thumbs.pop(i)
        except:
            continue
    ids = ids + found_ids
    thumbnails = thumbnails + found_thumbs
url = buildUrl(url)
print("Searching...\n")
for i in range(1,pages_to_search+1):
    print("Searching through page "+str(i))
    PageSearch(i, url)
print("\n")
for i in range(0,len(thumbnails)):
    try:
        for e in range(i+1,len(thumbnails)):
            if thumbnails[i] == thumbnails[e]:
                total_copies = total_copies + 1
                if ids[i] > ids[e]:
                    ids.pop(e)
                    thumbnails.pop(e)
                else:
                    ids.pop(i)
                    thumbnails.pop(i)
    except:
        continue
print("Completed scan (searched through "+str(total_ids)+" items on "+str(pages_to_search)+" pages, found "+str(total_copies)+" stolen clothes ("+str((total_copies/total_ids)*100)+"% copied)")
print("Clean IDs:")
f= open("Catalog Cleaner results.txt","w+")
for i in ids:
    f.write("https://www.roblox.com/catalog/"+str(i)+"\n")
f.close()
PrintResults = input("These results have been saved to a .txt file titled \"Catalog Cleaner results\".\nWould you like to print them in the console? (y/n) ")
if 'y' in PrintResults:
    for i in ids:
        print("https://www.roblox.com/catalog/"+str(i))
