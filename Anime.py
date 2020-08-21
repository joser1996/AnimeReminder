
class AnimeScheduler:

	promptList = ["Print current Anime Shows", "View saved remiders", "Add a new reminder", "Delete a reminder", "Done"]
	
	def printPrompt(self):

		while True:

			for idx, prompt in enumerate(self.promptList):
				print(idx, ") ", prompt)
			inp = input("Enter a option: ")
			#do input command here
			if inp == '4':
				break


