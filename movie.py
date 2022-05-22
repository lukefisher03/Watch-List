"""
This is a completely random barebones python cli app that uses .txt files as a backend to store and manage what movies
you've got on your wishlist. Just for fun it's got a snarky attitude and tells you Chuck Norris jokes when you leave.
Percieve it any way you'd like. 

"""
import random
from datetime import datetime
import requests

#initalize our lists holding watched movies
unwatched = []

def populateMovies(display=False):
    if display:
        print("\n\nYour Movie List")
    with open("unwatched.txt", "r") as f:
        #skip the header and spacer
        next(f)
        next(f)
        empty = True if (len(unwatched) == 0) else False
        for i,line in enumerate(f):
            if empty: 
                unwatched.append(line.strip())
            if display:
                print(str(i+1)+".",line)
        
    if len(unwatched) == 0:
        print("There are no movies in queue!")
        return

def rewriteMovies(populate=False):
    if populate:
        populateMovies(display=False)

    with open("unwatched.txt", "w") as f:
        f.write("MOVIE LIST\n")
        f.write("---------------------------------------\n")
        for movie in unwatched:
            f.write(movie + "\n")

def addMovie():
    titles = input("What is the movie title: ")
    inputted_movies = titles.split(",")
    with open("unwatched.txt", "a") as f:
        for movie in inputted_movies:
            f.write(movie.strip() + "\n")
    print(f"Added movie[s]: {titles}")

def removeMovie():
    populateMovies(display=True)
    if len(unwatched) == 0:
        print("There are no movies in queue!")
        return
    index = int(input("Please input the index of the movie you'd like to remove: ".strip()))
    removed_movie = unwatched[index-1]
    unwatched.pop(index-1)
    rewriteMovies()
    print(f"Removed {removed_movie}")

def displayWatched():
    print("\n\n")
    with open("watched.txt", "r") as f:
        for line in f:
            print(line)

def chooseMovie(moveTitle=True) -> str or None:
    #read all movies and add them to a list, select a random movie to watch.
    populateMovies(display=False)
    if len(unwatched) == 0:
        print("There are no movies in queue!")
        return
    rand_index = random.randrange(0, len(unwatched))
    random_movie = unwatched[rand_index]
    unwatched.pop(rand_index)
    #remove the "watched" movie from the list
    if moveTitle:
        with open("unwatched.txt", "w") as f:
            f.write("MOVIE LIST\n")
            f.write("---------------------------------------\n")
            for movie in unwatched:
                f.write(movie + "\n")
    
    #write to watched movies
    with open("watched.txt", "a") as f:
        now = datetime.now()
        current_time = now.strftime("%m/%d/%Y")
        line = random_movie.ljust(40)
        f.write(f'{line}{current_time}\n')
    print(f"Movie selected: {random_movie}")
    return random_movie

#when you're lazy
print("Welcome to your favorite movie manager!\n")
print("Please select an option: ")
print("1. Select Random Movie (Remove from watched list)")
print("2. Select Random Movie (Keep on watched list)")
print("3. List unwatched movies")
print("4. List watched movies")
print("5. Add movie")
print("6. Remove movie")

user_choice = int(input("\n\n:").strip())

#definitely could've used the fancy new match case statement. But oh well
if user_choice == 1:
    chooseMovie(moveTitle=True)
elif user_choice == 2:
    chooseMovie(moveTitle=False)
elif user_choice == 3:
    populateMovies(display=True)
elif user_choice == 4:
    displayWatched()
elif user_choice == 5:
    addMovie()
elif user_choice == 6:
    removeMovie()
else:
    print("You did not enter valid input!")


print("\n\nHasta la vista, baby!")
req = requests.get("https://api.chucknorris.io/jokes/random")
response = req.json()
print(f"A chuck norris joke for ya on the way out!\n\t{response['value']}")