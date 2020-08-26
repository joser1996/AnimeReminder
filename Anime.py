
import requests
import json
import pickle
import pathlib
from datetime import date, datetime

class AnimeScheduler:

	promptList = ["Print current Anime Shows", "View saved remiders", "Add a new reminder", "Delete a reminder", "Done"]
	currentAnime = []

	url = "https://graphql.anilist.co"
	query = '''
	query ($page: Int, $perPage: Int) {
		Page (page: $page, perPage: $perPage) {
			pageInfo {
				total
				currentPage
				lastPage
				hasNextPage
				perPage
			}
		
			media (season: SUMMER, seasonYear: 2020, type: ANIME){
				id
				title {
					romaji
					native
					english
				}
				nextAiringEpisode {
					airingAt
					episode
				}
			}
		}
	}
	'''

	variables = {
		'page': 1,
		'perPage': 20
	}
	def __init__(self):
		#initialize current anime list
		path = pathlib.Path("Summer.pkl")
		if path.exists():
			#load the fle
			print("Loading the file.")
			with open("Summer.pkl", "rb") as fp:
				self.animeList = pickle.load(fp)
		else:
			#make new file
			print("Making new file")
			tempList = []
			while True:
				response = requests.post(self.url, json={'query': self.query, 'variables': self.variables})
				pasteBin = response.text
				pyObject = json.loads(pasteBin)
				mediaList = pyObject['data']['Page']['media']
				hasNext = pyObject['data']['Page']['pageInfo']['hasNextPage']
				tempList = tempList + mediaList
				if hasNext == False :
					break

				self.variables['page'] = self.variables['page'] + 1
			with open("Summer.pkl", "wb") as fp:
				pickle.dump(tempList, fp)
			self.animeList = tempList



	def printCurrentAnime(self):
		#check to see if I have cached list; else request new list
		print("Printing Anime.")
		border = '''
		#############################################################################
		#############################################################################
		'''
		buff = []
		count = 0
		for a in self.animeList:

			if a['nextAiringEpisode'] == None:
				continue
			if count == 3:
				count = 0
				#print out buffer
				for idx, item in enumerate(buff):
					print("Anime: %s, Time: %s" %(item[0], item[1]), end='')
					print("   ", end='')
				print(border, flush=True)
				buff = []
			else:
				title = a['title']['romaji']
				time = datetime.fromtimestamp(a['nextAiringEpisode']['airingAt'])
				buff.append((title, time))
				count = count + 1



		


	def printPrompt(self):

		while True:

			for idx, prompt in enumerate(self.promptList):
				print(idx, ") ", prompt)
			inp = input("Enter a option: ")
			#do input command here
			if inp == '0':
				self.printCurrentAnime()
			elif inp == '1':
				self.printReminders()
			elif inp == '2':
				self.addReminder()
			elif inp == '3':
				self.deleteReminder()
			elif inp == '4':
				break
			else:
				print("Invalid Input; please try again")

