import streamlit as st
import random
import urllib.parse
import time

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & INSANE CSS
# ---------------------------------------------------------
st.set_page_config(page_title="The Ultimate Holiday Finder ✈️", page_icon="🌍", layout="wide")

def set_bg(color, text_color):
    css = f"""
<style>
    .stApp {{
        background-color: {color} !important;
        color: {text_color} !important;
        transition: background-color 0.8s ease-in-out;
    }}
    h1, h2, h3, h4, p, span, label, div {{ color: {text_color} !important; font-family: 'Arial', sans-serif; }}
    
    /* Beautiful Buttons */
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: {text_color} !important;
        border: 2px solid {text_color} !important;
        border-radius: 20px !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 15px 30px !important;
        transition: all 0.3s ease-in-out !important;
        box-shadow: 0 8px 15px rgba(0,0,0,0.3) !important;
        width: 100% !important;
    }}
    .stButton > button:hover {{
        background-color: {text_color} !important;
        color: {color} !important;
        transform: translateY(-5px) scale(1.02) !important;
    }}
    
    /* Radio buttons container */
    .stRadio > div {{
        background-color: rgba(0, 0, 0, 0.25) !important;
        padding: 25px !important;
        border-radius: 20px !important;
        font-size: 24px !important;
        box-shadow: inset 0 0 10px rgba(0,0,0,0.5);
    }}
    
    /* Animations */
    @keyframes heartbeat {{
      0% {{ transform: scale(1); }} 14% {{ transform: scale(1.3); }} 28% {{ transform: scale(1); }}
      42% {{ transform: scale(1.3); }} 70% {{ transform: scale(1); }}
    }}
    .beating-heart {{ font-size: 150px; text-align: center; animation: heartbeat 1.5s infinite; display: block; margin: 40px 0; }}
    .giant-emoji {{ font-size: 80px !important; text-align: center; display: block; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

def safe_image(prompt):
    """Uses a free generative AI image endpoint to guarantee a beautiful, relevant holiday picture every time!"""
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=700&nologo=true"
    html = f'<img src="{url}" style="width:100%; max-height:500px; object-fit:cover; border-radius:25px; box-shadow: 0 15px 30px rgba(0,0,0,0.6); margin-bottom: 25px;">'
    st.markdown(html, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. 50 DESTINATIONS DATABASE (MASSIVE!)
# ---------------------------------------------------------
# Tags used for logic: hot, cold, mild, beach, city, nature, mountains, adventure, relax, luxury, budget, foodie, culture
destinations = {
    "Seychelles": {"tags": ["hot", "beach", "relax", "luxury"], "color": "#FF61A6", "prompt": "luxury beautiful seychelles beach resort ocean", 
                   "acts": ["Private beach dining with fresh lobster 🦞", "Couples jungle canopy spa 💆‍♀️", "Feeding giant Aldabra tortoises 🐢", "Yacht cruise with champagne 🥂", "Snorkeling with sea turtles 🐠", "Creole cooking class with local chef 🥘"]},
    "Maldives": {"tags": ["hot", "beach", "relax", "luxury"], "color": "#00CED1", "prompt": "maldives overwater bungalow crystal clear water", 
                 "acts": ["Sleeping in an overwater bungalow 🌊", "Dining in an underwater glass restaurant 🍽️", "Night swim with bioluminescent plankton ✨", "Private seaplane tour 🛩️", "Deep sea fishing for tuna 🎣", "Floating breakfast in infinity pool 🥞"]},
    "Bora Bora": {"tags": ["hot", "beach", "relax", "luxury"], "color": "#1E90FF", "prompt": "bora bora tropical island luxury", 
                  "acts": ["Swimming with friendly reef sharks 🦈", "Polynesian fire dancing show 🔥", "Helicopter ride over Mount Otemanu 🚁", "Drinking coconut cocktails on a private motu 🥥", "Jet skiing the turquoise lagoon 🚤", "Eating Tahitian Poisson Cru (raw fish) 🐟"]},
    "Fiji": {"tags": ["hot", "beach", "adventure", "nature"], "color": "#3CB371", "prompt": "fiji tropical jungle beach beautiful", 
             "acts": ["Taking a mud bath in the Sabeto Hot Springs 🌋", "Whitewater rafting the Upper Navua River 🚣", "Attending a traditional Kava ceremony 🥥", "Scuba diving the Great Astrolabe Reef 🤿", "Ziplining through the jungle canopy 🧗", "Eating Kokoda (Fijian ceviche) 🍋"]},
    "Amalfi Coast": {"tags": ["mild", "hot", "beach", "foodie", "luxury"], "color": "#FF8C00", "prompt": "amalfi coast italy cliffside colorful houses", 
                     "acts": ["Driving a vintage Vespa along the cliffs 🛵", "Private boat tour to the Blue Grotto 🚤", "Eating endless Neapolitan Pizza 🍕", "Limoncello tasting at a lemon farm 🍋", "Cliff jumping into the Mediterranean 🌊", "Shopping for handmade leather in Positano 👡"]},
    "Santorini": {"tags": ["hot", "beach", "relax", "culture"], "color": "#00008B", "prompt": "santorini greece white houses blue domes sunset", 
                  "acts": ["Watching the world's best sunset in Oia 🌅", "Wine tasting on a volcanic cliff 🍷", "Sailing on a luxury catamaran ⛵", "Eating fresh Feta and Moussaka 🥗", "Hiking the caldera trail 🥾", "Swimming in the hot springs 🌋"]},
    "Bali": {"tags": ["hot", "nature", "relax", "budget", "culture"], "color": "#2E8B57", "prompt": "bali indonesia rice terraces jungle temple", 
             "acts": ["Swinging over the Tegallalang Rice Terraces 🌴", "Sunrise hike up Mount Batur volcano 🌋", "Getting a traditional Balinese massage 💆", "Eating spicy Nasi Goreng at a street warung 🍛", "Surfing the waves in Uluwatu 🏄", "Visiting the sacred Monkey Forest 🐒"]},
    "Maui": {"tags": ["hot", "beach", "adventure", "nature"], "color": "#FF4500", "prompt": "maui hawaii tropical sunset surfing", 
             "acts": ["Driving the winding Road to Hana 🚗", "Attending a traditional Hawaiian Luau 🌺", "Snorkeling in the Molokini Crater 🐠", "Eating massive plates of Garlic Shrimp 🍤", "Helicopter tour over Jurassic waterfalls 🚁", "Surfing at Ho'okipa Beach 🏄"]},
    "Tokyo": {"tags": ["mild", "city", "foodie", "culture"], "color": "#FF003F", "prompt": "tokyo japan neon lights night city shibuya", 
              "acts": ["Mario Kart street racing through Shibuya 🏎️", "Eating at a weird Robot Restaurant 🤖", "Early morning VIP Tsukiji Sushi tour 🍣", "Singing karaoke in a private high-rise room 🎤", "Wagyu beef tasting in a hidden alley 🥩", "Playing VR in Akihabara 🕹️"]},
    "Kyoto": {"tags": ["mild", "city", "culture", "relax"], "color": "#8B0000", "prompt": "kyoto japan bamboo forest traditional temple", 
              "acts": ["Walking the Arashiyama Bamboo Forest 🎋", "Secret Geisha tea ceremony 🍵", "Staying in a traditional Ryokan with an Onsen ♨️", "Eating a multi-course Kaiseki dinner 🍱", "Renting Kimonos and walking the shrines 👘", "Tasting 10 types of Matcha 🌿"]},
    "New York City": {"tags": ["cold", "mild", "city", "foodie", "luxury"], "color": "#4682B4", "prompt": "new york city times square skyline night", 
                      "acts": ["Helicopter tour over Manhattan 🚁", "Eating massive NY slices of pizza 🍕", "Ice skating in Central Park ⛸️", "Watching a Broadway show from VIP seats 🎭", "Drinking martinis in a speakeasy 🍸", "Shopping spree on 5th Avenue 🛍️"]},
    "Paris": {"tags": ["mild", "city", "foodie", "luxury", "culture"], "color": "#C71585", "prompt": "paris france eiffel tower sunset romance", 
              "acts": ["Midnight boat cruise on the Seine ⛴️", "Eating warm croissants and escargot 🥐", "Private tour of the Louvre 🎨", "Drinking champagne at the top of the Eiffel Tower 🥂", "Shopping in luxury boutiques 👗", "Eating a Michelin-star dinner 🍽️"]},
    "London": {"tags": ["mild", "cold", "city", "culture"], "color": "#191970", "prompt": "london uk big ben thames river red bus", 
               "acts": ["Riding the London Eye at sunset 🎡", "Eating Fish & Chips in a historic pub 🍟", "Watching the Changing of the Guard 💂", "Having a luxurious High Tea 🫖", "Shopping at Harrods 🛍️", "Taking a Jack the Ripper ghost tour 👻"]},
    "Dubai": {"tags": ["hot", "city", "luxury", "adventure"], "color": "#D4AF37", "prompt": "dubai skyline burj khalifa luxury desert", 
              "acts": ["Skydiving over the Palm Islands 🪂", "Dune bashing in a luxury 4x4 🏜️", "Having a 24-karat gold steak 🥩", "Skiing indoors in the desert ⛷️", "Yacht party in the Marina 🛥️", "Riding camels at sunset 🐪"]},
    "Rome": {"tags": ["mild", "hot", "city", "foodie", "culture"], "color": "#A0522D", "prompt": "rome italy colosseum sunset ancient ruins", 
             "acts": ["Gladiator training school ⚔️", "Eating Carbonara and endless Gelato 🍝", "Tossing a coin in the Trevi Fountain 🪙", "Private tour of the Vatican 🇻🇦", "Riding a Vespa past the Colosseum 🛵", "Drinking espresso like a local ☕"]},
    "Barcelona": {"tags": ["mild", "hot", "city", "beach", "party"], "color": "#DC143C", "prompt": "barcelona spain sagrada familia colorful", 
                  "acts": ["Eating incredible Tapas and Paella 🥘", "Drinking Sangria on the beach 🍷", "Exploring the bizarre Park Güell 🦎", "Dancing till dawn at a beach club 💃", "Sailing the Mediterranean ⛵", "Watching a live Flamenco show 🎸"]},
    "Swiss Alps": {"tags": ["cold", "mountains", "adventure", "luxury"], "color": "#8B0000", "prompt": "swiss alps matterhorn snow cabin winter", 
                   "acts": ["Skiing massive slopes in Zermatt ⛷️", "Eating bubbling Cheese Fondue 🫕", "Taking the Glacier Express train 🚂", "Paragliding over snowy valleys 🪂", "Tasting unlimited Swiss Chocolate 🍫", "Soaking in a hot thermal bath while it snows ♨️"]},
    "Banff": {"tags": ["cold", "mountains", "nature", "adventure"], "color": "#2F4F4F", "prompt": "banff national park canada lake louise mountains", 
              "acts": ["Canoeing on the turquoise Lake Louise 🛶", "Hiking to the spectacular tea houses 🥾", "Spotting wild Grizzly Bears 🐻", "Eating Canadian Poutine 🍟", "Ice walking in Johnston Canyon 🧊", "Helicopter tour over the Rockies 🚁"]},
    "Patagonia": {"tags": ["cold", "mountains", "nature", "adventure"], "color": "#4682B4", "prompt": "patagonia mountains glacier rugged landscape", 
                  "acts": ["Trekking the massive Perito Moreno Glacier 🧊", "Hiking the base of Mount Fitz Roy ⛰️", "Eating traditional Argentine Asado (BBQ) 🥩", "Drinking Mate tea with Gauchos 🧉", "Kayaking through marble caves 🛶", "Spotting wild Pumas 🐆"]},
    "Antarctica": {"tags": ["cold", "nature", "adventure"], "color": "#000080", "prompt": "antarctica icebergs penguins extreme cold", 
                   "acts": ["Doing the freezing Polar Plunge 🥶", "Walking through a colony of Emperor Penguins 🐧", "Kayaking past massive blue icebergs 🛶", "Drinking whiskey chilled with glacier ice 🥃", "Spotting breaching Humpback Whales 🐋", "Camping overnight in a snow trench ⛺"]},
    "Iceland": {"tags": ["cold", "nature", "adventure", "relax"], "color": "#0B3D91", "prompt": "iceland northern lights volcano waterfall", 
                "acts": ["Exploring a glittering blue Ice Cave 🧊", "Floating in the VIP Blue Lagoon 🧖‍♀️", "Chasing the Northern Lights ✨", "Trying Fermented Shark (Hakarl) 🦈", "Snowmobiling across a glacier ❄️", "Hiking to a live erupting volcano 🔥"]},
    "Tromso": {"tags": ["cold", "nature", "adventure"], "color": "#000033", "prompt": "tromso norway snowy cabin northern lights", 
               "acts": ["Dog sledding with Siberian Huskies 🐕", "Feeding wild Reindeer 🦌", "Sleeping in an Ice Hotel 🧊", "Eating hearty Reindeer Stew 🍲", "Whale watching in the freezing fjords 🐋", "Sitting by a fire under the Aurora Borealis ✨"]},
    "Queenstown": {"tags": ["mild", "mountains", "adventure", "nature"], "color": "#556B2F", "prompt": "queenstown new zealand mountains lake extreme sports", 
                   "acts": ["Bungee jumping off the Kawarau Bridge 🪂", "Jet boating at 90km/h through canyons 🚤", "Skydiving over the Remarkables 🦅", "Eating the famous Fergburger 🍔", "Wine tasting in Central Otago 🍷", "Hiking the brutal Ben Lomond track 🥾"]},
    "Serengeti": {"tags": ["hot", "nature", "adventure", "luxury"], "color": "#CD853F", "prompt": "serengeti safari tanzania lions sunset plains", 
                  "acts": ["Hot air ballooning over the plains at dawn 🎈", "Open-top 4x4 Safari to spot Lions 🦁", "Staying in a luxury tented camp ⛺", "Eating dinner by a massive campfire 🥩", "Visiting a traditional Maasai village 🛖", "Spotting massive herds of elephants 🐘"]},
    "Madagascar": {"tags": ["hot", "nature", "adventure", "budget"], "color": "#228B22", "prompt": "madagascar baobab trees wild nature lemur", 
                   "acts": ["Night safari to spot elusive Aye-Ayes 🔦", "Sunset walk down Baobab Avenue 🌅", "Climbing the razor-sharp Tsingy rocks 🪨", "Trekking to find dancing Lemurs 🐒", "Eating Zebu Steak over a fire 🥩", "Snorkeling in Nosy Be 🏖️"]},
    "Costa Rica": {"tags": ["hot", "nature", "adventure", "relax"], "color": "#006400", "prompt": "costa rica jungle waterfall sloth volcano", 
                   "acts": ["Superman Ziplining 1000ft above the jungle 🧗", "Cuddling rescued Sloths 🦥", "Surfing in Tamarindo 🏄", "Bathing in Arenal's hot springs 🌋", "Eating Gallo Pinto and fresh ceviche 🍳", "Night hike to spot red-eyed tree frogs 🐸"]},
    "Amazon Rainforest": {"tags": ["hot", "nature", "adventure"], "color": "#004d00", "prompt": "amazon rainforest river jungle wild green", 
                          "acts": ["Fishing for terrifying Piranhas 🐟", "Riverboat cruise down the mighty Amazon ⛴️", "Spotting Pink River Dolphins 🐬", "Jungle survival training with an indigenous guide 🌿", "Eating exotic Amazonian fruits like Cupuaçu 🥥", "Night canoe trip to spot Caimans 🐊"]},
    "Galapagos": {"tags": ["hot", "nature", "adventure", "relax"], "color": "#20B2AA", "prompt": "galapagos islands giant tortoise pristine beach", 
                  "acts": ["Snorkeling with playful Sea Lions 🦭", "Walking alongside Giant Tortoises 🐢", "Scuba diving with Hammerhead Sharks 🦈", "Spotting blue-footed boobies 🐦", "Hiking a volcanic crater 🌋", "Eating fresh Ecuadorian ceviche 🐟"]},
    "Australian Outback": {"tags": ["hot", "nature", "adventure"], "color": "#B8860B", "prompt": "uluru australian outback red dirt kangaroo", 
                           "acts": ["Watching the sunset over Uluru rock 🌅", "Camping in a swag under a billion stars ✨", "Eating Kangaroo steak 🥩", "Off-roading in a massive 4x4 🚙", "Learning to throw a Boomerang 🪃", "Helicopter ride over the red desert 🚁"]},
    "Kruger National Park": {"tags": ["hot", "nature", "adventure", "luxury"], "color": "#8B4513", "prompt": "kruger national park south africa safari leopard", 
                             "acts": ["Tracking the Big 5 on foot 🦏", "Sleeping in a luxury treehouse 🌳", "Eating a traditional Braai BBQ 🥩", "Sunset game drive with gin and tonics 🍸", "Watching elephants drink from the river 🐘", "Spotting a leopard in a tree 🐆"]},
    "Peru (Inca Trail)": {"tags": ["mild", "mountains", "adventure", "culture"], "color": "#A0522D", "prompt": "machu picchu peru mountains ancient ruins", 
                          "acts": ["Hiking the grueling 4-day Inca Trail 🥾", "Taking selfies with Alpacas 🦙", "Eating world-class Peruvian Ceviche 🐟", "Sleeping in a glass pod hanging off a cliff 🧗", "Drinking Pisco Sours 🍹", "Exploring the Sacred Valley on mountain bikes 🚵"]},
    "Egypt (Pyramids)": {"tags": ["hot", "culture", "adventure"], "color": "#DAA520", "prompt": "egypt pyramids giza desert camels", 
                         "acts": ["Going inside the Great Pyramid 🔺", "Cruising down the Nile River 🚢", "Riding a camel through the desert 🐪", "Eating authentic Shawarma and Falafel 🥙", "Scuba diving in the Red Sea 🤿", "Exploring the Valley of the Kings 👑"]},
    "Petra": {"tags": ["hot", "culture", "adventure"], "color": "#CD5C5C", "prompt": "petra jordan ancient city red rocks", 
              "acts": ["Walking through the narrow Siq canyon 🚶", "Seeing the Treasury lit by thousands of candles ✨", "Floating effortlessly in the Dead Sea 🌊", "Eating massive plates of Mansaf 🍛", "Sleeping in a Bedouin desert camp in Wadi Rum ⛺", "Riding a 4x4 across the Martian desert 🚙"]},
    "Marrakesh": {"tags": ["hot", "city", "culture", "foodie"], "color": "#B22222", "prompt": "marrakesh morocco colorful market medina", 
                  "acts": ["Getting lost in the chaotic souks (markets) 🛍️", "Sleeping in a stunning traditional Riad 🕌", "Eating Tagine cooked in clay pots 🍲", "Getting a scrub in a local Hammam spa 🧼", "Drinking sweet Mint Tea 🍵", "Riding a hot air balloon over the Atlas Mountains 🎈"]},
    "Istanbul": {"tags": ["mild", "city", "culture", "foodie"], "color": "#483D8B", "prompt": "istanbul turkey grand bazaar mosques sunset", 
                 "acts": ["Exploring the massive Grand Bazaar 🏺", "Eating Turkish Delight and Baklava 🍯", "Taking a ferry across the Bosphorus ⛴️", "Eating a massive Turkish Kebab 🍖", "Smoking a hookah pipe in a cafe 💨", "Visiting the breathtaking Hagia Sophia 🕌"]},
    "Havana": {"tags": ["hot", "city", "culture", "party"], "color": "#C71585", "prompt": "havana cuba vintage cars colorful streets", 
               "acts": ["Riding in a bright pink 1950s convertible 🚗", "Smoking an authentic Cuban Cigar 💨", "Drinking Mojitos and Daquiris 🍹", "Dancing Salsa in the streets 💃", "Eating Ropa Vieja (shredded beef) 🍛", "Walking the Malecon seawall at sunset 🌅"]},
    "Angkor Wat": {"tags": ["hot", "culture", "nature", "adventure"], "color": "#556B2F", "prompt": "angkor wat cambodia ancient temple jungle", 
                   "acts": ["Watching the sunrise over the massive temple 🌅", "Exploring the Tomb Raider jungle ruins 🌿", "Eating Fish Amok curry 🍛", "Getting blessed by a Buddhist Monk 🙏", "Riding a tuk-tuk through the dirt roads 🛺", "Taking a boat through floating villages 🛶"]},
    "Kathmandu": {"tags": ["mild", "mountains", "adventure", "culture"], "color": "#8B0000", "prompt": "kathmandu nepal temples himalayas prayer flags", 
                  "acts": ["Helicopter tour to Everest Base Camp 🚁", "Eating massive plates of Momo dumplings 🥟", "Spinning prayer wheels at Swayambhunath 🛕", "Bungee jumping into a river gorge 🪂", "Shopping for pashminas in Thamel 🧣", "Trekking the Annapurna circuit 🥾"]},
    "Taj Mahal": {"tags": ["hot", "culture", "city", "foodie"], "color": "#FF4500", "prompt": "taj mahal india beautiful architecture sunset", 
                  "acts": ["Seeing the Taj Mahal at sunrise 🌅", "Eating insanely spicy Butter Chicken and Naan 🍛", "Riding a rickshaw through chaotic streets 🛺", "Attending a colorful Hindu festival 🎉", "Shopping for vibrant spices and silks 🌶️", "Seeing wild tigers in Ranthambore 🐅"]},
    "San Francisco": {"tags": ["mild", "city", "foodie", "culture"], "color": "#1E90FF", "prompt": "san francisco golden gate bridge cable car", 
                      "acts": ["Hanging off a moving Cable Car 🚃", "Eating clam chowder in a sourdough bowl 🦀", "Terrifying Alcatraz ghost tour 👻", "Biking across the Golden Gate Bridge 🚲", "Skydiving over the Bay 🪂", "Wine tasting in Napa Valley 🍷"]},
    "Las Vegas": {"tags": ["hot", "city", "party", "luxury"], "color": "#800080", "prompt": "las vegas neon lights casinos night", 
                  "acts": ["Gambling high stakes at the Bellagio 🎰", "Watching a Cirque du Soleil show 🎪", "Eating at a Gordon Ramsay restaurant 🥩", "Helicopter tour into the Grand Canyon 🚁", "Partying at a massive pool club 🍾", "Driving supercars on a racetrack 🏎️"]},
    "Miami": {"tags": ["hot", "beach", "party", "luxury"], "color": "#FF1493", "prompt": "miami south beach neon lights palm trees", 
              "acts": ["Sunbathing on South Beach 🏖️", "Riding an airboat through the Everglades looking for gators 🐊", "Eating Cuban sandwiches in Little Havana 🥪", "Clubbing until 6 AM 🪩", "Renting a luxury yacht 🛥️", "Rollerblading down Ocean Drive 🛼"]},
    "Yellowstone": {"tags": ["cold", "mild", "nature", "adventure"], "color": "#A0522D", "prompt": "yellowstone geyser bison nature rugged", 
                    "acts": ["Watching Old Faithful erupt 💦", "Spotting wild Bison and Wolves 🐺", "Hiking around the Grand Prismatic Spring 🌈", "Camping in the wilderness ⛺", "Eating campfire chili 🥣", "Fly fishing in freezing rivers 🎣"]},
    "Rio de Janeiro": {"tags": ["hot", "beach", "party", "culture"], "color": "#32CD32", "prompt": "rio de janeiro christ the redeemer beach sunset", 
                       "acts": ["Taking the cable car up Sugarloaf Mountain 🚠", "Sunning on Copacabana Beach 🏖️", "Dancing Samba at a street carnival 💃", "Eating endless meats at a Churrascaria 🥩", "Hang gliding over the city 🪂", "Drinking Caipirinhas by the ocean 🍹"]},
    "Phuket": {"tags": ["hot", "beach", "party", "budget"], "color": "#FF8C00", "prompt": "phuket thailand longtail boat beach limestone", 
               "acts": ["Partying at the Full Moon Festival 🌕", "Feeding rescued elephants 🐘", "Scuba diving with Whale Sharks 🦈", "Eating spicy Pad Thai on the street 🍜", "Getting a painful Thai massage 💆", "Taking a boat to Phi Phi Island 🛶"]},
    "Seoul": {"tags": ["mild", "city", "foodie", "culture"], "color": "#4B0082", "prompt": "seoul south korea neon lights palace", 
              "acts": ["Eating endless Korean BBQ 🥩", "Getting scrubbed at a Korean Bathhouse (Jjimjilbang) 🧖", "Singing K-Pop Karaoke 🎤", "Wearing traditional Hanboks at a palace 👘", "Drinking Soju in a street tent 🍶", "Shopping for high-end skincare 🧴"]},
    "Singapore": {"tags": ["hot", "city", "luxury", "foodie"], "color": "#8B008B", "prompt": "singapore marina bay sands supertrees", 
                  "acts": ["Swimming in the Marina Bay Sands infinity pool 🏊", "Eating Michelin-star street food 🍜", "Walking through the glowing Supertree Grove 🌳", "Drinking a Singapore Sling 🍹", "Night safari at the zoo 🐅", "Shopping in luxury mega-malls 🛍️"]},
    "Cape Town": {"tags": ["mild", "beach", "adventure", "nature"], "color": "#CD853F", "prompt": "cape town table mountain ocean sunset", 
                  "acts": ["Cage diving with Great White Sharks 🦈", "Hiking up Table Mountain ⛰️", "Walking with wild penguins at Boulders Beach 🐧", "Wine tasting in Stellenbosch 🍷", "Eating South African Biltong 🥩", "Paragliding over the coastline 🪂"]},
    "Amsterdam": {"tags": ["mild", "city", "culture", "party"], "color": "#FF4500", "prompt": "amsterdam canals bicycles sunset houses", 
                  "acts": ["Renting a bike and dodging traffic 🚲", "Taking a canal boat cruise 🛶", "Eating warm Stroopwafels 🧇", "Visiting the Van Gogh Museum 🎨", "Exploring the nightlife 🍻", "Eating massive Gouda cheese wheels 🧀"]},
    "Tulum": {"tags": ["hot", "beach", "party", "culture"], "color": "#20B2AA", "prompt": "tulum mexico beach cenote ancient ruins", 
              "acts": ["Swimming in underground crystal Cenotes 🤿", "Exploring ancient Mayan beach ruins 🏛️", "Eating massive plates of street Tacos 🌮", "Drinking Mezcal at a jungle rave 🍸", "Yoga on the beach at sunrise 🧘", "Swimming with giant sea turtles 🐢"]}
}

# ---------------------------------------------------------
# 3. 20 QUESTIONS ENGINE
# ---------------------------------------------------------
# We use tags to build a profile. Each answer adds points to specific tags.
questions = [
    {"q": "1. What is your absolute ideal morning? 🌅", "opts": {"Sleeping in until noon on 1000-thread count sheets": {"luxury": 3, "relax": 3, "adventure": -2}, "Up at 5 AM, putting on war paint, ready to conquer": {"adventure": 3, "nature": 2, "relax": -2}, "Grabbing an artisanal coffee and hitting busy streets": {"city": 3, "culture": 2, "nature": -1}}},
    {"q": "2. Pick an animal companion for the trip 🐾", "opts": {"A cuddly baby sea turtle": {"beach": 3, "nature": 1}, "A mischievous monkey or lemur": {"nature": 3, "adventure": 1, "hot": 1}, "A fluffy waddling penguin or husky": {"cold": 4, "nature": 2}, "A stray cat outside a cafe": {"city": 2, "culture": 1}}},
    {"q": "3. How do you feel about extreme heights? 🎢", "opts": {"Love them! Throw me out of a plane right now!": {"adventure": 3, "mountains": 1}, "Only if I'm safely looking out a high-rise window": {"city": 2, "luxury": 1}, "Keep my feet firmly on the ground, thanks": {"relax": 2, "beach": 1}}},
    {"q": "4. Pick a flavor profile that makes you drool! 👅", "opts": {"Fresh, tropical, sweet, and fruity": {"hot": 2, "beach": 2}, "Savory, rich, carb-heavy, and comforting": {"mild": 2, "cold": 1, "foodie": 3}, "Spicy, exotic, and totally weird": {"foodie": 3, "culture": 2}, "High-end, expensive, Michelin-star meats": {"luxury": 3, "foodie": 1}}},
    {"q": "5. What’s your ideal footwear for this trip? 👟", "opts": {"Barefoot or designer flip flops": {"beach": 4, "hot": 2}, "Heavy duty, mud-covered hiking boots": {"mountains": 3, "nature": 2, "adventure": 2}, "Stylish sneakers for walking 20k steps": {"city": 3, "culture": 1}, "Thick thermal insulated snow boots": {"cold": 4, "mountains": 1}}},
    {"q": "6. Choose a magical item to take with you ✨", "opts": {"Invisibility cloak (for epic people watching)": {"city": 2, "culture": 2}, "A teleportation ring (to skip the grueling hike)": {"relax": 3, "luxury": 1}, "An endless bottle of perfect vintage wine": {"foodie": 2, "relax": 1, "mild": 1}, "A magic amulet that keeps you perfectly warm": {"cold": 3, "adventure": 1}}},
    {"q": "7. What’s your evening vibe? 🌙", "opts": {"Dancing until dawn under neon lights or beach fires": {"party": 4, "city": 1, "beach": 1}, "A wildly romantic candlelit dinner by the water": {"luxury": 2, "relax": 2}, "Staring at the Milky Way by a campfire": {"nature": 3, "adventure": 1}, "Passing out from sheer physical exhaustion": {"adventure": 3, "mountains": 1}}},
    {"q": "8. Weather preference? ☀️❄️", "opts": {"Roasting hot, give me a deep tan": {"hot": 4, "cold": -4}, "Brisk and freezing, I want snow and ice": {"cold": 4, "hot": -4}, "Mild, breezy, and perfect for a light jacket": {"mild": 4, "hot": -1, "cold": -1}}},
    {"q": "9. How do you handle getting lost? 🗺️", "opts": {"Panic slightly but find a cute cafe": {"city": 2, "mild": 1}, "Ask locals and end up at a crazy underground party": {"party": 3, "culture": 2}, "I don't get lost, I go on survival adventures": {"adventure": 3, "nature": 2}, "I literally can't get lost, I have a private butler": {"luxury": 4, "adventure": -2}}},
    {"q": "10. Pick a movie genre for your life right now 🎬", "opts": {"Romantic Comedy in a beautiful dress": {"city": 2, "relax": 1, "luxury": 1}, "High-Octane Action / Thriller": {"adventure": 3, "party": 1}, "Sci-Fi / Cyberpunk / Futuristic": {"city": 3, "culture": 1}, "Epic Fantasy / Lord of the Rings": {"mountains": 3, "nature": 2}}},
    {"q": "11. Choose a baller mode of transport 🚀", "opts": {"A Mega Luxury Yacht": {"luxury": 3, "beach": 2, "hot": 1}, "A Private Helicopter over mountains": {"mountains": 3, "luxury": 2, "cold": 1}, "A 300mph Bullet Train": {"city": 3, "culture": 1}, "A rugged 4x4 Jeep covered in mud": {"adventure": 3, "nature": 2, "hot": 1}}},
    {"q": "12. How much luggage are you bringing? 🧳", "opts": {"Just a dusty backpack, keep it rugged": {"adventure": 3, "budget": 3, "luxury": -3}, "One perfectly curated stylish suitcase": {"city": 2, "mild": 1}, "Three massive trunks of designer outfits": {"luxury": 4, "relax": 1, "budget": -3}}},
    {"q": "13. Pick a historical era to visit 🕰️", "opts": {"Ancient Empires (Samurai, Romans, Incas)": {"culture": 4, "city": 1}, "The Wild, Untamed Prehistoric Age": {"nature": 4, "adventure": 2}, "The glamorous roaring 1920s": {"city": 2, "luxury": 2, "party": 1}, "The distant, shiny Cyber-Future": {"city": 3, "luxury": 1}}},
    {"q": "14. What's your budget style? 💸", "opts": {"Unlimited wealth. Spoil me rotten.": {"luxury": 5, "budget": -5}, "A healthy mix of cheap street food and one fancy splurge": {"foodie": 3, "culture": 1}, "I just need a tent, some rice, and good vibes": {"budget": 5, "nature": 2, "luxury": -5}}},
    {"q": "15. Water or Land? 🌊🌍", "opts": {"Oceans, lakes, and rivers! Get me wet!": {"beach": 4}, "Mountains, forests, and towering cities!": {"mountains": 2, "city": 2}, "A perfect mix of both!": {"nature": 2, "relax": 1}}},
    {"q": "16. Choose a color palette to look at 🎨", "opts": {"Blinding Neon pinks and bright blues": {"city": 2, "party": 2}, "Earthy jungle greens and dirt browns": {"nature": 3, "adventure": 1}, "Ocean blues and golden sunset oranges": {"beach": 3, "relax": 2}, "Blinding icy whites and dark blacks": {"cold": 4, "mountains": 2}}},
    {"q": "17. Pick a travel snack right now 🥨", "opts": {"A freshly baked, warm, flaky pastry": {"city": 2, "culture": 1, "foodie": 1}, "A massive plate of exotic tropical fruit": {"hot": 2, "beach": 1}, "A hardcore energy bar or trail mix": {"adventure": 3, "mountains": 2}, "Matcha KitKats or crazy flavored chips": {"city": 2, "culture": 2}}},
    {"q": "18. What's your absolute worst nightmare on holiday? 😱", "opts": {"No WiFi or cell service for days": {"city": 3, "luxury": 1}, "Getting a terrible sunburn": {"cold": 2, "mild": 2, "beach": -2}, "A wild venomous animal in my tent": {"city": 2, "nature": -3}, "Freezing my toes off": {"hot": 4, "cold": -4}}},
    {"q": "19. Choose a sound to fall asleep to 🎧", "opts": {"Crashing warm ocean waves": {"beach": 4, "relax": 2}, "Jungle insects and distant animal roars": {"nature": 4, "hot": 1}, "City traffic, sirens, and train hums": {"city": 4, "culture": 1}, "Fierce howling blizzard winds": {"cold": 4, "mountains": 2}}},
    {"q": "20. Finally, what is the ULTIMATE goal of this trip? 🎯", "opts": {"To relax so hard I forget my own name": {"relax": 5, "adventure": -3}, "To push my physical limits and feel alive": {"adventure": 5, "relax": -3}, "To eat absolutely EVERYTHING in sight": {"foodie": 5}, "To take insane photos and show off": {"luxury": 2, "party": 2, "culture": 1}}},
]

# ---------------------------------------------------------
# 4. STATE MANAGEMENT & ENGINE LOGIC
# ---------------------------------------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.q_index = 0
    st.session_state.user_profile = {tag: 0 for tag in ["hot", "cold", "mild", "beach", "city", "nature", "mountains", "adventure", "relax", "luxury", "budget", "foodie", "culture", "party"]}
    st.session_state.available_dests = list(destinations.keys())
    st.session_state.chosen_dest = None
    st.session_state.activities = []
    st.session_state.activity_round = 0
    st.session_state.current_activity_pool = []

def set_stage(new_stage):
    st.session_state.stage = new_stage

def handle_answer(selected_option):
    # Apply tags weights to user profile
    weights = questions[st.session_state.q_index]["opts"][selected_option]
    for tag, value in weights.items():
        st.session_state.user_profile[tag] += value
    
    st.session_state.q_index += 1
    
    # Trigger Stick or Risk exactly at Question 10
    if st.session_state.q_index == 10:
        set_stage('stick_or_risk')
    elif st.session_state.q_index >= len(questions):
        calculate_final_match()
        set_stage('final_match_reveal')

def get_best_match():
    best_score = -9999
    best_dest = None
    
    # Shuffle available to prevent alphabetical bias on ties
    random.shuffle(st.session_state.available_dests)
    
    for dest in st.session_state.available_dests:
        tags = destinations[dest]["tags"]
        score = sum([st.session_state.user_profile[t] for t in tags])
        if score > best_score:
            best_score = score
            best_dest = dest
            
    return best_dest

def stick_choice():
    # User decided to stick with the halfway match
    st.session_state.chosen_dest = get_best_match()
    load_activities()
    set_stage('activity_selection')

def risk_choice():
    # Throw away current best match and continue!
    current_best = get_best_match()
    st.session_state.available_dests.remove(current_best)
    set_stage('questions')

def calculate_final_match():
    st.session_state.chosen_dest = get_best_match()
    load_activities()

def load_activities():
    acts = destinations[st.session_state.chosen_dest]["acts"]
    # Grab exactly 6 activities for 3 Tinder rounds
    st.session_state.current_activity_pool = random.sample(acts, 6)

def pick_activity(act):
    st.session_state.activities.append(act)
    st.session_state.activity_round += 1
    if st.session_state.activity_round >= 3:
        set_stage('final_itinerary')

# ---------------------------------------------------------
# 5. UI RENDERING
# ---------------------------------------------------------

if st.session_state.stage == 'welcome':
    set_bg("#1E1E1E", "#00FF7F") # Dark with neon green
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='giant-emoji'>✈️🌍✨</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 65px; font-weight: 900;'>The Ultimate Holiday Finder</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; text-align: center; margin: 20px auto; max-width: 800px;'>
    <h3 style='margin-bottom: 20px;'>Here is how it works:</h3>
    <p style='font-size: 22px;'>1. You will answer <b>20 psychological travel questions</b>.</p>
    <p style='font-size: 22px;'>2. Our engine will filter through <b>50 global destinations</b> to find your exact match.</p>
    <p style='font-size: 22px;'>3. Halfway through, you will get a <b>Stick or Risk</b> offer.</p>
    <p style='font-size: 22px;'>4. Finally, you will swipe to pick your perfect activities!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("LET'S GO! 🚀", on_click=set_stage, args=('questions',))
    st.balloons()

elif st.session_state.stage == 'questions':
    set_bg("#2C3E50", "#FFFFFF") # Deep slate blue
    q_data = questions[st.session_state.q_index]
    
    st.markdown(f"<h1 style='font-size: 45px; text-align: center;'>{q_data['q']}</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Render radio button options
    options = list(q_data["opts"].keys())
    choice = st.radio("👇 Click your vibe:", options, index=0)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("LOCK IT IN! 🔒➡️", on_click=handle_answer, args=(choice,))
    
    st.progress(st.session_state.q_index / 20)

elif st.session_state.stage == 'stick_or_risk':
    # Question 10 Pause
    best_dest = get_best_match()
    dest_data = destinations[best_dest]
    set_bg(dest_data["color"], "#FFFFFF")
    
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>🚨 HALFWAY POINT! 🚨</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        safe_image(dest_data["prompt"])
    
    with col2:
        st.markdown(f"<h2 style='font-size: 45px;'>Right now, you are matching perfectly with: <br><u style='font-size: 60px;'>{best_dest}</u></h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 25px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;'>Imagine: {random.choice(dest_data['acts'])}</p>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 30px;'>Do you want to STICK with this holiday, or RISK it for something else?</h3>", unsafe_allow_html=True)
        st.markdown("<p><i>(Warning: If you RISK, this destination goes in the bin forever!)</i></p>", unsafe_allow_html=True)
        
        sub1, sub2 = st.columns(2)
        with sub1:
            st.button("😍 STICK! TAKE ME HERE!", on_click=stick_choice)
        with sub2:
            st.button("🎲 RISK! KEEP ASKING!", on_click=risk_choice)

elif st.session_state.stage == 'final_match_reveal':
    # Exciting Reveal screen
    best_dest = st.session_state.chosen_dest
    dest_data = destinations[best_dest]
    set_bg(dest_data["color"], "#FFFFFF")
    
    # Conditional animations
    if "cold" in dest_data["tags"]:
        st.snow()
    else:
        st.balloons()
        
    st.markdown("<h1 style='text-align: center; font-size: 80px; text-transform: uppercase;'>🎉 WE'VE FOUND YOU A MATCH! 🎉</h1>", unsafe_allow_html=True)
    
    safe_image(dest_data["prompt"])
    
    st.markdown(f"<h1 style='text-align: center; font-size: 100px; font-weight: 900;'>{best_dest}!</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("PICK MY ACTIVITIES! ➡️", on_click=set_stage, args=('activity_selection',))

elif st.session_state.stage == 'activity_selection':
    best_dest = st.session_state.chosen_dest
    dest_data = destinations[best_dest]
    set_bg(dest_data["color"], "#FFFFFF")
    
    rnd = st.session_state.activity_round
    act1 = st.session_state.current_activity_pool[rnd * 2]
    act2 = st.session_state.current_activity_pool[(rnd * 2) + 1]
    
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>Build your {best_dest} Itinerary! 📅</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Tinder Rules: You can only KEEP ONE of these activities. The other is thrown in the trash.</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: center;'>Round {rnd + 1} of 3</h4><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 40px; border-radius: 20px; height: 200px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act1}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ KEEP THIS ONE", key=f"btn1_{rnd}", on_click=pick_activity, args=(act1,))
        
    with col2:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 40px; border-radius: 20px; height: 200px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act2}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ NO, KEEP THIS ONE", key=f"btn2_{rnd}", on_click=pick_activity, args=(act2,))

elif st.session_state.stage == 'final_itinerary':
    best_dest = st.session_state.chosen_dest
    dest_data = destinations[best_dest]
    set_bg(dest_data["color"], "#FFFFFF")
    
    if "cold" in dest_data["tags"]:
        st.snow()
    else:
        st.balloons()
    
    st.markdown("<h1 style='text-align: center; font-size: 70px; font-weight: 900;'>🎊 PACK YOUR BAGS! 🎊</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        safe_image(dest_data["prompt"])
    
    with col2:
        st.markdown(f"<h2 style='font-size: 60px; text-decoration: underline;'>📍 {best_dest}</h2>", unsafe_allow_html=True)
        st.markdown("<h3>Your Hand-Picked Ultimate Itinerary:</h3>", unsafe_allow_html=True)
        
        for act in st.session_state.activities:
            st.markdown(f"<div style='background-color: rgba(255,255,255,0.25); padding: 20px; margin-bottom: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'><h3 style='margin:0;'>🌟 {act}</h3></div>", unsafe_allow_html=True)
            
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .twist-btn > button {
        background-color: #FF0000 !important; color: white !important; border: none !important; animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1.0); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(255, 0, 0, 0); }
        100% { transform: scale(1.0); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); }
    }
    </style>
    """, unsafe_allow_html=True)
    
    col_x, col_y, col_z = st.columns([1, 2, 1])
    with col_y:
        st.markdown("<div class='twist-btn'>", unsafe_allow_html=True)
        st.button("CLICK FOR ONE MORE SURPRISE... 👀", on_click=set_stage, args=('twist',))
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.stage == 'twist':
    set_bg("#000000", "#FFFFFF")
    
    st.markdown("<div class='beating-heart'>❤️</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>Do you love Damien?</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns([1, 2, 2, 1])
    with col2:
        st.button("YES", on_click=lambda: setattr(st.session_state, 'twist_ans', 'yes') or set_stage('twist_result'))
    with col3:
        st.button("NO", on_click=lambda: setattr(st.session_state, 'twist_ans', 'no') or set_stage('twist_result'))

elif st.session_state.stage == 'twist_result':
    set_bg("#000000", "#FFFFFF")
    st.markdown("<div class='giant-emoji' style='margin-top: 50px;'>❤️</div>", unsafe_allow_html=True)
    
    if st.session_state.twist_ans == "yes":
        st.markdown("<h1 style='text-align: center; font-size: 80px; color: #FF1493 !important;'>I love you too Katie bear 🐻</h1>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("<h1 style='text-align: center; font-size: 80px; color: #FF1493 !important;'>I love you too Katie bear 🐻</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; font-size: 50px; color: #FFFFFF !important;'>...but enjoy your holiday on your own 😜</h2>", unsafe_allow_html=True)
