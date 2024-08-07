# Django App README

# Foreword

Hi, my name is Dmytro and I am a backend developer from Ukraine. 🇺🇦
I am just starting my way in the IT sphere and I am writing this 
project for educational purposes 🎓📕. A lot of work has been done 
in this project, and I have not regretted a drop of these efforts. 

When creating this API, I wanted to implement a fairly simple 
dice game. It is called "Liars Dice". The rules are given below. 🎲

P. S. I am also not against cooperation to create a frontend for the game.

# Rules

RULES:

The object of the game is to outbluff your opponents.
Liar’s dice can be played by 2 or more players.

Setup:
Each player starts with five dice.

At the onset of each round, every player 
reshuffles their dice. Each player secretly 
looks at their dice but keeps them hidden 
from their opponents.

Beginning with the start player and going 
clockwise, each player calls out a quantity 
of a certain dice face value that have 
supposedly been rolled by all players collectively.
For example, “four 3’s” means that you claim 
there are at least four dice with a face value 
of 3 amongst all the players. Each player 
then subsequently calls out a higher hand 
than the previous. Either the number of 
identical dice must be higher and/or the face 
value must be larger. The number of identical 
dice cannot be lower.

For example:
- Two 3’s is greater than two 2’s.
- Three 3’s is greater than two 3’s.
- Four 2’s is greater than three 3’s.
- Five 4’s is greater than four 2’s.

1’s are wild and can represent any face value in a call.

Instead of calling out a higher hand on your turn, 
you can call a bluff on the previous player by 
saying “liar” or call that previous bid was correct 
by saying "spot on". 

When this is done all the dice are revealed.
- If you said "liar" and there are not enough 
  dice amongst all the players that match the claim, 
  the challenged player loses that round. 
  But if there are enough dice to match the claim, 
  then the challenger loses the round.
- If you said "spot on" and the number of dice and 
  the denomination figure exactly match, then 
  everyone except the player himself loses one cube. 
  Otherwise, the player himself loses two cubes.


## Setup Instructions

1. **Configure Settings**

   Before starting the application, you need to set up your own configurations. Update the following settings in your Django project:
   - **Database**: Configure your database settings in `settings.py`.
   - **Redis**: Set up Redis by updating the relevant settings in `settings.py`.
   - **Channels Layer**: Configure the Channels layer in `settings.py`.
   - **Celery**: Configure Celery settings in `settings.py`.

2. **Install Dependencies**

   Install the required libraries by running:
        "pip install -r requirements.txt"

3. **Start Redis Server**

    Make sure Redis server is running. You can start it with:
        "wsl"
        "redis-server"

4. **Apply Database Migrations**

    Create the necessary database migrations by running:
        "python manage.py makemigrations"

    Apply the migrations to the database:
        "python manage.py migrate"

5. **Create Superuser**

    For easier management of the Django admin interface, create a superuser account:
        "python manage.py createsuperuser"

6. **Run the Django Development Server**

    Start the Django development server:
        "python manage.py runserver"

7. **Run Celery Worker**

    If you're using Windows, start the Celery worker with the following command:
        "celery -A config worker --loglevel=info -P eventlet"