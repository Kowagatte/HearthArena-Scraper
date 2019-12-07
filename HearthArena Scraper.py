from bs4 import BeautifulSoup
import requests
import json

print('--== [ Requesting Info from HearthStoneArena ] ==--')
page = requests.get("https://www.heartharena.com/tierlist")
print('DONE')

print('--== [ Parsing HearthStoneArena HTML ] ==--')
soup = BeautifulSoup(page.text, 'html.parser')
print('DONE')

def downloadHearthStoneArenaPage():
    file = open("hearthstonearena.html", mode= 'w+', encoding='utf-8')
    file.write(page.text)
    file.close()

raw_cards = []
cards = []

def compileCards():
    print('--== [ Finding Cards ] ==--')
    category = soup.find_all("ol", {"class":"cards"})
    print('DONE')
    print('--== [ Adding Raw Cards ] ==--')
    count = 0
    for element in category:
        raw_cards.extend(element.findAll('li')[0:])
        count += 1
        print(round(((count/len(category)) * 100), 3), "percent complete!")
    print("DONE")
    
compileCards()

def cleanCards():
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
    
cleanCards()

def downloadCardData():
    print('--== [ Writing cards to file ] ==--')
    file = open("arenaCards.json", mode='w+', encoding='utf-8')
    file.write(json.dumps(cards))
    file.close()
    print('DONE')

downloadCardData()

