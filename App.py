import streamlit as st

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & CUSTOM CSS
# ---------------------------------------------------------
st.set_page_config(page_title="The Perfect Holiday Finder ✈️", page_icon="🌍", layout="centered")

def set_bg_color(hex_color, text_color="#FFFFFF"):
    """Injects custom CSS to change the background and text color of the app."""
    css = f"""
    <style>
    .stApp {{
        background-color: {hex_color};
        color: {text_color};
    }}
    h1, h2, h3, h4, h5, h6, p, div, span, label {{
        color: {text_color} !important;
    }}
    .stButton>button {{
        background-color: transparent !important;
        color: {text_color} !important;
        border: 2px solid {text_color} !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: {text_color} !important;
        color: {hex_color} !important;
    }}
    .stRadio>div {{
        padding: 10px;
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. HOLIDAY DATABASE
# ---------------------------------------------------------
destinations = {
    "Seychelles": {
        "title": "The Seychelles 🇸🇨",
        "theme": "Romantic & Relaxing 💖",
        "bg_color": "#FF8DA1", # Soft Pink
        "text_color": "#4A001F",
        "description": "Welcome to pure paradise! Crystal clear waters, ultimate luxury, and breathtaking sunsets. Perfect for total relaxation.",
        "image": "https://images.unsplash.com/photo-1570533314489-0820bb2629b0?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Champagne Welcome & Beachfront Villa Check-in 🥂",
        "pairs": [
            ("Ultimate Full-Day Spa Experience with Ocean Waves 💆‍♀️", "Insane Jungle Canopy Zipline 🧗‍♀️"),
            ("Private Beach Dining under the Stars with fresh Lobster 🦞", "Local Creole Street Food Tasting Tour 🍢"),
            ("Scuba Diving in coral reefs with Sea Turtles 🐢", "Sunset Yacht Cruise with a personal butler 🛥️")
        ]
    },
    "Madagascar": {
        "title": "Madagascar 🇲🇬",
        "theme": "Wild Nature & Adventure 🌿",
        "bg_color": "#2E8B57", # Sea Green
        "text_color": "#FFFFFF",
        "description": "An untouched, exotic wonderland! Trek through lush jungles, see incredible wildlife, and explore hidden gems.",
        "image": "https://images.unsplash.com/photo-1554866585-cd94860890b7?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Jungle Eco-Lodge Check-in & Sunrise Breakfast 🍳",
        "pairs": [
            ("Nighttime Predator Safari to spot rare Lemurs 🔦", "Sunset Walk down the Avenue of the Baobabs 🌅"),
            ("Traditional Zebu Steak & Local Rum Tasting under the stars 🥩", "Cooking Class with Local Villagers 🥘"),
            ("Climbing the Razor-sharp Tsingy Stone Forest 🪨", "Snorkeling in the warm waters of Nosy Be 🏖️")
        ]
    },
    "San Francisco": {
        "title": "San Francisco, USA 🇺🇸",
        "theme": "City Fun & Hidden Gems 🌉",
        "bg_color": "#4682B4", # Steel Blue
        "text_color": "#FFFFFF",
        "description": "A vibrant, modern city packed with world-class food, incredible sights, and endless entertainment!",
        "image": "https://images.unsplash.com/photo-1501594907352-04cda38ebc29?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Riding the iconic Cable Cars overlooking the bay 🚃",
        "pairs": [
            ("Skydiving over the Golden Gate Bridge 🪂", "VIP Behind-the-scenes Tour at SF Zoo 🦒"),
            ("Alcatraz Night Tour & Ghost Hunt 👻", "Relaxing Picnic at Alamo Square (Painted Ladies) 🧺"),
            ("10-course Michelin Star Tasting Menu in Soma 🍷", "Clam Chowder in a sourdough bowl at Fisherman's Wharf 🦀")
        ]
    },
    "Mount Everest / Nepal": {
        "title": "Mount Everest, Nepal 🇳🇵",
        "theme": "Insane Adventure 🏔️",
        "bg_color": "#1C1C1C", # Dark Grey
        "text_color": "#FFFFFF",
        "description": "The roof of the world! For those who want their breath taken away (literally). Thrills, heights, and spiritual peace.",
        "image": "https://images.unsplash.com/photo-1544735716-392fe2489ffa?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Arrival in Kathmandu & Everest Base Camp Briefing ⛺",
        "pairs": [
            ("Helicopter Tour of Everest Base Camp with Champagne 🚁", "Summiting a 6000m sub-peak with Sherpas 🧗‍♂️"),
            ("Bungee jumping into a deep Himalayan gorge 🪂", "Sunrise Meditation with Monks at a remote Monastery 🧘‍♀️"),
            ("Authentic Momo (Dumpling) Masterclass 🥟", "Staying in a high-altitude traditional Sherpa Village 🛖")
        ]
    },
    "Japan": {
        "title": "Tokyo & Kyoto, Japan 🇯🇵",
        "theme": "Culture & Vibrant CityLife 🏮",
        "bg_color": "#DC143C", # Crimson
        "text_color": "#FFFFFF",
        "description": "A perfect blend of insane neon lights, incredible food, and deep, relaxing ancient traditions.",
        "image": "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Bullet Train (Shinkansen) ride with Mount Fuji views 🚄",
        "pairs": [
            ("Real-life Mario Kart street racing through Shibuya 🏎️", "Secret Geisha Tea Ceremony in Kyoto 🍵"),
            ("Early morning Tsukiji Fish Market VIP Sushi Tour 🍣", "Wagyu Beef & Sake Pairing in a hidden neon alley 🍶"),
            ("Paragliding past Mount Fuji 🪂", "Relaxing in a Private Onsen (Hot Spring) in the snow ♨️")
        ]
    },
    "Italy": {
        "title": "Amalfi Coast, Italy 🇮🇹",
        "theme": "Foodie & Romantic Heaven 🍝",
        "bg_color": "#FFB347", # Pastel Orange
        "text_color": "#333333",
        "description": "La Dolce Vita! Stunning cliffside towns, the best food in the world, and ultimate romance.",
        "image": "https://images.unsplash.com/photo-1516483638261-f40889228853?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Checking into a cliffside villa overlooking the sea 🌅",
        "pairs": [
            ("Cliff jumping into the Mediterranean Sea 🌊", "Private Boat Tour to the sparkling Blue Grotto 🚤"),
            ("Truffle hunting with dogs in the lush forests 🐕", "Authentic Nonna-led Pasta & Limoncello Class 🍋"),
            ("Driving a vintage Vespa along the winding coastal roads 🛵", "Wine tasting at a gorgeous cliffside vineyard 🍷")
        ]
    },
    "Iceland": {
        "title": "Iceland 🇮🇸",
        "theme": "Dark, Cold & Magical 🌌",
        "bg_color": "#000033", # Deep Night Blue
        "text_color": "#E0FFFF",
        "description": "Otherworldly landscapes, roaring waterfalls, and magical skies. A totally unique escape.",
        "image": "https://images.unsplash.com/photo-1476610182048-b716b8518aae?auto=format&fit=crop&w=800&q=80",
        "base_activity": "Super-Jeep ride across the volcanic tundra 🚙",
        "pairs": [
            ("Exploring deep inside a glittering Glacier Ice Cave 🧊", "Floating in the exclusive Blue Lagoon VIP Retreat 🧖‍♀️"),
            ("Midnight Sun ATV Volcano ride 🌋", "Northern Lights chasing with Hot Cocoa & Blankets ✨"),
            ("Trying Hakarl (Fermented Shark) and Brennivin 🦈", "High-end Nordic fine dining in Reykjavik 🍽️")
        ]
    }
}

# ---------------------------------------------------------
# 3. 20 FUN QUESTIONS
# ---------------------------------------------------------
questions = [
    {"q": "1. What is your ideal morning? 🌅", "opts": {"Sleeping in until noon": ["Seychelles", "Italy"], "Up at 5 AM ready to conquer": ["Mount Everest / Nepal", "Madagascar", "Iceland"], "Grabbing a coffee and hitting the streets": ["San Francisco", "Japan"]}},
    {"q": "2. Pick an animal companion for the trip 🐾", "opts": {"A cuddly sea turtle": ["Seychelles"], "A mischievous lemur": ["Madagascar"], "A snow leopard": ["Mount Everest / Nepal"], "A Shiba Inu": ["Japan"]}},
    {"q": "3. How do you feel about heights? 🎢", "opts": {"Love them! Throw me out of a plane!": ["San Francisco", "Mount Everest / Nepal"], "Only if there's a cocktail at the top": ["Japan", "Italy"], "Keep me on solid ground, thanks": ["Seychelles", "Madagascar"]}},
    {"q": "4. Pick a flavor profile! 👅", "opts": {"Fresh, tropical, and sweet": ["Seychelles", "Madagascar"], "Savory, rich, and comforting": ["Italy", "San Francisco"], "Spicy, exotic, and surprising": ["Japan", "Mount Everest / Nepal"], "Weird and wonderful": ["Iceland"]}},
    {"q": "5. What’s your ideal footwear? 👟", "opts": {"Barefoot or flip flops": ["Seychelles"], "Heavy duty hiking boots": ["Mount Everest / Nepal", "Iceland", "Madagascar"], "Stylish sneakers": ["San Francisco", "Japan"], "Elegant evening shoes": ["Italy"]}},
    {"q": "6. Choose a magical item to take with you ✨", "opts": {"Invisibility cloak (for people watching)": ["San Francisco", "Japan"], "A teleportation ring (to skip the hike)": ["Mount Everest / Nepal", "Madagascar"], "An endless bottle of perfect wine": ["Italy", "Seychelles"], "A warmth amulet": ["Iceland"]}},
    {"q": "7. What’s your evening vibe? 🌙", "opts": {"Dancing under the neon lights": ["Japan", "San Francisco"], "A romantic candlelit dinner": ["Italy", "Seychelles"], "Staring at the stars by a campfire": ["Madagascar", "Iceland"], "Passing out from exhaustion": ["Mount Everest / Nepal"]}},
    {"q": "8. Weather preference? ☀️❄️", "opts": {"Roasting hot, give me a tan": ["Seychelles", "Madagascar"], "Brisk and freezing, I want snow": ["Iceland", "Mount Everest / Nepal"], "Mild and breezy": ["San Francisco", "Italy", "Japan"]}},
    {"q": "9. How do you handle getting lost? 🗺️", "opts": {"Panic slightly but find a cute cafe": ["Italy", "San Francisco"], "Ask locals and make friends": ["Japan", "Madagascar"], "I don't get lost, I go on unexpected adventures": ["Mount Everest / Nepal", "Iceland"], "I just stay at the resort": ["Seychelles"]}},
    {"q": "10. Pick a movie genre for your life 🎬", "opts": {"Romantic Comedy": ["Italy", "Seychelles"], "Action / Thriller": ["Mount Everest / Nepal", "Madagascar"], "Sci-Fi / Cyberpunk": ["Japan"], "Indie Coming-of-Age": ["San Francisco", "Iceland"]}},
    {"q": "11. Choose a mode of transport 🚀", "opts": {"Luxury Yacht": ["Seychelles", "Italy"], "Helicopter": ["Mount Everest / Nepal", "Iceland"], "Bullet Train": ["Japan"], "Your own two feet": ["Madagascar", "San Francisco"]}},
    {"q": "12. How much luggage are you bringing? 🧳", "opts": {"Just a backpack, keep it rugged": ["Mount Everest / Nepal", "Madagascar"], "One suitcase, well curated": ["San Francisco", "Japan", "Iceland"], "Three massive trunks of outfits": ["Italy", "Seychelles"]}},
    {"q": "13. Pick a historical era to visit 🕰️", "opts": {"Ancient Empires (Samurai, Romans)": ["Japan", "Italy"], "The Wild, Untamed Prehistoric age": ["Madagascar", "Iceland"], "The glamorous 1920s": ["Seychelles", "San Francisco"]}},
    {"q": "14. What's your budget style? 💸", "opts": {"Luxury all the way, spoil me": ["Seychelles", "Italy"], "Mix of street food and one fancy splurge": ["Japan", "San Francisco"], "I just need a tent and vibes": ["Mount Everest / Nepal", "Madagascar"]}},
    {"q": "15. Water or Land? 🌊🌍", "opts": {"Ocean, lakes, rivers!": ["Seychelles", "Iceland"], "Mountains, forests, cities!": ["Mount Everest / Nepal", "San Francisco"], "A mix of both!": ["Madagascar", "Italy", "Japan"]}},
    {"q": "16. Choose a color palette 🎨", "opts": {"Neon pinks and blues": ["Japan", "San Francisco"], "Earthy greens and browns": ["Madagascar", "Mount Everest / Nepal"], "Ocean blues and sunset oranges": ["Seychelles", "Italy"], "Icy whites and dark blacks": ["Iceland"]}},
    {"q": "17. Pick a travel snack 🥨", "opts": {"Freshly baked pastry": ["San Francisco", "Italy"], "Exotic tropical fruit": ["Seychelles", "Madagascar"], "Energy bar or trail mix": ["Mount Everest / Nepal", "Iceland"], "Matcha KitKats": ["Japan"]}},
    {"q": "18. What's your worst nightmare on holiday? 😱", "opts": {"No WiFi": ["San Francisco", "Japan"], "Sunburn": ["Seychelles", "Italy"], "A wild animal in my tent": ["Madagascar", "Mount Everest / Nepal"], "Freezing to death": ["Iceland"]}},
    {"q": "19. Choose a sound to fall asleep to 🎧", "opts": {"Crashing ocean waves": ["Seychelles", "Italy"], "Jungle insects and distant roars": ["Madagascar"], "City traffic and sirens": ["San Francisco", "Japan"], "Howling wind": ["Mount Everest / Nepal", "Iceland"]}},
    {"q": "20. Finally, what's the main goal of this trip? 🎯", "opts": {"To relax completely": ["Seychelles", "Italy"], "To push my limits": ["Mount Everest / Nepal", "Iceland", "Madagascar"], "To eat EVERYTHING": ["Japan", "San Francisco", "Italy"]}},
]

# ---------------------------------------------------------
# 4. STATE MANAGEMENT & CALLBACKS
# ---------------------------------------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.q_index = 0
    st.session_state.scores = {d: 0 for d in destinations.keys()}
    st.session_state.available_dests = list(destinations.keys())
    st.session_state.chosen_dest = None
    st.session_state.activities = []
    st.session_state.activity_round = 0

def start_quiz():
    st.session_state.stage = 'questions'

def handle_answer(selected_option):
    # Add points
    for d in questions[st.session_state.q_index]["opts"][selected_option]:
        if d in st.session_state.scores:
            st.session_state.scores[d] += 1
    
    st.session_state.q_index += 1
    
    # Check if we should show an interim offer (Every 2 questions)
    if st.session_state.q_index % 2 == 0 and st.session_state.q_index > 0:
        st.session_state.stage = 'interim_offer'
    elif st.session_state.q_index >= len(questions):
        st.session_state.stage = 'interim_offer' # Force final offer

def accept_offer(dest_name):
    st.session_state.chosen_dest = dest_name
    st.session_state.stage = 'activity_selection'

def reject_offer(dest_name):
    st.session_state.available_dests.remove(dest_name)
    if st.session_state.q_index >= len(questions) or len(st.session_state.available_dests) == 0:
        # If no questions left or no destinations left, force them to pick from remaining
        if len(st.session_state.available_dests) == 0:
            st.session_state.chosen_dest = list(destinations.keys())[0] # Fallback
        else:
            st.session_state.chosen_dest = st.session_state.available_dests[0]
        st.session_state.stage = 'activity_selection'
    else:
        st.session_state.stage = 'questions'

def pick_activity(activity):
    st.session_state.activities.append(activity)
    st.session_state.activity_round += 1
    if st.session_state.activity_round >= 3:
        st.session_state.stage = 'final_itinerary'

def go_to_twist():
    st.session_state.stage = 'twist'

def answer_twist(answer):
    st.session_state.twist_answer = answer
    st.session_state.stage = 'twist_result'

# ---------------------------------------------------------
# 5. UI RENDERING
# ---------------------------------------------------------

if st.session_state.stage == 'welcome':
    set_bg_color("#6A5ACD", "#FFFFFF") # Slate Blue
    st.title("✨ Welcome to the Perfect Holiday Finder! ✨")
    st.write("Answer a series of fun questions to find your absolute dream holiday and the most amazing activities.")
    st.write("Are you ready for the adventure of a lifetime? 🌍✈️")
    st.button("Let's Go! 🚀", on_click=start_quiz)

elif st.session_state.stage == 'questions':
    set_bg_color("#2F4F4F", "#FFFFFF") # Dark Slate Gray
    q_data = questions[st.session_state.q_index]
    st.title(q_data["q"])
    
    # Options
    choice = st.radio("Choose your answer:", list(q_data["opts"].keys()))
    
    st.write("---")
    st.button("Next Question ➡️", on_click=handle_answer, args=(choice,))
    
    st.progress(st.session_state.q_index / len(questions))

elif st.session_state.stage == 'interim_offer':
    # Find the top scoring destination from AVAILABLE destinations
    valid_scores = {k: v for k, v in st.session_state.scores.items() if k in st.session_state.available_dests}
    best_dest_name = max(valid_scores, key=valid_scores.get)
    dest_data = destinations[best_dest_name]
    
    set_bg_color(dest_data["bg_color"], dest_data["text_color"])
    
    st.title(f"🎉 WE FOUND A MATCH! 🎉")
    st.header(dest_data["title"])
    st.subheader(dest_data["theme"])
    
    st.image(dest_data["image"], use_container_width=True)
    st.write(f"**{dest_data['description']}**")
    
    st.write("### Do you want to ACCEPT this holiday, or continue searching?")
    st.write("*(Warning: If you continue, this destination will be lost forever!)*")
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("😍 ACCEPT HOLIDAY!", on_click=accept_offer, args=(best_dest_name,), use_container_width=True)
    with col2:
        st.button("🤔 Continue Searching...", on_click=reject_offer, args=(best_dest_name,), use_container_width=True)

elif st.session_state.stage == 'activity_selection':
    dest_data = destinations[st.session_state.chosen_dest]
    set_bg_color(dest_data["bg_color"], dest_data["text_color"])
    
    st.title(f"Let's plan your {dest_data['title']} itinerary! 📅")
    st.write("You must pick ONE activity to keep, and ONE to throw away.")
    
    rnd = st.session_state.activity_round
    pair = dest_data["pairs"][rnd]
    
    st.write(f"### Choice {rnd + 1} of 3:")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(pair[0])
        st.button("Keep This! ✅", key=f"keep_0_{rnd}", on_click=pick_activity, args=(pair[0],), use_container_width=True)
    with col2:
        st.info(pair[1])
        st.button("Keep This! ✅", key=f"keep_1_{rnd}", on_click=pick_activity, args=(pair[1],), use_container_width=True)

elif st.session_state.stage == 'final_itinerary':
    dest_data = destinations[st.session_state.chosen_dest]
    set_bg_color(dest_data["bg_color"], dest_data["text_color"])
    
    st.title("🎊 WELL DONE! THIS IS YOUR HOLIDAY! 🎊")
    st.image(dest_data["image"], use_container_width=True)
    
    st.header(f"📍 Destination: {dest_data['title']}")
    
    st.subheader("Your Ultimate Itinerary:")
    st.write(f"🌟 **{dest_data['base_activity']}**")
    for idx, act in enumerate(st.session_state.activities):
        st.write(f"🌟 **{act}**")
        
    st.write("---")
    st.button("Click one more thing... 👀", on_click=go_to_twist)

elif st.session_state.stage == 'twist':
    # Pitch black screen, big heart
    set_bg_color("#000000", "#FFFFFF")
    
    st.markdown("<h1 style='text-align: center; font-size: 100px;'>❤️</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>Do you love Damien?</h2>", unsafe_allow_html=True)
    
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        sub_col1, sub_col2 = st.columns(2)
        with sub_col1:
            st.button("YES", on_click=answer_twist, args=("yes",), use_container_width=True)
        with sub_col2:
            st.button("NO", on_click=answer_twist, args=("no",), use_container_width=True)

elif st.session_state.stage == 'twist_result':
    set_bg_color("#000000", "#FFFFFF")
    st.markdown("<h1 style='text-align: center; font-size: 100px;'>❤️</h1>", unsafe_allow_html=True)
    
    if st.session_state.twist_answer == "yes":
        st.markdown("<h2 style='text-align: center; color: #FF69B4 !important;'>I love you too Katie bear 🐻</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='text-align: center; color: #FF69B4 !important;'>I love you too Katie bear 🐻</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>...but enjoy your holiday on your own 😜</h3>", unsafe_allow_html=True)
