from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import sqlalchemy
import databases


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



@app.route("/")
def homepage():
        return render_template("index.html") 

