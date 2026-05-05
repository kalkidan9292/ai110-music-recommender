"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

"""
Command line runner for the Music Recommender Simulation.

This file demonstrates the recommender system with various user profiles.
"""

from typing import List, Dict, Any
from src.recommender import load_songs, recommend_songs


def main() -> None:
    """Run the recommender system with sample user profiles."""
    songs: List[Dict[str, Any]] = load_songs("data/songs.csv") 

    # Define diverse test profiles
    profiles: List[Dict[str, Any]] = [
        {
            "genre": "pop",
            "mood": "happy",
            "energy": 0.85,
            "valence": 0.85,
            "likes_dance": True
        },
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.4,
            "valence": 0.6,
            "likes_dance": False
        },
        {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.9,
            "valence": 0.5,
            "likes_dance": True
        },
        {
            "genre": "ambient",
            "mood": "peaceful",
            "energy": 0.3,
            "valence": 0.7,
            "likes_dance": False
        }
    ]

    for user_prefs in profiles:
        print("\n" + "=" * 50)
        print(f"User Profile: {user_prefs['genre']} | {user_prefs['mood']} | E:{user_prefs['energy']}")
        print("=" * 50)

        try:
            recommendations = recommend_songs(user_prefs, songs, k=5)

            for i, rec in enumerate(recommendations, start=1):
                song, score, explanation, confidence = rec

                print(f"\n{i}. {song['title']} by {song['artist']}")
                print(f"   Score: {score:.2f} | Confidence: {confidence:.1%}")
                print(f"   Because: {explanation}")
        
        except ValueError as e:
            print(f"Error: {e}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
