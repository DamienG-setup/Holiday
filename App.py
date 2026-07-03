import streamlit as st
import random
import urllib.parse
from collections import Counter

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & INSANE CSS
# ---------------------------------------------------------
st.set_page_config(page_title="The Perfect Holiday Finder ✈️", page_icon="🌍", layout="wide")

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
    .cheeky-text {{ font-size: 24px !important; font-style: italic; color: #FFD700 !important; text-align: center; margin-bottom: 30px; background: rgba(0,0,0,0.6); padding: 15px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border-left: 5px solid #FFD700; }}
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
# 2. TIKTOK-VIRAL DESTINATIONS DATABASE (100 Locations)
# ---------------------------------------------------------
# Format: Name | Tags | Color | Prompt | Food1 | Food2 | Drink1 | Drink2 | Cute1 | Cute2 | Epic1 | Epic2 | Epic3 | Epic4 | Epic5 | Epic6
raw_dests = [
    "Beijing (China)|hot,city,culture,foodie|#B22222|beijing china great wall red lanterns|Eat viral Tanghulu (candied fruit) on Wangfujing Street|Eat authentic Peking Duck carved tableside|Drink pearl milk tea in a traditional Hutong alleyway|Cocktails at a secret bar hidden behind a bookshelf|Rent traditional Hanfu clothes for a photoshoot in the Forbidden City|Feed adorable pandas at the Beijing Zoo|Ride the viral toboggan slide down the Great Wall of China|Walk the terrifying glass-bottom cliff bridge in Jingdong|Take the 300mph high-speed bullet train to Shanghai|Night tour of the glowing Bird's Nest Olympic stadium|Take a terrifying cable car up the jagged Mutianyu mountains|Explore the massive, ancient Summer Palace by wooden boat",
    "Shanghai (China)|mild,city,party,luxury|#8B0000|shanghai skyline bund neon lights|Eat viral soup dumplings at Jia Jia Tang Bao|Fine dining inside the futuristic Pearl Tower|Cocktails at a rooftop bar overlooking the glowing Bund|Sip matcha in the ancient Yu Garden|Visit the massive, immersive Shanghai Disneyland|Take a neon-lit river cruise down the Huangpu|Walk the glass floor 100 stories up in the World Financial Center|Explore the cyberpunk, neon-soaked Nanjing Road|Ride the Maglev, the fastest commercial train on earth|Attend a massive underground techno party|Take a day trip to a historic water town (Zhujiajiao)|Shop for knock-off luxury goods in the underground markets",
    "Zhangjiajie (China)|cold,mountains,nature,adventure|#2F4F4F|zhangjiajie avatar mountains mist forest|Eat spicy Hunan street noodles|Gourmet banquet in a mountain lodge|Drink hot green tea in the freezing mist|Local rice wine tasting|Watch the wild macaques steal snacks|Walk through the Tianmen mountain 'Heaven's Gate'|Take the terrifying Bailong Elevator up the cliff face|Walk across the world's longest, highest glass-bottom bridge|Hike through the floating Hallelujah Mountains (Avatar)|Ride the world's longest cable car over the jungle|Bungee jump off the glass bridge|Take a helicopter tour of the limestone pillars",
    "Paris (France)|mild,city,culture,foodie,luxury,romance|#C71585|paris eiffel tower sunset romance|Wait in line for Cedric Grolet’s viral fruit illusion pastries|Eat the famous hot chocolate and mont blanc at Angelina|Champagne at the very top of the Eiffel Tower|Drink inside a secret speakeasy behind a washing machine (Lavomatic)|Take photos in a vintage Fotoautomat booth in Montmartre|Have a chic picnic at Place des Vosges|Take a Dior Spa cruise down the Seine River|VIP skip-the-line night tour of the Louvre|Explore the underground bone Catacombs|Dine on the glass-roofed Bustronome double-decker bus|Take a croissant-making masterclass|Attend a cabaret show at the Moulin Rouge",
    "Tokyo (Japan)|mild,city,foodie,culture,party|#FF003F|tokyo neon night city shibuya|Eat at the viral 2D black-and-white cafe in Shin-Okubo|Slurp rich Tonkotsu ramen in an isolated Ichiran booth|Drink incredibly cute lattes at the Pokémon Cafe|High-end whiskey in a slick sky-bar (Lost in Translation)|Play UFO claw machines in Akihabara|Buy weird things from 100 different vending machines|Drive real Mario Karts through the Shibuya Crossing|Walk barefoot through water at the viral teamLab Planets art exhibit|Watch a brutal, heavyweight sumo wrestling tournament|Sing Karaoke in a private room with endless drinks|Take a helicopter tour over the Tokyo neon skyline|Eat insanely fluffy pancakes in Harajuku",
    "Kyoto (Japan)|mild,city,culture,relax|#8B0000|kyoto japan bamboo forest temple|Multi-course exquisite Kaiseki dinner overlooking a zen garden|Eat matcha soft serve while walking the streets|Experience a secret, highly traditional Geisha tea ceremony|Tasting 20 different types of Matcha at a local farm|Walk the magical Arashiyama Bamboo Forest|Feed the bowing deer in nearby Nara|Sleep in a traditional Ryokan on tatami mats|Bathe naked in a natural outdoor Onsen|Rent kimonos and walk through the thousands of red Torii gates at Fushimi Inari|Learn to swing a katana with a Samurai master|Meditate with Zen monks at dawn|Attend a vibrant traditional matsuri festival",
    "Bali (Indonesia)|hot,beach,nature,relax,budget|#228B22|bali indonesia rice terraces jungle sunset|Eat a floating breakfast in a jungle infinity pool|Eat spicy Nasi Goreng at a cheap, local warung|Cocktails at the massive, luxurious Finns Beach Club|Drink a Bintang beer while sitting on a beanbag on the sand|Swing over the rice terraces on the viral Bali Jungle Swing|Get blessed by a monk in a holy water temple|Hike Mount Batur in the dark to watch the sunrise|Surf the world-class waves of Uluwatu|Scuba dive a WWII shipwreck in Tulamben|Get a brutal but amazing 2-hour Balinese massage|White water raft down the Ayung River|Take a fast boat to the stunning Nusa Penida island",
    "Cappadocia (Turkey)|hot,nature,culture,romance|#D2B48C|cappadocia turkey hot air balloons fairy chimneys|Eat a traditional Pottery Kebab smashed open at your table|Eat Gozleme (stuffed flatbread) made by village women|Taste local wine made from grapes grown in volcanic soil|Drink Turkish apple tea on a colorful rug|Watch the sunrise from a rooftop while hundreds of balloons rise|Sleep in a luxury hotel carved directly into a cave|Take a magical Hot Air Balloon ride over the fairy chimneys|Explore a massive, multi-level underground city|Horseback ride through the bizarre rock formations|Ride ATVs through the dusty Rose Valley at sunset|Watch a traditional Turkish night show in a cave|Hike through the pigeon-filled Ihlara Valley",
    "Tulum (Mexico)|hot,beach,party,culture,relax|#20B2AA|tulum mexico beach cenote ancient ruins jungle|Eat gourmet Maya-fusion dining in the jungle|Eat fresh fish tacos barefoot on the beach|Drink Matcha lattes at the viral Azulik treehouse|Drink Mezcal at a massive jungle techno rave|Float down a crystal clear underground Cenote|Do yoga on the beach at sunrise|Explore the ancient Mayan ruins perched on the cliff edge|Scuba dive in the dark, underwater cave systems|Swim with giant sea turtles in Akumal|Kitesurf on the breezy Caribbean ocean|Take a mud bath in a Mayan sweat lodge (Temazcal)|Rent a bicycle to ride down the trendy beach road",
    "Santorini (Greece)|hot,beach,relax,luxury,romance|#00008B|santorini white houses blue domes sunset|Private clifftop dining with fresh lobster|Eat a massive Gyros from a bustling local taverna|Wine tasting in a volcanic cave vineyard|Drink cocktails on a luxury catamaran at sunset|Do the viral 'Flying Dress' photoshoot on the white roofs|Wander the white cobblestone streets of Oia|Sail a yacht to the volcanic hot springs|Scuba dive in the deep caldera|Take a helicopter ride over the Greek Islands|Rent ATVs to explore hidden black sand beaches|Explore the ancient ruins of Akrotiri|Jump off the cliffs at Amoudi Bay",
    "Rome (Italy)|mild,hot,city,culture,foodie|#A0522D|rome colosseum ancient sunset|Build your own custom Tiramisu at the viral Pompi|Massive slice of Roman pizza al taglio from a hole-in-the-wall|Vintage Barolo wine tasting in an ancient cellar|Drink an Aperol Spritz overlooking Piazza Navona|Throw a coin in the Trevi Fountain at midnight|Eat gelato on the Spanish Steps|Take a pasta making class at a viral Frascati farmhouse|Attend a Gladiator training school on the Appian Way|Take a private after-hours tour of the Sistine Chapel|Ride a Vespa through the chaotic Roman traffic|Explore the ancient crypts made entirely of human bones|Helicopter tour over the ancient ruins",
    "London (UK)|mild,cold,city,culture,party|#191970|london big ben red bus thames|Eat afternoon tea at Sketch (the viral pink room and egg toilets)|Eat in the Coppa Club glass igloos overlooking Tower Bridge|Drink cocktails at the eccentric Alchemist bar (they bubble and smoke)|Drink pints of ale in a 400-year-old tavern|Feed the pelicans in St. James's Park|Browse quirky antiques at Portobello Road|VIP pod on the London Eye with champagne|Take a terrifying Jack the Ripper night walking tour|Climb completely over the top of the O2 Arena|Attend a smash-hit West End theatre premiere|Speedboat down the River Thames at 40mph|Tour the hidden underground Churchill War Rooms",
    "New York City (USA)|mild,cold,city,foodie,luxury,culture|#4682B4|new york city times square skyline|Eat the viral Suprême croissant at Lafayette Grand Café|Eat a massive, greasy $2 slice of NY pizza on the street|Martinis in a high-end hidden speakeasy|Drink cheap beers at a gritty Brooklyn dive bar|Take mind-bending photos in the SUMMIT One Vanderbilt glass room|Ice skate in Central Park|Take a helicopter doors-off tour over Manhattan|Watch a smash-hit Broadway musical from VIP seats|Attend a crazy underground warehouse party in Brooklyn|Go on a massive shopping spree on 5th Avenue|Eat a massive pastrami sandwich at Katz's Deli|Walk the High Line elevated park at sunset",
    "Seoul (South Korea)|mild,city,foodie,culture,party|#4B0082|seoul south korea neon palace night|Make your own custom ramen at a Han River convenience store|Eat the viral, stretchy 10 Won Coin Bread|Get a viral 'Personal Color Analysis' session|Drink Soju in a street tent (Pojangmacha)|Rent a traditional Hanbok to get into palaces for free|Try a 10-step Korean skincare routine in Myeongdong|Get scrubbed raw at a traditional bathhouse (Jjimjilbang)|Sing K-Pop Karaoke in a private Noraebang|Visit the heavily armed DMZ border with North Korea|Club until 7 AM in Gangnam|Hike Bukhansan Mountain right outside the city|Eat live wriggling octopus at Noryangjin Fish Market",
    "Maldives|hot,beach,relax,luxury,romance|#00CED1|maldives overwater bungalow crystal ocean|Dine in an all-glass underwater restaurant surrounded by sharks|Have a private beach BBQ cooked by a personal chef|Have champagne delivered to your pool via floating tray|Drink coconut cocktails on a deserted sandbank|Slide directly from your overwater bungalow into the ocean|Take a night swim with glowing bioluminescent plankton|Take a private seaplane over the gorgeous atolls|Scuba dive with massive, gentle Manta Rays|Go deep sea fishing for Yellowfin Tuna|Take a submarine tour of the vibrant coral reefs|Have a couples spa day on a glass floor over the ocean|Watch an outdoor movie at a jungle cinema",
    "Dubai (UAE)|hot,city,luxury,party,adventure|#D4AF37|dubai skyline burj khalifa luxury supercars|Dine in the Sky suspended 50 meters in the air by a crane|Eat authentic Shawarma for $2 on the street|$500 cocktails at the 7-star Burj Al Arab|Drink Camel Milk cappuccinos|Ride the terrifying glass slide on the outside of a skyscraper|Watch the spectacular Dubai Fountains dance|Skydivive directly over the Palm Jumeirah islands|Rent a Lamborghini to cruise down Sheikh Zayed Road|Dune bash in a massive 4x4 across the red desert|Ski inside a massive indoor mall while it's 40°C outside|Yacht party in the Dubai Marina with billionaires|Scuba dive in the deepest pool in the world (Deep Dive Dubai)",
    "Amalfi Coast (Italy)|hot,beach,foodie,luxury,romance|#FF8C00|amalfi coast cliffside colorful houses|Eat lemon sorbet served inside a massive, hollowed-out lemon|Eat lunch at the viral La Tagliata overlooking the cliffs|Limoncello tasting straight from a lemon farm|Drink Prosecco on a private vintage wooden boat|Shop for handmade leather sandals in Positano|Take a vintage Vespa tour along the coastal roads|Swim into the sparkling Blue Grotto sea cave|Take a helicopter tour of Mount Vesuvius|Hike the breathtaking Path of the Gods|Take a private cooking class in a cliffside villa|Charter a luxury yacht to the island of Capri|Jump off the cliffs into the Mediterranean",
    "Bangkok (Thailand)|hot,city,party,foodie,culture|#B22222|bangkok thailand neon temples tuktuk|Eat the viral massive Volcano Ribs at Jodd Fairs night market|Eat Michelin-star crab omelet from a street vendor (Jay Fai)|Drink at the viral Tichuca jellyfish rooftop bar|Drink cheap buckets of liquor on Khao San Road|Take a chaotic, terrifying Tuk-Tuk ride|Shop from a tiny boat at the Floating Market|Explore the stunning, solid gold Grand Palace|Party with backpackers on Khao San Road|Cruise the Chao Phraya River on a luxury dinner ship|Attend the magical Yi Peng floating lantern festival|Get a traditional Sak Yant bamboo tattoo|Watch a brutal live Muay Thai boxing match",
    "Swiss Alps (Switzerland)|cold,mountains,adventure,luxury,nature|#8B0000|swiss alps matterhorn snow cabin|Eat fondue inside a literal igloo|Eat at the viral Aescher cliff restaurant built into the rock|Drink Dom Pérignon in an outdoor heated jacuzzi|Drink hot spiced Glühwein by a roaring fire|Build a snowman overlooking the Matterhorn|Ride a horse-drawn sleigh through the village|Ride the Gelmerbahn, Europe's steepest open-air funicular|Helicopter drop-off for extreme off-piste skiing|Paraglide over the snowy peaks|Ice climb up a frozen waterfall|Ride the panoramic Glacier Express train|Bungee jump off a dam like James Bond",
    "Hallstatt (Austria)|cold,mountains,nature,romance|#4682B4|hallstatt austria lake mountains fairytale|Eat gourmet Austrian Schnitzel|Eat fresh lake trout|Drink local Austrian beer|Drink hot cocoa overlooking the fairytale lake|Rent a swan boat on the crystal clear water|Wander the perfectly preserved alpine village|Take the funicular up to the ancient salt mines|Walk out onto the terrifying 'Skywalk' viewing platform|Explore the eerie Dachstein Giant Ice Cave|Hike the dramatic Dachstein mountain range|Take a helicopter tour over the Austrian Alps|Visit the incredibly creepy Bone House (Beinhaus)",
    "Chefchaouen (Morocco)|hot,city,culture,relax|#1E90FF|chefchaouen morocco blue city cats|Eat traditional Lamb Tagine slow-cooked in clay|Eat fresh Moroccan pastries|Drink endless cups of sweet Mint Tea|Drink fresh squeezed orange juice|Get lost in the completely blue-painted alleyways|Pet the hundreds of friendly street cats|Hike up to the Spanish Mosque for a panoramic sunset|Shop for hand-woven colorful blankets|Take a day trip to the Akchour Waterfalls|Get a brutal but amazing scrub in a traditional Hammam|Camp in the nearby Rif Mountains|Take an intense cooking class with a local family",
    "Sintra (Portugal)|mild,nature,culture,romance|#FFD700|sintra portugal pena palace colorful fairytale|Eat gourmet Portuguese fusion|Eat Travesseiros (puff pastry with almond cream)|Drink Port wine|Drink Ginjinha (cherry liqueur) from a chocolate cup|Explore the incredibly colorful, viral Pena Palace|Wander the mystical, moss-covered Initiation Well at Quinta da Regaleira|Hike up to the ancient Moorish Castle|Take a vintage tram down to the beach|Surf the massive waves at nearby Praia da Ursa|Explore the spooky, abandoned convent in the woods|Take a private tuk-tuk tour of the hills|Drive to Cabo da Roca, the westernmost point of Europe",
    "Salar de Uyuni (Bolivia)|cold,nature,adventure|#E0FFFF|salar de uyuni salt flats mirror reflection|Gourmet dinner served on a table made entirely of salt|Eat llama meat cooked over a stove|Drink Singani (Bolivian brandy)|Chew coca leaves to stay awake in the altitude|Take insane perspective-bending photos on the white salt|Spot bright pink flamingos in a blood-red lake|Drive a 4x4 across the endless, mirror-like Salt Flats|Sleep in a hotel made entirely out of salt blocks|Bathe in natural hot springs surrounded by freezing desert|Explore the creepy Train Cemetery|Hike a massive, dormant volcano at high altitude|Visit the surreal, bubbling mud geysers at dawn",
    "Banff (Canada)|cold,mountains,nature,adventure|#2F4F4F|banff canada lake louise mountains snow|Fine dining at the Fairmont Chateau Lake Louise|Eat massive plates of Canadian Poutine (fries, curds, gravy)|Drink ice wine from the local vineyards|Sip hot chocolate while ice skating|Rent a clear glass canoe on the impossibly turquoise Lake Louise|Soak in the Banff Upper Hot Springs|Take a helicopter tour over the massive Canadian Rockies|Hike to the spectacular Plain of Six Glaciers|Ski world-class powder at Sunshine Village|Ice climb up a frozen waterfall in Johnston Canyon|Spot massive wild Grizzly Bears|Take the steep gondola up Sulphur Mountain",
    "Tromso (Norway)|cold,nature,adventure,mountains|#000033|tromso norway snowy fjords aurora|Arctic fine dining with king crab|Eat dried fish like a true Viking|Taste Aquavit in the world's northernmost brewery|Drink hot toddies on a silent electric whale watching boat|Sleep in a viral glass igloo under the Northern Lights|Warm up by a fire in a cozy, candlelit cafe|Chase the Northern Lights in the arctic wilderness|Whale watch for massive Orcas in the fjords|Dog sled across the frozen tundra with Siberian Huskies|Snowshoe through silent, snowy valleys|Feed reindeer with indigenous Sami people|Ride the Fjellheisen cable car for sunset views",
    "Cinque Terre (Italy)|mild,hot,beach,culture|#DC143C|cinque terre italy colorful houses cliff sea|Eat pesto pasta (invented here!)|Eat fried seafood out of a paper cone|Taste Sciacchetrà sweet wine|Drink Aperol Spritz on a cliffside terrace|Take the scenic train between the 5 colorful villages|Hike the coastal trails with insane ocean views|Charter a private boat to sail past the colorful cliffs|Cliff jump into the Mediterranean Sea|Take a pesto-making masterclass|Scuba dive in the protected marine park|Watch the sunset from the viral Nessun Dorma restaurant|Explore the terraced vineyards on the cliffs",
    "Oaxaca (Mexico)|hot,city,culture,foodie|#FF4500|oaxaca mexico day of the dead colorful|Eat incredible authentic Mole|Eat Chapulines (toasted grasshoppers)|Take a high-end Mezcal tasting tour|Drink Mexican hot chocolate|Celebrate the spectacular Day of the Dead festival|Wander the insanely colorful streets and markets|Explore the ancient Zapotec ruins of Monte Albán|Swim in the petrified waterfalls of Hierve el Agua|Take a massive traditional cooking masterclass|Shop for Alebrijes (brightly painted wooden animals)|Visit a traditional Mezcal distillery|Hike the Sierra Norte mountains",
    
    # Adding the rest using compressed bulk variables for speed/safety. 
    "Miami (USA)|hot,beach,party,luxury|#FF1493|miami south beach neon palm trees|Luxury stone crab dining at Joe's|Eat authentic Cuban sandwiches in Little Havana|Champagne on a mega-yacht|Drink mojitos at a salsa club|Rollerblade down Ocean Drive in neon gear|Look at street art in Wynwood Walls|Party until 6 AM at a massive club like E11EVEN|Ride an airboat through the Everglades looking for alligators|Charter a private yacht to the Bahamas|Drive a neon Lamborghini down South Beach|Deep sea fishing for Marlin|Attend an exclusive Art Basel party",
    "Yellowstone (USA)|cold,mild,nature,adventure|#A0522D|yellowstone geyser bison nature|Gourmet game meat at a luxury lodge|Eat campfire chili out of a tin can|Craft beer tasting in a cowboy saloon|Drink cowboy coffee boiled over a fire|Watch Old Faithful erupt on schedule|Spot adorable bear cubs through binoculars|Snowmobile through the park in dead of winter|Spot packs of wild wolves in the Lamar Valley|Hike around the neon-colored Grand Prismatic Spring|Camp deep in grizzly bear country|Fly fish in freezing, crystal-clear rivers|Whitewater raft down the Snake River",
    "Costa Rica|hot,nature,adventure,relax|#006400|costa rica jungle waterfall sloth volcano|Gourmet dining at a luxury eco-resort|Eat hearty Gallo Pinto for breakfast|Drink Imperial beer on a surfboard|Taste fresh Costa Rican coffee right on the plantation|Cuddle rescued sloths at an animal sanctuary|Relax in a hammock listening to howler monkeys|Superman Zipline 1000ft above the jungle canopy|Soak in natural volcanic hot springs near Arenal|Surf world-class waves in Tamarindo|Night hike to spot deadly snakes and glowing frogs|Whitewater raft through Class 4 jungle rapids|Rappel down a massive roaring waterfall",
    "Rio de Janeiro (Brazil)|hot,beach,party,culture|#32CD32|rio de janeiro christ the redeemer copacabana|Endless premium meats at a luxury Churrascaria|Eat Pão de Queijo on the street|Drink Caipirinhas on Copacabana beach|Drink cold chopp in a lively boteco|Take the cable car up Sugarloaf Mountain|Buy a tiny bikini/sunga and play footvolley|Take a helicopter around the massive Christ the Redeemer statue|Dance Samba until dawn at the massive Carnival parade|Hang glide off a mountain and land on the beach|Explore the vibrant Favela communities|Hike through the Tijuca urban rainforest|Attend a massive soccer game at Maracanã Stadium",
    "Patagonia|cold,mountains,nature,adventure|#4682B4|patagonia glaciers mountains rugged|Gourmet Patagonian lamb cooked over an open fire|Eat empanadas after a freezing hike|Drink high-end Malbec wine|Drink bitter Mate tea with Gauchos|Spot adorable penguins on the coast|Pet wild guanacos (llamas)|Trek across the massive, cracking Perito Moreno Glacier|Hike the brutal base of Mount Fitz Roy|Kayak through incredible glowing marble caves|Spot wild Pumas on a tracking safari|Sail past towering icebergs on an expedition ship|Horseback ride across the endless steppe",
    "Amazon Rainforest|hot,nature,adventure|#004D00|amazon rainforest river jungle wild|Gourmet jungle fusion on a luxury riverboat|Eat roasted piranha you caught yourself|Drink Ayahuasca in a terrifying shamanic ceremony|Drink fresh exotic fruit juices|Spot sleepy sloths in the trees|Hold a colourful macaw parrot|Fish for deadly, sharp-toothed Piranhas|Take a night canoe trip to spot glowing Caiman eyes|Survive a multi-day deep jungle trek with a machete|Swim with legendary Pink River Dolphins|Visit an isolated indigenous tribe|Sleep in a hammock surrounded by jaguar territory",
    "Galapagos Islands|hot,nature,adventure,beach|#20B2AA|galapagos islands giant tortoise pristine beach|Luxury seafood dinner on a chartered yacht|Eat fresh Ecuadorian Ceviche|Drink cocktails on a cruise deck|Drink Pilsener beer with locals|Walk alongside massive, ancient Giant Tortoises|Watch Blue-Footed Boobies do their mating dance|Scuba dive with hundreds of Hammerhead Sharks|Snorkel with playful, curious Sea Lions|Hike across a barren, black lava field|Swim with marine iguanas|Take a Zodiac boat to remote islands|Spot penguins on the equator",
    "Machu Picchu (Peru)|mild,mountains,adventure,culture|#A0522D|machu picchu peru inca ruins mountains|Michelin-star modern Peruvian food|Eat roasted Guinea Pig (Cuy)|Drink Pisco Sours in a lively tavern|Drink Coca Tea to fight off the altitude sickness|Take selfies with fluffy Alpacas|Shop for vibrant colourful textiles|Hike the grueling 4-day classic Inca Trail|Sleep in a transparent capsule hanging 400ft off a cliff wall|Take a panoramic glass-roof train through the Andes|Mountain bike down the terrifying 'Death Road'|Hike the impossibly colourful Rainbow Mountain|Spot massive Andean Condors flying",
    "Cape Town (South Africa)|mild,beach,adventure,luxury|#CD853F|cape town table mountain ocean|10-course tasting menu at The Test Kitchen|Eat South African Biltong on a hike|World-class wine tasting via a wine tram|Drink Gin and Tonics on a sunset cruise|Walk with wild penguins at Boulders Beach|Ride the spinning cable car up Table Mountain|Cage dive with massive Great White Sharks|Paraglide off Lion's Head mountain over the ocean|Drive the spectacular Chapman's Peak coastal road|Visit the prison where Nelson Mandela was held|Surf the freezing waves of the Atlantic|Go on a nearby Big 5 Safari",
    "Serengeti (Tanzania)|hot,nature,adventure,luxury|#CD853F|serengeti plains acacia tree sunset|Champagne bush breakfast after a balloon ride|Eat Ugali and roasted goat|Drink local Safari beer|Drink fresh coffee grown on Kilimanjaro|Visit a traditional Maasai village|Watch cheetah cubs play in the tall grass|Take a Hot Air Balloon over the plains at dawn|Witness the Great Migration of millions of wildebeest|Sleep in a luxury canvas tent surrounded by roaring lions|Track the endangered Black Rhino in the Ngorongoro Crater|Climb to the roof of Africa: Mount Kilimanjaro|Scuba dive in nearby Zanzibar",
    "Marrakesh (Morocco)|hot,city,culture,foodie|#B22222|marrakesh morocco market medina colorful|Luxury dining in a stunning Riad courtyard|Eat slow-cooked Lamb Tagine|Drink endless cups of sweet Moroccan Mint Tea|Drink fresh squeezed orange juice|Get a brutal but amazing scrub in a traditional Hammam|Pet the stray cats in the souks|Get lost in the chaotic, maze-like markets (Souks)|Ride camels through the Sahara Desert|Sleep in a luxury desert camp under the stars|Take a hot air balloon over the Atlas Mountains|Watch snake charmers in Jemaa el-Fnaa square|Drive an ATV through the rocky desert",
    "Sydney (Australia)|mild,hot,city,beach,party|#1E90FF|sydney opera house harbour bridge ocean|Fine dining inside the Sydney Opera House sails|Eat a classic Aussie meat pie|Cocktails at a rooftop bar overlooking the Harbour|Drink pints of Victoria Bitter|Pet Kangaroos and Koalas at the zoo|Take the scenic ferry to Manly Beach|Climb the massive arch of the Sydney Harbour Bridge|Surf the famous waves at Bondi Beach|Sail a yacht around the spectacular Sydney Harbour|Take a seaplane to a luxury waterside restaurant|Party at the massive Mardi Gras festival|Scuba dive with Grey Nurse Sharks in Manly",
    "Queenstown (New Zealand)|mild,cold,mountains,adventure|#556B2F|queenstown new zealand mountains lake extreme|Fine dining accessible only by a steep gondola|Eat the world-famous, massive Fergburger|Taste world-class Pinot Noir|Drink shots in an ice bar|Ride the Luge go-karts down the mountain|Soak in the private, cliffside Onsen Hot Pools|Bungee jump off the Kawarau Bridge|Jet boat at 90km/h through narrow river canyons|Skydive over the breathtaking Remarkables mountain range|Helicopter ski on untouched alpine powder|Hike the brutal, rewarding Ben Lomond track|Paraglide off a mountain over the town",
    "Bora Bora (French Polynesia)|hot,beach,relax,luxury|#00BFFF|bora bora tropical island luxury overwater|Private dinner served on the beach|Eat Tahitian Poisson Cru|Drink cocktails out of a freshly cut coconut|Drink Hinano Tahiti beer|Get a traditional Polynesian flower crown|Have breakfast delivered to your bungalow by canoe|Sleep in a massive, $2000/night overwater bungalow|Swim with friendly reef sharks and stingrays|Take a helicopter ride around Mount Otemanu|Jet ski across the impossibly blue lagoon|Attend an intense Polynesian fire dancing show|Scuba dive outside the reef for lemon sharks",
    
    # Standardizing rest to fill to exactly 100 perfectly formatted options.
    "Tahiti|hot,beach,culture|#20B2AA|tahiti jungle beach waterfall|Luxury French-Polynesian dining|Food truck steak frites|Hinano beer|Coconut rum|Black pearl shopping|Fire dancing|Surfing Teahupo'o|Hiking Mount Aorai|Scuba diving|Whale watching|4x4 jungle safari|Lagoon cruise",
    "Samoa|hot,beach,adventure|#3CB371|samoa tropical ocean trench|Umu feast|Taro root chips|Vailima beer|Kava|Swimming in To Sua Ocean Trench|Watching blowholes|Surfing|Jungle trekking|Fire knife dancing|Scuba diving|Village homestay|Waterfall sliding",
    "Vanuatu|hot,adventure,nature|#8B4513|vanuatu volcano jungle|Luxury resort dining|Laplap root dish|Tusker beer|Kava|Swimming in blue holes|Watching land diving (original bungee)|Standing on the rim of an erupting volcano|Scuba diving the SS President Coolidge|Jungle trekking|Helicopter tours|Sailing|Deep sea fishing",
    "Hawaii (Oahu)|hot,beach,city,surfing|#1E90FF|oahu hawaii waikiki beach surfing|Nobu Honolulu|Poke bowl from a grocery store|Mai Tais at the Royal Hawaiian|Kona brewing beer|Visiting Pearl Harbor|Eating Dole Whip|Surfing massive winter waves on North Shore|Hiking the terrifying Haiku Stairs (Stairway to Heaven)|Shark cage diving|Helicopter tours|Attending a luau|Skydiving",
    "Hawaii (Kauai)|hot,nature,adventure|#006400|kauai hawaii napali coast cliffs|Luxury oceanfront dining|Shave ice|Tropical cocktails|Local coffee|Hiking Waimea Canyon|Helicopter over Jurassic Park falls|Sailing the dramatic Na Pali coast|Kayaking the Wailua River|Ziplining|Surfing|Scuba diving|Off-roading",
    "Alaska|cold,nature,adventure|#4682B4|alaska glacier bears mountains|Gourmet King Salmon|Reindeer sausage|Alaskan Amber beer|Hot toddy|Spotting bald eagles|Dog sledding on a glacier|Taking a bush plane to bear country|Ice climbing|Whale watching cruise|Hiking Denali|Kayaking near glaciers|Fishing for halibut",
    "Yosemite|mild,mountains,nature|#2F4F4F|yosemite half dome valley trees|Ahwahnee Hotel dining|Trail mix on a cliff|Craft beer|Campfire whiskey|Watching rock climbers on El Capitan|Photographing waterfalls|Hiking the brutal Half Dome cables|Camping in the wilderness|Snowshoeing in winter|Whitewater rafting|Helicopter tours|Bear spotting",
    "Grand Canyon|hot,nature,adventure|#D2691E|grand canyon red rocks massive|El Tovar dining|Campfire beans|Prickly pear margaritas|Canteen water|Walking the glass Skywalk|Riding mules down the canyon|Whitewater rafting the violent Colorado River|Taking a helicopter into the canyon|Hiking rim to rim|Camping at the bottom|Skydiving|Off-roading",
    "Zion National Park|hot,nature,adventure|#A0522D|zion national park red rocks canyon|Luxury lodge dining|Bison burger|Local IPA|Campfire coffee|Wading through the Narrows|Stargazing|Hiking the terrifying Angel's Landing|Canyoneering down waterfalls|Rock climbing|Helicopter tours|ATV riding|Horseback riding",
    "Sedona|hot,nature,relax|#CD5C5C|sedona red rocks vortex spiritual|Gourmet southwestern food|Cactus tacos|Agave tequila|Local wine|Visiting a spiritual energy vortex|Shopping for crystals|Taking a Pink Jeep tour over the rocks|Hiking Cathedral Rock|Hot air ballooning|Mountain biking|Spa retreat|Helicopter tours",
    "New Orleans|mild,city,party,foodie|#800080|new orleans bourbon street jazz|Commander's Palace turtle soup|Massive powdered Beignets at Cafe Du Monde|Hurricanes at Pat O'Brien's|Hand Grenade on Bourbon Street|Listening to live jazz on Frenchmen St|Taking a voodoo walking tour|Partying at Mardi Gras|Swamp airboat tour for alligators|Steamboat cruise on the Mississippi|Drinking on the street legally|Eating spicy crawfish boils|Exploring the above-ground cemeteries",
    "Chicago|cold,city,foodie|#4682B4|chicago skyline bean lake|Alinea 3-Michelin star|Deep dish pizza|Goose Island beer|Malort shots (disgusting but local)|Taking a picture at the Bean|Watching a Cubs game at Wrigley Field|Architecture river cruise|Standing on the glass floor at the Willis Tower|Eating a Chicago dog|Visiting the Art Institute|Walking the Navy Pier|Blues club hopping",
    "Toronto|cold,city,culture|#708090|toronto skyline cn tower city|Dining in the rotating CN Tower restaurant|Poutine|Canadian Club whiskey|Caesar cocktail|Visiting the Hockey Hall of Fame|Walking the Distillery District|EdgeWalk (hanging off the outside of the CN Tower)|Niagara Falls day trip|Exploring the massive underground city|Attending TIFF|Sailing Lake Ontario|Eating at St. Lawrence Market",
    "Montreal|cold,city,foodie,party|#8B0000|montreal canada cobblestone french|Joe Beef gluttony|Montreal smoked meat sandwich|Ice cider|Craft beer|Walking Old Montreal|Eating bagels|Partying at a massive underground club|Attending the Jazz Festival|Ice skating|Hiking Mount Royal|Formula 1 race|Casino de Montreal",
    "Vancouver|mild,city,nature,adventure|#2E8B57|vancouver mountains ocean city skyline|High-end sushi|Japadog from a street cart|BC Wine|Craft IPA|Walking Stanley Park|Crossing the Capilano Suspension Bridge|Skiing at Whistler Blackcomb|Whale watching|Seaplane tour|Hiking the Grouse Grind|Mountain biking|Kayaking",
    "Whistler|cold,mountains,adventure|#E0FFFF|whistler skiing mountains snow|Gourmet alpine dining|Beavertails pastry|Hot toddy|Apres-ski beers|Riding the Peak 2 Peak gondola|Snowshoeing|Skiing massive slopes|Heli-skiing|Bungee jumping|Ziplining|Mountain biking in summer|Bear watching",
    "Belize|hot,beach,nature,adventure|#20B2AA|belize blue hole ocean jungle|Luxury lobster dinner|Fry jacks|Belikin beer|Rum punch|Exploring Mayan ruins|Cave tubing|Scuba diving the massive Great Blue Hole|Swimming with sharks at Shark Ray Alley|Jungle trekking|Ziplining|Sailing|Deep sea fishing",
    "Panama City|hot,city,culture|#B22222|panama canal city skyline|High-end seafood|Sancocho soup|Panama beer|Rum|Walking Casco Viejo|Buying a Panama hat|Watching massive ships go through the Panama Canal|Jungle tour|Visiting indigenous tribes|Helicopter tour|Sailing|Scuba diving",
    "Bogota|mild,city,culture,party|#800080|bogota colombia street art city|Gourmet Colombian fusion|Ajiaco soup|Aguardiente|Colombian coffee|Riding the cable car up Monserrate|Taking a graffiti tour|Partying in a massive multi-story club (Theatron)|Visiting the Gold Museum|Eating exotic fruits in Paloquemao|Salt Cathedral of Zipaquira|Hiking|Cycling on Sunday (Ciclovia)",
    "Medellin|mild,city,party|#32CD32|medellin colombia mountains cable car|High-end dining in El Poblado|Bandeja Paisa (massive meat platter)|Aguardiente|Craft beer|Riding the Metrocable|Taking a Pablo Escobar history tour|Partying on rooftops|Paragliding over the city|Day trip to Guatape rock|Exploring Comuna 13|Salsa dancing|Coffee farm tour",
    "Quito|mild,mountains,culture|#8B4513|quito ecuador volcanoes colonial|Gourmet Andean food|Ceviche|Pilsener beer|Canelazo (hot rum drink)|Standing on the Equator|Walking the historic center|Taking the teleferiQo up the volcano|Hiking Cotopaxi|Exploring the cloud forest|Visiting the Galapagos|Mountain biking|Shopping at Otavalo market",
    "Lima|mild,city,foodie|#A0522D|lima peru coast city food|Central (world's #1 restaurant)|Anticuchos (beef heart skewers)|Pisco Sour|Chicha Morada|Walking the Malecon|Paragliding off the cliffs|Surfing in the city|Exploring the catacombs|Visiting Huaca Pucllana ruins|Eating massive ceviche platters|Sandboarding in nearby dunes|Pisco tasting",
    "Santiago|mild,city,mountains|#4682B4|santiago chile andes mountains|Gourmet Chilean seafood|Empanadas|Carménère wine|Pisco|Riding the funicular up San Cristobal|Visiting Pablo Neruda's house|Skiing in the nearby Andes|Wine tasting in the Maipo Valley|Hiking|Helicopter tour|Partying in Bellavista|Day trip to Valparaiso",
    "Atacama Desert|hot,nature,adventure|#D2691E|atacama desert chile dry mars|Luxury desert lodge dining|Llama meat|Pisco Sour|Coca tea|Floating in a hyper-salty lagoon|Stargazing with powerful telescopes|Watching the Tatio Geysers erupt at dawn|Sandboarding down massive dunes|Exploring the Valle de la Luna (Moon Valley)|Hiking volcanoes|Mountain biking|Hot air ballooning",
    "Mendoza|mild,nature,relax,foodie|#8B0000|mendoza vineyards mountains wine|7-course wine pairing lunch|Asado BBQ|Malbec wine|Fernet|Biking between vineyards|Horseback riding|Tasting world-class Malbec directly from the barrel|Whitewater rafting|Hiking Mount Aconcagua|Paragliding|Hot springs|Zip lining",
    "Iguazu Falls|hot,nature,adventure|#006400|iguazu falls massive waterfalls jungle|Luxury lodge dining|Empanadas|Caipirinha|Mate tea|Spotting toucans|Walking the boardwalks|Taking a speedboat directly under the massive waterfalls|Helicopter tour over the falls|Jungle trekking|Whitewater rafting|Ziplining|Bird watching park",
    "Salvador|hot,city,culture,party|#FF8C00|salvador brazil colorful colonial capoeira|Moqueca (seafood stew)|Acaraje (fried bean dough)|Caipirinha|Cold beer|Watching Capoeira in the street|Buying a colorful ribbon|Dancing at a massive street party|Attending a Candomble ceremony|Exploring the Pelourinho|Sailing|Scuba diving|Beach hopping",
    "Zanzibar|hot,beach,culture,relax|#20B2AA|zanzibar beach spice island doors|Luxury seafood at The Rock restaurant|Zanzibar pizza in the night market|Cocktails on a dhow boat|Spiced tea|Exploring Stone Town's carved doors|Taking a spice farm tour|Scuba diving the coral reefs|Swimming with wild dolphins|Kitesurfing|Sailing a traditional dhow|Feeding giant tortoises|Deep sea fishing",
    "Mauritius|hot,beach,nature,luxury|#FF61A6|mauritius beach ocean luxury|Gourmet French-Creole fusion|Dholl puri street food|Phoenix beer|Rum tasting|Visiting the Seven Colored Earth|Swimming in waterfalls|Taking a helicopter to see the 'Underwater Waterfall' illusion|Scuba diving|Kitesurfing|Deep sea fishing|Hiking Le Morne|Catamaran cruise",
    "Kilimanjaro|cold,mountains,adventure|#2F4F4F|kilimanjaro mountain snow africa|Celebratory steak post-climb|Camp food in a tent|Kilimanjaro beer|Hot tea in the freezing cold|Seeing monkeys at the base|Stargazing|Enduring a brutal 7-day trek to the highest peak in Africa|Summiting at dawn in freezing temperatures|Going on a nearby safari|Visiting a coffee farm|Hot springs dip|Helicopter rescue/tour",
    "Nairobi|hot,city,nature|#8B4513|nairobi kenya giraffe city safari|Carnivore restaurant (exotic meats)|Nyama Choma (roast meat)|Tusker beer|Kenyan coffee|Feeding giraffes from a hotel window|Fostering baby elephants|Going on a safari with city skyscrapers in the background|Hiking Mount Kenya|Helicopter over the Rift Valley|Visiting the Masai Mara|Hot air ballooning|Cultural village tours",
    "Kigali|mild,city,nature,adventure|#228B22|rwanda gorillas jungle green|Gourmet dining at Hotel Rwanda|Brochettes|Virunga beer|Rwandan coffee|Visiting the Genocide Memorial|Shopping in vibrant markets|Trekking through the dense jungle to sit with wild Silverback Gorillas|Chimpanzee tracking|Canopy walkway|Helicopter tours|Safari in Akagera|Lake Kivu cruise",
    "Dakar|hot,city,culture|#D2691E|dakar senegal coast colorful|Thiéboudienne (fish and rice)|Street peanuts|Flag beer|Bissap juice|Visiting the African Renaissance Monument|Taking a ferry to Goree Island|Surfing the warm waves|Off-roading to the Pink Lake (Retba)|Listening to live Mbalax music|Exploring vibrant markets|Scuba diving|Desert safaris",
    "Tel Aviv|hot,city,beach,party|#FF4500|tel aviv israel beach sunset city|High-end Mediterranean fusion|The best hummus and falafel of your life|Arak shots|Goldstar beer|Playing Matkot (paddleball) on the beach|Browsing Carmel Market|Partying until dawn in massive underground clubs|Surfing|Day trip to float in the Dead Sea|Exploring ancient Jaffa|Sailing|Helicopter tours",
    "Jerusalem|hot,city,culture|#B22222|jerusalem ancient walls religion|Gourmet kosher dining|Shawarma|Pomegranate juice|Israeli wine|Leaving a note in the Western Wall|Walking the Via Dolorosa|Exploring the ancient underground tunnels|Visiting the Dome of the Rock|Floating in the Dead Sea|Touring the Mount of Olives|Machane Yehuda market at night|Exploring Bethlehem",
    "Beirut|mild,city,party,foodie|#800080|beirut lebanon city ruins sea|Gourmet Lebanese Mezze|Manakish (flatbread)|Arak|Almaza beer|Walking the Corniche|Visiting the Pigeon Rocks|Partying in a massive rooftop club|Exploring Roman ruins in Baalbek|Skiing in the mountains (same day as beach)|Wine tasting in the Bekaa Valley|Exploring the Jeita Grotto caves|Helicopter tours",
    "Muscat|hot,city,nature,culture|#D4AF37|muscat oman grand mosque desert|Luxury Omani dining|Shuwa (slow cooked meat)|Omani coffee with cardamom|Mint tea|Visiting the stunning Grand Mosque|Shopping for Frankincense in the souk|Swimming in the emerald waters of Wadi Shab|Dune bashing in the Wahiba Sands|Scuba diving the Daymaniyat Islands|Sleeping in a luxury desert camp|Sailing a traditional dhow|Turtle watching",
    "Abu Dhabi|hot,city,luxury,adventure|#DAA520|abu dhabi grand mosque luxury|Emirates Palace gold-flaked cappuccino|Shawarma|Champagne on a yacht|Camel milk|Visiting the massive, white Grand Mosque|Exploring the Louvre Abu Dhabi|Riding the fastest rollercoaster in the world at Ferrari World|Driving a Formula 1 car on the Yas Marina Circuit|Dune bashing|Falconry hospital|Luxury desert resort|Scuba diving",
    "Doha|hot,city,luxury,culture|#8B0000|doha qatar skyline desert|Luxury dining at Nobu Doha|Machboos (spiced rice)|Mocktails in a skyscraper|Karak Chai|Browsing the Souq Waqif|Visiting the Museum of Islamic Art|Dune bashing in a 4x4|Taking a traditional dhow cruise|Watching camel racing (with robot jockeys!)|Shopping in massive luxury malls|Skydiving|Helicopter tours",
    "Malta|hot,beach,culture,party|#D2691E|malta valletta ancient sea boats|Gourmet rabbit stew|Pastizzi (cheese pastries)|Cisk beer|Kinnie (local soda)|Exploring the silent city of Mdina|Taking a boat to the Blue Lagoon|Scuba diving massive WWII shipwrecks|Partying in Paceville|Exploring ancient megalithic temples|Rock climbing|Sailing|Cliff jumping",
    "Cyprus|hot,beach,culture,party|#FF8C00|cyprus beach ruins sea|High-end Meze|Halloumi cheese|Commandaria wine|Ouzo|Visiting the Tombs of the Kings|Bathing in the Baths of Aphrodite|Partying at massive clubs in Ayia Napa|Scuba diving the Zenobia shipwreck|Skiing in the Troodos Mountains|Kitesurfing|Sailing|Wine tasting",
    "Crete|hot,beach,culture|#00008B|crete greece beach ruins|Gourmet Greek seafood|Dakos (rusk with tomato)|Raki shots|Local wine|Exploring the Palace of Knossos|Walking the pink sand of Elafonissi beach|Hiking the massive, brutal Samaria Gorge|Scuba diving|Sailing|Off-roading in the mountains|Cooking class|Helicopter tours",
    "Mykonos|hot,beach,party,luxury|#00BFFF|mykonos windmills party beach|Luxury seafood at Nammos|Gyros|Champagne bottle service|Ouzo|Taking photos with the iconic windmills|Wandering Little Venice|Partying until 8 AM at massive beach clubs|Chartering a luxury yacht|Scuba diving|Helicopter to Santorini|Windsurfing|Private villa party",
    "Krakow|cold,city,culture,party|#8B4513|krakow poland square winter|Gourmet Polish Pierogi|Zapiekanka (street pizza bread)|Vodka tasting|Tyskie beer|Listening to the bugle call in the main square|Exploring the Wawel Castle|Visiting the dark, historical Auschwitz memorial|Exploring the massive underground Salt Mine|Partying in underground cellar bars|Shooting range|Hot air ballooning|Day trip to the Tatra mountains",
    "Budapest|cold,city,party,relax|#B22222|budapest parliament river baths|Gourmet Goulash|Chimney cake|Palinka (fruit brandy)|Unicum|Soaking in the Szechenyi Thermal Baths|Walking the Chain Bridge|Partying in the wild, eclectic Ruin Pubs|Taking a nighttime river cruise past the glowing Parliament|Exploring the Buda Castle labyrinth|Caving under the city|Helicopter tour|Escape rooms",
    "Vienna|mild,city,culture|#FFD700|vienna austria palaces music|Gourmet Wiener Schnitzel|Sachertorte|Viennese coffee|Gruner Veltliner wine|Watching the Lipizzaner horses|Riding the historic Riesenrad ferris wheel|Attending a grand ball in a tuxedo/gown|Listening to a Mozart concert in a golden hall|Touring the massive Schonbrunn Palace|Visiting the creepy catacombs|Horse-drawn carriage ride|Sailing the Danube",
    "Salzburg|cold,mountains,culture|#2E8B57|salzburg austria mountains mozart|Fine dining in the Hohensalzburg Fortress|Mozartkugel chocolate|Stiegl beer|Schnapps|Taking the Sound of Music tour|Visiting Mozart's birthplace|Exploring the massive ice caves (Eisriesenwelt)|Skiing in the nearby Alps|Paragliding|Attending the Salzburg Festival|Salt mine tour|Hiking",
    "Copenhagen|cold,city,foodie,culture|#4682B4|copenhagen nyhavn boats bikes|Noma (world's best restaurant)|Smorrebrod (open sandwich)|Carlsberg beer|Aquavit|Riding the wooden rollercoasters at Tivoli Gardens|Walking the colorful Nyhavn harbor|Renting a boat and driving it through the canals yourself|Exploring the hippie commune of Christiania|Cycling the city|Bathing in the freezing harbor baths|Helicopter tour|Castle tour",
    "Stockholm|cold,city,culture|#708090|stockholm sweden islands boats|Gourmet Swedish meatballs|Cinnamon buns (Fika)|Absolut Vodka|Craft beer|Exploring the Vasa Museum (massive sunken ship)|Walking Gamla Stan (Old Town)|Sailing through the 30,000 islands of the archipelago|Ice skating on frozen lakes|Kayaking the city canals|ABBA Museum|Hot air ballooning|Sleeping in the Ice Hotel (day trip)",
    "Oslo|cold,city,nature|#0B3D91|oslo norway fjord modern|New Nordic cuisine|Brown cheese|Aquavit|Craft beer|Walking on the roof of the Opera House|Visiting the Viking Ship Museum|Skiing at the Holmenkollen jump|Cruising the Oslofjord|Floating in a sauna and jumping in the freezing fjord|Ziplining|Hiking|Helicopter tour",
    "Bergen|cold,mountains,nature|#2F4F4F|bergen norway fjords colorful houses|Gourmet seafood|Fish market crab|Aquavit|Hot cocoa|Taking the funicular up Mount Floyen|Walking the historic Bryggen wooden houses|Taking a boat deep into the massive, dramatic fjords|Hiking the rugged mountains|Helicopter over the glaciers|Kayaking|Scuba diving|Train ride to Flam",
    "Helsinki|cold,city,relax,nature|#E0FFFF|helsinki finland sauna snow|Gourmet reindeer|Karelian pasty|Koskenkorva vodka|Lonkero (gin long drink)|Visiting the Suomenlinna sea fortress|Shopping in Market Square|Getting naked in a public sauna and jumping in the Baltic Sea|Icebreaking cruise|Dog sledding|Ferry to Tallinn|Helicopter tour|Hiking in Nuuksio",
    "Tallinn|cold,city,culture|#8B4513|tallinn estonia medieval walls|Gourmet Baltic food|Roasted almonds|Vana Tallinn liqueur|Craft beer|Walking the preserved medieval walls|Exploring the secret KGB museum|Partying in hidden speakeasies|Taking a bog-shoeing tour in the wilderness|Ice skating|Hot air ballooning|Shooting range|Ferry to Helsinki",
    "Riga|cold,city,party|#B22222|riga latvia art nouveau|Gourmet Latvian food|Rye bread pudding|Black Balsam|Local beer|Admiring the Art Nouveau architecture|Browsing the massive Central Market (housed in Zeppelin hangars)|Bobsledding on an actual Olympic track|Partying in massive clubs|Husky dog sledding|Shooting AK-47s|Wind tunnel flying|Kayaking the city canal",
    "Vilnius|cold,city,culture|#800080|vilnius lithuania churches|Gourmet Lithuanian food|Cepelinai (potato dumplings)|Midus (mead)|Craft beer|Visiting the independent republic of Uzupis|Walking the old town|Taking a hot air balloon directly over the city center|Visiting the terrifying KGB museum|Exploring Trakai Island Castle|Shooting range|Ice skating|Kayaking",
    "Kyiv|cold,city,culture|#FFD700|kyiv ukraine golden domes|Gourmet Chicken Kyiv|Borscht|Horilka (vodka)|Kvass|Visiting the golden-domed Pechersk Lavra|Walking the deep metro stations|Taking a chilling, fascinating tour of the Chernobyl Exclusion Zone|Exploring massive Soviet monuments|Partying in underground techno clubs|Shooting range|Tank driving|Hot air ballooning",
    "Bratislava|cold,city,party|#4682B4|bratislava slovakia castle|Gourmet Slovak food|Bryndzove halusky (potato dumplings)|Slivovica (plum brandy)|Local beer|Visiting the UFO tower|Walking to the Bratislava Castle|Partying in wild stag-do clubs|Speedboating on the Danube to Vienna|Wine tasting in the Small Carpathians|Shooting range|Escape rooms|Hiking",
    "Ljubljana|mild,city,nature|#32CD32|ljubljana slovenia dragons river|Gourmet Slovenian food|Kranjska klobasa (sausage)|Slovenian wine|Union beer|Taking a photo with the Dragon Bridge|Taking the funicular to the castle|Exploring the massive, incredible Postojna Cave|Taking a day trip to row a boat to the island on Lake Bled|Hiking the Julian Alps|Whitewater rafting the Soca River|Hot air ballooning|Wine tasting",
    "Zagreb|mild,city,culture|#DC143C|zagreb croatia city red roofs|Gourmet Croatian food|Strukli|Rakija|Ozujsko beer|Visiting the Museum of Broken Relationships|Riding the tiny funicular|Taking a day trip to the stunning Plitvice Lakes waterfalls|Exploring the Medvednica mountain|Partying on Tkalciceva street|Escape rooms|Hot air ballooning|Wine tasting",
    "Split|hot,beach,culture,party|#00BFFF|split croatia diocletians palace sea|Gourmet Dalmatian seafood|Cevapi|Rakija|Local wine|Rubbing the toe of Gregory of Nin|Walking the Riva promenade|Exploring the massive, ancient ruins of Diocletian's Palace|Taking a speedboat to the Blue Cave|Partying at Ultra Europe (in summer)|Sailing to Hvar|Ziplining over the Cetina canyon|Whitewater rafting",
    "Hvar|hot,beach,party,luxury|#FF1493|hvar croatia yacht party beach|Luxury seafood|Peka (meat cooked under a bell)|Champagne|Cocktails at Carpe Diem|Climbing to the Spanjola fortress|Wandering the lavender fields|Partying all night at famous beach clubs|Chartering a yacht to the Pakleni Islands|Scuba diving|Skydiving|Deep sea fishing|Wine tasting",
    "Kotor|hot,mountains,nature|#2F4F4F|kotor montenegro bay mountains|Gourmet seafood|Njeguski prsut (prosciutto)|Rakija|Vranac wine|Feeding the hundreds of cats|Taking a boat to Our Lady of the Rocks|Climbing the brutal 1,350 steps to the fortress for insane views|Whitewater rafting the Tara River Canyon|Sailing the dramatic Bay of Kotor|Ziplining|Paragliding|Canyoning",
    "Tirana|hot,city,culture|#FF4500|tirana albania bunkers colorful|Gourmet Albanian food|Byrek|Raki|Tirana beer|Riding the Dajti Ekspres cable car|Walking Skanderbeg Square|Exploring Bunk'Art (massive underground Cold War bunker)|Taking a day trip to the Albanian Riviera beaches|Hiking the Accursed Mountains|Off-roading|Wine tasting|Helicopter tours",
    "Sarajevo|mild,city,culture,mountains|#8B4513|sarajevo bosnia culture mountains|Gourmet Bosnian food|Cevapi in Baščaršija|Rakija|Bosnian coffee|Visiting the Latin Bridge (where WWI started)|Walking the copper smith streets|Exploring the fascinating Tunnel of Hope from the siege|Hiking or skiing the abandoned 1984 Olympic bobsled track|Whitewater rafting the Neretva|Canyoning|Paragliding|Off-roading",
    "Belgrade|mild,city,party|#B22222|belgrade serbia river fort|Gourmet Serbian food|Pljeskavica (Serbian burger)|Rakija|Jelen beer|Walking the Kalemegdan fortress|Visiting the massive St. Sava Temple|Partying until dawn on the floating river clubs (Splavovi)|Taking a boat cruise on the Danube and Sava|Exploring underground tunnels|Shooting range|Escape rooms|Wine tasting",
    "Sofia|mild,city,mountains|#556B2F|sofia bulgaria cathedral mountains|Gourmet Bulgarian food|Banitsa|Rakia|Ayran|Visiting the massive Alexander Nevsky Cathedral|Walking Vitosha Boulevard|Skiing or hiking Vitosha Mountain right outside the city|Exploring the Rila Monastery|Bathing in mineral hot springs|Escape rooms|Off-roading|Paragliding",
    "Bucharest|mild,city,party|#800080|bucharest romania parliament city|Gourmet Romanian food|Mici (grilled meat rolls)|Tuica (plum brandy)|Ursus beer|Walking the Old Town|Visiting the Village Museum|Touring the absurdly massive Palace of the Parliament|Partying in wild, massive clubs|Taking a day trip to 'Dracula's' Bran Castle|Driving the spectacular Transfagarasan highway|Shooting range|Escape rooms",
    "Athens|hot,city,culture|#D2691E|athens greece acropolis ruins|Gourmet Greek dining|Souvlaki|Ouzo|Frappe coffee|Watching the changing of the guard|Wandering Plaka|Climbing the Acropolis to see the Parthenon|Taking a ferry to the Greek Islands|Sailing the Athenian Riviera|Scuba diving|Helicopter tour|Partying in Gazi",
    "Torshavn|cold,nature,adventure|#2F4F4F|faroe islands puffins cliffs green|Gourmet Faroese food|Fermented lamb|Føroya Bjór beer|Aquavit|Watching the grass-roofed houses|Spotting adorable puffins|Hiking to the spectacular Mulafossur waterfall over the ocean|Taking a helicopter between the islands|Sailing beneath towering sea cliffs|Kayaking the fjords|Deep sea fishing|Rappelling",
    "Edinburgh|cold,city,culture,party|#4682B4|edinburgh scotland castle harry potter|Gourmet Scottish dining|Deep fried Mars bar|Scotch whiskey|Tennent's beer|Walking the Royal Mile|Finding Harry Potter inspirations|Climbing Arthur's Seat (a dormant volcano) for city views|Exploring the massive Edinburgh Castle|Taking a terrifying underground vault ghost tour|Attending the chaotic Fringe Festival|Day trip to the Highlands|Partying in Cowgate",
    "Dublin|mild,city,party,culture|#228B22|dublin ireland guinness pub|Gourmet Irish food|Irish stew|Guinness|Jameson whiskey|Seeing the Book of Kells|Walking Temple Bar|Drinking endless pints in a 300-year-old pub|Touring the Guinness Storehouse and pulling your own pint|Taking a day trip to the stunning Cliffs of Moher|Exploring the haunting Kilmainham Gaol|Listening to live trad music|Attending a massive hurling match",
    "Galway|mild,city,culture,party|#32CD32|galway ireland coast pub|Gourmet seafood|Galway oysters|Guinness|Irish coffee|Walking the Salthill Promenade|Listening to buskers on Shop Street|Taking a boat to the rugged Aran Islands|Driving the spectacular Wild Atlantic Way|Partying in Latin Quarter pubs|Horseback riding on the beach|Surfing|Deep sea fishing",
    "Belfast|mild,city,culture|#708090|belfast titanic murals history|Gourmet Northern Irish food|Ulster fry|Bushmills whiskey|Guinness|Taking a Black Cab political mural tour|Visiting the massive Titanic Belfast museum|Driving the spectacular Causeway Coastal Route|Walking the Giant's Causeway|Exploring Game of Thrones filming locations|Crossing the terrifying Carrick-a-Rede rope bridge|Partying in the Cathedral Quarter|Escape rooms",
    "Cardiff|mild,city,culture|#B22222|cardiff wales castle rugby|Gourmet Welsh food|Welsh rarebit|Brains beer|Welsh whisky|Walking Cardiff Bay|Visiting Cardiff Castle|Attending a massive, deafening rugby match at the Principality Stadium|Taking a speedboat ride on the bay|Hiking the nearby Brecon Beacons|Coasteering (cliff jumping) in Pembrokeshire|Exploring coal mines|Whitewater rafting",
    "Manchester|mild,city,party|#FF4500|manchester uk city football|Gourmet dining|Meat pie|Craft beer|Gin|Walking the Northern Quarter|Visiting the John Rylands Library|Attending a massive Premier League football match (City or United)|Partying at the Warehouse Project|Taking a music history tour (Oasis, The Smiths)|Skiing at the indoor Chill Factore|Escape rooms|Helicopter tour",
    "Liverpool|mild,city,party,culture|#DC143C|liverpool uk beatles docks|Gourmet dining|Scouse (stew)|Craft beer|Gin|Walking the Albert Dock|Visiting the Cavern Club|Taking the Magical Mystery Beatles Tour|Attending a match at Anfield|Taking the ferry cross the Mersey|Partying on Mathew Street|Escape rooms|Helicopter tour"
]

# Safely unpack the compressed destinations
dests = {}
for row in raw_dests:
    parts = row.split("|")
    dests[parts[0]] = {
        "t": parts[1].split(","), "c": parts[2], "p": parts[3],
        "f": [parts[4], parts[5]], "d": [parts[6], parts[7]], "cu": [parts[8], parts[9]],
        "e": [parts[10], parts[11], parts[12], parts[13], parts[14], parts[15]]
    }

# ---------------------------------------------------------
# 3. 50 OPAQUE & SILLY PSYCHOLOGICAL QUESTIONS
# ---------------------------------------------------------
# Format: "Question|Opt1|tags|cheeky|Opt2|tags|cheeky|Opt3|tags|cheeky|Opt4|tags|cheeky|Opt5|tags|cheeky"
raw_qs = [
    "How do you handle a group project?|I do 100% of the work so it's perfect|city,luxury,culture|Control freak energy. I respect it.|I make the PowerPoint look pretty and do nothing else|beach,relax,mild|Aesthetic over substance. Classic.|I am the one who brings the snacks|foodie,party,hot|You are the true MVP.|I argue with everyone and take charge|adventure,mountains,cold|Dictator vibes. Let's conquer.|I disappear completely and ghost the group|nature,budget,relax|Into the wild you go.",
    "How do you approach a mildly expired carton of milk?|Throw it away. It's poison now.|luxury,city,culture|A refined palate takes no risks.|Smell test. If it doesn't burn my nose, we're good.|adventure,hot,party|Living dangerously!|Drink it to build immunity|nature,mountains,cold|You have a stomach of steel.|Force a friend to taste it first|beach,relax,mild|A true test of friendship.|Bake it into something and hope for the best|foodie,budget,romance|Resourceful and terrifying.",
    "What is your dominant toxic trait?|I think I could win a fistfight with a bear|adventure,mountains,nature|Confidence is key, I guess?|I buy clothes for the fantasy version of myself|luxury,romance,city|We all need an imaginary gala to attend.|I ghost people because I was 'too busy relaxing'|relax,beach,cold|The ultimate chiller.|I turn every conversation into a debate|culture,party,hot|You sound exhausting. I love it.|I literally cannot eat without watching a specific YouTube video|foodie,mild,budget|Ah, a digital diner.",
    "Your response to 'We need to talk'?|Fake my own death and move to a new country|adventure,nature,budget|A reasonable reaction.|Reply 'Yes we do.' Turn the tables.|city,culture,cold|Checkmate. Brilliant.|Panic, sweat, and apologize for things I didn't do|relax,beach,mild|Anxiety level: 1000.|Ignore the text and go to a club|party,hot,luxury|Denial is a beautiful thing.|Send a meme to defuse the tension|foodie,romance,mountains|Laughter is the best defense.",
    "What’s your preferred method of passive aggression?|'As per my last email...'|city,culture,luxury|Corporate savagery.|Leaving them on read for 48 hours|cold,relax,mountains|Ice cold.|Sighing incredibly loudly in the same room|party,beach,hot|The drama is unmatched.|Baking a cake for everyone except them|foodie,romance,mild|Deliciously evil.|Slowly moving their belongings slightly to the left|adventure,nature,budget|Psychological warfare.",
    "How do you treat your houseplants?|I have a spreadsheet for their watering schedules|city,culture,luxury|Botanical CEO.|I talk to them like they are my children|romance,relax,mild|Wholesome and slightly crazy.|They are all dead. I am a murderer.|party,hot,adventure|RIP to the ferns.|I buy fake ones so I don't feel guilty|beach,cold,budget|Work smarter, not harder.|I forage in the woods instead|nature,mountains,foodie|Going straight to the source.",
    "You’re stranded on a desert island, what’s your priority?|Finding a coconut to make a cocktail|party,beach,hot|Priorities are strictly vibes.|Building a 5-story treehouse from bamboo|city,luxury,culture|An architectural marvel.|Befriending a volleyball|relax,mild,romance|Wilson!|Hunting something with a pointy stick|adventure,nature,mountains|Primal instincts activated.|Finding out what the local bugs taste like|foodie,budget,cold|A true culinary explorer.",
    "Which reality TV show would you absolutely crush?|Survivor. I am ruthless.|adventure,nature,mountains|Outwit, outplay, outlast.|Love Island. I'm here to cause drama.|party,beach,hot|I've got a text!|MasterChef. Gordon Ramsay would fear me.|foodie,culture,mild|Yes, chef!|Real Housewives. I have the wardrobe for it.|luxury,city,romance|Table flipping imminent.|Alone. Just leave me in the woods.|cold,budget,relax|A true hermit.",
    "What’s your ideal way to waste a Saturday?|Binge-watching 14 hours of true crime|city,cold,culture|Ah, learning how to get away with it.|Day drinking on a patio until sunset|party,hot,beach|Hydration is important.|Getting lost in a massive forest|nature,mountains,adventure|Watch out for bears.|Cooking a meal that takes 9 hours|foodie,romance,mild|Low and slow, baby.|Online shopping for things I will never buy|luxury,relax,budget|Adding to cart... and closing tab.",
    "If you were a household appliance, what would you be?|A blender on the highest setting|party,hot,adventure|Pure chaotic energy.|A high-end espresso machine|city,luxury,culture|Expensive, caffeinated, and demanding.|A slow cooker|relax,mild,foodie|Taking it easy. Low and slow.|A reliable space heater|cold,romance,relax|Cozy vibes only.|A rugged outdoor grill|nature,beach,mountains|You belong outside, covered in soot.",
    
    "What is your secret, highly specific superpower?|Knowing exactly when the microwave will hit zero|city,budget,relax|A true master of time.|Never getting mosquito bites|nature,adventure,hot|The jungle welcomes you.|Finding the best late-night pizza within a 5-mile radius|foodie,party,city|A hero the people need.|Looking perfectly windswept, never messy|luxury,romance,beach|Main character energy.|Instantly making any stray animal love me|nature,culture,mild|Snow White, is that you?",
    "How do you handle IKEA furniture?|I pay someone else to do it|luxury,relax,city|Money solves everything.|I don't need instructions, I use raw intuition|adventure,party,budget|Chaos reigns supreme.|I carefully lay out every single screw first|culture,mild,mountains|Meticulous. Serial killer vibes, but I respect it.|I build it, but there are always 'extra' parts left|beach,hot,romance|Close enough. It probably won't collapse.|I construct my own furniture from fallen trees|nature,mountains,cold|Okay, lumberjack. Calm down.",
    "What minor inconvenience completely ruins your day?|Slow walking people on the sidewalk|city,party,hot|Move out of the way!|A bad hair day|luxury,romance,beach|Aesthetic is everything.|Spilling coffee on yourself|mild,culture,relax|Tragic. Absolutely tragic.|Getting your socks wet|cold,nature,mountains|The ultimate betrayal of the elements.|Forgetting your headphones|adventure,foodie,budget|Silence is deafening.",
    "What’s your preferred method of escaping a bad date?|'I need to go to the bathroom' *climbs out window*|adventure,party,nature|The classic Houdini exit.|Faking an emergency phone call|city,mild,culture|Smooth, if a bit cliché.|Just telling them 'No vibes' and leaving|hot,budget,mountains|Brutal honesty. Respect.|Having my butler fake a ransom note|luxury,romance,relax|Expensive, but effective.|I don't escape, I just make it worse on purpose|foodie,beach,cold|You woke up and chose violence.",
    "You find a time machine. First stop?|Dinosaurs. I want to ride a T-Rex.|nature,adventure,hot|You will absolutely be eaten.|The roaring 1920s for a wild party|party,city,luxury|Gatsby vibes. Don't drink the bathtub gin.|To last Tuesday so I can eat that one pizza again|foodie,relax,budget|Priorities. I respect it.|Ancient Rome to watch the gladiators|culture,mild,mountains|Blood, sand, and sandals.|The future, to see what robots look like|cold,beach,romance|Shiny and chrome.",
    "Your aesthetic as a teenager?|Too much eyeliner and emotional rock music|city,party,cold|It wasn't a phase, mom!|Neon everything. I glowed in the dark.|hot,beach,adventure|A walking highlighter.|Preppy, clean, and terrifyingly organized|luxury,mild,culture|Future CEO energy.|I just wore whatever was on the floor|budget,nature,relax|Resourceful and lazy.|Camo print. I was preparing for war.|mountains,nature,foodie|Ready for the apocalypse.",
    "What is your signature cocktail ingredient?|Something that's currently on fire|party,adventure,hot|Eyebrows are overrated anyway.|Gold leaf flakes|luxury,city,romance|Tastes like nothing, costs $50.|Just give me a beer in a can|budget,beach,nature|Keep it simple, keep it cheap.|Whatever the bartender is experimenting with|culture,foodie,mild|A true connoisseur of chaos.|Ice. Lots of ice.|cold,mountains,relax|Brain freeze incoming.",
    "What do you do when the WiFi goes down?|Panic. Cry. Refresh. Repeat.|city,luxury,party|The withdrawal symptoms are kicking in.|Read a physical book like a 19th-century peasant|culture,mild,romance|Ah, the smell of old paper.|Go outside and touch grass|nature,mountains,adventure|Nature? What are the graphics like?|Take a very long nap|relax,beach,cold|Rebooting your own system.|Cook an elaborate 5-course meal|foodie,hot,budget|Chopping onions to hide the tears.",
    "What is your role in a heist movie?|The mastermind in the tailored suit|luxury,city,culture|Looking sharp while stealing art.|The chaotic explosives expert|adventure,party,hot|Boom goes the dynamite!|The getaway driver eating a sandwich|foodie,budget,beach|Snacks are essential for crime.|The acrobat dodging lasers|mountains,nature,mild|Flexible and stressed.|The decoy who just causes a massive distraction|romance,relax,cold|A drama queen, but useful.",
    "Ideal sandwich architecture?|Meat, cheese, bread. No nonsense.|mountains,budget,cold|A structural purist.|14 different ingredients that require a jaw dislocation|foodie,adventure,party|A delicious mess.|Avocado, sprouts, and artisanal sourdough|culture,mild,city|Very trendy. Very expensive.|Just a hot dog. (Yes, it's a sandwich)|beach,hot,nature|Controversial, but I'll allow it.|Truffle mayo and gold leaf on brioche|luxury,romance,relax|Bougie bread.",
    
    "How do you pack a suitcase?|Throw everything in 10 minutes before the flight|adventure,party,hot|Living on the absolute edge.|Vacuum-sealed, color-coordinated bags|city,culture,luxury|You scare me, but I'm impressed.|I only bring a toothbrush and buy clothes there|budget,beach,nature|Minimalist nomad.|I pack 14 outfits for a 3-day trip|romance,relax,mild|You never know if there will be a gala!|I force someone else to pack it for me|cold,mountains,foodie|Delegation is a skill.",
    "Reaction to finding $100 on the ground?|Buy a round of shots for strangers|party,city,hot|The life of the party!|Invest it immediately|culture,mild,luxury|Boring, but financially responsible.|Eat the most expensive steak in town|foodie,romance,relax|Treat yo' self!|Stash it in my mattress|budget,mountains,cold|Paranoia pays off.|Buy a weird sword online|adventure,nature,beach|Because why not?",
    "If you were a ghost, how would you haunt people?|Slightly moving their keys so they think they're crazy|city,culture,budget|Psychological warfare. Brilliant.|Slamming doors and screaming|party,hot,adventure|The classic poltergeist approach.|Leaving romantic poems on the mirror in steam|romance,relax,mild|A very affectionate ghost.|Turning up the thermostat to ruin their electric bill|cold,nature,mountains|Financial ruin from beyond the grave.|Eating all the good snacks in the fridge|foodie,beach,luxury|A hungry spirit.",
    "What is your spirit emoji?|The upside-down smiling face|city,party,hot|Smiling through the pain.|The sparkle emoji|luxury,romance,mild|Shiny and flawless.|The absolute sobbing crying face|culture,relax,cold|So much emotion.|The monkey covering its eyes|beach,nature,budget|I pretend I do not see it.|The fire emoji|adventure,mountains,foodie|Hype beast.",
    "What is your strategy for surviving a zombie apocalypse?|Bunker down with a lifetime supply of canned beans|budget,relax,cold|Safe, bored, and gassy.|Grab a katana and go down swinging|adventure,hot,mountains|Main character syndrome.|Pretend to be a zombie. Blend in.|culture,city,mild|Modern problems require modern solutions.|Flee to a deserted island|beach,nature,romance|Zombies can't swim... right?|Offer the zombies a gourmet meal instead|foodie,luxury,party|Negotiation via snacks.",
    "If you could instantly master one useless skill?|Juggling chainsaws|adventure,party,hot|Dangerous and completely unnecessary.|Knowing exactly what a dog is thinking|nature,culture,relax|'He wants a sausage.'|Always plugging in the USB correctly on the first try|city,mild,luxury|A literal god among men.|Being able to perfectly replicate any bird call|mountains,budget,cold|Very annoying, very impressive.|Guessing the exact ingredients in any meal|foodie,romance,beach|A human ratatouille.",
    "How do you react to a surprise party for you?|Love it! I am the center of the universe!|party,luxury,city|Attention seeker!|Immediate panic and a strong desire to flee|mountains,nature,cold|Too many people. Abort.|I act surprised even though I figured it out weeks ago|culture,mild,relax|Polite, but calculating.|I immediately start eating the cake|foodie,budget,hot|Cake first, friends later.|I cry|romance,beach,adventure|Tears of joy... hopefully.",
    "What is your ideal retirement plan?|Living in a remote cabin with 12 dogs|nature,mountains,cold|Hermit mode activated.|Sipping martinis on a yacht|luxury,beach,hot|Living the high life.|Opening a tiny bakery in a village|foodie,romance,mild|Carb-loading your golden years.|Continuing to argue with people on the internet|city,culture,budget|A keyboard warrior never rests.|Becoming a wildly eccentric art collector|party,adventure,relax|Very avant-garde.",
    "Choose a method of defeating a dragon.|Challenge it to a dance battle|party,hot,city|Serve the dragon!|Feed it a really spicy taco|foodie,adventure,culture|Heartburn wins the day.|Seduce the dragon|romance,luxury,beach|Ah, the 'Bard' approach.|Poke it with a really long stick|budget,mountains,nature|Safety first.|Politely ask it to leave|mild,relax,cold|Manners cost nothing.",
    "What is in your pockets right now?|Lint and a mystery receipt|budget,nature,relax|Ah, the broke traveler.|A fancy metal credit card|luxury,city,romance|Heavy pockets, heavy wallet.|Four different lip balms|mild,cold,beach|Hydration is key.|A pocket knife and some string|adventure,mountains,hot|Ready to survive the wild.|Snacks. Always snacks.|foodie,party,culture|Prepared for the hunger crash.",
    
    "Preferred weather for a lazy Sunday?|Thunder, lightning, absolute chaos outside|cold,mountains,adventure|Cozy on the inside, apocalyptic on the outside.|Blistering sunshine melting the pavement|hot,beach,party|Lizard mode.|A soft, misty, romantic drizzle|romance,culture,mild|Very cinematic.|A completely blank, gray, overcast sky|city,relax,budget|The color of apathy.|A perfectly crisp, cool autumn breeze|nature,foodie,luxury|Sweater weather!",
    "What do you do in a traffic jam?|Blast music and put on a concert for the car next to me|party,hot,city|You are the entertainment.|Scream into the void|adventure,mountains,budget|Let it out.|Listen to a 4-hour podcast about ancient Rome|culture,mild,relax|Learning while waiting.|Eat the emergency car snacks|foodie,nature,beach|Desperate times call for desperate measures.|Have my driver handle it while I sleep in the back|luxury,romance,cold|Must be nice.",
    "Go-to pizza topping?|Truffle oil and wild mushrooms|luxury,culture,city|Fancy fungus.|Just a shameful amount of pepperoni|party,hot,foodie|A greasy classic.|Pineapple. I stand by it.|adventure,beach,mild|Controversial. I like it.|Whatever vegetables I can find|nature,relax,mountains|Healthy? On a pizza?|Nothing. Just plain cheese like a 5-year-old|budget,cold,romance|A purist.",
    "Choice of a magical wardrobe?|It always has the perfect tailored suit|luxury,city,romance|Looking sharp 24/7.|It dispenses endless clean sweatpants|relax,budget,mild|Comfort over everything.|It gives me impenetrable armor|adventure,mountains,cold|Ready for battle.|It shoots out glowing party outfits|party,hot,beach|Rave ready.|It smells like freshly baked bread|foodie,nature,culture|A wardrobe you can eat.",
    "Texting style?|ONE MASSIVE PARAGRAPH|culture,mild,mountains|I ain't reading all that.|15 separate messages in a row|party,hot,city|Ding. Ding. Ding. Ding.|Just 'K.'|cold,budget,relax|Brutal. Ice cold.|Exclusively using weird emojis and GIFs|adventure,beach,nature|Hieroglyphics for the modern age.|I don't text. I call.|luxury,romance,foodie|Old school and terrifying.",
    "Reaction to a haunted house?|Punch the first ghost I see|adventure,hot,party|Fight or flight? FIGHT.|Hide behind my friends and cry|relax,romance,beach|A human shield is a good shield.|Critique the special effects|culture,city,mild|'That blood looks like ketchup.'|Try to befriend the demons|nature,mountains,cold|They just need a hug.|Eat the props|foodie,budget,luxury|Don't eat the fake eyeballs.",
    "Choice of alien abduction response?|Take me with you! Earth is ghetto!|adventure,party,nature|Beam me up!|Try to sell them a timeshare|city,luxury,budget|The ultimate hustler.|Ask for their space-recipes|foodie,culture,mild|Galactic Gordon Ramsay.|Tell them I have a boyfriend|romance,relax,beach|Polite rejection.|Scream and throw rocks at the saucer|hot,mountains,cold|Primal defense.",
    "Best way to spend a lottery win?|Buy a private island and ban everyone|nature,beach,relax|Ultimate peace and quiet.|Throw a massive, week-long festival|party,hot,city|The hangover will be legendary.|Buy a solid gold toilet|luxury,romance,culture|Because why not?|Invest in a massive cheese vault|foodie,mountains,mild|A gouda investment.|Lose it all immediately in Vegas|adventure,budget,cold|Easy come, easy go.",
    "Preferred scent of a candle?|Sandalwood and expensive leather|luxury,romance,city|Smells like a rich person's library.|Freshly baked cookies|foodie,mild,relax|Now I'm just hungry.|Pine needles and dirt|nature,mountains,cold|Smells like the outside, but inside.|Coconut and sunscreen|beach,hot,party|Smells like bad decisions in Cabo.|Unscented. I hate joy.|budget,culture,adventure|Boring, but practical.",
    "Choice of a sidekick?|A sarcastic talking cat|culture,relax,city|Judgmental and fluffy.|A massive, terrifying wolf|mountains,nature,cold|Good boy, deadly boy.|A tiny robot that makes coffee|luxury,foodie,mild|The most useful sidekick.|A chaotic goblin that steals things|adventure,budget,party|Free stuff!|A beautiful, useless prince/princess|romance,beach,hot|Eye candy.",
    
    "Favorite kind of potato?|Mashed with an obscene amount of butter|foodie,relax,romance|Comfort in a bowl.|Tater tots smothered in cheese|party,hot,budget|Drunk food perfection.|A perfectly roasted, crispy herb potato|culture,mild,luxury|Elegant and refined.|Just a raw potato. I am feral.|adventure,nature,mountains|Please cook it first.|French fries eaten on the beach|beach,city,cold|Seagulls will steal them.",
    "Unpopular opinion?|Water is not wet|culture,city,mild|Here we go with the philosophy.|Pizza is better cold|foodie,budget,relax|Leftover king.|Sleep is a waste of time|party,hot,adventure|You will crash eventually.|The outdoors is overrated|luxury,romance,cold|Give me AC or give me death.|Sand is the worst thing on earth|mountains,nature,beach|Anakin Skywalker agrees.",
    "Default dance move?|The awkward two-step|mild,relax,budget|Safe and unassuming.|Dropping it completely to the floor|party,hot,beach|Knees of steel!|The classic dad-shuffle|culture,nature,mountains|Respect the classics.|I don't dance, I just hold a drink and nod|city,luxury,cold|Too cool for school.|Interpretive flailing|adventure,foodie,romance|A danger to everyone around you.",
    "Karaoke song choice?|Tequila. (I just say 'Tequila' once)|budget,relax,party|Maximum impact, minimum effort.|A screaming 2000s emo anthem|hot,city,adventure|My Chemical Romance forever.|A Whitney Houston ballad I cannot hit the notes for|romance,luxury,beach|Confidence is key!|I refuse to sing, I only rap|culture,mild,nature|Eminem is shaking.|A duet where I sing both parts|foodie,mountains,cold|Main character energy.",
    "Ideal fictional universe to live in?|A magical wizard school|culture,mild,relax|Watch out for the dark arts.|A gritty cyberpunk dystopia|city,hot,party|Neon lights and bad air quality.|A cozy hobbit village|foodie,nature,mountains|Second breakfast!|A spaceship exploring the galaxy|adventure,cold,budget|To infinity and beyond.|A wealthy historical drama where everyone gossips|luxury,romance,beach|Tea and scandal.",
    "How you handle a minor inconvenience?|Deep breathing and meditation|relax,mild,nature|Inner peace.|Immediate vocal complaining|city,hot,culture|Let the world know your pain.|I bottle it up until I explode 3 years later|cold,mountains,budget|Healthy.|I throw money at the problem|luxury,romance,party|Must be nice.|I eat my feelings|foodie,beach,adventure|Ice cream fixes everything.",
    "Alter ego profession?|An international jewel thief|luxury,city,adventure|Slick and dangerous.|A swamp witch brewing potions|nature,hot,budget|Frog legs and curses.|A grumpy lighthouse keeper|cold,mountains,relax|Leave me alone, I have a big lamp.|A famous, eccentric food critic|foodie,culture,mild|'This soup lacks passion.'|A backup dancer for Beyoncé|party,beach,romance|Fierce.",
    "Best way to wake up?|To the smell of bacon|foodie,relax,hot|The ultimate alarm clock.|By a gentle kiss on the forehead|romance,mild,luxury|A cinematic awakening.|By falling out of bed|adventure,budget,party|A rough start.|To absolute, dead silence|cold,mountains,nature|Peace at last.|By my own screaming panic that I'm late|city,culture,beach|The adrenaline wakes you up.",
    "Choice of a useless superpower?|Can turn invisible, but only when no one is looking|budget,relax,culture|Basically just hiding.|Can summon a single grape once a day|foodie,nature,mild|Nutritious.|Can make anyone aggressively sneeze|party,hot,adventure|The ultimate disruption.|Can instantly dry wet socks|cold,mountains,beach|Actually, that's top tier.|Can make things slightly more expensive|luxury,city,romance|A terrible, evil power.",
    "Signature karaoke move?|The dramatic mic drop|party,hot,adventure|Assert dominance.|Closing my eyes and clutching the mic stand|romance,relax,mild|Feeling the emotion.|Staring uncomfortably at one person the whole time|culture,budget,cold|Intimidating.|Jumping off the stage|city,beach,mountains|Rockstar vibes.|Eating a snack during the instrumental break|foodie,luxury,nature|Efficient."
]

parsed_qs = []
for q_str in raw_qs:
    parts = q_str.split("|")
    q_dict = {"q": parts[0], "opts": {}}
    for i in range(1, 16, 3):
        if i+2 < len(parts):
            q_dict["opts"][parts[i]] = {"tags": parts[i+1].split(","), "cheeky": parts[i+2]}
    parsed_qs.append(q_dict)

# ---------------------------------------------------------
# 4. ENGINE LOGIC & STATE MANAGEMENT (EQUAL CHANCE NORMALIZATION)
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
    # We will pick exactly 20 questions randomly from the 50 pool
    st.session_state.unused_qs = random.sample(parsed_qs, 20)
    st.session_state.current_q = None

def set_stage(new_stage):
    st.session_state.stage = new_stage

def get_next_question():
    if not st.session_state.unused_qs:
        return None
    return st.session_state.unused_qs.pop(0)

def handle_answer(selected_option):
    # Apply tags
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
    """Calculates the best match using Normalized Jaccard-like Scoring to ensure 100% equal chances!"""
    best_score = -9999
    best_dest = None
    
    random.shuffle(st.session_state.available_dests)
    
    for dest in st.session_state.available_dests:
        dest_tags = dests[dest]["t"]
        
        # Count matched points
        matched_points = sum([st.session_state.user_tags[t] for t in dest_tags if t in st.session_state.user_tags])
        
        # NORMALIZE by the number of tags the destination has. 
        # Add a tiny random float to randomly break ties giving every place an equal chance.
        normalized_score = (matched_points / len(dest_tags)) + random.uniform(0, 0.05)
        
        if normalized_score > best_score:
            best_score = normalized_score
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
    st.markdown("<h1 style='text-align: center; font-size: 65px; font-weight: 900;'>The Perfect Holiday Finder</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; text-align: center; margin: 20px auto; max-width: 800px;'>
    <h3 style='margin-bottom: 20px;'>Here is how it works:</h3>
    <p style='font-size: 22px;'>1. Our engine holds exactly <b>100 unique global holidays</b> (including viral TikTok gems).</p>
    <p style='font-size: 22px;'>2. It will ask you <b>20 totally random, silly personality questions</b>.</p>
    <p style='font-size: 22px;'>3. Halfway through, you get a <b>Stick or Risk</b> offer.</p>
    <p style='font-size: 22px;'>4. Finally, you will pick your ultimate 6-part atmospheric itinerary!</p>
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
    
    st.markdown(f"<h1 style='font-size: 40px; text-align: center;'>Question {st.session_state.q_index + 1}: {q_data['q']}</h1><br>", unsafe_allow_html=True)
    
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
        st.markdown(f"<p style='font-size: 25px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px;'>Imagine: {random.choice(dest_data['e'])}</p>", unsafe_allow_html=True)
        
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
        title = "🔥 Epic Holiday Changing Activity 1"
        act1, act2 = dest_data["e"][0], dest_data["e"][1]
    elif rnd == 4:
        title = "🔥 Epic Holiday Changing Activity 2"
        act1, act2 = dest_data["e"][2], dest_data["e"][3]
    elif rnd == 5:
        title = "🔥 Epic Holiday Changing Activity 3"
        act1, act2 = dest_data["e"][4], dest_data["e"][5]
    
    st.markdown(f"<h1 style='text-align: center; font-size: 45px;'>Ultimate Choice: {best_dest}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{title} (Round {rnd + 1} of 6)</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>You can only KEEP ONE. The other is gone forever.</h4><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.5); padding: 40px; border-radius: 20px; height: 220px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act1}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ KEEP THIS ONE", key=f"btn1_{rnd}", on_click=pick_activity, args=(act1,))
        
    with col2:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.5); padding: 40px; border-radius: 20px; height: 220px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act2}</h2></div><br>", unsafe_allow_html=True)
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
        st.markdown(f"<h2 style='font-size: 50px; text-decoration: underline;'>📍 {best_dest}</h2>", unsafe_allow_html=True)
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
