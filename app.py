import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config.Config")

db = SQLAlchemy(app)
migrate = Migrate(app=app, db=db)


class Director(db.Model):
    __tablename__ = "Directors"
    DirectorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    BirthYear = db.Column(db.Integer)
    Nationality = db.Column(db.String)


class Actor(db.Model):
    __tablename__ = "Actors"
    ActorID = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String, nullable=False)
    BirthYear = db.Column(db.Integer)
    Nationality = db.Column(db.String)


class Movie(db.Model):
    __tablename__ = "Movies"
    MovieID = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String, nullable=False)
    ReleaseYear = db.Column(db.Integer)
    Genre = db.Column(db.String)
    Rating = db.Column(db.Float)
    DirectorID = db.Column(db.Integer, db.ForeignKey("Directors.DirectorID"))


class MovieActor(db.Model):
    __tablename__ = "MovieActor"
    MovieID = db.Column(db.Integer, db.ForeignKey("Movies.MovieID"), primary_key=True)
    ActorID = db.Column(db.Integer, db.ForeignKey("Actors.ActorID"), primary_key=True)


@app.route("/load-data", methods=["POST"])
def load_data_endpoint():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if file and (file.filename.endswith(".csv") or file.filename.endswith(".xlsx")):
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        for index, row in df.iterrows():
            director_name = row.get("director", None)
            if director_name and isinstance(director_name, str):
                director = Director.query.filter_by(Name=director_name).first()
                if not director:
                    director = Director(Name=director_name)
                    db.session.add(director)
                    db.session.commit()
            movie = Movie.query.filter_by(Title=row["title"]).first()
            if not movie:
                movie = Movie(
                    Title=row["title"],
                    ReleaseYear=row["year"],
                    Genre=row["genre"],
                    Rating=row["avg_vote"] if isinstance(row["avg_vote"], float) else 0.0,
                    DirectorID=director.DirectorID if director_name else None,
                )
                db.session.add(movie)
                db.session.commit()

            actors = row.get("actors", "")
            if isinstance(actors, str):
                actors_list = actors.split(", ")
                for actor_name in actors_list:
                    if actor_name:
                        actor = Actor.query.filter_by(Name=actor_name).first()
                        if not actor:
                            actor = Actor(Name=actor_name)
                            db.session.add(actor)
                            db.session.commit()

                        movie_actor = MovieActor.query.filter_by(
                            MovieID=movie.MovieID, ActorID=actor.ActorID
                        ).first()
                        if not movie_actor:
                            movie_actor = MovieActor(
                                MovieID=movie.MovieID, ActorID=actor.ActorID
                            )
                            db.session.add(movie_actor)
                            db.session.commit()

        return jsonify({"message": "Data imported successfully"}), 200
    else:
        return jsonify({"error": "Unsupported file type"}), 400


@app.route("/export-data", methods=["GET"])
def export_data():
    query = """
        SELECT m.MovieID, m.Title, m.ReleaseYear, m.Genre, m.Rating, d.Name as Director,
               group_concat(a.Name, ', ') as Actors
        FROM Movies m
        JOIN Directors d ON m.DirectorID = d.DirectorID
        JOIN MovieActor ma ON m.MovieID = ma.MovieID
        JOIN Actors a ON ma.ActorID = a.ActorID
        GROUP BY m.MovieID
    """
    df = pd.read_sql_query(query, db.engine)

    export_format = request.args.get("format", "csv")
    if export_format == "xlsx":
        export_path = "exported_data.xlsx"
        df.to_excel(export_path, index=False)
    else:
        export_path = "exported_data.csv"
        df.to_csv(export_path, index=False)

    return send_file(export_path, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
