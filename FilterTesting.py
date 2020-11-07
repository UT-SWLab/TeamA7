import main
'''This file is a playground to test queries and see if we get the expected responses.
In the final product, these will most likely be moved to main if this file is small. 
Each one of these helper functions prints out the JSON response after filters of the boardgamesobjects collection
'''

'''
Player Ranges
2-4 Players
4 Players or More

Year Published ranges
1940 -1970 
1971-2001
2001-Present
'''

def four_or_more_players_Filter():
    num = 3
    for doc1 in main.boardgameobjects.find({"Min_Players": {"$gt": num}}):
        print(doc1)
def two_to_four_plauers_Filter():
    num = 4
    for doc1 in main.boardgameobjects.find({"Min_Players": {"$lt": num}}):
        print(doc1)

def less_than_2hrs_Filter():
    time = 121
    for doc1 in main.boardgameobjects.find({"Max_Playtime": {"$lt": time}}):
        print(doc1)

def less_than_1hr_Filter():
    time = 61
    for doc1 in main.boardgameobjects.find({"Max_Playtime": {"$lt": time}}):
        print(doc1)
def year_1940_1970_Filter():
    date0 = 1939
    date1 = 1971
    for doc1 in main.boardgameobjects.find({"Year_Published": {"$gt": date0, "$lt": date1}}):
        print(doc1)

def year_1971_2001_Filter():
    date0 = 1970
    date1 = 2002
    for doc1 in main.boardgameobjects.find({"Year_Published": {"$gt": date0, "$lt": date1}}):
        print(doc1)

def year_2001_Present_Filter():
    date0 = 2000
    date1 = 2021
    for doc1 in main.boardgameobjects.find({"Year_Published": {"$gt": date0, "$lt": date1}}):
        print(doc1)



if __name__ == "__main__":
    year_2001_Present_Filter()
