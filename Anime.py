
import requests
import json
import pickle
import pathlib


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
				# print("MediaList ")
				# print(mediaList)
				# print("hasNext")
				# print(hasNext)
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
		print(self.animeList)


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

