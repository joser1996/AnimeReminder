
import requests




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
		'perPage': 10
	}
	#__init__(self):
		#initialize current anime list

	def printCurrentAnime(self):
		#check to see if I have cached list; else request new list
		response = requests.post(self.url, json={'query': self.query, 'variables': self.variables})
		pasteBin = response.text
		print("All of the shit is: %s"%pasteBin)

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

