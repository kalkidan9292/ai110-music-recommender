"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = [
        {"genre": "pop", "mood": "happy", "energy": 0.85},
        {"genre": "lofi", "mood": "chill", "energy": 0.4},
        {"genre": "rock", "mood": "intense", "energy": 0.9}
    ]

    for user_prefs in profiles:
        print("\n==============================")
        print(f"Testing profile: {user_prefs}")
        print("==============================\n")

        recommendations = recommend_songs(user_prefs, songs, k=5)

        for rec in recommendations:
            song, score, explanation = rec
            print(f"{song['title']} - Score: {score:.2f}")
            print(f"Because: {explanation}")
            print()

if __name__ == "__main__":
    main()
