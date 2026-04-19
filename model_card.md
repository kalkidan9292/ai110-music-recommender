# 🎧 Model Card - Music Recommender Simulation

## Model Name  
VibeMatch 1.0  

---

## Goal / Task  

This recommender system suggests songs based on a user’s preferred genre, mood, and energy level. It tries to predict which songs a user would enjoy based on how closely they match these preferences.

---

## Data Used  

The dataset contains about 20 songs with features such as genre, mood, energy, tempo, and valence.  

It includes a mix of genres like pop, rock, lofi, EDM, and ambient, and moods such as happy, chill, intense, and relaxed.  

However, the dataset is small and does not represent all music styles, which limits the variety of recommendations.

---

## Algorithm Summary  

The system assigns a score to each song based on how well it matches the user’s preferences.  

- Songs get +2 points if the genre matches  
- Songs get +1.5 points if the mood matches  
- Songs get additional points based on how close their energy is to the user’s target  

After scoring all songs, the system sorts them from highest to lowest score and returns the top recommendations.

---

## Observed Behavior / Biases  

The system tends to favor genre because it has the highest weight. This means songs from the preferred genre often rank higher even if other features don’t match as well.  

I also noticed that songs with high energy, like "Gym Hero," appear often across different profiles, even when the mood does not fully match.  

This shows a bias toward energy and genre, and the small dataset also limits diversity in results.

---

## Evaluation Process  

I tested the system using three different user profiles:  
- High-energy pop  
- Chill lofi  
- Intense rock  

For each profile, I ran the recommender and observed the top 5 results. I compared the outputs to my expectations to see if they matched the intended vibe.  

I also experimented with changing feature weights to see how the recommendations changed.

---

## Intended Use and Non-Intended Use  

This system is intended for educational purposes to demonstrate how a simple recommender works.  

It is not designed for real users or production systems because it uses a small dataset and simple logic.  

It should not be used for real recommendations since it does not consider listening history, user behavior, or large-scale data.

---

## Ideas for Improvement  

- Add more features such as lyrics, artist popularity, or listening history  
- Improve diversity so the same songs don’t appear repeatedly  
- Support more complex user preferences (multiple genres or moods)  

---

## Personal Reflection  

My biggest learning moment was understanding how a simple scoring system can turn data into meaningful recommendations. I didn’t expect such a basic approach to feel so accurate.  

Using AI tools helped me move faster when writing code and structuring ideas, but I still had to double-check logic and fix errors myself.  

What surprised me most was how even simple algorithms can feel “smart,” even though they are just following basic rules.  

If I extended this project, I would experiment with more advanced features and try to make the recommendations more diverse and realistic.