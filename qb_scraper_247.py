from bs4 import BeautifulSoup
import requests
import csv

URL = r'https://247sports.com/Season/{year}-Football/CompositeRecruitRankings/?InstitutionGroup=HighSchool&PositionGroup=QB'
player_list = []
MAX_YEAR = 2013
MIN_YEAR = 2000 
#print(URL)

#calculate stars based on https://247sports.com/college/appalachian-state/Article/247Sports-Rating-Explanation-81574/
def score_to_stars(score):
	double_score = float(score)
	if double_score >= .98:
		return '5'
	if double_score >= .90:
		return '4'
	if double_score >= .80:
		return '3'
	return '2' 
def get_recruits_for_year(year):
	players_for_year = []
	year_url = URL.replace("{year}", year)
	headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}
	r = requests.get(year_url, headers = headers)
	soup = BeautifulSoup(r.content, 'html.parser')
	players = soup.find_all("li", class_= "rankings-page__list-item")
	#skip the header element
	for player in players[1::]:
		name = player.find("a", class_="rankings-page__name-link").string
		score = player.find("span", class_="score").string
		
		stars = score_to_stars(score)
		player_data = name + "," + year + "," + stars + ',' + score
		players_for_year.append(player_data)
	return players_for_year

for i in range(MIN_YEAR, MAX_YEAR+1):
	player_list += get_recruits_for_year(str(i))

with open('./cfb_recruits.csv', 'w') as csvfile:
	fieldnames = ['Player', 'Year', 'Stars', '247_Rating']
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames, delimiter = ',')
	writer.writeheader()
	for player in player_list:
		values = player.split(',')
		player_dict = {}
		for i in range(0,4):
			player_dict[fieldnames[i]] = values[i]
		writer.writerow(player_dict)


