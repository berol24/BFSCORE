

from flask import Flask, render_template, request, jsonify
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, expr


app = Flask(__name__)

# Création d'une session Spark
spark = SparkSession.builder.appName("BundesligaApp").getOrCreate()

# Chargement du fichier CSV contenant les résultats des matchs
df_bundesliga = spark.read.csv("results/football_matches.csv", header=True, inferSchema=True)

df_bundesliga = df_bundesliga.withColumn("Season", col("Season").cast("integer"))

# association des statistiques des matchs à domicile
df_home_matches = (
    df_bundesliga.groupBy("Season", "HomeTeam")
    .agg(
        spark_sum(expr("case when FTR = 'H' then 1 else 0 end")).alias("TotalHomeWin"),
        spark_sum(expr("case when FTR = 'A' then 1 else 0 end")).alias("TotalHomeLoss"),
        spark_sum(expr("case when FTR = 'D' then 1 else 0 end")).alias("TotalHomeTie"),
        spark_sum("FTHG").alias("HomeScoredGoals"),
        spark_sum("FTAG").alias("HomeAgainstGoals")
    )
)
df_home_matches = df_home_matches.withColumnRenamed("HomeTeam", "Team")

# association des statistiques des matchs à l'extérieur

df_away_matches = (
    df_bundesliga.groupBy("Season", "AwayTeam")
    .agg(
        spark_sum(expr("case when FTR = 'A' then 1 else 0 end")).alias("TotalAwayWin"),
        spark_sum(expr("case when FTR = 'H' then 1 else 0 end")).alias("TotalAwayLoss"),
        spark_sum(expr("case when FTR = 'D' then 1 else 0 end")).alias("TotalAwayTie"),
        spark_sum("FTAG").alias("AwayScoredGoals"),
        spark_sum("FTHG").alias("AwayAgainstGoals")
    )
)
df_away_matches = df_away_matches.withColumnRenamed("AwayTeam", "Team")

# Fusion des statistiques des matchs à domicile et à l'extérieur
df_merged = df_home_matches.join(df_away_matches, on=["Season", "Team"], how="inner")

# Calcul des totaux pour chaque équipe
df_totals = df_merged.withColumn("GoalsScored", col("HomeScoredGoals") + col("AwayScoredGoals"))
df_totals = df_totals.withColumn("GoalsAgainst", col("HomeAgainstGoals") + col("AwayAgainstGoals"))
df_totals = df_totals.withColumn("Win", col("TotalHomeWin") + col("TotalAwayWin"))
df_totals = df_totals.withColumn("Loss", col("TotalHomeLoss") + col("TotalAwayLoss"))
df_totals = df_totals.withColumn("Tie", col("TotalHomeTie") + col("TotalAwayTie"))


# Routes

#Accueil
@app.route("/")
def home():
    df_filtered = df_bundesliga.filter(col("Season") == 1993).limit(20)
    matches = [row.asDict() for row in df_filtered.collect()]
    return render_template("index.html", matches=matches)

#filtrer les matchs par année
@app.route("/annee")
def filter_annee():
    annee = int(request.args.get("annee"))
    df_filtered = df_bundesliga.filter(col("Season") == annee).limit(20)
    matches = [row.asDict() for row in df_filtered.collect()]
    return render_template("index.html", matches=matches)

# ajouter plus de matchs
@app.route("/load_more")
def load_more():
    year = int(request.args.get("year"))
    offset = int(request.args.get("offset"))
    limit = 20

    df_filtered = df_bundesliga.filter(col("Season") == year).limit(offset + limit).subtract(df_bundesliga.filter(col("Season") == year).limit(offset))
    matches = [row.asDict() for row in df_filtered.collect()]
    return jsonify(matches=matches)

# obtenir les informations sur un match spécifique
@app.route("/info/<int:match_id>")
def get_match_info(match_id):
    match = df_bundesliga.filter(col("Match_ID") == match_id).collect()
    if not match:
        return "Match not found", 404

    match_data = match[0].asDict()

    home_team = match_data["HomeTeam"]
    away_team = match_data["AwayTeam"]
    current_season = match_data["Season"]

    previous_seasons = find_previous_seasons(home_team, away_team, current_season)
    return render_template("match_info.html", match=match_data, previous_seasons=previous_seasons)

# trouver les saisons précédentes entre deux équipes
def find_previous_seasons(home_team, away_team, current_season):
    filtered_df = df_bundesliga.filter(
        ((col("HomeTeam") == home_team) & (col("AwayTeam") == away_team)) |
        ((col("HomeTeam") == away_team) & (col("AwayTeam") == home_team))
    ).filter(col("Season") < current_season)

    seasons = [row["Season"] for row in filtered_df.select("Season").distinct().orderBy("Season").collect()]
    return seasons

#  obtenir les détails d'une équipe
@app.route("/team/<team_name>")
def team_details(team_name):
    team_data = df_totals.filter(col("Team") == team_name).collect()
    if not team_data:
        return f"No data found for team: {team_name}", 404

    team_data = [row.asDict() for row in team_data]
    return render_template("team_details.html", team_name=team_name, team_data=team_data)

# Exécution de l'application Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

