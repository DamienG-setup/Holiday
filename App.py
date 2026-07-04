import streamlit as st
import random
import urllib.parse
from collections import Counter

# ---------------------------------------------------------
# 1. PAGE CONFIGURATION & INSANE CSS
# ---------------------------------------------------------
st.set_page_config(page_title="Our Next Escape ✈️", page_icon="🌍", layout="wide")

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
# 2. EXCLUSIVE DESTINATIONS (100 Globally Balanced)
# ---------------------------------------------------------
raw_dests = [
    # ASIA (25)
    "Beijing (China)|hot,city,culture,foodie|#B22222|beijing china great wall red lanterns|Eat world-famous Tanghulu candied fruit|Eat authentic Peking Duck carved tableside|Drink pearl milk tea in a traditional Hutong|Cocktails at a secret bar hidden behind a bookshelf|Rent traditional Hanfu clothes for a photoshoot|Feed adorable pandas at the Beijing Zoo|Ride the legendary toboggan slide down the Great Wall|Walk the terrifying glass-bottom cliff bridge in Jingdong|Take the 300mph high-speed bullet train|Night tour of the glowing Bird's Nest stadium|Cable car up the jagged Mutianyu mountains|Explore the massive Summer Palace by wooden boat",
    "Shanghai (China)|mild,city,party,luxury|#8B0000|shanghai skyline bund neon lights|Eat legendary soup dumplings at Jia Jia Tang Bao|Fine dining inside the futuristic Pearl Tower|Cocktails at a rooftop bar overlooking the glowing Bund|Sip matcha in the ancient Yu Garden|Visit the massive Shanghai Disneyland|Take a neon-lit river cruise down the Huangpu|Walk the glass floor 100 stories up in the World Financial Center|Explore the cyberpunk Nanjing Road|Ride the Maglev fastest commercial train|Attend a massive underground techno party|Take a day trip to a historic water town|Shop for knock-off luxury goods in underground markets",
    "Zhangjiajie (China)|cold,mountains,nature,adventure|#2F4F4F|zhangjiajie avatar mountains mist|Eat spicy Hunan street noodles|Gourmet banquet in a mountain lodge|Drink hot green tea in the freezing mist|Local rice wine tasting|Watch the wild macaques steal snacks|Walk through the Tianmen mountain Heaven's Gate|Take the terrifying Bailong Elevator up the cliff face|Walk across the world's longest glass-bottom bridge|Hike through the floating Hallelujah Mountains|Ride the world's longest cable car over the jungle|Bungee jump off the glass bridge|Take a helicopter tour of the limestone pillars",
    "Chengdu (China)|mild,city,foodie,culture|#DC143C|chengdu china pandas bamboo spicy|Eat insanely spicy Sichuan Hot Pot|Eat Dan Dan noodles from a street cart|Drink bamboo tea in a historic teahouse|Taste fiery Baijiu liquor|Cuddle baby pandas at the research base|Watch the magical Bian Lian face-changing opera|Explore the ancient Jinli walking street|Hike the misty Mount Emei|See the massive Leshan Giant Buddha carved into a cliff|Experience a brutal traditional ear-cleaning|Party in the Lan Kwai Fong district|Take a cooking class with a Sichuan master",
    "Tokyo (Japan)|mild,city,foodie,culture,party|#FF003F|tokyo neon night city shibuya|Eat at the exclusive 2D black-and-white cafe|Slurp Tonkotsu ramen in an isolated Ichiran booth|Drink cute lattes at the Pokémon Cafe|High-end whiskey in a slick sky-bar|Play UFO claw machines in Akihabara|Buy weird things from 100 different vending machines|Drive real Mario Karts through the Shibuya Crossing|Walk barefoot through water at the breathtaking teamLab Planets|Watch a brutal heavyweight sumo wrestling tournament|Sing Karaoke in a private room with endless drinks|Take a helicopter tour over the Tokyo neon skyline|Eat insanely fluffy pancakes in Harajuku",
    "Kyoto (Japan)|mild,city,culture,relax|#8B0000|kyoto japan bamboo forest temple|Multi-course exquisite Kaiseki dinner|Eat matcha soft serve while walking the streets|Experience a secret Geisha tea ceremony|Tasting 20 different types of Matcha|Walk the magical Arashiyama Bamboo Forest|Feed the bowing deer in nearby Nara|Sleep in a traditional Ryokan on tatami mats|Bathe naked in a natural outdoor Onsen|Rent kimonos and walk the red Torii gates of Fushimi Inari|Learn to swing a katana with a Samurai master|Meditate with Zen monks at dawn|Attend a vibrant traditional matsuri festival",
    "Osaka (Japan)|mild,city,foodie,party|#FF4500|osaka japan neon dotonbori food|Eat premium Kobe beef cooked in front of you|Eat endless Takoyaki octopus balls on the street|Craft Japanese gin tasting|Drink Sake until dawn in a tiny Izakaya|Take photos with the giant Glico running man sign|Explore the massive Kuromon fish market|Eat literally everything in the Dotonbori food district|Ride the rollercoasters at Universal Studios Japan|Explore the massive imposing Osaka Castle|Party in the vibrant Amerikamura district|Attend a frantic loud baseball game|Take a day trip to explore Kyoto",
    "Hokkaido (Japan)|cold,mountains,nature,adventure|#E0FFFF|hokkaido japan snow skiing crab|Eat massive expensive King Crab legs|Slurp hot Miso Ramen with a slab of butter|Taste Sapporo beer at the original brewery|Drink hot sake in an outdoor snow bath|Watch the adorable snow monkeys bathe|See the massive ice sculptures at the Snow Festival|Ski waist-deep world-class powder snow in Niseko|Bathe in a natural hot spring Onsen while it snows|Snowmobile across vast frozen plains|Icebreaker cruising on the Sea of Okhotsk|Hike a smoking active volcano|Eat incredible fresh sea urchin at the morning market",
    "Seoul (South Korea)|mild,city,foodie,culture,party|#4B0082|seoul south korea neon palace night|Make custom ramen at a Han River convenience store|Eat the famous stretchy 10 Won Coin Bread|Get an exclusive Personal Color Analysis session|Drink Soju in a street tent|Rent a traditional Hanbok to get into palaces|Try a 10-step Korean skincare routine|Get scrubbed raw at a traditional bathhouse|Sing K-Pop Karaoke in a private Noraebang|Visit the heavily armed DMZ border with North Korea|Club until 7 AM in Gangnam|Hike Bukhansan Mountain right outside the city|Eat live wriggling octopus at Noryangjin Fish Market",
    "Jeju Island (South Korea)|mild,beach,nature,relax|#32CD32|jeju island south korea beach volcano|Eat famous Jeju Black Pork BBQ|Eat fresh abalone caught by Haenyeo free-divers|Drink Hallabong tangerine juice|Drink craft beer on the beach|Walk through glowing digital art at Arte Museum|Explore the massive Manjanggul lava tube|Hike to the crater of Hallasan volcano|Scuba dive in crystal clear volcanic waters|Explore the quirky Loveland theme park|Watch the sunrise from Seongsan Ilchulbong|Surf the waves at Jungmun Beach|Take a submarine tour",
    "Bangkok (Thailand)|hot,city,party,foodie,culture|#B22222|bangkok thailand neon temples|Eat legendary Volcano Ribs at Jodd Fairs night market|Eat Michelin-star crab omelet from a street vendor|Drink at the famous Tichuca jellyfish rooftop bar|Drink cheap buckets of liquor on Khao San Road|Take a chaotic Tuk-Tuk ride|Shop from a tiny boat at the Floating Market|Explore the stunning solid gold Grand Palace|Party with backpackers on Khao San Road|Cruise the Chao Phraya River on a luxury dinner ship|Attend the magical Yi Peng lantern festival|Get a traditional Sak Yant bamboo tattoo|Watch a brutal live Muay Thai boxing match",
    "Chiang Mai (Thailand)|hot,mountains,culture,foodie,relax|#2E8B57|chiang mai thailand temples lanterns|Luxury Khao Soi curry noodle soup tasting|Eat insanely spicy papaya salad at the night bazaar|Artisanal coffee grown in the local mountains|Drink Thai Iced Tea out of a plastic bag|Get a blessed string tied by a monk|Release a glowing paper lantern into the night sky|Bathe and feed elephants at an ethical sanctuary|Take an aggressive 5-day jungle survival trek|Attend an authentic Thai cooking masterclass|Get a brutal traditional Thai massage|Zipline through the jungle with Flight of the Gibbon|Rent a scooter to drive the massive Mae Hong Son loop",
    "Phuket (Thailand)|hot,beach,party,budget,adventure|#FF8C00|phuket thailand longtail boat limestone|Gourmet Thai fusion on a cliff edge|Eat insanely spicy Pad Thai from a street cart|VIP table at an insane beach club|Drink cheap buckets of liquor on Bangla Road|Get a cheap aggressive Thai foot massage|Shop at the chaotic weekend night market|Party until dawn at the Full Moon Party|Bathe and feed rescued elephants in a sanctuary|Take a longtail boat to James Bond Island|Scuba dive with massive Whale Sharks|Watch a brutal live Muay Thai boxing match|Zipline through the dense tropical jungle",
    "Bali (Indonesia)|hot,beach,nature,relax,budget|#228B22|bali indonesia rice terraces jungle sunset|Eat a floating breakfast in a jungle infinity pool|Eat spicy Nasi Goreng at a cheap local warung|Cocktails at the massive luxurious Finns Beach Club|Drink a Bintang beer sitting on a beanbag|Swing over the rice terraces on the famous Bali Swing|Get blessed by a monk in a holy water temple|Hike Mount Batur in the dark to watch the sunrise|Surf the world-class waves of Uluwatu|Scuba dive a WWII shipwreck in Tulamben|Get a brutal but amazing 2-hour Balinese massage|White water raft down the Ayung River|Take a fast boat to stunning Nusa Penida",
    "Komodo Island (Indonesia)|hot,nature,adventure,beach|#2F4F4F|komodo island dragons pink beach jungle|Gourmet seafood on a luxury liveaboard boat|Eat grilled fish on a stick on the beach|Cold Bintang beer after a long hike|Drink fresh coconut water straight from the tree|Relax on a rare beautiful Pink Sand Beach|Watch thousands of flying foxes erupt at sunset|Trek through the brush to find deadly Komodo Dragons|Scuba dive with Manta Rays in strong currents|Sail the Indonesian archipelago on a Phinisi boat|Hike to the stunning viewpoint on Padar Island|Swim in crystal clear turquoise bays|Spearfish your own dinner",
    "Raja Ampat (Indonesia)|hot,beach,nature,adventure|#00CED1|raja ampat coral islands pristine|Luxury seafood on a remote eco-resort|Eat traditional Papuan Sago|Drink coconut cocktails|Drink cold Bintang|Take photos at the iconic Piaynemo viewpoint|Swim with thousands of stingless jellyfish|Scuba dive the most biodiverse coral reefs on Earth|Kayak through towering limestone karst islands|Explore hidden glowing sea caves|Stay in an overwater bungalow with no WiFi|Hike into the jungle to spot Birds of Paradise|Take a liveaboard diving safari",
    "Singapore|hot,city,luxury,foodie|#8B008B|singapore marina bay sands supertrees|Eat $300 Chili Crab at a luxury seafood house|Eat $3 Michelin-star Chicken Rice at a hawker centre|Drink the original Singapore Sling at the Raffles Hotel|Craft cocktails in a hidden speakeasy|Walk through the glowing Supertree Grove|Explore the indoor waterfall at the Jewel airport|Swim in the Marina Bay Sands infinity pool 57th floor|Take a night safari to see nocturnal predators|Shop in insanely massive luxury mega-malls|Ride the Singapore Flyer observation wheel|Bungee jump on Sentosa Island|Watch the Formula 1 Night Race",
    "Hanoi (Vietnam)|hot,city,culture,foodie,budget|#556B2F|hanoi vietnam busy streets motorbikes|Gourmet French-Vietnamese fusion|Eat $1 Pho sitting on a tiny plastic stool|Drink incredible Egg coffee in a hidden narrow cafe|Drink Bia Hoi fresh beer for 20 cents|Dodge thousands of motorbikes to cross the street|Watch a traditional Water Puppet show|Take a luxury overnight junk boat cruise in Ha Long Bay|Trek the terraced rice fields of Sapa|Crawling through the Cu Chi tunnels|Take a sleeper train down the coast|Eat Banh Mi from a street cart|Explore the massive ancient cave of Son Doong",
    "Ha Long Bay (Vietnam)|hot,nature,relax,romance|#20B2AA|ha long bay vietnam limestone boats|Gourmet seafood on a luxury wooden junk boat|Eat fresh spring rolls|Drink cocktails on the top deck at sunset|Drink strong Vietnamese drip coffee|Take a bamboo rowboat through floating fishing villages|Explore the massive Sung Sot cave|Kayak silently through the towering limestone karsts|Take a seaplane flight over the emerald waters|Swim in isolated hidden coves|Take a Tai Chi class on the deck at dawn|Squid fishing at midnight|Hike to the top of Titop Island for a panoramic view",
    "Palawan (Philippines)|hot,beach,nature,adventure,budget|#00CED1|palawan philippines limestone lagoons|Fresh lobster cooked on a remote island|Eat Adobo and Lechon roast pig|Rum cocktails out of a pineapple|Drink Red Horse beer by a beach bonfire|Take a tiny outrigger boat to a hidden lagoon|Find a totally deserted white sand beach|Paddle deep into the massive Underground River cave|Island hop through the breathtaking Bacuit Archipelago|Scuba dive WWII Japanese shipwrecks in Coron|Zipline between two islands over the ocean|Kayak through secret emerald lagoons|Camp on a deserted island like Survivor",
    "Siargao (Philippines)|hot,beach,adventure,party|#3CB371|siargao philippines surfing palm trees|Gourmet smoothie bowls at a trendy cafe|Eat fresh Kinilaw (Filipino ceviche)|Drink cheap rum at a massive jungle party|Drink fresh coconut water|Swing from a rope into the Maasin River|Drive a scooter through thousands of palm trees|Surf the legendary Cloud 9 barrel waves|Island hop to Naked Island (just a sandbar)|Explore the glowing Sugba Lagoon|Party all night at the infamous General Luna clubs|Wakeboard across the pristine ocean|Cliff jump into the Magpupungko rock pools",
    "Taipei (Taiwan)|mild,city,foodie,culture|#D2691E|taipei taiwan night market 101 tower|Soup dumplings at the original Din Tai Fung|Eat Stinky Tofu at a chaotic night market|High mountain Oolong tea ceremony|Drink absurdly sugary Boba Bubble Tea|Release a glowing paper lantern in Shifen|Ride the Maokong glass-bottom gondola|Take the ultra-fast elevator up Taipei 101|Soak in the Beitou thermal hot springs|Hike Elephant Mountain for the perfect city view|Explore the stunning Taroko Gorge marble canyons|Eat literally everything at Shilin Night Market|Scooter road trip along the dramatic east coast",
    "Luang Prabang (Laos)|hot,culture,nature,relax|#8B4513|luang prabang laos monks temples waterfalls|Luxury French-Lao fusion dining|Eat spicy Laap and sticky rice|Drink Beerlao by the Mekong river|Drink fresh sugar cane juice|Give alms to the hundreds of monks at dawn|Shop the vibrant night market|Swim in the spectacular multi-tiered Kuang Si Falls|Take a slow boat down the Mekong River|Explore the Pak Ou caves filled with Buddha statues|Take an organic rice farming masterclass|Bathe elephants in the river|Get a traditional Lao herbal sauna and massage",
    "Jaipur (India)|hot,city,culture,romance|#FF4500|jaipur india pink city palaces desert|Royal Rajasthani Thali in a converted palace|Eat ultra-spicy Laal Maas curry|Cocktails on a palace rooftop|Drink fresh Lassi from a clay pot|Explore the insanely intricate Hawa Mahal Palace of Winds|Get a traditional Henna tattoo|Take a hot air balloon over the desert forts|Ride a jeep up to the massive Amber Fort|Sleep like royalty in an actual Maharaja's palace|Spot wild Bengal Tigers in Ranthambore on safari|Shop for precious gems and textiles|Watch a snake charmer in the street markets",
    "Maldives|hot,beach,relax,luxury,romance|#00CED1|maldives overwater bungalow crystal ocean|Dine in an all-glass underwater restaurant|Have a private beach BBQ cooked by a personal chef|Champagne delivered to your pool via floating tray|Drink coconut cocktails on a deserted sandbank|Slide directly from your overwater bungalow into the ocean|Night swim with glowing bioluminescent plankton|Take a private seaplane over the gorgeous atolls|Scuba dive with massive gentle Manta Rays|Go deep sea fishing for Yellowfin Tuna|Take a submarine tour of the vibrant coral reefs|Couples spa day on a glass floor over the ocean|Watch an outdoor movie at a jungle cinema",

    # AMERICAS (25)
    "New York City (USA)|mild,cold,city,foodie,luxury,culture|#4682B4|new york city times square skyline|Eat the legendary Suprême croissant at Lafayette|Eat a massive greasy $2 slice of NY pizza|Martinis in a high-end hidden speakeasy|Drink cheap beers at a gritty Brooklyn dive bar|Take mind-bending photos in the SUMMIT One Vanderbilt|Ice skate in Central Park|Take a helicopter doors-off tour over Manhattan|Watch a smash-hit Broadway musical from VIP seats|Attend a crazy underground warehouse party in Brooklyn|Go on a massive shopping spree on 5th Avenue|Eat a massive pastrami sandwich at Katz's Deli|Walk the High Line elevated park at sunset",
    "Los Angeles (USA)|hot,city,beach,party,luxury|#FF1493|los angeles hollywood palm trees sunset|Eat at the exclusive Erewhon bakery|Eat tacos from a street truck at 2 AM|Drink insanely expensive green juice|Drink cocktails on a West Hollywood rooftop|Hike to the Hollywood sign|Rollerblade down Venice Beach|Take a VIP studio backlot tour|Surf the waves in Malibu|Drive a convertible down the Pacific Coast Highway|Party with celebrities in Beverly Hills|Shop on Rodeo Drive|Take a helicopter tour over the mansions",
    "San Francisco (USA)|mild,city,foodie,culture,adventure|#1E90FF|san francisco golden gate bridge cable car|10-course Michelin star tasting menu in Soma|Eat Clam Chowder out of a massive sourdough bowl|Wine tasting trip to Napa Valley via private limo|Drink Irish Coffees at the Buena Vista|Hang off the side of a moving Cable Car|Have a picnic at the Painted Ladies|Take a terrifying midnight Alcatraz ghost tour|Bike across the Golden Gate Bridge|Skydive directly over the Bay|Hike among massive Redwoods in Muir Woods|Eat giant burritos in the Mission District|Sail a catamaran under the Golden Gate Bridge",
    "Miami (USA)|hot,beach,party,luxury|#FF1493|miami south beach neon palm trees|Luxury stone crab dining at Joe's|Eat authentic Cuban sandwiches in Little Havana|Champagne on a mega-yacht|Drink mojitos at a salsa club|Rollerblade down Ocean Drive in neon gear|Look at street art in Wynwood Walls|Party until 6 AM at a massive club like E11EVEN|Ride an airboat through the Everglades looking for alligators|Charter a private yacht to the Bahamas|Drive a neon Lamborghini down South Beach|Deep sea fishing for Marlin|Attend an exclusive Art Basel party",
    "Oahu (Hawaii)|hot,beach,city,adventure|#1E90FF|oahu hawaii waikiki beach surfing|Eat luxury Japanese fusion at Nobu|Eat fresh Poke bowls from a local grocery store|Drink Mai Tais at the Royal Hawaiian|Drink Kona brewing beer on the beach|Visit the historic Pearl Harbor memorial|Eat Dole Whip at the pineapple plantation|Surf massive winter waves on the North Shore|Hike the terrifying Haiku Stairs|Shark cage diving in the open ocean|Helicopter tours over the volcanic craters|Attend a massive traditional Luau fire show|Skydive over the crystal clear ocean",
    "Kauai (Hawaii)|hot,nature,adventure,relax|#006400|kauai hawaii napali coast cliffs|Luxury oceanfront dining|Eat massive colorful Shave Ice|Drink tropical cocktails out of a pineapple|Drink local Hawaiian coffee|Hike the breathtaking Waimea Canyon|Take a doors-off Helicopter over Jurassic Park falls|Sail a catamaran along the dramatic Na Pali coast|Kayak the Wailua River to hidden waterfalls|Zipline over the lush valleys|Surf the warm waves|Scuba dive with sea turtles|Off-roading in a 4x4 through the mud",
    "Yellowstone (USA)|cold,mild,nature,adventure|#A0522D|yellowstone geyser bison nature|Gourmet game meat at a luxury lodge|Eat campfire chili out of a tin can|Craft beer tasting in a cowboy saloon|Drink cowboy coffee boiled over a fire|Watch Old Faithful erupt on schedule|Spot adorable bear cubs through binoculars|Snowmobile through the park in dead of winter|Spot packs of wild wolves in the Lamar Valley|Hike around the neon-colored Grand Prismatic Spring|Camp deep in grizzly bear country|Fly fish in freezing crystal-clear rivers|Whitewater raft down the Snake River",
    "Banff (Canada)|cold,mountains,nature,adventure|#2F4F4F|banff canada lake louise mountains snow|Fine dining at the Fairmont Chateau Lake Louise|Eat massive plates of Canadian Poutine|Drink ice wine from the local vineyards|Sip hot chocolate while ice skating|Rent a clear glass canoe on the turquoise Lake Louise|Soak in the Banff Upper Hot Springs|Take a helicopter tour over the massive Canadian Rockies|Hike to the spectacular Plain of Six Glaciers|Ski world-class powder at Sunshine Village|Ice climb up a frozen waterfall in Johnston Canyon|Spot massive wild Grizzly Bears|Take the steep gondola up Sulphur Mountain",
    "Whistler (Canada)|cold,mountains,adventure,party|#E0FFFF|whistler skiing mountains snow|Gourmet alpine dining|Eat Beavertails pastry|Drink hot toddy|Drink Apres-ski beers in a loud pub|Ride the Peak 2 Peak gondola|Snowshoe through the quiet forests|Ski massive world-class slopes|Heli-skiing on untouched powder peaks|Bungee jumping into a freezing gorge|Ziplining over the pine trees|Mountain biking the extreme downhill trails in summer|Go bear watching in the wild",
    "Mexico City|mild,city,foodie,culture,party|#B22222|mexico city zocalo vibrant culture|Dine at Pujol (top 10 restaurant in the world)|Eat endless $1 Al Pastor street tacos|High-end Mezcal tasting in a slick speakeasy|Drink Micheladas in a loud Cantina|Ride colorful boats in Xochimilco|Browse art in the Frida Kahlo Museum|Climb the massive ancient Pyramids of the Sun and Moon|Watch a wild high-flying Lucha Libre wrestling match|Party until dawn in the trendy Roma Norte district|Take a hot air balloon over the Teotihuacan ruins|Eat exotic insects like chapulines|Explore the massive Chapultepec Castle",
    "Tulum (Mexico)|hot,beach,party,culture,relax|#20B2AA|tulum mexico beach cenote ancient ruins jungle|Eat gourmet Maya-fusion dining in the jungle|Eat fresh fish tacos barefoot on the beach|Drink Matcha lattes at the exclusive Azulik treehouse|Drink Mezcal at a massive jungle techno rave|Float down a crystal clear underground Cenote|Do yoga on the beach at sunrise|Explore the ancient Mayan ruins perched on the cliff edge|Scuba dive in the dark underwater cave systems|Swim with giant sea turtles in Akumal|Kitesurf on the breezy Caribbean ocean|Take a mud bath in a Mayan sweat lodge|Rent a bicycle to ride down the trendy beach road",
    "Oaxaca (Mexico)|hot,city,culture,foodie|#FF4500|oaxaca mexico day of the dead colorful|Eat incredible authentic Mole|Eat Chapulines (toasted grasshoppers)|Take a high-end Mezcal tasting tour|Drink Mexican hot chocolate|Celebrate the spectacular Day of the Dead festival|Wander the insanely colorful streets and markets|Explore the ancient Zapotec ruins of Monte Albán|Swim in the petrified waterfalls of Hierve el Agua|Take a massive traditional cooking masterclass|Shop for Alebrijes brightly painted wooden animals|Visit a traditional Mezcal distillery|Hike the Sierra Norte mountains",
    "Costa Rica|hot,nature,adventure,relax,beach|#006400|costa rica jungle waterfall sloth volcano|Gourmet dining at a luxury eco-resort|Eat hearty Gallo Pinto for breakfast|Drink Imperial beer on a surfboard|Taste fresh Costa Rican coffee right on the plantation|Cuddle rescued sloths at an animal sanctuary|Relax in a hammock listening to howler monkeys|Superman Zipline 1000ft above the jungle canopy|Soak in natural volcanic hot springs near Arenal|Surf world-class waves in Tamarindo|Night hike to spot deadly snakes and glowing frogs|Whitewater raft through Class 4 jungle rapids|Rappel down a massive roaring waterfall",
    "Belize|hot,beach,nature,adventure|#20B2AA|belize blue hole ocean jungle|Luxury lobster dinner|Eat Fry jacks on the beach|Drink Belikin beer|Drink Rum punch|Explore massive ancient Mayan ruins|Go Cave tubing through pitch black rivers|Scuba dive the massive Great Blue Hole|Swim with sharks at Shark Ray Alley|Jungle trekking with a machete|Zipline through the canopy|Sail a catamaran|Go Deep sea fishing",
    "Havana (Cuba)|hot,city,culture,party|#C71585|havana cuba vintage cars colorful streets|Eat lobster at a fancy paladar|Eat Ropa Vieja shredded beef with black beans|Drink Daiquiris at Hemingway's favorite bar|Drink cheap rum out of a coconut|Roll an authentic Cuban Cigar|Walk the Malecon seawall at sunset|Ride in a bright pink 1950s vintage convertible|Dance Salsa in the streets with locals|Explore the crumbling colorful architecture of Old Havana|Attend the extravagant Tropicana Cabaret show|Take a day trip to the stunning Viñales tobacco valley|Scuba dive the untouched coral reefs of the Bay of Pigs",
    "Rio de Janeiro (Brazil)|hot,beach,party,culture,city|#32CD32|rio de janeiro christ the redeemer copacabana|Endless premium meats at a luxury Churrascaria|Eat Pão de Queijo on the street|Drink Caipirinhas on Copacabana beach|Drink cold chopp in a lively boteco|Take the cable car up Sugarloaf Mountain|Buy a tiny bikini/sunga and play footvolley|Take a helicopter around the massive Christ the Redeemer statue|Dance Samba until dawn at the massive Carnival parade|Hang glide off a mountain and land on the beach|Explore the vibrant Favela communities|Hike through the Tijuca urban rainforest|Attend a massive soccer game at Maracanã Stadium",
    "Amazon Rainforest (Brazil)|hot,nature,adventure|#004D00|amazon rainforest river jungle wild green|Gourmet jungle fusion on a luxury riverboat|Eat roasted piranha you caught yourself|Drink Ayahuasca in a terrifying shamanic ceremony|Drink fresh exotic fruit juices|Spot sleepy sloths in the trees|Hold a colourful macaw parrot|Fish for deadly sharp-toothed Piranhas|Take a night canoe trip to spot glowing Caiman eyes|Survive a multi-day deep jungle trek with a machete|Swim with legendary Pink River Dolphins|Visit an isolated indigenous tribe|Sleep in a hammock surrounded by jaguar territory",
    "Patagonia (Argentina)|cold,mountains,nature,adventure|#4682B4|patagonia glaciers mountains rugged ice|Gourmet Patagonian lamb cooked over an open fire|Eat empanadas after a freezing hike|Drink high-end Malbec wine|Drink bitter Mate tea with Gauchos|Spot adorable penguins on the coast|Pet wild guanacos (llamas)|Trek across the massive cracking Perito Moreno Glacier|Hike the brutal base of Mount Fitz Roy|Kayak through incredible glowing marble caves|Spot wild Pumas on a tracking safari|Sail past towering icebergs on an expedition ship|Horseback ride across the endless steppe",
    "Atacama Desert (Chile)|hot,nature,adventure|#D2691E|atacama desert chile dry mars|Luxury desert lodge dining|Eat Llama meat|Drink Pisco Sours|Drink Coca tea to fight altitude|Float effortlessly in a hyper-salty lagoon|Stargaze with powerful telescopes under zero light pollution|Watch the Tatio Geysers erupt at dawn|Sandboard down massive dunes|Explore the Valle de la Luna (Moon Valley)|Hike massive dormant volcanoes|Mountain bike through the red rocks|Take a hot air balloon flight at sunrise",
    "Salar de Uyuni (Bolivia)|cold,nature,adventure|#E0FFFF|salar de uyuni salt flats mirror reflection|Gourmet dinner served on a table made entirely of salt|Eat llama meat cooked over a stove|Drink Singani (Bolivian brandy)|Chew coca leaves to stay awake|Take insane perspective-bending photos on the white salt|Spot bright pink flamingos in a blood-red lake|Drive a 4x4 across the endless mirror-like Salt Flats|Sleep in a hotel made entirely out of salt blocks|Bathe in natural hot springs surrounded by freezing desert|Explore the creepy Train Cemetery|Hike a massive dormant volcano at high altitude|Visit the surreal bubbling mud geysers at dawn",
    "Galapagos Islands (Ecuador)|hot,nature,adventure,beach|#20B2AA|galapagos islands giant tortoise pristine beach|Luxury seafood dinner on a chartered yacht|Eat fresh Ecuadorian Ceviche|Drink cocktails on a cruise deck at sunset|Drink Pilsener beer with the locals|Walk alongside massive ancient Giant Tortoises|Watch Blue-Footed Boobies do their mating dance|Scuba dive with hundreds of Hammerhead Sharks|Snorkel with playful curious Sea Lions|Hike across a barren black lava field|Swim with marine iguanas that look like Godzilla|Take a Zodiac boat to remote untouched islands|Spot the only penguins that live on the equator",
    "Machu Picchu (Peru)|mild,mountains,adventure,culture|#A0522D|machu picchu peru inca ruins mountains|Michelin-star modern Peruvian food in Lima|Eat roasted Guinea Pig (Cuy)|Drink Pisco Sours in a lively Cusco tavern|Drink Coca Tea to fight off the altitude sickness|Take selfies with fluffy Alpacas|Shop for vibrant colourful textiles in a local market|Hike the grueling 4-day classic Inca Trail|Sleep in a transparent capsule hanging 400ft off a cliff wall|Take a panoramic glass-roof train through the Andes|Mountain bike down the terrifying 'Death Road'|Hike the impossibly colourful Rainbow Mountain|Spot massive Andean Condors flying in Colca Canyon",
    "Mendoza (Argentina)|mild,nature,relax,foodie,romance|#8B0000|mendoza vineyards mountains wine|7-course wine pairing lunch in the vineyards|Eat a massive traditional Asado BBQ|Drink world-class Malbec wine directly from the barrel|Drink Fernet and coke|Bike leisurely between the massive vineyards|Go Horseback riding with Gauchos at sunset|Whitewater raft down the Mendoza River|Hike the base of Mount Aconcagua (highest in the Americas)|Paraglide over the Andes mountains|Soak in natural thermal hot springs|Zipline across the valleys|Take a massive outdoor cooking masterclass",
    "Cartagena (Colombia)|hot,city,beach,culture,party|#FF8C00|cartagena colombia colorful colonial streets|Upscale Caribbean-Colombian fusion dining|Eat Arepas filled with cheese from a street cart|Drink Aguardiente firewater shots until you drop|Drink fresh Lulo fruit juice in the sun|Take photos with the Palenqueras fruit ladies|Ride a horse-drawn carriage through the old town|Sail a yacht to the pristine Rosario Islands|Dance Salsa in the legendary Cafe Havana|Bathe in a warm bizarre Mud Volcano (El Totumo)|Walk the massive stone fortress walls at sunset|Explore the colourful gritty Getsemani neighbourhood|Scuba dive the warm Caribbean reefs",
    "Medellin (Colombia)|mild,city,party,culture|#32CD32|medellin colombia mountains cable car|High-end dining in the trendy El Poblado district|Eat a massive Bandeja Paisa meat platter|Drink Aguardiente|Drink fresh Colombian Craft beer|Ride the Metrocable cars over the mountain slums|Take a fascinating Pablo Escobar history tour|Party on exclusive rooftops until dawn|Paraglide high over the entire city|Take a day trip to climb the massive Guatape rock|Explore the street art of Comuna 13|Take intensive Salsa dancing lessons|Take a 4x4 Coffee farm tour",

    # EUROPE (25)
    "Paris (France)|mild,city,culture,foodie,luxury,romance|#C71585|paris eiffel tower sunset romance|Wait in line for Cedric Grolet’s legendary fruit illusion pastries|Eat the famous hot chocolate and mont blanc at Angelina|Champagne at the very top of the Eiffel Tower|Drink inside a secret speakeasy behind a washing machine|Take photos in a vintage Fotoautomat booth in Montmartre|Have a chic picnic at Place des Vosges|Take a Dior Spa cruise down the Seine River|VIP skip-the-line night tour of the Louvre|Explore the underground bone Catacombs|Dine on the glass-roofed Bustronome double-decker bus|Take a croissant-making masterclass|Attend a cabaret show at the Moulin Rouge",
    "Rome (Italy)|mild,hot,city,culture,foodie|#A0522D|rome colosseum ancient sunset|Build your own custom Tiramisu at the famous Pompi|Massive slice of Roman pizza al taglio|Vintage Barolo wine tasting in an ancient cellar|Drink an Aperol Spritz overlooking Piazza Navona|Throw a coin in the Trevi Fountain at midnight|Eat gelato on the Spanish Steps|Take a pasta making class at a stunning Frascati farmhouse|Attend a Gladiator training school on the Appian Way|Take a private after-hours tour of the Sistine Chapel|Ride a Vespa through the chaotic Roman traffic|Explore the ancient crypts made entirely of human bones|Helicopter tour over the ancient ruins",
    "Amalfi Coast (Italy)|hot,beach,foodie,luxury,romance|#FF8C00|amalfi coast cliffside colorful houses|Eat lemon sorbet served inside a massive hollowed-out lemon|Eat lunch at the famous La Tagliata overlooking the cliffs|Limoncello tasting straight from a lemon farm|Drink Prosecco on a private vintage wooden boat|Shop for handmade leather sandals in Positano|Take a vintage Vespa tour along the coastal roads|Swim into the sparkling Blue Grotto sea cave|Take a helicopter tour of Mount Vesuvius|Hike the breathtaking Path of the Gods|Take a private cooking class in a cliffside villa|Charter a luxury yacht to the island of Capri|Jump off the cliffs into the Mediterranean",
    "Venice (Italy)|mild,city,romance,culture|#008080|venice canals gondola sunset romance|Romantic seafood dinner on a floating terrace|Venetian tapas in a crowded local bacaro|Bellinis at the famous Harry's Bar|Spritz in St. Mark's Square listening to the orchestra|Get lost in the tiny alleyways|Watch a glassblower in Murano|Private sunset Gondola ride with a serenader|Attend a masquerade ball in a grand palazzo|Kayak through the quiet hidden canals|VIP tour of the Doge's Palace secret passages|Take a water taxi across the lagoon at high speed|Make your own authentic Carnival mask",
    "Cinque Terre (Italy)|mild,hot,beach,culture|#DC143C|cinque terre italy colorful houses cliff|Eat authentic pesto pasta invented right here|Eat fried seafood out of a paper cone|Taste Sciacchetrà sweet wine|Drink Aperol Spritz on a cliffside terrace|Take the scenic train between the 5 colorful villages|Hike the coastal trails with insane ocean views|Charter a private boat to sail past the colorful cliffs|Cliff jump into the Mediterranean Sea|Take a pesto-making masterclass|Scuba dive in the protected marine park|Watch the sunset from the famous Nessun Dorma restaurant|Explore the terraced vineyards on the cliffs",
    "Swiss Alps (Switzerland)|cold,mountains,adventure,luxury,nature|#8B0000|swiss alps matterhorn snow cabin|Eat fondue inside a literal igloo|Eat at the famous Aescher cliff restaurant built into the rock|Drink Dom Pérignon in an outdoor heated jacuzzi|Drink hot spiced Glühwein by a roaring fire|Build a snowman overlooking the Matterhorn|Ride a horse-drawn sleigh through the village|Ride the Gelmerbahn Europe's steepest open-air funicular|Helicopter drop-off for extreme off-piste skiing|Paraglide over the snowy peaks|Ice climb up a frozen waterfall|Ride the panoramic Glacier Express train|Bungee jump off a dam like James Bond",
    "Hallstatt (Austria)|cold,mountains,nature,romance|#4682B4|hallstatt austria lake mountains fairytale|Eat gourmet Austrian Schnitzel|Eat fresh lake trout|Drink local Austrian beer|Drink hot cocoa overlooking the fairytale lake|Rent a swan boat on the crystal clear water|Wander the perfectly preserved alpine village|Take the funicular up to the ancient salt mines|Walk out onto the terrifying Skywalk viewing platform|Explore the eerie Dachstein Giant Ice Cave|Hike the dramatic Dachstein mountain range|Take a helicopter tour over the Austrian Alps|Visit the incredibly creepy Bone House (Beinhaus)",
    "Vienna (Austria)|mild,city,culture,romance|#FFD700|vienna austria palaces music|Gourmet Wiener Schnitzel|Eat a slice of the famous Sachertorte|Sip elegant Viennese coffee in a grand cafe|Drink local Gruner Veltliner wine in a vineyard|Watch the Lipizzaner dancing horses|Ride the giant historic Ferris wheel|Attend a grand ball in a tuxedo/gown|Listen to Mozart performed in a golden hall|Tour the massive Schönbrunn Palace|Visit the creepy catacombs of St. Stephen's|Take a horse-drawn fiaker ride at night|Sail the Danube river",
    "London (UK)|mild,cold,city,culture,party|#191970|london big ben red bus thames|Eat afternoon tea at Sketch|Eat in the Coppa Club glass igloos overlooking Tower Bridge|Drink cocktails at the eccentric Alchemist bar|Drink pints of ale in a 400-year-old tavern|Feed the pelicans in St. James's Park|Browse quirky antiques at Portobello Road|VIP pod on the London Eye with champagne|Take a terrifying Jack the Ripper night walking tour|Climb completely over the top of the O2 Arena|Attend a smash-hit West End theatre premiere|Speedboat down the River Thames at 40mph|Tour the hidden underground Churchill War Rooms",
    "Scottish Highlands (UK)|cold,mild,mountains,nature,adventure|#2E8B57|scottish highlands castle loch fog mountains|Gourmet venison at a luxury castle|Eat traditional Haggis Neeps and Tatties|Taste 50-year-old single malt Scotch whisky|Drink pints of heavy ale in a 16th-century inn|Spot highland cows (hairy coos)|Search the loch for the Loch Ness Monster|Sleep in a massive historic haunted castle|Ride the real Hogwarts Express steam train|Hike the dramatic ridges of Glencoe|Sea kayak with wild seals|Off-road in a Land Rover through the mud|Learn archery and falconry on a noble estate",
    "Barcelona (Spain)|hot,city,beach,party,culture|#DC143C|barcelona sagrada familia colorful gaudi|Eat Avant-garde molecular gastronomy|Eat endless massive pans of seafood Paella|Sangria tasting on a luxury rooftop|Cava in a historic underground cellar|Find the hidden mosaics in Park Güell|Watch street performers on La Rambla|Sail a catamaran on the Mediterranean at sunset|VIP tour of the unfinished Sagrada Familia|Attend a live passionate Flamenco show|Helicopter ride over the coastline|Dance until 6 AM at a massive beach club|Take a hot air balloon over Catalonia",
    "Ibiza (Spain)|hot,beach,party,luxury|#FF1493|ibiza beach party neon sunset ocean|VIP dining at a superclub|Eat fresh grilled octopus at a quiet hidden cove|Bottle service with sparklers at Pacha|Drink Hierbas liqueur at a bohemian beach shack|Shop at the hippie markets|Watch the sunset at Es Vedra with bongos|Dance until 8 AM with the world's biggest DJs|Charter a luxury yacht to Formentera|Cliff jump into the crystal clear Mediterranean|Parasail high above the party beaches|Explore hidden sea caves on a paddleboard|Attend an exclusive secret villa afterparty",
    "Seville (Spain)|hot,city,culture,romance|#FF8C00|seville spain moorish architecture orange trees|Gourmet Andalusian tapas|Eat Churros con Chocolate|Drink Sherry wine|Drink Tinto de Verano|Walk through the massive Plaza de España|Smell the orange trees in the courtyards|Explore the stunning Royal Alcázar palace|Watch a deeply passionate Flamenco performance in a tiny cave|Walk the wooden Metropol Parasol at sunset|Take a carriage ride through the old town|Attend the wild Feria de Abril festival|Take a boat cruise down the Guadalquivir river",
    "Amsterdam (Netherlands)|mild,city,culture,party|#FF4500|amsterdam canals bicycles sunset|Gourmet Dutch tasting menu in a greenhouse|Eat hot Stroopwafels fresh off the iron|Heineken VIP brewing experience|Jenever tasting in a dimly lit 17th-century tasting room|Browse the floating flower market|Have a picnic in Vondelpark|Rent a private canal boat with endless drinks|Cycle through the tulip fields of Keukenhof|Explore the secret annex of Anne Frank|Party at a massive underground techno warehouse|Tour the bizarre and wild Red Light District|Eat a massive wheel of authentic Gouda cheese",
    "Iceland|cold,nature,adventure,relax|#0B3D91|iceland northern lights glacier waterfalls|High-end Nordic tasting menu|Try fermented shark and a street hot dog|Brennivín shots in an ice bar|Blue lagoon cocktails floating in thermal water|Pet fluffy Icelandic horses|Search for hidden elf houses in the rocks|Explore deep inside a glittering blue Ice Cave|Snowmobile across a massive glacier|Chase the Northern Lights in a Super-Jeep|Snorkel between two tectonic plates in freezing water|Hike up to a live flowing volcano|Walk behind the roaring Seljalandsfoss waterfall",
    "Tromso (Norway)|cold,nature,adventure,mountains|#000033|tromso norway snowy fjords aurora|Arctic fine dining with king crab|Eat dried fish like a true Viking|Taste Aquavit in the world's northernmost brewery|Drink hot toddies on a silent electric whale watching boat|Sleep in a breathtaking glass igloo under the Northern Lights|Warm up by a fire in a cozy candlelit cafe|Chase the Northern Lights in the arctic wilderness|Whale watch for massive Orcas in the fjords|Dog sled across the frozen tundra with Siberian Huskies|Snowshoe through silent snowy valleys|Feed reindeer with indigenous Sami people|Ride the Fjellheisen cable car for sunset views",
    "Svalbard (Norway)|cold,nature,adventure,mountains|#E0FFFF|svalbard polar bears arctic ice|Gourmet dining at the edge of the world|Eat freeze-dried expedition meals in a tent|Champagne tasting in a coal miner's cellar|Drink pure melted glacier water|Mail a letter from the world's northernmost post office|Spot arctic foxes playing in the snow|Armed expedition to safely spot wild Polar Bears|Explore the Global Seed Vault|Snowmobile to an abandoned Soviet ghost town|Ice cave inside a massive glacier|Kayak in freezing waters past walruses|Experience 24 hours of total darkness or sunlight",
    "Santorini (Greece)|hot,beach,relax,luxury,romance|#00008B|santorini white houses blue domes sunset|Private clifftop dining with fresh lobster|Eat a massive Gyros from a bustling local taverna|Wine tasting in a volcanic cave vineyard|Drink cocktails on a luxury catamaran at sunset|Do the famous Flying Dress photoshoot on the white roofs|Wander the white cobblestone streets of Oia|Sail a yacht to the volcanic hot springs|Scuba dive in the deep caldera|Take a helicopter ride over the Greek Islands|Rent ATVs to explore hidden black sand beaches|Explore the ancient ruins of Akrotiri|Jump off the cliffs at Amoudi Bay",
    "Mykonos (Greece)|hot,beach,party,luxury|#00BFFF|mykonos windmills party beach|Luxury seafood at Nammos|Eat Gyros on the street|Champagne bottle service at a beach club|Drink Ouzo shots|Take photos with the iconic windmills|Wander the alleys of Little Venice|Party until 8 AM at massive beach clubs|Charter a luxury yacht|Scuba dive the crystal clear reefs|Take a helicopter to Santorini|Windsurf the breezy ocean|Host a private villa party",
    "Dubrovnik (Croatia)|hot,beach,city,culture|#D2691E|dubrovnik croatia kings landing walls sea|Upscale Mediterranean dining on the cliffs|Eat black squid ink risotto in the old town|Cocktails at a bar literally clinging to the cliffside|Local Rakija shots with a fisherman|Find the Game of Thrones Walk of Shame steps|Pet the hundreds of street cats|Walk the massive ancient city walls at sunset|Sea kayak to the cursed island of Lokrum|Take a cable car up Mount Srd for insane views|Sail the Elaphiti Islands on a pirate ship|Cliff jump at Buza Bar|Zipline over the coastal mountains",
    "Plitvice Lakes (Croatia)|mild,nature,relax|#32CD32|plitvice lakes croatia waterfalls green clear|Gourmet Croatian forest dining|Eat fresh trout|Drink local Croatian wine|Drink cold Ozujsko beer|Walk the endless wooden boardwalks over the lakes|Take stunning photos of the massive waterfalls|Hike the extensive national park trails|Row a wooden boat across the pristine upper lakes|Take a panoramic train ride through the forest|Explore the hidden Barac Caves nearby|Rent bicycles to explore the surrounding villages|Zipline across the nearby Korana river canyon",
    "Prague (Czechia)|cold,mild,city,culture,party|#B22222|prague charles bridge castle sunset|Fine dining overlooking the Vltava river|Eat a massive roasted pork knuckle in a beer hall|Drink absurdly cheap world-class Pilsner|Absinthe tasting in a dark gothic basement|Watch the medieval Astronomical Clock chime|Walk the Charles Bridge at dawn|Take a ghost and legends night tour|Shoot AK-47s at an underground range|Bathe in a literal tub of dark beer at a Beer Spa|Cruise the river on a jazz boat|Attend a classical concert in a 14th-century church|Explore a nuclear bunker from the Cold War",
    "Budapest (Hungary)|cold,city,party,relax|#B22222|budapest parliament river baths|Gourmet Goulash at a high-end restaurant|Eat sweet Chimney cake on the street|Drink Palinka fruit brandy|Drink Unicum herbal liqueur|Soak in the massive outdoor Szechenyi Thermal Baths|Walk the iconic Chain Bridge|Party in the wild eclectic Ruin Pubs|Take a nighttime river cruise past the glowing Parliament|Explore the spooky Buda Castle labyrinth|Go caving under the city streets|Take a helicopter tour over the Danube|Do an intense Escape room",
    "Copenhagen (Denmark)|cold,city,foodie,culture|#4682B4|copenhagen nyhavn boats bikes|Eat at Noma (world's best restaurant)|Eat Smorrebrod open sandwiches|Drink Carlsberg beer at the brewery|Taste Aquavit|Ride the wooden rollercoasters at Tivoli Gardens|Walk the colorful Nyhavn harbor|Rent a boat and drive it through the canals yourself|Explore the hippie commune of Christiania|Cycle the entire city like a local|Bathe in the freezing harbor baths|Take a helicopter tour|Tour the massive Renaissance castles",
    "Lapland (Finland)|cold,nature,adventure,relax|#F0F8FF|lapland snow igloo northern lights reindeer|Luxury Arctic tasting menu|Hearty Reindeer stew cooked over a campfire|Cloudberry liquor in an ice glass|Hot cocoa while wrapped in reindeer hides|Meet the real Santa Claus|Feed wild gentle reindeer|Sleep in a stunning glass igloo under the Northern Lights|Drive a team of huskies on a sled through the forest|Take an icebreaker cruise and swim in the freezing sea|Snowmobile across massive frozen lakes|Ice fishing and cook your catch|Get whipped with birch branches in a traditional sauna",

    # AFRICA & MIDDLE EAST (15)
    "Chefchaouen (Morocco)|hot,city,culture,relax|#1E90FF|chefchaouen morocco blue city cats|Eat traditional Lamb Tagine slow-cooked in clay|Eat fresh Moroccan pastries|Drink endless cups of sweet Mint Tea|Drink fresh squeezed orange juice|Get lost in the completely blue-painted alleyways|Pet the hundreds of friendly street cats|Hike up to the Spanish Mosque for a panoramic sunset|Shop for hand-woven colorful blankets|Take a day trip to the Akchour Waterfalls|Get a brutal but amazing scrub in a traditional Hammam|Camp in the nearby Rif Mountains|Take an intense cooking class with a local family",
    "Cape Town (South Africa)|mild,beach,adventure,nature,luxury|#CD853F|cape town table mountain ocean sunset|10-course tasting menu at The Test Kitchen|Eat South African Biltong jerky on a hike|World-class wine tasting in Stellenbosch via a wine tram|Drink Gin and Tonics on a sunset cruise|Walk with wild penguins at Boulders Beach|Ride the spinning cable car up Table Mountain|Cage dive with massive Great White Sharks|Paraglide off Lion's Head mountain over the ocean|Drive the spectacular Chapman's Peak coastal road|Visit the prison where Nelson Mandela was held|Surf the freezing massive waves of the Atlantic|Go on a nearby Big 5 Safari",
    "Kruger National Park (South Africa)|hot,nature,adventure,luxury|#8B4513|kruger national park safari lion leopard elephant|Gourmet dining under the stars in a luxury lodge|Eat a traditional Braai BBQ by the campfire|Drink Amarula liqueur on ice|Drink Sundowner cocktails parked next to a herd of elephants|Watch baby elephants play in the mud|Sleep in a luxury treehouse with no walls|Open-top 4x4 Safari to spot the Big 5 at dawn|Go on a dangerous walking safari to track Rhinos on foot|Spot a Leopard dragging its prey up a tree|Take a hot air balloon over the savannah|Bungee jump off the nearby Bloukrans Bridge|Helicopter tour over the Blyde River Canyon",
    "Serengeti (Tanzania)|hot,nature,adventure,luxury|#CD853F|serengeti plains acacia tree sunset safari|Champagne bush breakfast after a balloon ride|Eat Ugali and roasted goat|Drink local Safari beer|Drink fresh coffee grown on the slopes of Kilimanjaro|Visit a traditional Maasai village and learn to jump|Watch cheetah cubs play in the tall grass|Take a Hot Air Balloon over the plains at dawn|Witness the Great Migration of millions of wildebeest|Sleep in a luxury canvas tent surrounded by roaring lions|Track the endangered Black Rhino in the Ngorongoro Crater|Climb to the roof of Africa Mount Kilimanjaro|Scuba dive in nearby Zanzibar",
    "Zanzibar (Tanzania)|hot,beach,culture,relax|#20B2AA|zanzibar beach spice island doors|Luxury seafood at the famous The Rock restaurant|Eat Zanzibar pizza in the night market|Drink Cocktails on a dhow boat|Drink Spiced tea|Explore Stone Town's carved wooden doors|Take a fragrant spice farm tour|Scuba dive the vibrant coral reefs|Swim with wild dolphins|Kitesurf on the breezy beaches|Sail a traditional dhow at sunset|Feed giant tortoises on Prison Island|Go Deep sea fishing",
    "Marrakesh (Morocco)|hot,city,culture,foodie|#B22222|marrakesh morocco market medina colorful spices|Luxury dining in a stunning tiled Riad courtyard|Eat slow-cooked Lamb Tagine out of a clay pot|Drink endless cups of sweet Moroccan Mint Tea|Drink fresh squeezed orange juice in the chaotic main square|Get a brutal but amazing scrub in a traditional Hammam|Pet the stray cats in the souks|Get lost in the chaotic maze-like markets (Souks)|Ride camels through the Sahara Desert|Sleep in a luxury desert camp under the stars|Take a hot air balloon over the Atlas Mountains|Watch snake charmers in Jemaa el-Fnaa square|Drive an ATV through the rocky Palmeraie desert",
    "Cairo (Egypt)|hot,city,culture,adventure|#DAA520|cairo egypt pyramids sphinx desert camels|Fine dining overlooking the Nile River|Eat Koshari mixed carb bowl from a street vendor|Drink thick strong Turkish Coffee|Drink hibiscus tea in a smoky shisha cafe|Haggle for spices and lamps in the Khan el-Khalili bazaar|Ride a felucca sailboat on the Nile at sunset|Crawling deep inside the Great Pyramid of Giza|Ride an Arabian horse through the desert at high speed|Take a luxury multi-day cruise down the Nile|Scuba dive the incredible Red Sea shipwrecks|Explore the Valley of the Kings tombs|Stare into the eyes of the Great Sphinx",
    "Luxor (Egypt)|hot,culture,adventure|#DAA520|luxor egypt ancient temples desert|Gourmet Egyptian dining|Eat stuffed pigeon (a delicacy)|Drink strong mint tea|Drink fresh sugarcane juice|Walk the Avenue of Sphinxes|Browse the local markets|Take a spectacular Hot Air Balloon ride at sunrise over the temples|Explore the massive Karnak Temple complex|Go deep into the tombs in the Valley of the Kings|Sail the Nile on a traditional boat|Explore the Temple of Hatshepsut|Ride a donkey through the local villages",
    "Dubai (UAE)|hot,city,luxury,party,adventure|#D4AF37|dubai skyline burj khalifa luxury supercars|Dine in the Sky suspended 50 meters in the air|Eat authentic Shawarma for $2 on the street|$500 cocktails at the 7-star Burj Al Arab|Drink Camel Milk cappuccinos|Ride the terrifying glass slide on the outside of a skyscraper|Watch the spectacular Dubai Fountains dance|Skydive directly over the Palm Jumeirah islands|Rent a Lamborghini to cruise down Sheikh Zayed Road|Dune bash in a massive 4x4 across the red desert|Ski inside a massive indoor mall while it's 40°C outside|Yacht party in the Dubai Marina with billionaires|Scuba dive in the deepest pool in the world (Deep Dive Dubai)",
    "Abu Dhabi (UAE)|hot,city,luxury,adventure|#DAA520|abu dhabi grand mosque luxury|Emirates Palace gold-flaked cappuccino|Eat massive Shawarma platters|Champagne on a mega-yacht|Drink Camel milk|Visit the massive white Sheikh Zayed Grand Mosque|Explore the stunning Louvre Abu Dhabi|Ride the fastest rollercoaster in the world at Ferrari World|Drive a Formula 1 car on the Yas Marina Circuit|Dune bashing in the Empty Quarter|Visit the unique Falconry hospital|Sleep in a luxury desert resort|Scuba dive the warm gulf waters",
    "Petra (Jordan)|hot,culture,adventure,nature|#CD5C5C|petra jordan ancient city carved rocks desert|Luxury dining under the stars in Wadi Rum|Eat massive communal plates of Mansaf|Drink sweet Bedouin tea cooked over a fire|Drink Arak anise spirit|Float effortlessly in the hyper-salty Dead Sea|Cover yourself in healing Dead Sea mud|Walk through the narrow canyon (Siq) to see the Treasury reveal|See Petra lit by thousands of candles at night|Sleep in a transparent Martian dome in the Wadi Rum desert|Ride a 4x4 through the red sands like Lawrence of Arabia|Scuba dive in the Red Sea at Aqaba|Hike the rugged Dana Biosphere Reserve",
    "Socotra (Yemen)|hot,nature,adventure,beach|#2F4F4F|socotra yemen alien trees dragon blood|Eat fresh fish caught by local fishermen|Eat traditional Yemeni rice dishes|Drink sweet black tea|Drink fresh water from desert springs|Take photos with the alien-like Dragon's Blood trees|Find giant bottle trees in the desert|Camp under the absolute darkest star-filled skies on earth|Swim in the stunning crystal clear Detwah Lagoon|Hike the massive white sand dunes of Archer Beach|Explore the massive Hoq cave system|Scuba dive untouched pristine coral reefs|Interact with the completely isolated local tribes",
    "Mauritius|hot,beach,nature,luxury|#FF61A6|mauritius beach ocean luxury|Gourmet French-Creole fusion|Eat Dholl puri street food|Drink Phoenix beer|Rum tasting at a local distillery|Visit the surreal Seven Colored Earth|Swim in warm jungle waterfalls|Take a helicopter to see the legendary Underwater Waterfall illusion|Scuba dive the colorful reefs|Kitesurf the breezy Indian Ocean|Go Deep sea fishing for Marlin|Hike the massive Le Morne Brabant mountain|Charter a luxury catamaran cruise",
    "Seychelles|hot,beach,relax,luxury,romance|#FF61A6|seychelles beach granite rocks crystal ocean|Private beach dining with fresh lobster|Eat spicy octopus curry from a local Creole takeaway|Champagne served in a floating pool tray|Drink Takamaka rum on the rocks|Feed the massive ancient Aldabra Giant Tortoises|Find the rare oddly shaped Coco de Mer nut|Arrive at your 5-star resort via Private Seaplane|Scuba dive through untouched coral reefs|Charter a luxury yacht to island hop|Hike through the dense Jurassic-like Vallée de Mai|Take a transparent glass-bottom kayak over the reefs|Have a full-day couples spa treatment in the jungle canopy",
    "Madagascar|hot,nature,adventure,budget|#228B22|madagascar baobab trees wild lemur nature|Eat Zebu humped cow steak|Eat massive bowls of rice and beans cooked over a fire|Drink home-brewed rum infused with exotic fruits|Drink Three Horses Beer|Trek through the forest to find dancing Lemurs|Spot incredibly rare colourful chameleons|Take a sunset photo walk down the Avenue of the Baobabs|Nighttime predator safari to spot the elusive Aye-Aye|Climb the dangerous razor-sharp Tsingy Stone Forest|Snorkel with Whale Sharks in Nosy Be|Take a traditional Pirogue boat down a massive river|Explore hidden pirate graveyards on Île Sainte-Marie",

    # OCEANIA (10)
    "Great Barrier Reef (Australia)|hot,beach,nature,adventure|#00CED1|great barrier reef coral ocean turtle|Luxury seafood buffet on a catamaran|Eat Barramundi fish and chips on the beach|Champagne on a remote sand cay|Drink Bundaberg Rum|Take a glass-bottom boat tour|Find Nemo in the sea anemones|Scuba dive the largest most vibrant coral reef on earth|Take a scenic helicopter flight over the Heart Reef|Skydive over the reef and land on the beach|Sleep overnight on a pontoon floating on the reef|Sail the beautiful Whitsunday Islands|Bungee jump in the nearby Daintree Rainforest",
    "Australian Outback (Uluru)|hot,nature,adventure,culture|#B8860B|uluru outback red dirt kangaroo sunset|Gourmet Sounds of Silence dinner under the stars|Eat Kangaroo or Emu steak cooked on a BBQ|Drink cold beer out of an esky|Drink Billy Tea boiled over a campfire|Watch the massive Uluru rock change colors at sunset|Learn to throw a returning Boomerang|Sleep in a swag bedroll under a billion stars|Take a helicopter ride over the red desert|Hike the massive dome-shaped Kata Tjuta rocks|Learn Aboriginal Dreamtime stories from indigenous elders|Off-road in a massive 4x4 across the dunes|Ride a camel through the outback at dawn",
    "Queenstown (New Zealand)|mild,cold,mountains,adventure,party|#556B2F|queenstown new zealand mountains lake extreme|Fine dining accessible only by a steep gondola|Eat the world-famous massive Fergburger|Taste world-class Pinot Noir in Central Otago|Drink shots in an ice bar made of glaciers|Ride the Luge go-karts down the mountain|Soak in the private cliffside Onsen Hot Pools|Bungee jump off the Kawarau Bridge where the sport was invented|Jet boat at 90km/h through narrow shallow river canyons|Skydive over the breathtaking Remarkables mountain range|Helicopter ski on untouched alpine powder|Hike the brutal rewarding Ben Lomond track|Paraglide off a mountain over the town",
    "Milford Sound (New Zealand)|cold,nature,mountains,adventure,relax|#2F4F4F|milford sound new zealand fjords waterfalls|Gourmet lunch on a luxury nature cruise|Eat a classic Kiwi meat pie on the bus ride in|Drink hot tea while getting sprayed by a waterfall|Drink Speights beer in a cozy pub|Spot playful Kea alpine parrots|See wild dolphins swimming alongside your boat|Cruise through the majestic towering fjords and waterfalls|Take a scenic flight over the dramatic Southern Alps|Kayak silently through the massive fjords|Hike the multi-day world-famous Milford Track|Scuba dive in the dark deep fjord waters to see black coral|Explore the glowworm caves in nearby Te Anau",
    "Bora Bora (French Polynesia)|hot,beach,relax,luxury,romance|#00BFFF|bora bora tropical island luxury overwater bungalow|Private dinner served on the beach surrounded by tiki torches|Eat Tahitian Poisson Cru raw fish in coconut milk|Drink cocktails out of a freshly cut coconut|Drink Hinano Tahiti beer on a boat|Get a traditional Polynesian flower crown|Have breakfast delivered to your bungalow by canoe|Sleep in a massive $2000/night overwater bungalow|Swim with friendly reef sharks and stingrays|Take a helicopter ride around Mount Otemanu|Jet ski across the impossibly blue lagoon|Attend an intense Polynesian fire dancing show|Scuba dive outside the reef for lemon sharks",
    "Sydney (Australia)|mild,hot,city,beach,party|#1E90FF|sydney opera house harbour bridge ocean|Fine dining inside the Sydney Opera House sails|Eat a classic Aussie meat pie with ketchup|Cocktails at a rooftop bar overlooking the Harbour|Drink pints of Victoria Bitter at a local pub|Pet Kangaroos and Koalas at the zoo|Take the scenic ferry to Manly Beach|Climb the massive arch of the Sydney Harbour Bridge|Surf the famous waves at Bondi Beach|Sail a yacht around the spectacular Sydney Harbour|Take a seaplane to a luxury waterside restaurant|Party at the massive Mardi Gras festival|Scuba dive with Grey Nurse Sharks in Manly",
    "Melbourne (Australia)|mild,city,culture,foodie|#4682B4|melbourne city street art coffee|10-course tasting menu at Attica|Eat incredible Asian-fusion in Chinatown|Drink world-class flat white coffee in a hidden laneway|Drink craft beer in a trendy rooftop bar|Wander the vibrant graffiti-filled Hosier Lane|Watch the little penguins parade at Phillip Island|Drive the spectacular Great Ocean Road to the 12 Apostles|Attend a massive deafening AFL footy match|Explore the hidden underground speakeasies|Take a hot air balloon over the Yarra Valley vineyards|Go surfing at Bells Beach|Hike the rugged Grampians National Park",
    "Fiji|hot,beach,nature,adventure,culture|#3CB371|fiji tropical jungle beach beautiful ocean|Eat Lovo meat and veggies cooked in an earth oven|Eat Kokoda Fijian ceviche|Attend a traditional Kava drinking ceremony|Drink Fiji Bitter beer on the beach|Take a mud bath in the Sabeto Hot Springs|Listen to the locals sing traditional farewell songs|Scuba dive the colorful Great Astrolabe Reef|Whitewater raft the spectacular Upper Navua River|Zipline through the dense jungle canopy|Take a seaplane to the remote Yasawa Islands|Surf the massive world-class Cloudbreak wave|Island hop on a luxury catamaran",
    "Samoa|hot,beach,adventure,culture|#3CB371|samoa tropical ocean trench|Eat a massive traditional Umu feast|Eat crispy Taro root chips|Drink Vailima beer|Drink Kava with the village chief|Swim in the spectacular To Sua Ocean Trench|Watch the massive Alofaaga blowholes erupt|Surf the uncrowded pristine reef breaks|Jungle trek to hidden massive waterfalls|Watch a terrifying traditional Fire Knife dance|Scuba dive the untouched coral reefs|Stay in a traditional open-air Fale on the beach|Slide down the natural Papaseea sliding rocks",
    "Rotorua (New Zealand)|mild,nature,adventure,culture|#8B4513|rotorua new zealand geysers mud pools maori|Eat traditional Maori Hangi cooked underground by geothermal heat|Eat a classic Kiwi pavlova|Drink local craft beer|Drink Sauvignon Blanc from Marlborough|Watch the massive Pohutu Geyser erupt|Soak in the colorful geothermal mud pools|Zipline through the massive ancient Redwood forest|Whitewater raft down the highest commercially rafted waterfall in the world|Roll down a hill inside a giant inflatable Zorb ball|Learn the fierce Haka dance at a Maori village|Mountain bike the world-class Whakarewarewa trails|Luge down the mountain track at high speeds"
]

# Unpack securely
dests = {}
for row in raw_dests:
    parts = row.split("|")
    dests[parts[0]] = {
        "t": parts[1].split(","), "c": parts[2], "p": parts[3],
        "f": [parts[4], parts[5]], "d": [parts[6], parts[7]], "cu": [parts[8], parts[9]],
        "e": [parts[10], parts[11], parts[12], parts[13], parts[14], parts[15]]
    }

# ---------------------------------------------------------
# 3. STATIC & DYNAMIC QUESTION BANK (50 UNIQUE QUESTIONS)
# ---------------------------------------------------------
static_qs = [
    {"q": "Let's set the scene. When I whisk you away, what's the temperature? ☀️❄️", "opts": {
        "Roasting hot. I want to wear next to nothing.": {"tags": ["hot"], "cheeky": "That's exactly how I like you."},
        "Freezing cold. So we can stay in bed all day.": {"tags": ["cold"], "cheeky": "Perfect excuse to keep you warm."},
        "Mild. Just enough breeze to mess up your hair.": {"tags": ["mild"], "cheeky": "I can definitely work with that."}}},
    
    {"q": "When it's just you and me, what's our vibe? 🏃‍♂️🧘‍♀️", "opts": {
        "Extreme adventure. I want my heart racing.": {"tags": ["adventure", "mountains"], "cheeky": "I'll make sure your heart is racing."},
        "Total relaxation. I want you to pamper me.": {"tags": ["relax", "beach"], "cheeky": "I've got you completely covered. Just lean back."},
        "Culture and chaos. Let's get lost together.": {"tags": ["city", "culture"], "cheeky": "Getting lost with you is the best part."},
        "Partying all night. Sleep is optional.": {"tags": ["party"], "cheeky": "I can absolutely keep you up all night."}}},

    {"q": "How exactly am I spoiling you this time? 💸🎒", "opts": {
        "Unlimited luxury. Treat me like a queen.": {"tags": ["luxury"], "cheeky": "You deserve the absolute best. Say less."},
        "A mix of hidden gems and one massive splurge.": {"tags": ["foodie", "culture"], "cheeky": "Smart and sexy. I love the way you think."},
        "Wild and free. We don't need money to have fun.": {"tags": ["budget", "nature"], "cheeky": "Just you, me, and zero distractions."}}}
]

# 50 fully unique, confident, and balanced dynamic questions
raw_qs = [
    "If I kidnapped you for the weekend, what’s the one thing you’d hope I packed for you?|My sexiest dress. We are going out.|city,luxury,party|Oh, I'd definitely make sure that was in there.|Just a bikini. I want sun.|beach,relax,hot|I love the way you think.|My hiking boots. Let's get dirty.|adventure,mountains,nature|I'll definitely make you sweat.|Nothing. Buy me a whole new wardrobe.|culture,foodie,luxury|Spoiling you is my favorite hobby.",
    "When we're out together in a crowded room, what's your favorite secret way to get my attention?|Giving me that specific look from across the bar.|city,luxury,culture|You know exactly what that look does to me.|Brushing your hand against me under the table.|romance,relax,mild|It takes everything in me not to drag you out of there.|Whispering something wicked in my ear.|party,hot,adventure|You’re a menace. I love it.|Stealing a bite of my food so I look at you.|foodie,budget,nature|You can have whatever you want.",
    "I love taking the lead, but tell me… what’s your favorite way to try and take charge?|Telling me exactly what you want me to do to you.|hot,party,adventure|Keep talking like that. See what happens.|Planning out our entire evening down to the minute.|city,culture,luxury|I love watching you get bossy.|Pinning me down when I'm not expecting it.|mountains,nature,cold|You think you're so strong. It's adorable.|Ordering for me at dinner because you know what I like.|foodie,romance,budget|You do know me perfectly.",
    "If we canceled all our plans and stayed in bed all weekend, what's the one rule?|Silk sheets and room service only.|luxury,city,culture|You look incredible in silk.|We only get up for food.|adventure,hot,party|I'll work up your appetite.|No phones, total isolation.|nature,mountains,cold|Just the way I want you. All to myself.|Cooking a massive feast together.|foodie,budget,romance|I love watching you get messy.",
    "What's your absolute favorite way that I distract you?|Whispering something entirely inappropriate.|adventure,mountains,nature|I love watching you blush.|Buying you something you didn't even know you wanted.|luxury,romance,city|Spoiling you is way too easy.|Pulling you close when you're trying to work.|relax,beach,cold|You love it when I don't let you work.|Looking at you that specific way.|culture,party,hot|You know the exact look I mean.",
    "When I tell you to pack a bag for a surprise trip, how do you react?|I trust you completely. I'm ready.|adventure,nature,budget|Good girl. Leave it to me.|I demand to know exactly what I should wear.|city,culture,cold|Don't worry, you won't be wearing much anyway.|I overpack 15 outfits just in case.|relax,beach,mild|I'll just unpack the ones I don't like.|I grab my sexiest dress and my passport.|party,hot,luxury|That's literally all you need.",
    "What's that one wicked trait of yours that I secretly find completely irresistible?|I know exactly how to push your buttons.|adventure,mountains,nature|And you love the consequences.|I expect to be treated like absolute royalty.|luxury,romance,city|Your wish is my command.|I always need the last word.|culture,party,hot|I know exactly how to shut you up.|I steal your clothes and refuse to give them back.|foodie,mild,budget|Keep them. They look better on you.",
    "If I gave you a blank check for one perfect night out with me, what are you wearing?|Something extremely tight and black.|city,luxury,culture|I won't be able to keep my hands off you.|Something totally backless.|beach,relax,mild|I love tracing my fingers down your spine.|Something short and bright red.|foodie,party,hot|You are going to ruin me.|Nothing but one of my button-down shirts.|nature,budget,relax|Best outfit on the list.",
    "When we’re taking our sweet time on a lazy Sunday morning, how do you want me to wake you up?|With coffee and a kiss on the neck.|city,luxury,culture|I know all your sensitive spots.|By pulling you tighter against me.|romance,relax,mild|I never want to let you go.|By whispering what we're doing later.|party,hot,adventure|I love giving you something to look forward to.|With a massive breakfast in bed.|foodie,budget,nature|I love feeding you.",
    "You always know how to earn my undivided attention. What’s a secret fantasy you’ve been waiting to tell me?|Doing something we shouldn't, somewhere public.|party,adventure,hot|I love a girl who takes risks.|A totally private, candlelit evening where I do all the work.|luxury,city,romance|Sit back and let me take over.|Getting caught in a massive rainstorm together.|budget,beach,nature|I love you soaking wet.|A completely blindfolded tasting menu.|culture,foodie,mild|Trust me. I'll make it taste amazing.",
    "When we're out to dinner and I can't stop staring at you, what's going through your mind?|I know exactly what you're thinking.|luxury,city,culture|Oh, I bet you do.|I'm trying not to blush.|romance,relax,mild|It's not working, and I love it.|I'm daring you to do something about it.|party,hot,adventure|Careful what you wish for.|I'm staring right back.|cold,mountains,beach|Good. Don't look away.",
    "If I cleared your schedule for a completely free afternoon, what are we doing?|Something that gets our adrenaline pumping.|adventure,mountains,nature|I like your energy.|Finding a dark, quiet corner in a cocktail bar.|city,luxury,party|Just you and me. Perfect.|Getting lost wandering around somewhere beautiful.|culture,mild,budget|I'd follow you anywhere.|Absolutely nothing. Just us, horizontal.|relax,cold,romance|Best idea yet.",
    "What's your favorite way to get us into a little bit of trouble?|Sneaking into somewhere we definitely shouldn't be.|adventure,party,city|I love it when you're bad.|Ordering way too many expensive drinks.|luxury,hot,culture|I'll buy you the whole bar.|Convincing me to skip our plans and stay in.|cold,mountains,nature|You never have to ask twice.|Stealing a kiss somewhere very public.|beach,foodie,budget|I don't care who's watching.",
    "I pull up outside your house to take you away. What are we driving off in?|A sleek, blacked-out sports car.|city,luxury,party|Fast and dangerous. Just like you.|An open-top Jeep.|beach,hot,adventure|Sun on your skin, wind in your hair.|A rugged 4x4. We're going off-grid.|mountains,nature,cold|Nobody will find us.|I don't care, as long as you're driving.|relax,foodie,budget|I've got you.",
    "After a long, exhausting day, exactly how am I taking care of you?|Running a hot bath and pouring the wine.|luxury,relax,mild|Sink in. I've got this.|A deep, slow massage.|romance,hot,beach|I'll work out every knot.|Taking you out for a massive, messy meal.|foodie,city,culture|I love spoiling your appetite.|Building a fire and pulling you close.|cold,mountains,nature|I'll keep you warm.",
    "When I tell you to close your eyes and hold out your hand, what are you hoping I give you?|Plane tickets to somewhere we've never been.|adventure,nature,culture|Pack your bags, gorgeous.|Something shiny in a small box.|luxury,city,romance|You have expensive taste.|A key to our own private villa.|beach,hot,relax|I'll make sure there are no neighbors.|Something sweet that you baked for me.|foodie,budget,mild|I love taking care of you.",
    "How do you usually react when I catch you staring at me?|I hold eye contact and bite my lip.|party,hot,adventure|You know exactly what that does to me.|I look away and pretend I wasn't.|relax,beach,mild|You're so cute when you're shy.|I smile and walk over to you.|city,luxury,culture|I love how confident you are.|I tell you exactly what I was thinking about.|mountains,nature,cold|I love it when you're direct.",
    "If I told you to pick our next date, what's your opening move?|A high-end restaurant where we dress to kill.|luxury,city,foodie|I love showing you off.|A physical challenge. Let's see who wins.|adventure,mountains,nature|I'll let you win. Maybe.|A massive party where we dance until dawn.|party,hot,culture|I'll keep my hands on you all night.|A secret spot where no one can find us.|relax,beach,romance|My favorite place to be.",
    "When we are completely alone, what is your favorite way to be touched?|A slow hand running through my hair.|relax,mild,romance|I could do that for hours.|A firm grip on my waist.|party,hot,adventure|I love pulling you against me.|Tracing my jawline before you kiss me.|city,luxury,culture|You have the most beautiful face.|A surprise hug from behind.|nature,mountains,cold|I love wrapping you up.",
    "What is the most attractive thing I can do for you without saying a word?|Take control of the situation when I'm stressed.|city,luxury,relax|Just breathe. I've got it.|Pour me a drink exactly how I like it.|foodie,party,culture|I pay attention to the details.|Pick me up and carry me to bed.|hot,adventure,mountains|You are light as a feather.|Look at me from across the room with that smirk.|romance,mild,beach|I can't help myself around you.",
    "What's your signature move when you want me to skip a workout and stay with you?|Straddling my lap while I'm tying my shoes.|hot,party,adventure|That works literally every time.|Promising me something better if I stay.|city,luxury,culture|I'm listening...|Giving me that sad, puppy-dog look.|relax,beach,mild|You know I can't say no to that face.|Telling me you'll cook my favorite meal.|foodie,budget,nature|You know exactly how to bribe me.",
    "If I walked into the room and saw you wearing my favorite outfit of yours, what happens next?|We're going out so I can show you off.|city,luxury,party|Everyone is going to be jealous of me.|We are definitely not leaving the house.|hot,romance,relax|That outfit is coming right back off.|I'd spin you around to get a better look.|culture,mild,foodie|You look absolutely perfect.|I'd take you somewhere remote so you're all mine.|adventure,mountains,nature|No sharing tonight.",
    "What is your ultimate guilty pleasure when it's just the two of us?|Eating absolute junk food in a five-star hotel bed.|foodie,luxury,city|I love your style.|Skinny dipping in the dark.|adventure,hot,beach|I love how wild you are.|Binge-watching trash TV while I play with your hair.|relax,budget,mild|I'll watch whatever you want.|Drinking too much wine and telling each other secrets.|party,culture,romance|Your secrets are safe with me.",
    "When I pull you close by the waist, what's your first instinct?|To wrap my arms around your neck.|romance,relax,mild|Right where you belong.|To look up at your lips.|hot,party,adventure|I'll take the hint.|To lean into your chest and sigh.|cold,mountains,nature|I love holding you.|To whisper something teasing in your ear.|city,luxury,culture|You just love playing games.",
    "If I booked us a private cabin in the woods, how are we spending the first night?|Drinking whiskey by a massive roaring fire.|cold,mountains,relax|I'll keep you warm.|Testing out how sturdy the bed is.|hot,adventure,party|I'm sure we can break it.|Cooking a massive steak dinner together.|foodie,budget,nature|I love feeding you.|Sitting on the porch, completely off the grid.|culture,mild,romance|Just the two of us. Perfect.",
    "When we get into a playful argument, how do you usually try to win?|By using my charm until you cave.|city,luxury,romance|You know I have zero defense against you.|By stubbornly refusing to back down.|mountains,nature,adventure|I love how fierce you are.|By distracting you with a kiss.|hot,party,beach|That is completely unfair. Do it again.|By making you laugh until you forget why you're mad.|foodie,relax,budget|I love your laugh.",
    "If I told you I had a massive surprise planned for tonight, how do you prepare?|I spend two hours getting incredibly dressed up.|luxury,city,culture|I can't wait to see you.|I try to guess what it is relentlessly.|adventure,party,hot|I'm not telling you anything.|I just relax and let you take the wheel.|relax,beach,mild|I promise you'll love it.|I make sure I'm hungry.|foodie,nature,budget|Smart girl.",
    "What is your absolute favorite compliment that I give you?|When you tell me I look insanely sexy.|hot,party,adventure|Because you always do.|When you praise me for something smart I did.|city,culture,luxury|I love your brain.|When you tell me I make you crazy.|romance,relax,beach|You have no idea what you do to me.|When you tell me I taste good.|foodie,mountains,nature|I could eat you up.",
    "If we were trapped on a deserted island, what role do you naturally take?|I'm sunbathing while you build the shelter.|beach,relax,luxury|I wouldn't have it any other way.|I'm foraging for wild fruits and coconuts.|foodie,nature,budget|My little survivor.|I'm exploring the jungle to see what's out there.|adventure,mountains,hot|Stay close to me.|I'm organizing our rescue plan.|city,culture,mild|I love how bossy you are.",
    "What's your preferred method of being spoiled after a stressful week?|A massive shopping spree on your card.|luxury,city,party|Go ahead, ruin me.|A spa day where I don't have to lift a finger.|relax,beach,mild|You deserve to be pampered.|A wild night out to forget all my problems.|adventure,hot,culture|I'll make sure you forget everything.|Comfort food and cuddling on the couch.|foodie,budget,nature|I'll hold you as long as you need.",
    "When I look at you from across a crowded room, what do you want my eyes to say?|'You look incredible.'|luxury,city,romance|You always steal the show.|'We are leaving right now.'|hot,party,adventure|I'll have the car waiting.|'I can't wait to get you alone.'|relax,beach,mild|I really can't.|'You're mine.'|mountains,nature,cold|Absolutely. All mine.",
    "If I took you to a Michelin-star restaurant, how are we ordering?|You order for me. You know what I like.|luxury,city,culture|I know exactly how to feed you.|We order the tasting menu and try everything.|foodie,romance,mild|I love exploring with you.|We order the most expensive thing on the menu.|party,hot,adventure|Let's drain the bank account.|We get dessert first.|relax,budget,nature|I like the way you think.",
    "What is your favorite way for me to show off my strength?|Picking you up effortlessly.|adventure,mountains,hot|You weigh absolutely nothing to me.|Opening jars you can't open.|foodie,relax,budget|I am your personal jar opener.|Pinning your wrists above your head.|party,city,luxury|I love feeling you surrender.|Carrying all the heavy bags so you don't have to.|culture,beach,mild|I'll carry whatever you need.",
    "If I told you to close your eyes, what's the first thing you feel?|Your lips on my neck.|hot,party,romance|Right on your sweet spot.|Your hands on my waist.|adventure,nature,mountains|I love grabbing you.|A cold glass of champagne put in my hand.|luxury,city,beach|Only the best for you.|A bite of something delicious.|foodie,culture,relax|Open wide.",
    "When we are traveling, what is your biggest flex?|I can fall asleep anywhere, instantly.|relax,beach,mild|I love watching you sleep.|I always find the best secret local bars.|party,city,culture|I love drinking with you.|I look amazing even after a 10-hour flight.|luxury,romance,hot|You literally always look flawless.|I can pack my entire life into a carry-on.|adventure,nature,budget|Efficient and sexy.",
    "If I wanted to make you completely melt, what is the exact phrase I should whisper?|'You are so beautiful.'|romance,relax,mild|I mean it every time.|'Let me take care of that.'|city,luxury,culture|I love handling things for you.|'Get in the car.'|adventure,hot,party|I love bossing you around.|'I bought you food.'|foodie,nature,budget|The true key to your heart.",
    "When I catch you wearing my hoodie, what is your excuse?|'It smells exactly like you.'|romance,relax,cold|You can keep it.|'I was cold, and you weren't here to warm me up.'|nature,mountains,mild|I'll warm you up right now.|'It looks better on me anyway.'|city,party,hot|You're right. It really does.|'I didn't think you'd mind.'|budget,beach,culture|I never mind.",
    "If we went to a wild masquerade ball, what is our dynamic?|We are the most elegantly dressed couple there.|luxury,city,culture|We belong on a red carpet.|We ditch the party to find a private balcony.|romance,relax,mild|I only want to look at you.|We dance until our masks fall off.|party,hot,adventure|I'll keep up with you.|We spend the night judging everyone else's outfits.|foodie,budget,nature|I love gossiping with you.",
    "What is your favorite way for us to share a dessert?|I eat most of it, you get one bite.|foodie,budget,relax|I'll let you have it all.|Feeding it to each other slowly.|romance,luxury,city|I love the taste of you.|Eating it in bed and making a mess.|hot,party,adventure|I'll clean you up.|Ordering two different ones so we can swap.|culture,mild,nature|Perfectly balanced.",
    "If I challenged you to a game with a wager, what are you betting?|The loser has to pay for dinner.|foodie,city,culture|I hope you're hungry.|The loser has to give a full-body massage.|relax,beach,mild|I'll happily lose that bet.|The loser has to do whatever the winner says for 24 hours.|hot,party,adventure|You are playing a very dangerous game.|The loser has to jump in the pool fully clothed.|nature,mountains,budget|I love seeing you wet.",
    "When we're holding hands in public, what is your favorite subtle adjustment?|When I rub my thumb over your knuckles.|romance,relax,mild|I love keeping you calm.|When I pull you slightly behind me through a crowd.|adventure,mountains,nature|I'll always lead the way.|When I squeeze your hand tightly when I'm jealous.|party,hot,city|You belong to me.|When I kiss the back of your hand.|luxury,culture,foodie|Treating you like royalty.",
    "If we took a private yacht out for the day, where are you spending most of your time?|Laying on the deck getting completely tanned.|beach,hot,relax|I'll rub the oil on you.|Drinking cocktails in the hot tub.|luxury,party,city|I love your lavish side.|Jumping off the back into the deep water.|adventure,nature,budget|You fearless little thing.|Eating fresh seafood in the shaded cabin.|foodie,culture,mild|I love watching you enjoy yourself.",
    "What is the most attractive piece of clothing I can wear for you?|A perfectly tailored suit.|luxury,city,culture|I clean up well for you.|Sweatpants and a plain white tee.|relax,budget,mild|Keeping it simple.|Swim trunks and messy hair.|beach,hot,adventure|You like me a little rugged.|An apron while I cook for you.|foodie,romance,nature|I'll cook you whatever you want.",
    "When I tell you 'We need to talk,' what is your immediate reaction?|'What did I do?'|relax,mild,budget|You're always innocent, aren't you?|'What did YOU do?'|party,hot,adventure|Fair question. I'm usually the trouble.|'Just tell me, I can handle it.'|city,luxury,culture|I love how strong you are.|'Can we talk over food?'|foodie,nature,mountains|Always thinking with your stomach.",
    "If we got stuck in an elevator for three hours, how do we pass the time?|Making out until the rescue team arrives.|hot,party,romance|They might have to wait for us to finish.|Playing 20 questions and getting deep.|culture,mild,relax|I love picking your brain.|Panicking while you try to calm me down.|city,luxury,beach|I'll always keep you safe.|Prying the doors open ourselves.|adventure,mountains,nature|We don't need rescuing.",
    "What is your favorite way for me to say 'I love you' without using words?|Holding the door and pulling out my chair.|luxury,city,culture|Chivalry isn't dead with us.|Kissing my forehead before you leave the house.|romance,relax,mild|I always want you to feel protected.|Smacking my ass when I walk by.|party,hot,adventure|I literally cannot resist.|Bringing me coffee in bed.|foodie,budget,nature|I know exactly how you like it.",
    "If I took you to a secluded beach at midnight, what is our main objective?|A romantic moonlit walk in the sand.|relax,beach,romance|I love the quiet moments with you.|Going skinny dipping in the dark ocean.|hot,adventure,party|You are so delightfully bad.|Building a bonfire and roasting marshmallows.|foodie,nature,mountains|I'll keep you warm.|Drinking a bottle of expensive champagne.|luxury,city,culture|Only the finest for my girl.",
    "When you're mad at me, what is the fastest way for me to win you back?|Admitting you were right all along.|city,luxury,culture|You are always right.|Buying me food.|foodie,budget,nature|A classic, foolproof strategy.|Pinning me against the wall and kissing me hard.|hot,party,adventure|I know how to shut you up.|Giving me space, then drawing me a bath.|relax,beach,mild|I know how to take care of you.",
    "If we were in a high-speed car chase, what is your role in the passenger seat?|Screaming and holding on for dear life.|relax,mild,beach|Don't worry, I'm a great driver.|Hanging out the window firing back.|adventure,hot,party|My beautiful partner in crime.|Navigating and barking directions at me.|city,luxury,culture|I love when you take charge.|Eating the snacks we stole.|foodie,nature,budget|Priorities. I respect it.",
    "What is the most irresistible thing about my personality?|Your insane confidence.|city,luxury,hot|I only have it because you're mine.|Your sense of humor.|party,budget,adventure|I love making you smile.|Your protective nature.|mountains,nature,cold|Nobody will ever mess with you.|Your ambition.|culture,foodie,mild|I want to give you the world."
]

parsed_dynamic_qs = []
for q_str in raw_qs:
    parts = q_str.split("|")
    q_dict = {"q": parts[0], "opts": {}}
    for i in range(1, 16, 3):
        if i+2 < len(parts):
            q_dict["opts"][parts[i]] = {"tags": parts[i+1].split(","), "cheeky": parts[i+2]}
    parsed_dynamic_qs.append(q_dict)

# ---------------------------------------------------------
# 4. ENGINE LOGIC & ANTI-TAG ALGORITHM
# ---------------------------------------------------------
opposites = {
    "hot": "cold", "cold": "hot", 
    "city": "nature", "nature": "city", 
    "beach": "mountains", "mountains": "beach", 
    "adventure": "relax", "relax": "adventure", 
    "luxury": "budget", "budget": "luxury", 
    "party": "relax"
}

if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.q_index = 0
    st.session_state.user_tags = Counter()
    st.session_state.available_dests = list(dests.keys())
    st.session_state.chosen_dest = None
    st.session_state.activities = []
    st.session_state.activity_round = 0
    st.session_state.last_cheeky = ""
    # We now have exactly 50 unique dynamic questions. No duplication needed.
    st.session_state.unused_qs = list(parsed_dynamic_qs)
    random.shuffle(st.session_state.unused_qs)
    st.session_state.current_q = None

def set_stage(new_stage):
    st.session_state.stage = new_stage

def get_top_dests(n=10):
    scored = []
    for d in st.session_state.available_dests:
        dtags = dests[d]["t"]
        score = sum(st.session_state.user_tags[t] for t in dtags if t in st.session_state.user_tags)
        # Mathematical Tie-Breaker (Increased to 0.25 to prevent any single region dominating)
        norm = (score / len(dtags)) + random.uniform(0, 0.25)
        scored.append((norm, d))
    scored.sort(reverse=True)
    return [x[1] for x in scored[:n]]

def get_next_question():
    if st.session_state.q_index < 3:
        return static_qs[st.session_state.q_index]
    
    if not st.session_state.unused_qs:
        return None

    top_dests = get_top_dests(10)
    active_tags = set()
    for d in top_dests:
        active_tags.update(dests[d]['t'])

    for i, q in enumerate(st.session_state.unused_qs):
        q_tags = set(tag for opt in q['opts'].values() for tag in opt['tags'])
        if q_tags.intersection(active_tags):
            return st.session_state.unused_qs.pop(i)
            
    return st.session_state.unused_qs.pop(0)

def handle_answer(selected_option):
    weights = st.session_state.current_q["opts"][selected_option]["tags"]
    for tag in weights:
        st.session_state.user_tags[tag] += 2
        if tag in opposites:
            st.session_state.user_tags[opposites[tag]] -= 2
            
    st.session_state.last_cheeky = st.session_state.current_q["opts"][selected_option]["cheeky"]
    st.session_state.q_index += 1
    
    # 10 questions answered (Index hits 10) = Stick or Risk
    if st.session_state.q_index == 10:
        set_stage('stick_or_risk')
    # 20 questions answered total (Index hits 20) = Final Match
    elif st.session_state.q_index >= 20 or not st.session_state.unused_qs:
        st.session_state.chosen_dest = get_top_dests(1)[0]
        set_stage('final_match_reveal')
    else:
        st.session_state.current_q = get_next_question()

def stick_choice():
    st.session_state.chosen_dest = get_top_dests(1)[0]
    set_stage('activity_selection')

def risk_choice():
    current_best = get_top_dests(1)[0]
    st.session_state.available_dests.remove(current_best)
    st.session_state.current_q = get_next_question()
    set_stage('questions')

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
    st.markdown("<h1 style='text-align: center; font-size: 65px; font-weight: 900;'>Our Next Escape</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; text-align: center; margin: 20px auto; max-width: 800px;'>
    <h3 style='margin-bottom: 20px;'>Let's figure out exactly where I'm taking you:</h3>
    <p style='font-size: 22px;'>1. I've designed a custom engine that scans 100 exclusive, breathtaking getaways just for us.</p>
    <p style='font-size: 22px;'>2. Answer a few questions so I know exactly how to spoil you.</p>
    <p style='font-size: 22px;'>3. Midway through, I'll let you stick or twist.</p>
    <p style='font-size: 22px;'>4. Then I'll lock in our perfect itinerary. Trust me.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("LET'S GO 🚀", on_click=lambda: setattr(st.session_state, 'current_q', get_next_question()) or set_stage('questions'))
    st.balloons()

elif st.session_state.stage == 'questions':
    set_bg("#2C3E50", "#FFFFFF")
    
    if st.session_state.last_cheeky != "":
        st.markdown(f"<div class='cheeky-text'>💬 \"{st.session_state.last_cheeky}\"</div>", unsafe_allow_html=True)
    
    q_data = st.session_state.current_q
    
    st.markdown(f"<h1 style='font-size: 40px; text-align: center;'>{q_data['q']}</h1><br>", unsafe_allow_html=True)
    
    options = list(q_data["opts"].keys())
    choice = st.radio("👇 Click your vibe:", options, index=0)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("LOCK IT IN! 🔒➡️", on_click=handle_answer, args=(choice,))
    
    st.progress(st.session_state.q_index / 20)

elif st.session_state.stage == 'stick_or_risk':
    best_dest = get_top_dests(1)[0]
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    st.markdown("<h1 style='text-align: center; font-size: 70px;'>🚨 HALFWAY POINT! 🚨</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    with col1:
        safe_image(dest_data["p"])
    
    with col2:
        st.markdown(f"<h2 style='font-size: 45px;'>Right now, I'm taking you to: <br><u style='font-size: 60px;'>{best_dest}</u></h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 25px; background: rgba(0,0,0,0.4); padding: 15px; border-radius: 10px;'>Imagine: {random.choice(dest_data['e'])}</p>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='margin-top: 30px;'>Do you want to STICK with this escape, or RISK it for something else?</h3>", unsafe_allow_html=True)
        
        sub1, sub2 = st.columns(2)
        with sub1:
            st.button("😍 STICK! TAKE ME HERE!", on_click=stick_choice)
        with sub2:
            st.button("🎲 RISK! I WANT TO KEEP GOING!", on_click=risk_choice)

elif st.session_state.stage == 'final_match_reveal':
    best_dest = st.session_state.chosen_dest
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    if "cold" in dest_data["t"]:
        st.snow()
    else:
        st.balloons()
        
    st.markdown("<h1 style='text-align: center; font-size: 80px; text-transform: uppercase;'>🎉 PACK YOUR BAGS! 🎉</h1>", unsafe_allow_html=True)
    safe_image(dest_data["p"])
    st.markdown(f"<h1 style='text-align: center; font-size: 100px; font-weight: 900;'>{best_dest}!</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("HELP ME BUILD OUR ITINERARY ➡️", on_click=set_stage, args=('activity_selection',))

elif st.session_state.stage == 'activity_selection':
    best_dest = st.session_state.chosen_dest
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    rnd = st.session_state.activity_round
    
    if rnd == 0:
        title = "🍽️ What are we eating?"
        act1, act2 = dest_data["f"][0], dest_data["f"][1]
    elif rnd == 1:
        title = "🍸 What are we drinking?"
        act1, act2 = dest_data["d"][0], dest_data["d"][1]
    elif rnd == 2:
        title = "📸 Our hidden gem moment"
        act1, act2 = dest_data["cu"][0], dest_data["cu"][1]
    elif rnd == 3:
        title = "🔥 First epic activity"
        act1, act2 = dest_data["e"][0], dest_data["e"][1]
    elif rnd == 4:
        title = "🔥 Second epic activity"
        act1, act2 = dest_data["e"][2], dest_data["e"][3]
    elif rnd == 5:
        title = "🔥 One final unforgettable memory"
        act1, act2 = dest_data["e"][4], dest_data["e"][5]
    
    st.markdown(f"<h1 style='text-align: center; font-size: 45px;'>Designing our trip to: {best_dest}</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>{title} (Choice {rnd + 1} of 6)</h3>", unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: center;'>You can only KEEP ONE.</h4><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.5); padding: 40px; border-radius: 20px; height: 220px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act1}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ I WANT THIS ONE", key=f"btn1_{rnd}", on_click=pick_activity, args=(act1,))
        
    with col2:
        st.markdown(f"<div style='background-color: rgba(0,0,0,0.5); padding: 40px; border-radius: 20px; height: 220px; display: flex; align-items: center; justify-content: center;'><h2 style='text-align: center;'>{act2}</h2></div><br>", unsafe_allow_html=True)
        st.button("✅ NO, I WANT THIS ONE", key=f"btn2_{rnd}", on_click=pick_activity, args=(act2,))

elif st.session_state.stage == 'final_itinerary':
    best_dest = st.session_state.chosen_dest
    dest_data = dests[best_dest]
    set_bg(dest_data["c"], "#FFFFFF")
    
    if "cold" in dest_data["t"]:
        st.snow()
    else:
        st.balloons()
    
    st.markdown("<h1 style='text-align: center; font-size: 70px; font-weight: 900;'>🎊 OUR ITINERARY IS LOCKED! 🎊</h1>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    with col1:
        safe_image(dest_data["p"])
    
    with col2:
        st.markdown(f"<h2 style='font-size: 50px; text-decoration: underline;'>📍 {best_dest}</h2>", unsafe_allow_html=True)
        st.markdown("<h3>Exactly what we'll be doing:</h3>", unsafe_allow_html=True)
        
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
        st.button("CLICK FOR ONE LAST SURPRISE... 👀", on_click=set_stage, args=('twist',))
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.stage == 'twist':
    set_bg("#000000", "#FFFFFF")
    
    st.markdown("<div class='beating-heart'>❤️</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 80px;'>Confess: Are you completely obsessed with Damien?</h1>", unsafe_allow_html=True)
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
        st.markdown("<h1 style='text-align: center; font-size: 80px; color: #FF1493 !important;'>Good girl. I love you too, Katie bear 🐻</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; font-size: 50px; color: #FFFFFF !important;'>Now go pack your bags. We have plans.</h2>", unsafe_allow_html=True)
        st.balloons()
    else:
        st.markdown("<h1 style='text-align: center; font-size: 80px; color: #FF1493 !important;'>Liar. I know exactly what I do to you 😉.</h1>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; font-size: 50px; color: #FFFFFF !important;'>I love you too, Katie bear 🐻</h2>", unsafe_allow_html=True)
