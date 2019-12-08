from bs4 import BeautifulSoup
import requests
import json
import pymongo

client = pymongo.MongoClient("code")
db = client.HearthArena

classes = [{'name':"druid", 'db': db.druid, 'cards': []},
    {'name':"hunter", 'db': db.hunter, 'cards': []},
    {'name':"mage", 'db': db.mage, 'cards': []},
    {'name':"paladin", 'db': db.paladin, 'cards': []},
    {'name':"priest", 'db': db.priest, 'cards': []},
    {'name':"rogue", 'db': db.rogue, 'cards': []},
    {'name':"shaman", 'db': db.shaman, 'cards': []},
    {'name':"warlock", 'db': db.warlock, 'cards': []},
    {'name':"warrior", 'db': db.warrior, 'cards': []}]

def requestHearthArenaData():
    print('--== [ Requesting Info from HearthStoneArena ] ==--')
    page = requests.get("https://www.heartharena.com/tierlist")
    print('DONE')
    return page

def parseHTML(page):
    print('--== [ Parsing HearthStoneArena HTML ] ==--')
    soup = BeautifulSoup(page.text, 'html.parser')
    print('DONE')
    return soup

def getClassHTML(haHTML, hclass):
    print('--== [ Getting', hclass, ' html ] ==--')
    html = haHTML.find("section", {"id":hclass})
    print('DONE')
    return html
    

def compileRawCards(haHTML):
    raw_cards = []
    print('--== [ Finding Cards ] ==--')
    category = haHTML.find_all("ol", {"class":"cards"})
    print('DONE')
    print('--== [ Adding Raw Cards ] ==--')
    count = 0
    for element in category:
        raw_cards.extend(element.findAll('li')[0:])
        count += 1
        print(round(((count/len(category)) * 100), 3), "percent complete!")
    print("DONE")
    return raw_cards

def cleanCards(raw_cards):
    cards = []
    print('--== [ Cleaning Up Cards ] ==--')
    count = 0
    for raw_card in raw_cards:
        if not raw_card.find("dl").get("class")[0] == "empty":
            card = {}
            card["name"] = raw_card.text.replace("\n", "|").split("|")[0]
            card["score"] = raw_card.find("dl").find("dd").text
            card["class"] = raw_card.find("dl").find("dt").get("class")[0]
            card["rarity"] = raw_card.find("dl").find("dt").get("class")[1]
            cards.append(card)
        count += 1
        print(round(((count/len(raw_cards)) * 100), 3), "percent complete!")
    print("DONE")
    return cards

def downloadCardData(cards):
    print('--== [ Writing cards to file ] ==--')
    file = open("arenaCards.json", mode='w+', encoding='utf-8')
    file.write(json.dumps(cards))
    file.close()
    print('DONE')

def downloadHearthStoneArenaPage():
    file = open("hearthstonearena.html", mode= 'w+', encoding='utf-8')
    file.write(page.text)
    file.close()

def doesDataExist():
    try:                                                                                                                                        
        file = open("arenaCards.json")
        file.close()
        return True
    except IOError:
        return False

def compileCardsByClass():
    page = requestHearthArenaData()
    html = parseHTML(page)
    for hclass in classes:
        hclass['cards'] = cleanCards(compileRawCards(getClassHTML(html, hclass['name'])))

def uploadCardsToDatabase():
    print('--== [ Writing cards to database ] ==--')
    for hclass in classes:
        print('-= [ Saving', hclass['name'], 'cards ] =-')
        count = 0
        for card in hclass['cards']:
            hclass['db'].insert(card)
            count += 1
            print(round(((count/len(hclass['cards'])) * 100), 3), "percent complete!")
        print('DONE')
    print('DONE')
    count = 0


compileCardsByClass()
uploadCardsToDatabase()
