import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# --- Seed Moods ---
moods = [
    (1, 'Happy', '😊'),
    (2, 'Sad', '😢'),
    (3, 'Stressed', '😫'),
    (4, 'Cozy', '☕')
]
cursor.executemany("INSERT OR REPLACE INTO moods (id, name, emoji) VALUES (?, ?, ?);", moods)
print(f"Seeded {len(moods)} moods.")

# --- Seed Foods ---
foods = [
    ("Ahi Poke", "Sushi rice, marinated ahi tuna, edamame...", "https://images.unsplash.com/photo-1553641243-5a41a7834515?w=500", 1), # Happy
    ("Tofu Rainbow Bowl", "Brown rice, crispy tofu, mango, pickled radish...", "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=500", 1), # Happy
    ("Japanese Comfort Bowl", "Udon noodles, miso broth, mushrooms...", "https://images.unsplash.com/photo-1569718212165-fb6926c112a4?w=500", 2), # Sad
    ("Spiced Chickpea Curry Bowl", "Turmeric basmati, spinach, crispy chickpeas...", "https://images.unsplash.com/photo-1563379926898-059611e05472?w=500", 2), # Sad
    ("Seared Salmon Bowl", "Farro, spinach, roasted carrot, lemon tahini...", "https://images.unsplash.com/photo-151962381-847552363805?w=500", 3), # Stressed
    ("Mediterranean Bowl", "Couscous, falafel, cucumber, roasted eggplant...", "https://images.unsplash.com/photo-1505253716362-afb74b62f847?w=500", 3), # Stressed
    ("Peanut Butter Banana Bowl", "Quinoa or oats, sliced banana, peanut butter...", "https://images.unsplash.com/photo-1601004890684-d8cbf643f5f2?w=500", 4), # Cozy
    ("Bibimbap Bowl", "White rice, bulgogi beef or mushrooms, gochujang...", "https://images.unsplash.com/photo-1584278858536-5252a923709b?w=500", 4) # Cozy
]
cursor.executemany("INSERT INTO foods (name, description, imageUrl, mood_id) VALUES (?, ?, ?, ?);", foods)
print(f"Seeded {len(foods)} foods.")

conn.commit()
conn.close()