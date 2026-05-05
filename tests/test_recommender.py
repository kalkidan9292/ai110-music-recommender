"""
Comprehensive tests for the music recommender system.
Tests scoring logic, validation, edge cases, and feature combinations.
"""

import pytest
from src.recommender import load_songs, score_song, recommend_songs


# Test Data
SAMPLE_SONG_POP_HAPPY = {
    "id": 1,
    "title": "Pop Song",
    "artist": "Artist A",
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,
    "valence": 0.9,
    "danceability": 0.8,
    "acousticness": 0.2,
    "tempo_bpm": 120
}

SAMPLE_SONG_LOFI_CHILL = {
    "id": 2,
    "title": "Lofi Song",
    "artist": "Artist B",
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.3,
    "valence": 0.6,
    "danceability": 0.4,
    "acousticness": 0.8,
    "tempo_bpm": 80
}

SAMPLE_SONG_ROCK_INTENSE = {
    "id": 3,
    "title": "Rock Song",
    "artist": "Artist C",
    "genre": "rock",
    "mood": "intense",
    "energy": 0.95,
    "valence": 0.4,
    "danceability": 0.7,
    "acousticness": 0.1,
    "tempo_bpm": 150
}

SAMPLE_SONG_AMBIENT = {
    "id": 4,
    "title": "Ambient Song",
    "artist": "Artist D",
    "genre": "ambient",
    "mood": "peaceful",
    "energy": 0.2,
    "valence": 0.7,
    "danceability": 0.2,
    "acousticness": 0.95,
    "tempo_bpm": 60
}


class TestScoreSong:
    """Test the score_song function."""
    
    def test_score_exact_genre_and_mood_match(self):
        """Song with matching genre and mood should get highest points."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        score, explanation, confidence = score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
        
        # Genre (2.0) + Mood (1.5) + Energy similarity (~1.0) + Valence (~0.5) = ~5.0
        assert score >= 4.8, f"Expected score >= 4.8, got {score}"
        assert "genre match" in explanation
        assert "mood match" in explanation
        assert 0.8 <= confidence <= 1.0
    
    def test_score_no_match(self):
        """Song with different genre and mood should score lower."""
        user_prefs = {"genre": "classical", "mood": "sad", "energy": 0.8}
        score, explanation, confidence = score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
        
        # No genre match, no mood match, but energy similarity + valence
        assert score < 3.0, f"Expected score < 3.0, got {score}"
        assert "genre match" not in explanation
        assert "mood match" not in explanation
    
    def test_score_energy_similarity(self):
        """Songs with similar energy should score higher."""
        user_prefs = {"genre": "rock", "mood": "intense", "energy": 0.9}
        score, explanation, confidence = score_song(user_prefs, SAMPLE_SONG_ROCK_INTENSE)
        
        assert "energy similarity" in explanation
        assert score > 3.5
    
    def test_score_energy_dissimilarity(self):
        """Songs with very different energy should score lower on that metric."""
        user_prefs = {"genre": "lofi", "mood": "chill", "energy": 0.05}
        score, explanation, confidence = score_song(user_prefs, SAMPLE_SONG_ROCK_INTENSE)
        
        # Energy should be very low (0.95 - 0.05 = 0.9 difference)
        assert score < 2.5, f"Expected score < 2.5 for very different energy, got {score}"
    
    def test_score_danceability_bonus(self):
        """High danceability should give bonus if user likes dancing."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_dance": True}
        score1, _, _ = score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
        
        user_prefs["likes_dance"] = False
        score2, _, _ = score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
        
        # Score should be higher when user likes dance and song has high danceability
        assert score1 > score2, "Dance preference should increase score for high danceability song"
    
    def test_confidence_range(self):
        """Confidence should always be between 0 and 1."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        _, _, confidence = score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
        assert 0 <= confidence <= 1, f"Confidence out of range: {confidence}"
    
    def test_missing_user_prefs_key(self):
        """Missing required keys in user_prefs should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy"}  # Missing energy
        with pytest.raises(ValueError, match="missing required keys"):
            score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
    
    def test_missing_song_key(self):
        """Missing required keys in song should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        song = {"id": 1, "title": "Test", "genre": "pop", "mood": "happy"}  # Missing energy, valence, danceability
        with pytest.raises(ValueError, match="missing required keys"):
            score_song(user_prefs, song)
    
    def test_invalid_energy_value(self):
        """Energy values outside [0, 1] should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 1.5}  # Invalid
        with pytest.raises(ValueError, match="must be 0-1"):
            score_song(user_prefs, SAMPLE_SONG_POP_HAPPY)
    
    def test_invalid_song_energy_value(self):
        """Song energy values outside [0, 1] should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        song = SAMPLE_SONG_POP_HAPPY.copy()
        song["energy"] = -0.5
        with pytest.raises(ValueError, match="must be 0-1"):
            score_song(user_prefs, song)
    
    def test_case_insensitive_genre_matching(self):
        """Genre matching should be case-insensitive."""
        user_prefs = {"genre": "POP", "mood": "happy", "energy": 0.8}
        song = SAMPLE_SONG_POP_HAPPY.copy()
        song["genre"] = "pop"
        score, explanation, _ = score_song(user_prefs, song)
        
        assert "genre match" in explanation
    
    def test_case_insensitive_mood_matching(self):
        """Mood matching should be case-insensitive."""
        user_prefs = {"genre": "pop", "mood": "HAPPY", "energy": 0.8}
        song = SAMPLE_SONG_POP_HAPPY.copy()
        song["mood"] = "happy"
        score, explanation, _ = score_song(user_prefs, song)
        
        assert "mood match" in explanation


class TestRecommendSongs:
    """Test the recommend_songs function."""
    
    def test_recommend_returns_songs_sorted_by_score(self):
        """Recommendations should be sorted by score (descending)."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        songs = [SAMPLE_SONG_POP_HAPPY, SAMPLE_SONG_LOFI_CHILL, SAMPLE_SONG_ROCK_INTENSE]
        
        recommendations = recommend_songs(user_prefs, songs, k=3)
        
        assert len(recommendations) == 3
        # Pop song should be first (matches genre and mood)
        assert recommendations[0][0]["genre"] == "pop"
        # Scores should be in descending order
        for i in range(len(recommendations) - 1):
            assert recommendations[i][1] >= recommendations[i + 1][1]
    
    def test_recommend_respects_k_parameter(self):
        """Should return exactly k recommendations (or fewer if songs < k)."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        songs = [SAMPLE_SONG_POP_HAPPY, SAMPLE_SONG_LOFI_CHILL, SAMPLE_SONG_ROCK_INTENSE]
        
        result_k1 = recommend_songs(user_prefs, songs, k=1)
        assert len(result_k1) == 1
        
        result_k2 = recommend_songs(user_prefs, songs, k=2)
        assert len(result_k2) == 2
        
        result_k10 = recommend_songs(user_prefs, songs, k=10)
        assert len(result_k10) == 3  # Only 3 songs available
    
    def test_recommend_with_k_zero(self):
        """k=0 should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        songs = [SAMPLE_SONG_POP_HAPPY]
        
        with pytest.raises(ValueError, match="k must be >= 1"):
            recommend_songs(user_prefs, songs, k=0)
    
    def test_recommend_with_empty_songs(self):
        """Empty songs list should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        
        with pytest.raises(ValueError, match="songs list cannot be empty"):
            recommend_songs(user_prefs, [], k=5)
    
    def test_recommend_with_invalid_user_prefs(self):
        """Non-dict user_prefs should raise ValueError."""
        songs = [SAMPLE_SONG_POP_HAPPY]
        
        with pytest.raises(ValueError, match="user_prefs must be a dictionary"):
            recommend_songs("invalid", songs, k=5)
    
    def test_recommend_with_invalid_songs_type(self):
        """Non-list songs should raise ValueError."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        
        with pytest.raises(ValueError, match="songs must be a list"):
            recommend_songs(user_prefs, "invalid", k=5)
    
    def test_recommend_return_format(self):
        """Each recommendation should be a tuple of (song, score, explanation, confidence)."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        songs = [SAMPLE_SONG_POP_HAPPY, SAMPLE_SONG_LOFI_CHILL]
        
        recommendations = recommend_songs(user_prefs, songs, k=2)
        
        for song, score, explanation, confidence in recommendations:
            assert isinstance(song, dict)
            assert isinstance(score, float)
            assert isinstance(explanation, str)
            assert isinstance(confidence, float)
            assert 0 <= confidence <= 1
    
    def test_recommend_all_features_included(self):
        """Recommendation explanations should include energy and valence."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        songs = [SAMPLE_SONG_POP_HAPPY]
        
        recommendations = recommend_songs(user_prefs, songs, k=1)
        explanation = recommendations[0][2]
        
        assert "energy" in explanation.lower()
        assert "valence" in explanation.lower()
    
    def test_recommend_different_profiles_different_results(self):
        """Different user profiles should produce different rankings."""
        songs = [SAMPLE_SONG_POP_HAPPY, SAMPLE_SONG_LOFI_CHILL, SAMPLE_SONG_ROCK_INTENSE]
        
        # Pop-loving user
        pop_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        pop_recommendations = recommend_songs(pop_prefs, songs, k=1)
        
        # Rock-loving user
        rock_prefs = {"genre": "rock", "mood": "intense", "energy": 0.9}
        rock_recommendations = recommend_songs(rock_prefs, songs, k=1)
        
        # Top recommendation should be different
        assert pop_recommendations[0][0]["genre"] != rock_recommendations[0][0]["genre"]
    
    def test_recommend_k_greater_than_songs(self):
        """Requesting more recommendations than available songs should return all."""
        user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        songs = [SAMPLE_SONG_POP_HAPPY, SAMPLE_SONG_LOFI_CHILL]
        
        recommendations = recommend_songs(user_prefs, songs, k=100)
        
        assert len(recommendations) == 2


class TestLoadSongs:
    """Test the load_songs function."""
    
    def test_load_songs_succeeds(self):
        """Successfully load songs from the CSV file."""
        songs = load_songs("data/songs.csv")
        
        assert isinstance(songs, list)
        assert len(songs) > 0
        assert all(isinstance(song, dict) for song in songs)
    
    def test_loaded_songs_have_required_fields(self):
        """All loaded songs should have required fields."""
        songs = load_songs("data/songs.csv")
        
        required_fields = {"id", "title", "artist", "genre", "mood", "energy", 
                          "tempo_bpm", "valence", "danceability", "acousticness"}
        
        for song in songs:
            assert required_fields.issubset(set(song.keys()))
    
    def test_load_nonexistent_file(self):
        """Loading nonexistent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_songs("nonexistent.csv")
