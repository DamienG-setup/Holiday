import streamlit as st
import random
import urllib.parse
from collections import Counter

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & INSANE CSS
# ---------------------------------------------------------
st.set_page_config(page_title="The Ultimate Holiday Finder ✈️", page_icon="🌍", layout="wide")

def set_bg(color, text_color):
    css = f"""
<style>
    .stApp {{ background-color: {color} !important; color: {text_color} !important; transition: background-color 0.8s ease-in-out; }}
    h1, h2, h3, h4, p, span, label, div {{ color: {text_color} !important; font-family: 'Arial', sans-serif; }}
    .stButton > button {{
        background-color: rgba(255, 255, 255, 0.15) !important; color: {text_color} !important;
        border: 2px solid {text_color} !important; border-radius: 20px !important;
        font-size: 22px !important; font-weight: 900 !important; padding: 15px 30px !important;
        transition: all 0.3s ease-in-out !important; box-shadow: 0 8px 15px rgba(0,0,0,0.3) !important; width: 100% !important;
    }}
    .stButton > button:hover {{ background-color: {text_color} !important; color: {color} !important; transform: translateY(-5px) scale(1.02) !important; }}
    .stRadio > div {{ background-color: rgba(0, 0, 0, 0.3) !important; padding: 25px !important; border-radius: 20px !important; font-size: 24px !important; }}
    .cheeky-text {{ font-size: 24px !important; font-style: italic; color: #FFD700 !important; text-align: center; margin-bottom: 30px; background: rgba(0,0,0,0.5); padding: 10px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
    @keyframes heartbeat {{ 0% {{ transform: scale(1); }} 14% {{ transform: scale(1.3); }} 28% {{ transform: scale(1); }} 42% {{ transform: scale(1.3); }} 70% {{ transform: scale(1); }} }}
    .beating-heart {{ font-size: 150px; text-align: center; animation: heartbeat 1.5s infinite; display: block; margin: 40px 0; }}
</style>
"""
    st.markdown(css, unsafe_allow_html=True)

def safe_image(prompt):
    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=1200&height=700&nologo=true"
    html = f'<img src="{url}" style="width:100%; max-height:500px; object-fit:cover; border-radius:25px; box-shadow: 0 15px 30px rgba(0,0,0,0.6); margin-bottom: 25px;">'
    st.markdown(html, unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. MASSIVE COMPRESSED DATABASE (Prevents GitHub Crashes)
# ---------------------------------------------------------
# Format: Name, Tags, Color, Prompt, Food(2), Drinks(2), Cute(2), Epic(6)
raw_dests = [
    ("Paris", "mild,city,culture,foodie,luxury,romance", "#C71585", "paris eiffel tower sunset romance",
     "Michelin-star dinner at Le Jules Verne|Fresh savory crepes from a street vendor in Montmartre",
     "Champagne atop the Eiffel Tower|Absinthe in a hidden 1920s speakeasy",
     "Painting class along the Seine|Finding hidden bookstores in the Latin Quarter",
     "Private helicopter over Versailles|VIP night tour of the Louvre|Secret access to the underground Catacombs|Baking class with a master patissier|Seine dinner cruise on a private yacht|Attending a cabaret at Moulin Rouge"),
    
    ("Rome", "mild,hot,city,culture,foodie", "#A0522D", "rome colosseum ancient sunset",
     "10-course truffle tasting menu|Massive slice of Roman pizza al taglio",
     "Vintage Barolo wine tasting in an ancient cellar|Aperol Spritz overlooking Piazza Navona",
     "Throwing a coin in the Trevi Fountain at midnight|Eating gelato on the Spanish Steps",
     "Gladiator training school on the Appian Way|Private after-hours tour of the Sistine Chapel|Vespa tour through the chaotic Roman traffic|Exploring the ancient crypts made of bones|Pasta making class with a real Italian Nonna|Helicopter tour over the ancient ruins"),
    
    ("Swiss Alps", "cold,mountains,adventure,luxury,nature", "#8B0000", "zermatt matterhorn snow cabin",
     "Gourmet dining at a 5-star high-altitude restaurant|Massive pot of bubbling cheese fondue in a wooden chalet",
     "Dom Pérignon in an outdoor heated jacuzzi|Hot spiced Glühwein by a roaring fire",
     "Building a snowman overlooking the Matterhorn|Riding a horse-drawn sleigh through the village",
     "Helicopter drop-off for extreme off-piste skiing|Paragliding over the snowy peaks|Ice climbing up a frozen waterfall|Riding the Glacier Express train|Sleeping in an actual Igloo Village|Bungee jumping off a dam like James Bond"),
    
    ("Santorini", "hot,beach,relax,luxury,romance", "#00008B", "santorini white houses blue domes sunset",
     "Private clifftop dining with fresh lobster|Gyros from a bustling local taverna",
     "Wine tasting in a volcanic cave vineyard|Cocktails on a luxury catamaran at sunset",
     "Wandering the white cobblestone streets of Oia|Finding a secluded spot for the perfect sunset photo",
     "Sailing a yacht to the volcanic hot springs|Scuba diving in the deep caldera|Helicopter ride over the Greek Islands|Renting ATVs to explore hidden black sand beaches|Private photoshoot with flying dresses|Exploring the ancient ruins of Akrotiri"),
    
    ("London", "mild,cold,city,culture,party", "#191970", "london big ben red bus thames",
     "High-end dining at The Shard|Classic Fish & Chips wrapped in paper at a pub",
     "Cocktails at the eccentric Sketch bar|Pints of ale in a 400-year-old tavern",
     "Feeding the pelicans in St. James's Park|Browsing quirky antiques at Portobello Road",
     "VIP pod on the London Eye with champagne|Private Jack the Ripper night walking tour|Climbing over the top of the O2 Arena|Attending a West End theatre premiere|Speedboating down the River Thames|Touring the hidden underground Churchill War Rooms"),

    ("Amalfi Coast", "hot,beach,foodie,luxury,romance", "#FF8C00", "amalfi coast cliffside colorful houses",
     "Michelin-star seafood overlooking the cliffs|Massive Neapolitan pizza in a local piazza",
     "Limoncello tasting straight from a lemon farm|Prosecco on a private vintage wooden boat",
     "Shopping for handmade leather sandals|Eating lemon sorbet inside a real giant lemon",
     "Driving a vintage convertible along the coastal roads|Swimming into the sparkling Blue Grotto|Helicopter tour of Mount Vesuvius|Hiking the breathtaking Path of the Gods|Private cooking class in a cliffside villa|Chartering a yacht to the island of Capri"),

    ("Iceland", "cold,nature,adventure,relax", "#0B3D91", "iceland northern lights glacier waterfalls",
     "High-end Nordic tasting menu|Trying fermented shark and a street hot dog",
     "Brennivín shots in an ice bar|Blue lagoon cocktails floating in thermal water",
     "Petting fluffy Icelandic horses|Searching for hidden elf houses in the rocks",
     "Exploring deep inside a glittering blue Ice Cave|Snowmobiling across a massive glacier|Chasing the Northern Lights in a Super-Jeep|Snorkeling between two tectonic plates in freezing water|Hiking up to a live, flowing volcano|Walking behind the roaring Seljalandsfoss waterfall"),

    ("Amsterdam", "mild,city,culture,party", "#FF4500", "amsterdam canals bicycles sunset",
     "Gourmet Dutch tasting menu in a greenhouse|Eating hot Stroopwafels fresh off the iron",
     "Heineken VIP brewing experience|Jenever tasting in a dimly lit 17th-century tasting room",
     "Browsing the floating flower market|Having a picnic in Vondelpark",
     "Renting a private canal boat with endless drinks|Cycling through the tulip fields of Keukenhof|Exploring the secret annex of Anne Frank|Partying at a massive underground techno warehouse|Touring the bizarre and wild Red Light District|Eating a massive wheel of authentic Gouda cheese"),

    ("Barcelona", "hot,city,beach,party,culture", "#DC143C", "barcelona sagrada familia colorful gaudi",
     "Avant-garde molecular gastronomy|Endless massive pans of seafood Paella",
     "Sangria tasting on a luxury rooftop|Cava in a historic underground cellar",
     "Finding the hidden mosaics in Park Güell|Watching street performers on La Rambla",
     "Sailing a catamaran on the Mediterranean at sunset|VIP tour of the unfinished Sagrada Familia|Attending a live, passionate Flamenco show|Helicopter ride over the coastline|Dancing until 6 AM at a massive beach club|Taking a hot air balloon over Catalonia"),

    ("Venice", "mild,city,romance,culture", "#008080", "venice canals gondola sunset romance",
     "Romantic seafood dinner on a floating terrace|Venetian tapas in a crowded local bacaro",
     "Bellinis at the famous Harry's Bar|Spritz in St. Mark's Square listening to the orchestra",
     "Getting lost in the tiny alleyways|Watching a glassblower in Murano",
     "Private sunset Gondola ride with a serenader|Attending a masquerade ball in a grand palazzo|Kayaking through the quiet, hidden canals|VIP tour of the Doge's Palace secret passages|Taking a water taxi across the lagoon at high speed|Making your own authentic Carnival mask"),

    ("Tokyo", "mild,city,foodie,culture,party", "#FF003F", "tokyo neon night city shibuya",
     "$500 Omakase sushi masterclass|Slurping rich Tonkotsu ramen in a tiny booth",
     "High-end whiskey in a slick sky-bar|Sake in a tiny, smoky Golden Gai alley bar",
     "Playing claw machines in an arcade|Petting hedgehogs at an animal cafe",
     "Real-life Mario Kart racing through Shibuya crossing|Watching a brutal sumo wrestling tournament live|Attending the insane, flashy Robot Restaurant show|Exploring digital art at teamLab Planets|Singing Karaoke in a private room with endless drinks|Taking a helicopter tour over the neon skyline"),

    ("Kyoto", "mild,city,culture,relax", "#8B0000", "kyoto japan bamboo forest temple",
     "Multi-course exquisite Kaiseki dinner|Eating green tea soft serve on the street",
     "Secret Geisha tea ceremony|Tasting 20 different types of Matcha",
     "Walking the magical Arashiyama Bamboo Forest|Feeding the bowing deer in nearby Nara",
     "Sleeping in a traditional Ryokan on tatami mats|Bathing naked in a natural outdoor Onsen|Renting kimonos and walking the red Torii gates of Fushimi Inari|Learning to swing a katana with a Samurai master|Meditating with Zen monks at dawn|Attending a vibrant traditional matsuri festival"),

    ("Bali", "hot,beach,nature,relax,budget", "#228B22", "bali indonesia rice terraces jungle sunset",
     "Fine dining in a bamboo jungle restaurant|Eating spicy Nasi Goreng at a cheap local warung",
     "Cocktails at a luxurious cliffside beach club|Bintang beer while sitting on a beanbag on the sand",
     "Taking a picture on the massive Bali Swing|Getting blessed in a holy water temple",
     "Hiking Mount Batur in the dark for sunrise|Surfing the world-class waves of Uluwatu|Scuba diving a WWII shipwreck in Tulamben|Getting a brutal but amazing 2-hour Balinese massage|White water rafting down the Ayung River|Riding a scooter through lush green rice terraces"),

    ("Maldives", "hot,beach,relax,luxury,romance", "#00CED1", "maldives overwater bungalow crystal ocean",
     "Dining in an all-glass underwater restaurant|Private beach BBQ cooked by a personal chef",
     "Champagne delivered to your pool via floating tray|Coconut cocktails on a deserted sandbank",
     "Watching a movie at an outdoor jungle cinema|Night swim with glowing bioluminescent plankton",
     "Sleeping in a massive luxury overwater bungalow|Taking a private seaplane over the atolls|Scuba diving with massive, gentle Manta Rays|Deep sea fishing for Yellowfin Tuna|Submarine tour of the vibrant coral reefs|Couples spa day on a glass floor over the ocean"),

    ("Phuket", "hot,beach,party,budget,adventure", "#FF8C00", "phuket thailand longtail boat limestone cliffs",
     "Gourmet Thai fusion on a cliff edge|Eating insanely spicy Pad Thai from a street cart",
     "VIP table at an insane beach club|Drinking cheap buckets of liquor on Bangla Road",
     "Getting a cheap, aggressive Thai foot massage|Shopping at the chaotic weekend night market",
     "Partying until dawn at the Full Moon Party|Bathing and feeding rescued elephants in a sanctuary|Taking a longtail boat to James Bond Island|Scuba diving with massive Whale Sharks|Watching a brutal live Muay Thai boxing match|Ziplining through the dense tropical jungle"),

    ("New York City", "mild,cold,city,foodie,luxury,culture", "#4682B4", "new york city times square skyline",
     "$1000 tasting menu at Per Se|Eating a massive, greasy $2 slice of NY pizza",
     "Martinis in a high-end hidden speakeasy|Drinking cheap beers at a gritty dive bar",
     "Ice skating in Central Park|Walking the High Line elevated park",
     "Taking a helicopter doors-off tour over Manhattan|Watching a smash-hit Broadway musical from VIP seats|Attending a crazy underground warehouse party in Brooklyn|Shopping spree on 5th Avenue|Eating massive pastrami sandwiches at Katz's Deli|Watching the ball drop in Times Square on New Year's"),

    ("Las Vegas", "hot,city,party,luxury", "#800080", "las vegas neon casinos strip night",
     "Eating at Gordon Ramsay's Hell's Kitchen|Eating at a massive, endless 24-hour casino buffet",
     "Bottle service at a mega-club like Omnia|Drinking massive frozen margaritas out of a plastic yard glass",
     "Watching the Bellagio Fountains dance|Riding the gondolas inside the Venetian",
     "Gambling high stakes in a VIP casino room|Taking a helicopter tour into the Grand Canyon|Watching a mind-bending Cirque du Soleil show|Driving supercars on a professional racetrack|Partying at a massive daytime pool club|Getting married by an Elvis impersonator"),

    ("Yellowstone", "cold,mild,nature,adventure,mountains", "#A0522D", "yellowstone geyser bison rugged nature",
     "Gourmet game meat (elk/bison) at a luxury lodge|Eating campfire chili out of a tin can",
     "Craft beer tasting in a cowboy saloon|Drinking cowboy coffee boiled over a fire",
     "Watching Old Faithful erupt on schedule|Spotting adorable bear cubs through binoculars",
     "Snowmobiling through the park in dead of winter|Spotting packs of wild wolves in the Lamar Valley|Hiking around the neon-colored Grand Prismatic Spring|Camping deep in grizzly bear country|Fly fishing in freezing, crystal-clear rivers|Whitewater rafting down the Snake River"),

    ("Costa Rica", "hot,nature,adventure,relax,beach", "#006400", "costa rica jungle waterfall sloth volcano",
     "Gourmet dining at a luxury eco-resort|Eating hearty Gallo Pinto (rice and beans) for breakfast",
     "Drinking Imperial beer on a surfboard|Tasting fresh Costa Rican coffee right on the plantation",
     "Cuddling rescued sloths at an animal sanctuary|Relaxing in a hammock listening to howler monkeys",
     "Superman Ziplining 1000ft above the jungle canopy|Soaking in natural volcanic hot springs near Arenal|Surfing world-class waves in Tamarindo|Night hiking to spot deadly snakes and glowing frogs|Whitewater rafting through Class 4 jungle rapids|Rappelling down a massive roaring waterfall"),

    ("Rio de Janeiro", "hot,beach,party,culture,city", "#32CD32", "rio de janeiro christ the redeemer copacabana",
     "Endless premium meats at a luxury Churrascaria|Eating Pão de Queijo (cheese bread) on the street",
     "Drinking Caipirinhas on Copacabana beach|Drinking cold chopp (draft beer) in a lively boteco",
     "Taking the cable car up Sugarloaf Mountain|Buying a tiny bikini/sunga and playing footvolley",
     "Taking a helicopter around the massive Christ the Redeemer statue|Dancing Samba until dawn at the massive Carnival parade|Hang gliding off a mountain and landing on the beach|Exploring the vibrant, chaotic Favela communities|Hiking through the Tijuca urban rainforest|Attending a massive, deafening soccer game at Maracanã Stadium"),

    ("Patagonia", "cold,mountains,nature,adventure", "#4682B4", "patagonia glaciers mountains rugged ice",
     "Gourmet Patagonian lamb cooked over an open fire|Eating empanadas after a freezing hike",
     "Drinking high-end Malbec wine|Drinking bitter Mate tea through a metal straw with Gauchos",
     "Spotting adorable penguins on the coast|Petting wild guanacos (llamas)",
     "Trekking across the massive, cracking Perito Moreno Glacier|Hiking the brutal base of Mount Fitz Roy or Torres del Paine|Kayaking through incredible glowing marble caves|Spotting wild Pumas on a tracking safari|Sailing past towering icebergs on an expedition ship|Horseback riding across the endless steppe like a cowboy"),

    ("Amazon Rainforest", "hot,nature,adventure", "#004D00", "amazon rainforest river jungle wild green",
     "Gourmet jungle fusion on a luxury riverboat|Eating roasted piranha you caught yourself",
     "Drinking Ayahuasca in a terrifying shamanic ceremony|Drinking fresh exotic fruit juices like Cupuaçu",
     "Spotting sleepy sloths in the trees|Holding a colourful macaw parrot",
     "Fishing for deadly, sharp-toothed Piranhas|Taking a night canoe trip to spot glowing Caiman eyes|Surviving a multi-day deep jungle trek with a machete|Swimming with legendary Pink River Dolphins|Visiting an isolated indigenous tribe|Sleeping in a hammock surrounded by jaguar territory"),

    ("Galapagos Islands", "hot,nature,adventure,beach", "#20B2AA", "galapagos islands giant tortoise pristine beach",
     "Luxury seafood dinner on a chartered yacht|Eating fresh Ecuadorian Ceviche",
     "Drinking cocktails on a cruise deck at sunset|Drinking Pilsener beer with the locals",
     "Walking alongside massive, ancient Giant Tortoises|Watching Blue-Footed Boobies do their mating dance",
     "Scuba diving with hundreds of Hammerhead Sharks|Snorkeling with playful, curious Sea Lions|Hiking across a barren, black lava field|Swimming with marine iguanas that look like Godzilla|Taking a small Zodiac boat to remote, untouched islands|Spotting the only penguins that live on the equator"),

    ("Machu Picchu", "mild,mountains,adventure,culture", "#A0522D", "machu picchu peru inca ruins mountains",
     "Michelin-star modern Peruvian food in Lima|Eating roasted Guinea Pig (Cuy)",
     "Drinking Pisco Sours in a lively Cusco tavern|Drinking Coca Tea to fight off the altitude sickness",
     "Taking selfies with fluffy Alpacas|Shopping for vibrant colourful textiles in a local market",
     "Hiking the grueling 4-day classic Inca Trail|Sleeping in a transparent capsule hanging 400ft off a cliff wall|Taking a panoramic glass-roof train through the Andes|Mountain biking down the terrifying 'Death Road'|Hiking the impossibly colourful Rainbow Mountain|Spotting massive Andean Condors flying in Colca Canyon"),

    ("Cape Town", "mild,beach,adventure,nature,luxury", "#CD853F", "cape town table mountain ocean sunset",
     "10-course tasting menu at The Test Kitchen|Eating South African Biltong (jerky) on a hike",
     "World-class wine tasting in Stellenbosch via a wine tram|Drinking Gin and Tonics on a sunset cruise",
     "Walking with wild penguins at Boulders Beach|Riding the spinning cable car up Table Mountain",
     "Cage diving with massive Great White Sharks|Paragliding off Lion's Head mountain over the ocean|Driving the spectacular Chapman's Peak coastal road|Visiting the prison where Nelson Mandela was held|Surfing the freezing, massive waves of the Atlantic|Going on a nearby Big 5 Safari"),

    ("Serengeti", "hot,nature,adventure,luxury", "#CD853F", "serengeti plains acacia tree sunset safari",
     "Champagne bush breakfast after a balloon ride|Eating Ugali and roasted goat",
     "Drinking local Safari beer|Drinking fresh coffee grown on the slopes of Kilimanjaro",
     "Visiting a traditional Maasai village and learning to jump|Watching cheetah cubs play in the tall grass",
     "Taking a Hot Air Balloon over the plains at dawn|Witnessing the Great Migration of millions of wildebeest|Sleeping in a luxury canvas tent surrounded by roaring lions|Tracking the endangered Black Rhino in the Ngorongoro Crater|Climbing to the roof of Africa: Mount Kilimanjaro|Scuba diving in nearby Zanzibar"),

    ("Marrakesh", "hot,city,culture,foodie", "#B22222", "marrakesh morocco market medina colorful",
     "Luxury dining in a stunning, tiled Riad courtyard|Eating slow-cooked Lamb Tagine out of a clay pot",
     "Drinking endless cups of sweet Moroccan Mint Tea|Drinking fresh squeezed orange juice in the chaotic main square",
     "Getting a brutal but amazing scrub in a traditional Hammam|Petting the stray cats in the souks",
     "Getting lost in the chaotic, maze-like markets (Souks)|Riding camels through the Sahara Desert|Sleeping in a luxury desert camp under the stars|Taking a hot air balloon over the Atlas Mountains|Watching snake charmers in Jemaa el-Fnaa square|Driving an ATV through the rocky Palmeraie desert"),

    ("Dubai", "hot,city,luxury,party,adventure", "#D4AF37", "dubai skyline burj khalifa luxury supercars",
     "Eating a 24-karat gold leaf steak at Nusr-Et|Eating authentic Shawarma for $2 on the street",
     "$500 cocktails at the 7-star Burj Al Arab|Drinking Camel Milk cappuccinos",
     "Watching the spectacular Dubai Fountains dance|Shopping for solid gold jewelry in the Gold Souk",
     "Skydiving directly over the Palm Jumeirah islands|Renting a Lamborghini to cruise down Sheikh Zayed Road|Dune bashing in a massive 4x4 across the red desert|Skiing inside a massive indoor mall while it's 40°C outside|Yacht partying in the Dubai Marina with billionaires|Scuba diving in the deepest pool in the world (Deep Dive Dubai)"),

    ("Sydney", "mild,hot,city,beach,party", "#1E90FF", "sydney opera house harbour bridge ocean",
     "Fine dining inside the Sydney Opera House sails|Eating a classic Aussie meat pie with ketchup",
     "Cocktails at a rooftop bar overlooking the Harbour|Drinking pints of Victoria Bitter (VB) at a local pub",
     "Petting Kangaroos and Koalas at the zoo|Taking the scenic ferry to Manly Beach",
     "Climbing the massive arch of the Sydney Harbour Bridge|Surfing the famous waves at Bondi Beach|Sailing a yacht around the spectacular Sydney Harbour|Taking a seaplane to a luxury waterside restaurant|Partying at the massive Mardi Gras festival|Scuba diving with Grey Nurse Sharks in Manly"),

    ("Queenstown", "mild,cold,mountains,adventure,party", "#556B2F", "queenstown new zealand mountains lake extreme",
     "Fine dining accessible only by a steep gondola|Eating the world-famous, massive Fergburger",
     "Tasting world-class Pinot Noir in Central Otago|Drinking shots in an ice bar made of glaciers",
     "Riding the Luge go-karts down the mountain|Soaking in the private, cliffside Onsen Hot Pools",
     "Bungee jumping off the Kawarau Bridge where the sport was invented|Jet boating at 90km/h through narrow, shallow river canyons|Skydiving over the breathtaking Remarkables mountain range|Helicopter skiing on untouched alpine powder|Hiking the brutal, rewarding Ben Lomond track|Paragliding off a mountain over the town"),

    ("Bora Bora", "hot,beach,relax,luxury,romance", "#00BFFF", "bora bora tropical island luxury overwater bungalow",
     "Private dinner served on the beach surrounded by tiki torches|Eating Tahitian Poisson Cru (raw fish in coconut milk)",
     "Drinking cocktails out of a freshly cut coconut|Drinking Hinano Tahiti beer on a boat",
     "Getting a traditional Polynesian flower crown|Having breakfast delivered to your bungalow by canoe",
     "Sleeping in a massive, $2000/night overwater bungalow|Swimming with friendly reef sharks and stingrays|Taking a helicopter ride around Mount Otemanu|Jet skiing across the impossibly blue lagoon|Attending an intense Polynesian fire dancing show|Scuba diving outside the reef for lemon sharks")
]

# Unpack the compressed data structure dynamically
dests = {}
for name, tags, color, prompt, foods, drinks, cutes, epics in raw_dests:
    dests[name] = {
        "t": tags.split(","),
        "c": color,
        "p": prompt,
        "f": foods.split("|"),
        "d": drinks.split("|"),
        "cu": cutes.split("|"),
        "e": epics.split("|")
    }

# ---------------------------------------------------------
# 3. MASSIVE DYNAMIC QUESTION POOL
# ---------------------------------------------------------
all_questions = [
    {"q": "What is your absolute ideal morning? 🌅", "opts": {
        "Sleeping in until noon on 1000-thread count sheets": {"tags": ["luxury","relax"], "cheeky": "Ah, a professional napper. I respect the lazy hustle."},
        "Up at 5 AM, putting on war paint, ready to conquer": {"tags": ["adventure","nature"], "cheeky": "5 AM? You're a psycho. Let's keep that heart rate up."},
        "Grabbing an artisanal coffee and hitting busy streets": {"tags": ["city","culture"], "cheeky": "Caffeine and concrete. A classic combo."}}},
    {"q": "Pick an animal companion for the trip 🐾", "opts": {
        "A cuddly baby sea turtle": {"tags": ["beach","nature"], "cheeky": "Turtles = immaculate vibes. Beach it is."},
        "A mischievous monkey or lemur": {"tags": ["nature","hot","adventure"], "cheeky": "Watch your wallet, those monkeys are thieves."},
        "A fluffy waddling penguin or husky": {"tags": ["cold","nature"], "cheeky": "Pack a parka, it's about to get freezing."},
        "A stray cat outside a cafe": {"tags": ["city","culture"], "cheeky": "Street cats are the true rulers of the world."}}},
    {"q": "How do you feel about extreme heights? 🎢", "opts": {
        "Love them! Throw me out of a plane right now!": {"tags": ["adventure","mountains"], "cheeky": "Adrenaline junkie confirmed. Let's get dangerous."},
        "Only if I'm safely looking out a high-rise window": {"tags": ["city","luxury"], "cheeky": "Safe, warm, and holding a cocktail. Smart."},
        "Keep my feet firmly on the ground, thanks": {"tags": ["relax","beach"], "cheeky": "Gravity is your friend. No jumping today."}}},
    {"q": "Pick a flavor profile that makes you drool! 👅", "opts": {
        "Fresh, tropical, sweet, and fruity": {"tags": ["hot","beach","relax"], "cheeky": "You're basically a walking piña colada at this point."},
        "Savory, rich, carb-heavy, and comforting": {"tags": ["mild","cold","foodie"], "cheeky": "Carbs don't count on holiday. Fact."},
        "Spicy, exotic, and totally weird": {"tags": ["foodie","culture","adventure"], "cheeky": "Iron stomach! Hope you packed the Pepto just in case."},
        "High-end, expensive, Michelin-star meats": {"tags": ["luxury","foodie"], "cheeky": "Oh, we got a baller over here. Whip out the black card."}}},
    {"q": "What’s your ideal footwear for this trip? 👟", "opts": {
        "Barefoot or designer flip flops": {"tags": ["beach","hot"], "cheeky": "Free the toes! Sand gets everywhere anyway."},
        "Heavy duty, mud-covered hiking boots": {"tags": ["mountains","nature","adventure"], "cheeky": "Blisters and glory. You're ready to march."},
        "Stylish sneakers for walking 20k steps": {"tags": ["city","culture"], "cheeky": "Fashion meets function. Get those steps in."},
        "Thick thermal insulated snow boots": {"tags": ["cold","mountains"], "cheeky": "Frostbite is cancelled. Cozy toes only."}}},
    {"q": "Choose a magical item to take with you ✨", "opts": {
        "Invisibility cloak (for epic people watching)": {"tags": ["city","culture"], "cheeky": "Creepy, but I'll allow it. The ultimate tourist tool."},
        "A teleportation ring (to skip the grueling hike)": {"tags": ["relax","luxury"], "cheeky": "Work smarter, not harder. Let's skip the sweat."},
        "An endless bottle of perfect vintage wine": {"tags": ["foodie","relax","romance"], "cheeky": "Drunk by noon? It's 5 o'clock somewhere."},
        "A magic amulet that keeps you perfectly warm": {"tags": ["cold","adventure"], "cheeky": "You hate the cold but love the snow. We can work with that."}}},
    {"q": "What’s your evening vibe? 🌙", "opts": {
        "Dancing until dawn under neon lights or beach fires": {"tags": ["party","city","beach"], "cheeky": "Sleep is for the weak. Let's rage."},
        "A wildly romantic candlelit dinner by the water": {"tags": ["luxury","relax","romance"], "cheeky": "Ooooh, someone's in love. Or just loves fancy food."},
        "Staring at the Milky Way by a campfire": {"tags": ["nature","adventure"], "cheeky": "Just you, the stars, and probably some mosquitos."},
        "Passing out from sheer physical exhaustion": {"tags": ["adventure","mountains"], "cheeky": "You earned that sleep. RIP your calves tomorrow."}}},
    {"q": "Weather preference? ☀️❄️", "opts": {
        "Roasting hot, give me a deep tan": {"tags": ["hot"], "cheeky": "Bake me like a potato. Factor 50 required."},
        "Brisk and freezing, I want snow and ice": {"tags": ["cold"], "cheeky": " Elsa vibes. The cold never bothered you anyway."},
        "Mild, breezy, and perfect for a light jacket": {"tags": ["mild"], "cheeky": "Ah, the Goldilocks zone. Not too hot, not too cold."}}},
    {"q": "How do you handle getting lost? 🗺️", "opts": {
        "Panic slightly but find a cute cafe": {"tags": ["city","mild"], "cheeky": "When in doubt, eat pastries until you feel better."},
        "Ask locals and end up at a crazy underground party": {"tags": ["party","culture"], "cheeky": "You're the main character. That's a wild night ahead."},
        "I don't get lost, I go on survival adventures": {"tags": ["adventure","nature"], "cheeky": "Bear Grylls, is that you? Don't drink your own pee yet."},
        "I literally can't get lost, I have a private butler": {"tags": ["luxury"], "cheeky": "Must be nice! Let the help deal with the map."}}},
    {"q": "Pick a movie genre for your life right now 🎬", "opts": {
        "Romantic Comedy in a beautiful dress": {"tags": ["city","relax","luxury","romance"], "cheeky": "Cue the montage music and the meet-cute!"},
        "High-Octane Action / Thriller": {"tags": ["adventure","party"], "cheeky": "Explosions, car chases, and bad decisions. Let's go."},
        "Sci-Fi / Cyberpunk / Futuristic": {"tags": ["city","culture"], "cheeky": "Living in the year 3000. Give me neon."},
        "Epic Fantasy / Lord of the Rings": {"tags": ["mountains","nature"], "cheeky": "One does not simply walk into Mordor... unless it's a holiday."}}},
    {"q": "Choose a baller mode of transport 🚀", "opts": {
        "A Mega Luxury Yacht": {"tags": ["luxury","beach","hot"], "cheeky": "Step aboard, captain. Don't drop your champagne."},
        "A Private Helicopter over mountains": {"tags": ["mountains","luxury","cold"], "cheeky": "Get to the choppa! Best views guaranteed."},
        "A 300mph Bullet Train": {"tags": ["city","culture"], "cheeky": "Fast, efficient, and probably Japanese. Nice."},
        "A rugged 4x4 Jeep covered in mud": {"tags": ["adventure","nature","hot"], "cheeky": "Hold on tight, it's gonna be a bumpy ride."}}},
    {"q": "How much luggage are you bringing? 🧳", "opts": {
        "Just a dusty backpack, keep it rugged": {"tags": ["adventure","budget"], "cheeky": "Living out of one pair of underwear. Brave."},
        "One perfectly curated stylish suitcase": {"tags": ["city","mild"], "cheeky": "Capsule wardrobe activated. Looking sharp."},
        "Three massive trunks of designer outfits": {"tags": ["luxury","relax"], "cheeky": "RIP to whoever has to carry those up the stairs."}}},
    {"q": "Pick a historical era to visit 🕰️", "opts": {
        "Ancient Empires (Samurai, Romans, Incas)": {"tags": ["culture","city"], "cheeky": "History nerd detected. Let's go touch some old rocks."},
        "The Wild, Untamed Prehistoric Age": {"tags": ["nature","adventure"], "cheeky": "Dinosaur hunting vibes. Keep your eyes peeled."},
        "The glamorous roaring 1920s": {"tags": ["city","luxury","party"], "cheeky": "Flapper dresses and illegal liquor. What a time."},
        "The distant, shiny Cyber-Future": {"tags": ["city"], "cheeky": "Robots taking your order. The future is now."}}},
    {"q": "What's your budget style? 💸", "opts": {
        "Unlimited wealth. Spoil me rotten.": {"tags": ["luxury"], "cheeky": "Sugar daddy vibes. Let's drain the bank account."},
        "A healthy mix of cheap street food and one fancy splurge": {"tags": ["foodie","culture"], "cheeky": "Sensible, yet indulgent. The perfect balance."},
        "I just need a tent, some rice, and good vibes": {"tags": ["budget","nature"], "cheeky": "Dirt cheap and loving it. Nature is free."}}},
    {"q": "Water or Land? 🌊🌍", "opts": {
        "Oceans, lakes, and rivers! Get me wet!": {"tags": ["beach"], "cheeky": "You're basically Aquaman. Into the blue we go."},
        "Mountains, forests, and towering cities!": {"tags": ["mountains","city"], "cheeky": "Solid ground only. No seasickness for you."},
        "A perfect mix of both!": {"tags": ["nature","relax"], "cheeky": "Why choose when you can have it all?"}}},
    {"q": "Choose a color palette to look at 🎨", "opts": {
        "Blinding Neon pinks and bright blues": {"tags": ["city","party"], "cheeky": "My eyes are burning, but in a good way."},
        "Earthy jungle greens and dirt browns": {"tags": ["nature","adventure"], "cheeky": "Camouflage mode activated. Very earthy."},
        "Ocean blues and golden sunset oranges": {"tags": ["beach","relax"], "cheeky": "Golden hour forever. Perfect for the Gram."},
        "Blinding icy whites and dark blacks": {"tags": ["cold","mountains"], "cheeky": "Stark, dramatic, and freezing. Epic."}}},
    {"q": "Pick a travel snack right now 🥨", "opts": {
        "A freshly baked, warm, flaky pastry": {"tags": ["city","culture","foodie"], "cheeky": "Butter makes everything better. Crumbs everywhere."},
        "A massive plate of exotic tropical fruit": {"tags": ["hot","beach"], "cheeky": "Healthy and hydrating. Look at you glowing."},
        "A hardcore energy bar or trail mix": {"tags": ["adventure","mountains"], "cheeky": "Fuel for the machine. Crunch on, warrior."},
        "Matcha KitKats or crazy flavored chips": {"tags": ["city","culture"], "cheeky": "Weird snacks are the best part of traveling."}}},
    {"q": "What's your absolute worst nightmare on holiday? 😱", "opts": {
        "No WiFi or cell service for days": {"tags": ["city","luxury"], "cheeky": "Digital detox? No thanks. Need the TikToks."},
        "Getting a terrible sunburn": {"tags": ["cold","mild"], "cheeky": "Factor 100 sunscreen and staying in the shade."},
        "A wild venomous animal in my tent": {"tags": ["city","luxury"], "cheeky": "Nope. Nope. Nope. Burning the tent down."},
        "Freezing my toes off": {"tags": ["hot","beach"], "cheeky": "If I can't wear flip flops, I'm not going."}}},
    {"q": "Choose a sound to fall asleep to 🎧", "opts": {
        "Crashing warm ocean waves": {"tags": ["beach","relax"], "cheeky": "Nature's white noise machine. So soothing."},
        "Jungle insects and distant animal roars": {"tags": ["nature","adventure"], "cheeky": "A little terrifying, but undeniably epic."},
        "City traffic, sirens, and train hums": {"tags": ["city","party"], "cheeky": "Ah, the lullaby of chaos. A true urbanite."},
        "Fierce howling blizzard winds": {"tags": ["cold","mountains"], "cheeky": "Cozy inside, chaos outside. The best feeling."}}},
    {"q": "Finally, what is the ULTIMATE goal of this trip? 🎯", "opts": {
        "To relax so hard I forget my own name": {"tags": ["relax"], "cheeky": "Brain empty. Vibes only. Let's chill."},
        "To push my physical limits and feel alive": {"tags": ["adventure"], "cheeky": "Pain is just weakness leaving the body. Go get it."},
        "To eat absolutely EVERYTHING in sight": {"tags": ["foodie"], "cheeky": "Pack the stretchy pants. It's time to feast."},
        "To take insane photos and show off": {"tags": ["luxury","party","culture"], "cheeky": "Do it for the plot. And the followers."}}}
]

# ---------------------------------------------------------
# 4. ENGINE LOGIC & STATE MANAGEMENT
# ---------------------------------------------------------
if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.q_index = 0
    st.session_state.user_tags = Counter()
    st.session_state.available_dests = list(dests.keys())
    st.session_state.chosen_dest = None
    st.session_state.activities = []
    st.session_state.activity_round = 0
    st.session_state.last_cheeky = ""
    st.session_state.unused_qs = list(all_questions)
    st.session_state.current_q = None

def set_stage(new_stage):
    st.session_state.stage = new_stage

def get_next_question():
    if not st.session_state.unused_qs:
        return None
    
    scored_dests = []
    for d in st.session_state.available_dests:
        score = sum(st.session_state.user_tags[t] for t in dests[d]["t"])
        scored_dests.append((score, d))
    
    scored_dests.sort(reverse=True)
    top_dests = [d[1] for d in scored_dests[:15]]
    
    tag_counts = Counter()
    for d in top_dests:
        tag_counts.update(dests[d]['t'])
        
    best_q_idx, best_score = 0, -1
    for i, q in enumerate(st.session_state.unused_qs):
        q_score = sum(tag_counts[tag] for opt in q['opts'].values() for tag in opt['tags'])
        if q_score > best_score:
            best_score, best_q_idx = q_score, i
            
    return st.session_state.unused_qs.pop(best_q_idx)

def handle_answer(selected_option):
    weights = st.session_state.current_q["opts"][selected_option]["tags"]
    for tag in weights:
        st.session_state.user_tags[tag] += 1
        
    st.session_state.last_cheeky = st.session_state.current_q["opts"][selected_option]["cheeky"]
    st.session_state.q_index += 1
    
    if st.session_state.q_index == 10:
        set_stage('stick_or_risk')
    elif st.session_state.q_index >= 20 or not st.session_state.unused_qs:
        calculate_final_match()
        set_stage('final_match_reveal')
    else:
        st.session_state.current_q = get_next_question()

def get_best_match():
    best_score = -9999
    best_dest = None
    random.shuffle(st.session_state.available_dests)
    for dest in st.session_state.available_dests:
        score = sum([st.session_state.user_tags[t] for t in dests[dest]["t"]])
        if score > best_score:
            best_score = score
            best_dest = dest
    return best_dest

def stick_choice():
    st.session_state.chosen_dest = get_best_match()
    set_stage('activity_selection')

def risk_choice():
    current_best = get_best_match()
    st.session_state.available_dests.remove(current_best)
    st.session_state.current_q = get_next_question()
    set_stage('questions')

def calculate_final_match():
    st.session_state.chosen_dest = get_best_match()

def pick_activity(act):
    st.session_state.activities.append(act)
    st.session_state.activity_round += 1
    if st.session_state.activity_round >= 6:
        set_stage('final_itinerary')

# ---------------------------------------------------------
# 5. UI RENDERING
# ---------------------------------------------------------

if st.session_state.stage == 'welcome':
    set_bg("#1E1E1E", "#00FF7F")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='giant-emoji'>✈️🌍✨</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 65px; font-weight: 900;'>The Ultimate Holiday Finder</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; text-align: center; margin: 20px auto; max-width: 800px;'>
    <h3 style='margin-bottom: 20px;'>Here is how it works:</h3>
    <p style='font-size: 22px;'>1. Our engine actively searches <b>dozens of unique global holidays</b> as you answer.</p>
    <p style='font-size: 22px;'>2. The questions <b>dynamically change</b> based on what destinations are winning.</p>
    <p style='font-size: 22px;'>3. Halfway through, you get a <b>Stick or Risk</b> offer.</p>
    <p style='font-size: 22px;'>4. Finally, you will pick your ultimate 6-part itinerary!</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("LET'S GO! 🚀", on_click=lambda: setattr(st.session_state, 'current_q', get_next_question()) or set_stage('questions'))
    st.balloons()

elif st.session_state.stage == 'questions':
    set_bg("#2C3E50", "#FFFFFF")
    
    if st.session_state.last_cheeky != "":
        st.markdown(f"<div class='cheeky-text'>💬 \"{st.session_state.last_cheeky}\"</div>", unsafe_allow_html=True)
    
    q_data = st.session_state.current_q
    
    st.markdown(f"<h1 style='font-size: 45px; text-align: center;'>Question {st.session_state.q_index + 1}: {q_data['q']}</h1><br>", unsafe_allow_html=True)
    
    options = list(q_data["opts"].keys())
    choice = st.radio("👇 Click your vibe:", options, index=0)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("LOCK IT IN! 🔒➡️", on_click=handle_answer, args=(choice,))
    
    st.progress(st.session_state.q_index / 20)

elif st.session_state.stage == 'stick_or_risk':
    best_dest = get_best_match()
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>🚨 HALFWAY POINT! 🚨</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        safe_image(dest_data["p"])
    
    with col2:
        st.markdown(f"<h2 style='font-size: 45px;'>Right now, you are matching perfectly with: <br><u style='font-size: 60px;'>{best_dest}</u></h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 25px; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 10px;'>Imagine: {random.choice(dest_data['e'])}</p>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 30px;'>Do you want to STICK with this holiday, or RISK it for something else?</h3>", unsafe_allow_html=True)
        st.markdown("<p><i>(Warning: If you RISK, this destination goes in the bin forever!)</i></p>", unsafe_allow_html=True)
        
        sub1, sub2 = st.columns(2)
        with sub1:
            st.button("😍 STICK! TAKE ME HERE!", on_click=stick_choice)
        with sub2:
            st.button("🎲 RISK! KEEP ASKING!", on_click=risk_choice)

elif st.session_state.stage == 'final_match_reveal':
    best_dest = st.session_state.chosen_dest
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    if "cold" in dest_data["t"]:
        st.snow()
    else:
        st.balloons()
        
    st.markdown("<h1 style='text-align: center; font-size: 80px; text-transform: uppercase;'>🎉 WE'VE FOUND YOU A MATCH! 🎉</h1>", unsafe_allow_html=True)
    safe_image(dest_data["p"])
    st.markdown(f"<h1 style='text-align: center; font-size: 100px; font-weight: 900;'>{best_dest}!</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("PICK MY ACTIVITIES! ➡️", on_click=set_stage, args=('activity_selection',))

elif st.session_state.stage == 'activity_selection':
    best_dest = st.session_state.chosen_dest
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    rnd = st.session_state.activity_round
    
    if rnd == 0:
        title = "🍽️ Atmospheric Food Choice"
        act1, act2 = dest_data["f"][0], dest_data["f"][1]
    elif rnd == 1:
        title = "🍸 Atmospheric Drinks Choice"
        act1, act2 = dest_data["d"][0], dest_data["d"][1]
    elif rnd == 2:
        title = "📸 Cute / Hidden Gem Activity"
        act1, act2 = dest_data["cu"][0], dest_data["cu"][1]
    elif rnd == 3:
        title = "🔥 Holiday Changing Activity 1"
        act1, act2 = dest_data["e"][0], dest_data["e"][1]
    elif rnd == 4:
        title = "🔥 Holiday Changing Activity 2"
        act1, act2 = dest_data["e"][2], dest_data["e"][3]
    elif rnd == 5:
        title = "🔥 Holiday Changing Activity 3"
        act1, act2 = dest_data["e"][4], dest_data["e"][5]
    
    st.markdown(f"<h1 style='text-align: center; font-size: 50px;'>Ultimate Choice: {best_dest}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{title} (Round {rnd + 1} of 6)</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>You can only KEEP ONE. The other is gone forever.</h4><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 40px; border-radius: 20px; height: 200px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act1}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ KEEP THIS ONE", key=f"btn1_{rnd}", on_click=pick_activity, args=(act1,))
        
    with col2:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.4); padding: 40px; border-radius: 20px; height: 200px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act2}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ NO, KEEP THIS ONE", key=f"btn2_{rnd}", on_click=pick_activity, args=(act2,))

elif st.session_state.stage == 'final_itinerary':
    best_dest = st.session_state.chosen_dest
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    if "cold" in dest_data["t"]:
        st.snow()
    else:
        st.balloons()
    
    st.markdown("<h1 style='text-align: center; font-size: 70px; font-weight: 900;'>🎊 PACK YOUR BAGS! 🎊</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        safe_image(dest_data["p"])
    
    with col2:
        st.markdown(f"<h2 style='font-size: 60px; text-decoration: underline;'>📍 {best_dest}</h2>", unsafe_allow_html=True)
        st.markdown("<h3>Your Ultimate Hand-Picked Itinerary:</h3>", unsafe_allow_html=True)
        
        for act in st.session_state.activities:
            st.markdown(f"<div style='background-color: rgba(255,255,255,0.25); padding: 20px; margin-bottom: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'><h3 style='margin:0;'>🌟 {act}</h3></div>", unsafe_allow_html=True)
            
    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    st.markdown("""
    <style>
    .twist-btn > button { background-color: #FF0000 !important; color: white !important; border: none !important; animation: pulse 2s infinite; }
    @keyframes pulse { 0% { transform: scale(1.0); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0.7); } 70% { transform: scale(1.1); box-shadow: 0 0 0 20px rgba(255, 0, 0, 0); } 100% { transform: scale(1.0); box-shadow: 0 0 0 0 rgba(255, 0, 0, 0); } }
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
