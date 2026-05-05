from typing import List, Dict, Tuple
import csv

def load_songs(csv_path: str) -> List[Dict]:
    """
    Load songs from a CSV file.
    
    Args:
        csv_path: Path to the CSV file containing song data
        
    Returns:
        A list of song dictionaries with features like genre, mood, energy, etc.
        
    Raises:
        FileNotFoundError: If the CSV file does not exist
        ValueError: If the CSV is malformed or missing required columns
    """
    import os
    
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Songs file not found: {csv_path}")
    
    print(f"Loading songs from {csv_path}...")
    songs = []

    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty or malformed")
            
            required_fields = {"id", "title", "artist", "genre", "mood", "energy", 
                             "tempo_bpm", "valence", "danceability", "acousticness"}
            missing_fields = required_fields - set(reader.fieldnames)
            if missing_fields:
                raise ValueError(f"CSV missing required columns: {missing_fields}")
            
            for row_num, row in enumerate(reader, start=2):
                try:
                    song = {
                        "id": int(row["id"]),
                        "title": row["title"],
                        "artist": row["artist"],
                        "genre": row["genre"],
                        "mood": row["mood"],
                        "energy": float(row["energy"]),
                        "tempo_bpm": float(row["tempo_bpm"]),
                        "valence": float(row["valence"]),
                        "danceability": float(row["danceability"]),
                        "acousticness": float(row["acousticness"])
                    }
                    songs.append(song)
                except (ValueError, KeyError) as e:
                    raise ValueError(f"Error parsing row {row_num}: {e}")
    except csv.Error as e:
        raise ValueError(f"CSV parsing error: {e}")
    
    if not songs:
        raise ValueError("No songs loaded from CSV file")
    
    print(f"Successfully loaded {len(songs)} songs")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str, float]:
    """
    Score a song based on how well it matches user preferences.
    
    Scoring rules:
    - +2.0 points for genre match
    - +1.5 points for mood match
    - Energy similarity (0-1.0): 1 - |song_energy - user_energy|
    - Valence similarity (0-0.5): 0.5 * (1 - |song_valence - user_valence|)
    - Danceability bonus (0-0.5): 0.5 if song_danceability > 0.7, else 0
    
    Confidence is calculated as: (matched_weight / total_possible_weight)
    
    Args:
        user_prefs: Dict with keys: genre, mood, energy, valence (0-1), likes_dance (bool)
        song: Dict with song features
        
    Returns:
        Tuple of (score, explanation_string, confidence_0_to_1)
        
    Raises:
        ValueError: If required keys are missing from user_prefs or song
    """
    # Validate inputs
    required_user_keys = {"genre", "mood", "energy"}
    missing_user_keys = required_user_keys - set(user_prefs.keys())
    if missing_user_keys:
        raise ValueError(f"user_prefs missing required keys: {missing_user_keys}")
    
    required_song_keys = {"genre", "mood", "energy", "valence", "danceability"}
    missing_song_keys = required_song_keys - set(song.keys())
    if missing_song_keys:
        raise ValueError(f"song missing required keys: {missing_song_keys}")
    
    # Validate value ranges
    try:
        user_energy = float(user_prefs["energy"])
        if not (0 <= user_energy <= 1):
            raise ValueError(f"user energy must be 0-1, got {user_energy}")
        
        song_energy = float(song["energy"])
        if not (0 <= song_energy <= 1):
            raise ValueError(f"song energy must be 0-1, got {song_energy}")
            
        song_valence = float(song["valence"])
        if not (0 <= song_valence <= 1):
            raise ValueError(f"song valence must be 0-1, got {song_valence}")
            
        song_danceability = float(song["danceability"])
        if not (0 <= song_danceability <= 1):
            raise ValueError(f"song danceability must be 0-1, got {song_danceability}")
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid numeric values: {e}")
    
    score = 0
    reasons = []
    
    # Genre match: +2.0
    if song["genre"].lower() == user_prefs["genre"].lower():
        score += 2.0
        reasons.append("genre match (+2.0)")
    
    # Mood match: +1.5
    if song["mood"].lower() == user_prefs["mood"].lower():
        score += 1.5
        reasons.append("mood match (+1.5)")
    
    # Energy similarity: 0-1.0 (1 - absolute difference)
    energy_diff = abs(song_energy - user_energy)
    energy_score = 1.0 - energy_diff
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score:.2f})")
    
    # Valence similarity: 0-0.5 (optional preference)
    user_valence = float(user_prefs.get("valence", 0.5))  # Default to neutral
    valence_diff = abs(song_valence - user_valence)
    valence_score = 0.5 * (1.0 - valence_diff)
    score += valence_score
    reasons.append(f"valence match (+{valence_score:.2f})")
    
    # Danceability bonus: 0-0.5 (bonus if danceability > 0.7)
    if user_prefs.get("likes_dance", False):
        if song_danceability > 0.7:
            score += 0.5
            reasons.append("high danceability bonus (+0.5)")
    
    # Calculate confidence as: matched_weight / total_possible_weight
    # Total possible: 2.0 + 1.5 + 1.0 + 0.5 + 0.5 = 5.5
    total_possible = 5.5
    confidence = min(score / total_possible, 1.0)
    
    return score, ", ".join(reasons), confidence

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str, float]]:
    """
    Recommend the top-k songs for a user based on their preferences.
    
    Args:
        user_prefs: User preference dict with keys: genre, mood, energy
        songs: List of song dictionaries to rank
        k: Number of recommendations to return (default 5)
        
    Returns:
        List of tuples: (song_dict, score, explanation, confidence)
        Sorted by score descending. Returns fewer than k if songs < k.
        
    Raises:
        ValueError: If user_prefs is invalid, songs is empty, or k < 1
    """
    if not isinstance(user_prefs, dict):
        raise ValueError("user_prefs must be a dictionary")
    
    if not isinstance(songs, list):
        raise ValueError("songs must be a list")
    
    if len(songs) == 0:
        raise ValueError("songs list cannot be empty")
    
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")
    
    scored_songs = []
    
    for song in songs:
        try:
            score, explanation, confidence = score_song(user_prefs, song)
            scored_songs.append((song, score, explanation, confidence))
        except ValueError as e:
            # Skip songs with missing or invalid data
            print(f"Warning: Skipping song '{song.get('title', 'unknown')}': {e}")
            continue
    
    if len(scored_songs) == 0:
        raise ValueError("No valid songs could be scored")
    
    # Sort by score descending
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    
    # Return top k (or fewer if not enough songs)
    return scored_songs[:min(k, len(scored_songs))]