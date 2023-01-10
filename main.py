from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import sqlalchemy
import databases
import random
from sqlalchemy import create_engine, Column, Integer, String, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
bootstrap = Bootstrap(app)



#code block that creates the database. Make sure to pip install aiosqlite.
#Import sqlalchemy, databases and aiosqlite
DATABASE_URL = "sqlite:///./players.db"

database = databases.Database(DATABASE_URL)

metadata = sqlalchemy.MetaData()

players = sqlalchemy.Table(
        "players",
        metadata,
        sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
        sqlalchemy.Column("firstname", sqlalchemy.String),
        sqlalchemy.Column("lastname", sqlalchemy.String),
        sqlalchemy.Column("email", sqlalchemy.String),
        sqlalchemy.Column("target", sqlalchemy.String),
        sqlalchemy.Column("alive", sqlalchemy.Boolean),
        )
engine = sqlalchemy.create_engine(
        DATABASE_URL, connect_args={"check_same_thread": False}
        )
metadata.create_all(engine)
#end of the database creating block.

#Function that matches the players firstname with a target list that has made a copy of the firstname list.

def assign_players(players):
  # Make a copy of the list of players, so we can remove players from it as we assign them
  players_copy = players.copy()
  # Shuffle the list of players
  random.shuffle(players_copy)
  # Initialize an empty dictionary to store the assignments
  assignments = {}
  # Iterate over the list of players
  for player in players:
    # Find a player to assign to the current player
    assignee = None
    while assignee is None:
      # Get a random player from the list of players
      potential_assignee = random.choice(players_copy)
      # Make sure the potential assignee is not the current player
      if potential_assignee != player:
        assignee = potential_assignee
        # Remove the assignee from the list of players, so they can't be assigned again
        players_copy.remove(assignee)
    # Assign the current player to the assignee
    assignments[player] = assignee
  # Return the dictionary of assignments
  return assignments

# Test the function
print(assign_players(['Fanny', 'Bist', 'Jornt', 'Vince','Nancy', 'Noekie']))  # Should print {'Alice': 'Charlie', 'Bob': 'Alice', 'Charlie': 'Bob'}
assigned_dict=assign_players(['Fanny', 'Bist', 'Jornt', 'Vince','Nancy', 'Noekie', 'Alice', 'Bob', 'Charlie', 'Dave'])  # Should print a dictionary with the players randomly assigned to each other

#end of assignment function





#function that takes a dictionary and adds the values from the dictionary to the target column of 
#the players table in the database. Need some extra logic because this function can only run once.
#should use the dictionary from the assign_players function as input for this function

def add_assignments_to_db(assignments):
    Base = declarative_base()
    class Players(Base):
        __tablename__ = 'players'
        id = Column(Integer, primary_key=True)
        firstname = Column(String)
        target = Column(String)


    Session = sessionmaker(bind=engine)
    session = Session()

    for player, target in assignments.items():
        session.add(Players(target=target))
    
    session.commit()

# add_assignments_to_db(assigned_dict)

 



#function that drops the table in the database
def drop():
    players.drop(engine)

@app.route("/")
def homepage():
        return render_template("index.html") 

@app.route("/admin")
def adminpanel():
    return render_template("admin.html")

