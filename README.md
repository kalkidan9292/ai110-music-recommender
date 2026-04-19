# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

This project builds a simple music recommender system using a content-based filtering approach. The system compares song features such as genre, mood, and energy to a user's preferences and calculates a score for each song. Based on these scores, it ranks songs and returns the top recommendations. This project demonstrates how data can be transformed into personalized suggestions using basic algorithms.
---

## How The System Works

This recommender system suggests songs based on how well they match a user’s preferences using a content-based filtering approach. Instead of using other users’ data, the system compares features of each song directly to the user’s taste profile.

Each Song in the system includes features such as genre, mood, energy, tempo, and valence. These features help describe the overall style and “vibe” of the song.

The UserProfile stores the user’s preferred genre, mood, and target values for numerical features like energy and valence.

The recommender calculates a score for each song by awarding points for matching features. Songs receive higher scores if their genre and mood match the user’s preferences. Additional points are added based on how close the song’s energy and valence are to the user’s target values.

After scoring all songs, the system ranks them from highest to lowest score and returns the top results as recommendations.

### Algorithm Recipe

- +2.0 points for a genre match  
- +1.5 points for a mood match  
- Energy similarity score based on how close the song’s energy is to the user’s target:

  energy score = 1 − |song energy − user energy|

---

### Potential Bias

This system may over-prioritize genre since it has the highest weight. As a result, songs that match mood or energy but belong to a different genre may be ranked lower. Additionally, the limited dataset can reduce diversity and lead to repetitive recommendations.

Features Used

Song features:
              genre
              mood
              energy
              tempo_bpm
              valence
UserProfile features:
              preferred_genre
              preferred_mood
              target_energy
              target_valence

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried


- When I reduced the weight of genre from 2.0 to 1.0, the recommendations became more diverse but less accurate.
- When I increased the importance of energy similarity, the system favored songs with similar intensity but sometimes ignored mood.
- Testing different user profiles (e.g., energetic pop vs chill lofi) showed that the system correctly adjusted recommendations based on preferences.

---

## Limitations and Risks

- The system relies on a small dataset, which limits the variety of recommendations.
- It does not consider lyrics, artist popularity, or listening history.
- It may over-prioritize genre due to its higher weight, reducing diversity.
- It assumes all users have simple and consistent preferences.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Through this project, I learned how recommender systems transform user preferences and data into personalized suggestions. I was surprised by how a simple scoring system could produce results that feel meaningful and accurate. At the same time, I saw how biases can easily appear, such as over-prioritizing genre or ignoring other important aspects like diversity.

This project also showed me that even simple algorithms can feel intelligent, but they still lack deeper understanding compared to human judgment. In real-world systems, combining multiple data sources and improving fairness would be important for better recommendations.


---

## Evaluation Screenshots

### High-Energy Pop Profile
![Pop Profile](https://raw.githubusercontent.com/kalkidan9292/ai110-music-recommender/main/image1.png)

### Chill Lofi Profile
![Lofi Profile](https://raw.githubusercontent.com/kalkidan9292/ai110-music-recommender/main/image2.png)

### Intense Rock Profile
![Rock Profile](https://raw.githubusercontent.com/kalkidan9292/ai110-music-recommender/main/image3.png)

## 8. Future Work

If I had more time, I would improve this recommender by adding more advanced features such as tempo ranges, lyrics, and user listening history. 

I would also improve the diversity of recommendations so the same songs do not appear repeatedly across different profiles. Another improvement would be supporting more complex user preferences, such as combining multiple moods or genres.

---

## 9. Personal Reflection

Through this project, I learned how recommender systems use data and simple rules to create personalized suggestions. I was surprised by how effective a basic scoring system can be at capturing a musical “vibe.”  

At the same time, I saw how easily bias can appear when certain features are weighted more heavily. This changed how I think about real music apps, since they likely use much more complex data and models to improve accuracy and fairness.

