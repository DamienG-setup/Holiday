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
# 2. VIRAL TIKTOK DESTINATIONS (100 Globally Balanced)
# ---------------------------------------------------------
raw_dests = [
    "Beijing (China)|hot,city,culture,foodie|#B22222|beijing china great wall red lanterns|Eat viral Tanghulu candied fruit|Eat authentic Peking Duck carved tableside|Drink pearl milk tea in a traditional Hutong|Cocktails at a secret bar hidden behind a bookshelf|Rent traditional Hanfu clothes for a photoshoot|Feed adorable pandas at the Beijing Zoo|Ride the viral toboggan slide down the Great Wall|Walk the terrifying glass-bottom cliff bridge in Jingdong|Take the 300mph high-speed bullet train|Night tour of the glowing Bird's Nest stadium|Cable car up the jagged Mutianyu mountains|Explore the massive Summer Palace by wooden boat",
    "Shanghai (China)|mild,city,party,luxury|#8B0000|shanghai skyline bund neon lights|Eat viral soup dumplings at Jia Jia Tang Bao|Fine dining inside the futuristic Pearl Tower|Cocktails at a rooftop bar overlooking the glowing Bund|Sip matcha in the ancient Yu Garden|Visit the massive Shanghai Disneyland|Take a neon-lit river cruise down the Huangpu|Walk the glass floor 100 stories up in the World Financial Center|Explore the cyberpunk Nanjing Road|Ride the Maglev fastest commercial train|Attend a massive underground techno party|Take a day trip to a historic water town|Shop for knock-off luxury goods in underground markets",
    "Zhangjiajie (China)|cold,mountains,nature,adventure|#2F4F4F|zhangjiajie avatar mountains mist|Eat spicy Hunan street noodles|Gourmet banquet in a mountain lodge|Drink hot green tea in the freezing mist|Local rice wine tasting|Watch the wild macaques steal snacks|Walk through the Tianmen mountain Heaven's Gate|Take the terrifying Bailong Elevator up the cliff face|Walk across the world's longest glass-bottom bridge|Hike through the floating Hallelujah Mountains (Avatar)|Ride the world's longest cable car over the jungle|Bungee jump off the glass bridge|Take a helicopter tour of the limestone pillars",
    "Chengdu (China)|mild,city,foodie,culture|#DC143C|chengdu china pandas bamboo spicy|Eat insanely spicy Sichuan Hot Pot|Eat Dan Dan noodles from a street cart|Drink bamboo tea in a historic teahouse|Taste fiery Baijiu liquor|Cuddle baby pandas at the research base|Watch the magical Bian Lian face-changing opera|Explore the ancient Jinli walking street|Hike the misty Mount Emei|See the massive Leshan Giant Buddha carved into a cliff|Experience a brutal traditional ear-cleaning|Party in the Lan Kwai Fong district|Take a cooking class with a Sichuan master",
    "Tokyo (Japan)|mild,city,foodie,culture,party|#FF003F|tokyo neon night city shibuya|Eat at the viral 2D black-and-white cafe|Slurp Tonkotsu ramen in an isolated Ichiran booth|Drink cute lattes at the Pokémon Cafe|High-end whiskey in a slick sky-bar (Lost in Translation)|Play UFO claw machines in Akihabara|Buy weird things from 100 different vending machines|Drive real Mario Karts through the Shibuya Crossing|Walk barefoot through water at the viral teamLab Planets|Watch a brutal heavyweight sumo wrestling tournament|Sing Karaoke in a private room with endless drinks|Take a helicopter tour over the Tokyo neon skyline|Eat insanely fluffy pancakes in Harajuku",
    "Kyoto (Japan)|mild,city,culture,relax|#8B0000|kyoto japan bamboo forest temple|Multi-course exquisite Kaiseki dinner|Eat matcha soft serve while walking the streets|Experience a secret Geisha tea ceremony|Tasting 20 different types of Matcha|Walk the magical Arashiyama Bamboo Forest|Feed the bowing deer in nearby Nara|Sleep in a traditional Ryokan on tatami mats|Bathe naked in a natural outdoor Onsen|Rent kimonos and walk the red Torii gates of Fushimi Inari|Learn to swing a katana with a Samurai master|Meditate with Zen monks at dawn|Attend a vibrant traditional matsuri festival",
    "Osaka (Japan)|mild,city,foodie,party|#FF4500|osaka japan neon dotonbori food|Eat premium Kobe beef cooked in front of you|Eat endless Takoyaki octopus balls on the street|Craft Japanese gin tasting|Drink Sake until dawn in a tiny Izakaya|Take photos with the giant Glico running man sign|Explore the massive Kuromon fish market|Eat literally everything in the Dotonbori food district|Ride the rollercoasters at Universal Studios Japan|Explore the massive imposing Osaka Castle|Party in the vibrant Amerikamura district|Attend a frantic loud baseball game|Take a day trip to explore Kyoto",
    "Hokkaido (Japan)|cold,mountains,nature,adventure|#E0FFFF|hokkaido japan snow skiing crab|Eat massive expensive King Crab legs|Slurp hot Miso Ramen with a slab of butter|Taste Sapporo beer at the original brewery|Drink hot sake in an outdoor snow bath|Watch the adorable snow monkeys bathe|See the massive ice sculptures at the Snow Festival|Ski waist-deep world-class powder snow in Niseko|Bathe in a natural hot spring Onsen while it snows|Snowmobile across vast frozen plains|Icebreaker cruising on the Sea of Okhotsk|Hike a smoking active volcano|Eat incredible fresh sea urchin at the morning market",
    "Seoul (South Korea)|mild,city,foodie,culture,party|#4B0082|seoul south korea neon palace night|Make custom ramen at a Han River convenience store|Eat the viral stretchy 10 Won Coin Bread|Get a viral Personal Color Analysis session|Drink Soju in a street tent (Pojangmacha)|Rent a traditional Hanbok to get into palaces|Try a 10-step Korean skincare routine|Get scrubbed raw at a traditional bathhouse (Jjimjilbang)|Sing K-Pop Karaoke in a private Noraebang|Visit the heavily armed DMZ border with North Korea|Club until 7 AM in Gangnam|Hike Bukhansan Mountain right outside the city|Eat live wriggling octopus at Noryangjin Fish Market",
    "Jeju Island (South Korea)|mild,beach,nature,relax|#32CD32|jeju island south korea beach volcano|Eat famous Jeju Black Pork BBQ|Eat fresh abalone caught by Haenyeo free-divers|Drink Hallabong tangerine juice|Drink craft beer on the beach|Walk through glowing digital art at Arte Museum|Explore the massive Manjanggul lava tube|Hike to the crater of Hallasan volcano|Scuba dive in crystal clear volcanic waters|Explore the quirky Loveland theme park|Watch the sunrise from Seongsan Ilchulbong|Surf the waves at Jungmun Beach|Take a submarine tour",
    "Bangkok (Thailand)|hot,city,party,foodie,culture|#B22222|bangkok thailand neon temples|Eat viral Volcano Ribs at Jodd Fairs night market|Eat Michelin-star crab omelet from a street vendor|Drink at the viral Tichuca jellyfish rooftop bar|Drink cheap buckets of liquor on Khao San Road|Take a chaotic Tuk-Tuk ride|Shop from a tiny boat at the Floating Market|Explore the stunning solid gold Grand Palace|Party with backpackers on Khao San Road|Cruise the Chao Phraya River on a luxury dinner ship|Attend the magical Yi Peng lantern festival|Get a traditional Sak Yant bamboo tattoo|Watch a brutal live Muay Thai boxing match",
    "Chiang Mai (Thailand)|hot,mountains,culture,foodie,relax|#2E8B57|chiang mai thailand temples lanterns|Luxury Khao Soi curry noodle soup tasting|Eat insanely spicy papaya salad at the night bazaar|Artisanal coffee grown in the local mountains|Drink Thai Iced Tea out of a plastic bag|Get a blessed string tied by a monk|Release a glowing paper lantern into the night sky|Bathe and feed elephants at an ethical sanctuary|Take an aggressive 5-day jungle survival trek|Attend an authentic Thai cooking masterclass|Get a brutal traditional Thai massage|Zipline through the jungle with Flight of the Gibbon|Rent a scooter to drive the massive Mae Hong Son loop",
    "Phuket (Thailand)|hot,beach,party,budget,adventure|#FF8C00|phuket thailand longtail boat limestone|Gourmet Thai fusion on a cliff edge|Eat insanely spicy Pad Thai from a street cart|VIP table at an insane beach club|Drink cheap buckets of liquor on Bangla Road|Get a cheap aggressive Thai foot massage|Shop at the chaotic weekend night market|Party until dawn at the Full Moon Party|Bathe and feed rescued elephants in a sanctuary|Take a longtail boat to James Bond Island|Scuba dive with massive Whale Sharks|Watch a brutal live Muay Thai boxing match|Zipline through the dense tropical jungle",
    "Bali (Indonesia)|hot,beach,nature,relax,budget|#228B22|bali indonesia rice terraces jungle sunset|Eat a floating breakfast in a jungle infinity pool|Eat spicy Nasi Goreng at a cheap local warung|Cocktails at the massive luxurious Finns Beach Club|Drink a Bintang beer sitting on a beanbag|Swing over the rice terraces on the viral Bali Swing|Get blessed by a monk in a holy water temple|Hike Mount Batur in the dark to watch the sunrise|Surf the world-class waves of Uluwatu|Scuba dive a WWII shipwreck in Tulamben|Get a brutal but amazing 2-hour Balinese massage|White water raft down the Ayung River|Take a fast boat to stunning Nusa Penida",
    "Komodo Island (Indonesia)|hot,nature,adventure,beach|#2F4F4F|komodo island dragons pink beach jungle|Gourmet seafood on a luxury liveaboard boat|Eat grilled fish on a stick on the beach|Cold Bintang beer after a long hike|Drink fresh coconut water straight from the tree|Relax on a rare beautiful Pink Sand Beach|Watch thousands of flying foxes erupt at sunset|Trek through the brush to find deadly Komodo Dragons|Scuba dive with Manta Rays in strong currents|Sail the Indonesian archipelago on a Phinisi boat|Hike to the stunning viewpoint on Padar Island|Swim in crystal clear turquoise bays|Spearfish your own dinner",
    "Raja Ampat (Indonesia)|hot,beach,nature,adventure|#00CED1|raja ampat coral islands pristine|Luxury seafood on a remote eco-resort|Eat traditional Papuan Sago|Drink coconut cocktails|Drink cold Bintang|Take photos at the iconic Piaynemo viewpoint|Swim with thousands of stingless jellyfish|Scuba dive the most biodiverse coral reefs on Earth|Kayak through towering limestone karst islands|Explore hidden glowing sea caves|Stay in an overwater bungalow with no WiFi|Hike into the jungle to spot Birds of Paradise|Take a liveaboard diving safari",
    "Singapore|hot,city,luxury,foodie|#8B008B|singapore marina bay sands supertrees|Eat $300 Chili Crab at a luxury seafood house|Eat $3 Michelin-star Chicken Rice at a hawker centre|Drink the original Singapore Sling at the Raffles Hotel|Craft cocktails in a hidden speakeasy|Walk through the glowing Supertree Grove|Explore the indoor waterfall at the Jewel airport|Swim in the Marina Bay Sands infinity pool 57th floor|Take a night safari to see nocturnal predators|Shop in insanely massive luxury mega-malls|Ride the Singapore Flyer observation wheel|Bungee jump on Sentosa Island|Watch the Formula 1 Night Race",
    "Hanoi (Vietnam)|hot,city,culture,foodie,budget|#556B2F|hanoi vietnam busy streets motorbikes|Gourmet French-Vietnamese fusion|Eat $1 Pho sitting on a tiny plastic stool|Drink viral Egg coffee in a hidden narrow cafe|Drink Bia Hoi fresh beer for 20 cents|Dodge thousands of motorbikes to cross the street|Watch a traditional Water Puppet show|Take a luxury overnight junk boat cruise in Ha Long Bay|Trek the terraced rice fields of Sapa|Crawling through the Cu Chi tunnels|Take a sleeper train down the coast|Eat Banh Mi from a street cart|Explore the massive ancient cave of Son Doong",
    "Ha Long Bay (Vietnam)|hot,nature,relax,romance|#20B2AA|ha long bay vietnam limestone boats|Gourmet seafood on a luxury wooden junk boat|Eat fresh spring rolls|Drink cocktails on the top deck at sunset|Drink strong Vietnamese drip coffee|Take a bamboo rowboat through floating fishing villages|Explore the massive Sung Sot cave|Kayak silently through the towering limestone karsts|Take a seaplane flight over the emerald waters|Swim in isolated hidden coves|Take a Tai Chi class on the deck at dawn|Squid fishing at midnight|Hike to the top of Titop Island for a panoramic view",
    "Palawan (Philippines)|hot,beach,nature,adventure,budget|#00CED1|palawan philippines limestone lagoons|Fresh lobster cooked on a remote island|Eat Adobo and Lechon roast pig|Rum cocktails out of a pineapple|Drink Red Horse beer by a beach bonfire|Take a tiny outrigger boat to a hidden lagoon|Find a totally deserted white sand beach|Paddle deep into the massive Underground River cave|Island hop through the breathtaking Bacuit Archipelago|Scuba dive WWII Japanese shipwrecks in Coron|Zipline between two islands over the ocean|Kayak through secret emerald lagoons|Camp on a deserted island like Survivor",
    "Siargao (Philippines)|hot,beach,adventure,party|#3CB371|siargao philippines surfing palm trees|Gourmet smoothie bowls at a trendy cafe|Eat fresh Kinilaw (Filipino ceviche)|Drink cheap rum at a massive jungle party|Drink fresh coconut water|Swing from a rope into the Maasin River|Drive a scooter through thousands of palm trees|Surf the legendary Cloud 9 barrel waves|Island hop to Naked Island (just a sandbar)|Explore the glowing Sugba Lagoon|Party all night at the viral General Luna clubs|Wakeboard across the pristine ocean|Cliff jump into the Magpupungko rock pools",
    "Taipei (Taiwan)|mild,city,foodie,culture|#D2691E|taipei taiwan night market 101 tower|Soup dumplings at the original Din Tai Fung|Eat Stinky Tofu at a chaotic night market|High mountain Oolong tea ceremony|Drink absurdly sugary Boba Bubble Tea|Release a glowing paper lantern in Shifen|Ride the Maokong glass-bottom gondola|Take the ultra-fast elevator up Taipei 101|Soak in the Beitou thermal hot springs|Hike Elephant Mountain for the perfect city view|Explore the stunning Taroko Gorge marble canyons|Eat literally everything at Shilin Night Market|Scooter road trip along the dramatic east coast",
    "Luang Prabang (Laos)|hot,culture,nature,relax|#8B4513|luang prabang laos monks temples waterfalls|Luxury French-Lao fusion dining|Eat spicy Laap and sticky rice|Drink Beerlao by the Mekong river|Drink fresh sugar cane juice|Give alms to the hundreds of monks at dawn|Shop the vibrant night market|Swim in the spectacular multi-tiered Kuang Si Falls|Take a slow boat down the Mekong River|Explore the Pak Ou caves filled with Buddha statues|Take an organic rice farming masterclass|Bathe elephants in the river|Get a traditional Lao herbal sauna and massage",
    "Jaipur (India)|hot,city,culture,romance|#FF4500|jaipur india pink city palaces desert|Royal Rajasthani Thali in a converted palace|Eat ultra-spicy Laal Maas curry|Cocktails on a palace rooftop|Drink fresh Lassi from a clay pot|Explore the insanely intricate Hawa Mahal Palace of Winds|Get a traditional Henna tattoo|Take a hot air balloon over the desert forts|Ride a jeep up to the massive Amber Fort|Sleep like royalty in an actual Maharaja's palace|Spot wild Bengal Tigers in Ranthambore on safari|Shop for precious gems and textiles|Watch a snake charmer in the street markets",
    "Amalfi Coast (Italy)|hot,beach,foodie,luxury,romance|#FF8C00|amalfi coast cliffside colorful houses|Eat lemon sorbet served inside a massive hollowed-out lemon|Eat lunch at the viral La Tagliata overlooking the cliffs|Limoncello tasting straight from a lemon farm|Drink Prosecco on a private vintage wooden boat|Shop for handmade leather sandals in Positano|Take a vintage Vespa tour along the coastal roads|Swim into the sparkling Blue Grotto sea cave|Take a helicopter tour of Mount Vesuvius|Hike the breathtaking Path of the Gods|Take a private cooking class in a cliffside villa|Charter a luxury yacht to the island of Capri|Jump off the cliffs into the Mediterranean",

    "New York City (USA)|mild,cold,city,foodie,luxury,culture|#4682B4|new york city times square skyline|Eat the viral Suprême croissant at Lafayette|Eat a massive greasy $2 slice of NY pizza|Martinis in a high-end hidden speakeasy|Drink cheap beers at a gritty Brooklyn dive bar|Take mind-bending photos in the SUMMIT One Vanderbilt|Ice skate in Central Park|Take a helicopter doors-off tour over Manhattan|Watch a smash-hit Broadway musical from VIP seats|Attend a crazy underground warehouse party in Brooklyn|Go on a massive shopping spree on 5th Avenue|Eat a massive pastrami sandwich at Katz's Deli|Walk the High Line elevated park at sunset",
    "Los Angeles (USA)|hot,city,beach,party,luxury|#FF1493|los angeles hollywood palm trees sunset|Eat at the viral Erewhon bakery|Eat tacos from a street truck at 2 AM|Drink insanely expensive green juice|Drink cocktails on a West Hollywood rooftop|Hike to the Hollywood sign|Rollerblade down Venice Beach|Take a VIP studio backlot tour|Surf the waves in Malibu|Drive a convertible down the Pacific Coast Highway|Party with celebrities in Beverly Hills|Shop on Rodeo Drive|Take a helicopter tour over the mansions",
    "San Francisco (USA)|mild,city,foodie,culture,adventure|#1E90FF|san francisco golden gate bridge cable car|10-course Michelin star tasting menu in Soma|Eat Clam Chowder out of a massive sourdough bowl|Wine tasting trip to Napa Valley via private limo|Drink Irish Coffees at the Buena Vista|Hang off the side of a moving Cable Car|Have a picnic at the Painted Ladies|Take a terrifying midnight Alcatraz ghost tour|Bike across the Golden Gate Bridge|Skydive directly over the Bay|Hike among massive Redwoods in Muir Woods|Eat giant burritos in the Mission District|Sail a catamaran under the Golden Gate Bridge",
    "Miami (USA)|hot,beach,party,luxury|#FF1493|miami south beach neon palm trees|Luxury stone crab dining at Joe's|Eat authentic Cuban sandwiches in Little Havana|Champagne on a mega-yacht|Drink mojitos at a salsa club|Rollerblade down Ocean Drive in neon gear|Look at street art in Wynwood Walls|Party until 6 AM at a massive club like E11EVEN|Ride an airboat through the Everglades looking for alligators|Charter a private yacht to the Bahamas|Drive a neon Lamborghini down South Beach|Deep sea fishing for Marlin|Attend an exclusive Art Basel party",
    "Oahu (Hawaii)|hot,beach,city,adventure|#1E90FF|oahu hawaii waikiki beach surfing|Eat luxury Japanese fusion at Nobu|Eat fresh Poke bowls from a local grocery store|Drink Mai Tais at the Royal Hawaiian|Drink Kona brewing beer on the beach|Visit the historic Pearl Harbor memorial|Eat Dole Whip at the pineapple plantation|Surf massive winter waves on the North Shore|Hike the terrifying Haiku Stairs (Stairway to Heaven)|Shark cage diving in the open ocean|Helicopter tours over the volcanic craters|Attend a massive traditional Luau fire show|Skydive over the crystal clear ocean",
    "Kauai (Hawaii)|hot,nature,adventure,relax|#006400|kauai hawaii napali coast cliffs|Luxury oceanfront dining|Eat massive colorful Shave Ice|Drink tropical cocktails out of a pineapple|Drink local Hawaiian coffee|Hike the breathtaking Waimea Canyon|Take a doors-off Helicopter over Jurassic Park falls|Sail a catamaran along the dramatic Na Pali coast|Kayak the Wailua River to hidden waterfalls|Zipline over the lush valleys|Surf the warm waves|Scuba dive with sea turtles|Off-roading in a 4x4 through the mud",
    "Yellowstone (USA)|cold,mild,nature,adventure|#A0522D|yellowstone geyser bison nature|Gourmet game meat at a luxury lodge|Eat campfire chili out of a tin can|Craft beer tasting in a cowboy saloon|Drink cowboy coffee boiled over a fire|Watch Old Faithful erupt on schedule|Spot adorable bear cubs through binoculars|Snowmobile through the park in dead of winter|Spot packs of wild wolves in the Lamar Valley|Hike around the neon-colored Grand Prismatic Spring|Camp deep in grizzly bear country|Fly fish in freezing crystal-clear rivers|Whitewater raft down the Snake River",
    "Banff (Canada)|cold,mountains,nature,adventure|#2F4F4F|banff canada lake louise mountains snow|Fine dining at the Fairmont Chateau Lake Louise|Eat massive plates of Canadian Poutine|Drink ice wine from the local vineyards|Sip hot chocolate while ice skating|Rent a clear glass canoe on the turquoise Lake Louise|Soak in the prototype Banff Upper Hot Springs|Take a helicopter tour over the massive Canadian Rockies|Hike to the spectacular Plain of Six Glaciers|Ski world-class powder at Sunshine Village|Ice climb up a frozen waterfall in Johnston Canyon|Spot massive wild Grizzly Bears|Take the steep gondola up Sulphur Mountain",
    "Whistler (Canada)|cold,mountains,adventure,party|#E0FFFF|whistler skiing mountains snow|Gourmet alpine dining|Eat Beavertails pastry|Drink hot toddy|Drink Apres-ski beers in a loud pub|Ride the Peak 2 Peak gondola|Snowshoe through the quiet forests|Ski massive world-class slopes|Heli-skiing on untouched powder peaks|Bungee jumping into a freezing gorge|Ziplining over the pine trees|Mountain biking the extreme downhill trails in summer|Go bear watching in the wild",
    "Mexico City|mild,city,foodie,culture,party|#B22222|mexico city zocalo vibrant culture|Dine at Pujol (top 10 restaurant in the world)|Eat endless $1 Al Pastor street tacos|High-end Mezcal tasting in a slick speakeasy|Drink Micheladas in a loud Cantina|Ride colorful boats in Xochimilco|Browse art in the Frida Kahlo Museum|Climb the massive ancient Pyramids of the Sun and Moon|Watch a wild high-flying Lucha Libre wrestling match|Party until dawn in the trendy Roma Norte district|Take a hot air balloon over the Teotihuacan ruins|Eat exotic insects like chapulines|Explore the massive Chapultepec Castle",
    "Tulum (Mexico)|hot,beach,party,culture,relax|#20B2AA|tulum mexico beach cenote ancient ruins jungle|Eat gourmet Maya-fusion dining in the jungle|Eat fresh fish tacos barefoot on the beach|Drink Matcha lattes at the viral Azulik treehouse|Drink Mezcal at a massive jungle techno rave|Float down a crystal clear underground Cenote|Do yoga on the beach at sunrise|Explore the ancient Mayan ruins perched on the cliff edge|Scuba dive in the dark underwater cave systems|Swim with giant sea turtles in Akumal|Kitesurf on the breezy Caribbean ocean|Take a mud bath in a Mayan sweat lodge|Rent a bicycle to ride down the trendy beach road",
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

    "Chefchaouen (Morocco)|hot,city,culture,relax|#1E90FF|chefchaouen morocco blue city cats|Eat traditional Lamb Tagine slow-cooked in clay|Eat fresh Moroccan pastries|Drink endless cups of sweet Mint Tea|Drink fresh squeezed orange juice|Get lost in the completely blue-painted alleyways|Pet the hundreds of friendly street cats|Hike up to the Spanish Mosque for a panoramic sunset|Shop for hand-woven colorful blankets|Take a day trip to the Akchour Waterfalls|Get a brutal but amazing scrub in a traditional Hammam|Camp in the nearby Rif Mountains|Take an intense cooking class with a local family",
    "Cape Town (South Africa)|mild,beach,adventure,nature,luxury|#CD853F|cape town table mountain ocean sunset|10-course tasting menu at The Test Kitchen|Eat South African Biltong jerky on a hike|World-class wine tasting in Stellenbosch via a wine tram|Drink Gin and Tonics on a sunset cruise|Walk with wild penguins at Boulders Beach|Ride the spinning cable car up Table Mountain|Cage dive with massive Great White Sharks|Paraglide off Lion's Head mountain over the ocean|Drive the spectacular Chapman's Peak coastal road|Visit the prison where Nelson Mandela was held|Surf the freezing massive waves of the Atlantic|Go on a nearby Big 5 Safari",
    "Kruger National Park (South Africa)|hot,nature,adventure,luxury|#8B4513|kruger national park safari lion leopard elephant|Gourmet dining under the stars in a luxury lodge|Eat a traditional Braai BBQ by the campfire|Drink Amarula liqueur on ice|Drink Sundowner cocktails parked next to a herd of elephants|Watch baby elephants play in the mud|Sleep in a luxury treehouse with no walls|Open-top 4x4 Safari to spot the Big 5 at dawn|Go on a dangerous walking safari to track Rhinos on foot|Spot a Leopard dragging its prey up a tree|Take a hot air balloon over the savannah|Bungee jump off the nearby Bloukrans Bridge|Helicopter tour over the Blyde River Canyon",
    "Serengeti (Tanzania)|hot,nature,adventure,luxury|#CD853F|serengeti plains acacia tree sunset safari|Champagne bush breakfast after a balloon ride|Eat Ugali and roasted goat|Drink local Safari beer|Drink fresh coffee grown on the slopes of Kilimanjaro|Visit a traditional Maasai village and learn to jump|Watch cheetah cubs play in the tall grass|Take a Hot Air Balloon over the plains at dawn|Witness the Great Migration of millions of wildebeest|Sleep in a luxury canvas tent surrounded by roaring lions|Track the endangered Black Rhino in the Ngorongoro Crater|Climb to the roof of Africa Mount Kilimanjaro|Scuba dive in nearby Zanzibar",
    "Zanzibar (Tanzania)|hot,beach,culture,relax|#20B2AA|zanzibar beach spice island doors|Luxury seafood at the viral The Rock restaurant|Eat Zanzibar pizza in the night market|Drink Cocktails on a dhow boat|Drink Spiced tea|Explore Stone Town's carved wooden doors|Take a fragrant spice farm tour|Scuba dive the vibrant coral reefs|Swim with wild dolphins|Kitesurf on the breezy beaches|Sail a traditional dhow at sunset|Feed giant tortoises on Prison Island|Go Deep sea fishing",
    "Marrakesh (Morocco)|hot,city,culture,foodie|#B22222|marrakesh morocco market medina colorful spices|Luxury dining in a stunning tiled Riad courtyard|Eat slow-cooked Lamb Tagine out of a clay pot|Drink endless cups of sweet Moroccan Mint Tea|Drink fresh squeezed orange juice in the chaotic main square|Get a brutal but amazing scrub in a traditional Hammam|Pet the stray cats in the souks|Get lost in the chaotic maze-like markets (Souks)|Ride camels through the Sahara Desert|Sleep in a luxury desert camp under the stars|Take a hot air balloon over the Atlas Mountains|Watch snake charmers in Jemaa el-Fnaa square|Drive an ATV through the rocky Palmeraie desert",
    "Cairo (Egypt)|hot,city,culture,adventure|#DAA520|cairo egypt pyramids sphinx desert camels|Fine dining overlooking the Nile River|Eat Koshari mixed carb bowl from a street vendor|Drink thick strong Turkish Coffee|Drink hibiscus tea in a smoky shisha cafe|Haggle for spices and lamps in the Khan el-Khalili bazaar|Ride a felucca sailboat on the Nile at sunset|Crawling deep inside the Great Pyramid of Giza|Ride an Arabian horse through the desert at high speed|Take a luxury multi-day cruise down the Nile|Scuba dive the incredible Red Sea shipwrecks|Explore the Valley of the Kings tombs|Stare into the eyes of the Great Sphinx",
    "Luxor (Egypt)|hot,culture,adventure|#DAA520|luxor egypt ancient temples desert|Gourmet Egyptian dining|Eat stuffed pigeon (a delicacy)|Drink strong mint tea|Drink fresh sugarcane juice|Walk the Avenue of Sphinxes|Browse the local markets|Take a spectacular Hot Air Balloon ride at sunrise over the temples|Explore the massive Karnak Temple complex|Go deep into the tombs in the Valley of the Kings|Sail the Nile on a traditional boat|Explore the Temple of Hatshepsut|Ride a donkey through the local villages",
    "Dubai (UAE)|hot,city,luxury,party,adventure|#D4AF37|dubai skyline burj khalifa luxury supercars|Dine in the Sky suspended 50 meters in the air|Eat authentic Shawarma for $2 on the street|$500 cocktails at the 7-star Burj Al Arab|Drink Camel Milk cappuccinos|Ride the terrifying glass slide on the outside of a skyscraper|Watch the spectacular Dubai Fountains dance|Skydive directly over the Palm Jumeirah islands|Rent a Lamborghini to cruise down Sheikh Zayed Road|Dune bash in a massive 4x4 across the red desert|Ski inside a massive indoor mall while it's 40°C outside|Yacht party in the Dubai Marina with billionaires|Scuba dive in the deepest pool in the world (Deep Dive Dubai)",
    "Abu Dhabi (UAE)|hot,city,luxury,adventure|#DAA520|abu dhabi grand mosque luxury|Emirates Palace gold-flaked cappuccino|Eat massive Shawarma platters|Champagne on a mega-yacht|Drink Camel milk|Visit the massive white Sheikh Zayed Grand Mosque|Explore the stunning Louvre Abu Dhabi|Ride the fastest rollercoaster in the world at Ferrari World|Drive a Formula 1 car on the Yas Marina Circuit|Dune bashing in the Empty Quarter|Visit the unique Falconry hospital|Sleep in a luxury desert resort|Scuba dive the warm gulf waters",
    "Petra (Jordan)|hot,culture,adventure,nature|#CD5C5C|petra jordan ancient city carved rocks desert|Luxury dining under the stars in Wadi Rum|Eat massive communal plates of Mansaf|Drink sweet Bedouin tea cooked over a fire|Drink Arak anise spirit|Float effortlessly in the hyper-salty Dead Sea|Cover yourself in healing Dead Sea mud|Walk through the narrow canyon (Siq) to see the Treasury reveal|See Petra lit by thousands of candles at night|Sleep in a transparent Martian dome in the Wadi Rum desert|Ride a 4x4 through the red sands like Lawrence of Arabia|Scuba dive in the Red Sea at Aqaba|Hike the rugged Dana Biosphere Reserve",
    "Socotra (Yemen)|hot,nature,adventure,beach|#2F4F4F|socotra yemen alien trees dragon blood|Eat fresh fish caught by local fishermen|Eat traditional Yemeni rice dishes|Drink sweet black tea|Drink fresh water from desert springs|Take photos with the alien-like Dragon's Blood trees|Find giant bottle trees in the desert|Camp under the absolute darkest star-filled skies on earth|Swim in the stunning crystal clear Detwah Lagoon|Hike the massive white sand dunes of Archer Beach|Explore the massive Hoq cave system|Scuba dive untouched pristine coral reefs|Interact with the completely isolated local tribes",
    "Mauritius|hot,beach,nature,luxury|#FF61A6|mauritius beach ocean luxury|Gourmet French-Creole fusion|Eat Dholl puri street food|Drink Phoenix beer|Rum tasting at a local distillery|Visit the surreal Seven Colored Earth|Swim in warm jungle waterfalls|Take a helicopter to see the viral Underwater Waterfall illusion|Scuba dive the colorful reefs|Kitesurf the breezy Indian Ocean|Go Deep sea fishing for Marlin|Hike the massive Le Morne Brabant mountain|Charter a luxury catamaran cruise",
    "Seychelles|hot,beach,relax,luxury,romance|#FF61A6|seychelles beach granite rocks crystal ocean|Private beach dining with fresh lobster|Eat spicy octopus curry from a local Creole takeaway|Champagne served in a floating pool tray|Drink Takamaka rum on the rocks|Feed the massive ancient Aldabra Giant Tortoises|Find the rare oddly shaped Coco de Mer nut|Arrive at your 5-star resort via Private Seaplane|Scuba dive through untouched coral reefs|Charter a luxury yacht to island hop|Hike through the dense Jurassic-like Vallée de Mai|Take a transparent glass-bottom kayak over the reefs|Have a full-day couples spa treatment in the jungle canopy",
    "Madagascar|hot,nature,adventure,budget|#228B22|madagascar baobab trees wild lemur nature|Eat Zebu humped cow steak|Eat massive bowls of rice and beans cooked over a fire|Drink home-brewed rum infused with exotic fruits|Drink Three Horses Beer|Trek through the forest to find dancing Lemurs|Spot incredibly rare colourful chameleons|Take a sunset photo walk down the Avenue of the Baobabs|Nighttime predator safari to spot the elusive Aye-Aye|Climb the dangerous razor-sharp Tsingy Stone Forest|Snorkel with Whale Sharks in Nosy Be|Take a traditional Pirogue boat down a massive river|Explore hidden pirate graveyards on Île Sainte-Marie",

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

# Standardize and unpack rest to fill precisely 100 entries.
# Unpacking logic: Name | Tags | Color | Prompt | F1 | F2 | D1 | D2 | C1 | C2 | E1-6
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
static_qs = [
    {"q": "First things first. What is your absolute ideal climate? ☀️❄️", "opts": {
        "Roasting hot. Bake me like a potato.": {"tags": ["hot"], "cheeky": "Factor 50 sunscreen required. Chasing the sun."},
        "Brisk, freezing, and covered in snow.": {"tags": ["cold"], "cheeky": "Elsa vibes. The cold never bothered you anyway."},
        "Mild, breezy, and perfect for a light jacket.": {"tags": ["mild"], "cheeky": "Ah, the Goldilocks zone. Not too hot, not too cold."}}},
    {"q": "What is the desired pace for this trip? 🏃‍♂️🧘‍♀️", "opts": {
        "Extreme adventure. I want to risk my life.": {"tags": ["adventure", "mountains"], "cheeky": "Adrenaline junkie. Hope your insurance is paid up."},
        "Total relaxation. I want to forget my own name.": {"tags": ["relax", "beach"], "cheeky": "Brain empty. Vibes only. Let's chill."},
        "Chaos, culture, and non-stop exploring.": {"tags": ["city", "culture"], "cheeky": "You'll need a vacation to recover from this."},
        "Partying until the sun comes up.": {"tags": ["party"], "cheeky": "Sleep is for the weak. Let's rage."}}},
    {"q": "What is your budget/travel style? 💸🎒", "opts": {
        "Unlimited wealth. Spoil me absolutely rotten.": {"tags": ["luxury"], "cheeky": "Sugar daddy vibes. Let's drain the bank account."},
        "A mix of cheap street food and one fancy splurge.": {"tags": ["foodie", "culture"], "cheeky": "Sensible, yet indulgent. Perfect balance."},
        "I just need a tent, some rice, and good vibes.": {"tags": ["budget", "nature"], "cheeky": "Dirt cheap and loving it. Nature is free."}}}
]

raw_qs = [
    "How do you handle a group project?|I do 100% of the work so it's perfect|city,luxury,culture|Control freak. I respect it.|I make the PPT look pretty and do nothing|beach,relax,mild|Aesthetic over substance.|I am the one who brings the snacks|foodie,party,hot|True MVP.|I argue with everyone and take charge|adventure,mountains,cold|Dictator vibes.|I disappear completely and ghost the group|nature,budget,relax|Ghost mode.",
    "Expired milk strategy?|Throw it away. It's poison.|luxury,city,culture|Refined palate.|Smell test. If it doesn't burn, we go.|adventure,hot,party|Living dangerously!|Drink it to build immunity|nature,mountains,cold|Stomach of steel.|Force a friend to taste it first|beach,relax,mild|Evil genius.|Bake it into something|foodie,budget,romance|Terrifying resourceful.",
    "Dominant toxic trait?|I think I could win a fight with a bear|adventure,mountains,nature|Confidence or delusion?|I buy clothes for a fantasy self|luxury,romance,city|Imaginary gala incoming.|I ghost people because I was relaxing|relax,beach,cold|Pro chiller.|I turn every chat into a debate|culture,party,hot|You sound exhausting. Love it.|I can't eat without a specific YouTube vid|foodie,mild,budget|Digital diner.",
    "Response to 'We need to talk'?|Fake my death and move country|adventure,nature,budget|Reasonable reaction.|Reply 'Yes we do.' Turn the tables.|city,culture,cold|Checkmate.|Panic, sweat, and apologize|relax,beach,mild|Anxiety 1000.|Ignore and go to a club|party,hot,luxury|Denial is a gift.|Send a meme to defuse tension|foodie,romance,mountains|Funny defense.",
    "Preferred method of passive aggression?|'As per my last email...'|city,culture,luxury|Corporate savagery.|Leaving them on read for 48 hours|cold,relax,mountains|Ice cold.|Sighing loudly in the same room|party,beach,hot|Drama queen.|Baking a cake for everyone except them|foodie,romance,mild|Deliciously evil.|Moving their stuff slightly left|adventure,nature,budget|Mind games.",
    "Household appliance alter-ego?|Blender on highest setting|party,hot,adventure|Chaotic energy.|High-end espresso machine|city,luxury,culture|Expensive and demanding.|Slow cooker|relax,mild,foodie|Low and slow.|Reliable space heater|cold,romance,relax|Cozy vibes.|Rugged outdoor grill|nature,beach,mountains|Outdoor soot.",
    "Secret superpower?|Hitting zero on the microwave exactly|city,budget,relax|Master of time.|Never getting mosquito bites|nature,adventure,hot|The jungle king.|Finding pizza at 3 AM|foodie,party,city|The hero we need.|Looking perfectly windswept|luxury,romance,beach|Main character.|Making stray animals love me|nature,culture,mild|Snow White vibes.",
    "Stranded on an island priority?|Making a coconut cocktail|party,beach,hot|Priorities set to vibe.|Building a 5-story bamboo treehouse|city,luxury,culture|Architectural marvel.|Befriending a volleyball|relax,mild,romance|Wilson!|Hunting with a pointy stick|adventure,nature,mountains|Primal instincts.|Tasting the local bugs|foodie,budget,cold|Culinary explorer.",
    "Reality TV crush?|Survivor. I am ruthless.|adventure,nature,mountains|Outplay everyone.|Love Island. Drama time.|party,beach,hot|I've got a text!|MasterChef. Ramsay fears me.|foodie,culture,mild|Yes, chef!|Real Housewives wardrobe.|luxury,city,romance|Table flipping imminent.|Alone. Leave me in the woods.|cold,budget,relax|Pure hermit.",
    "WiFi down reaction?|Panic. Cry. Refresh. Repeat.|city,luxury,party|Withdrawal starting.|Physical book like a peasant|culture,mild,romance|Old paper smell.|Go outside and touch grass|nature,mountains,adventure|What are the graphics like?|Take a long nap|relax,beach,cold|Rebooting system.|Cook a 5-course meal|foodie,hot,budget|Hiding the tears.",
    "Heist movie role?|Mastermind in tailored suit|luxury,city,culture|Sharp criminal.|Chaotic explosives expert|adventure,party,hot|Boom!|Getaway driver eating a sandwich|foodie,budget,beach|Snacks are essential.|Acrobat dodging lasers|mountains,nature,mild|Stressed gymnast.|The decoy distraction|romance,relax,cold|Drama queen.",
    "Ideal sandwich architecture?|Meat, cheese, bread. Purist.|mountains,budget,cold|Purist.|14 ingredients. Jaw dislocation.|foodie,adventure,party|Delicious mess.|Avocado and sourdough|culture,mild,city|Trendy and pricey.|Just a hot dog.|beach,hot,nature|Controversial.|Truffle mayo and gold leaf|luxury,romance,relax|Bougie bread.",
    "Packing style?|10 mins before flight|adventure,party,hot|Extreme living.|Vacuum-sealed and color-coded|city,culture,luxury|Impressively scary.|One toothbrush, buy the rest|budget,beach,nature|Minimalist nomad.|14 outfits for 3 days|romance,relax,mild|Gala ready.|Force someone else to do it|cold,mountains,foodie|Master delegator.",
    "Finding $100 reaction?|Shots for the bar!|party,city,hot|Bar legend.|Invest it immediately|culture,mild,luxury|Responsible boring.|Most expensive steak in town|foodie,romance,relax|Treat yo' self!|Stash it in the mattress|budget,mountains,cold|Paranoia pays.|Buy a weird sword online|adventure,nature,beach|Why not?",
    "Haunting style?|Moving keys slightly|city,culture,budget|Mind games.|Slamming doors and screaming|party,hot,adventure|Classic poltergeist.|Romantic poems in steam|romance,relax,mild|Affectionate ghost.|Ruin the electric bill|cold,nature,mountains|Financial ruin ghost.|Eating the fridge snacks|foodie,beach,luxury|Hungry spirit.",
    "Spirit emoji?|Upside down smile|city,party,hot|Smiling through pain.|Sparkles|luxury,romance,mild|Shiny.|Sobbing face|culture,relax,cold|Emotional.|Monkey covering eyes|beach,nature,budget|I do not see it.|Fire|adventure,mountains,foodie|Hype beast.",
    "Zombie strategy?|Lifetime supply of beans|budget,relax,cold|Gassy survival.|Katana and go down swinging|adventure,hot,mountains|Main character.|Pretend to be a zombie|culture,city,mild|Modern solutions.|Deserted island|beach,nature,romance|Can they swim?|Gourmet meal negotiation|foodie,luxury,party|Snack diplomat.",
    "Master one useless skill?|Juggling chainsaws|adventure,party,hot|Unnecessary.|Dog mind reading|nature,culture,relax|'Sausage now.'|Always plugging USB in right|city,mild,luxury|Literal god.|Replicate bird calls|mountains,budget,cold|Annoying/impressive.|Guess meal ingredients|foodie,romance,beach|Ratatouille.",
    "Surprise party reaction?|Center of the universe!|party,luxury,city|Attention seeker!|Panic and flee|mountains,nature,cold|Too many people.|Act surprised, I knew weeks ago|culture,mild,relax|Calculating.|Start eating the cake|foodie,budget,hot|Cake first.|I cry|romance,beach,adventure|Joy tears.",
    "Retirement plan?|Remote cabin with 12 dogs|nature,mountains,cold|Hermit activated.|Martinis on a yacht|luxury,beach,hot|High life.|Bakery in a village|foodie,romance,mild|Carb loading.|Argue on the internet|city,culture,budget|Keyboard warrior.|Eccentric art collector|party,adventure,relax|Avant-garde.",
    "Dragon defeat method?|Dance battle|party,hot,city|Serve the dragon!|Spicy taco|foodie,adventure,culture|Heartburn win.|Seduce the dragon|romance,luxury,beach|Bard style.|Poke it with a stick|budget,mountains,nature|Safety first.|Politely ask it to leave|mild,relax,cold|Manners cost nothing.",
    "What's in your pockets?|Lint and a receipt|budget,nature,relax|Broke traveler.|Fancy metal card|luxury,city,romance|Heavy wallet.|Four lip balms|mild,cold,beach|Hydrated.|Knife and string|adventure,mountains,hot|Survivalist.|Snacks. Always.|foodie,party,culture|Ready to eat.",
    "Traffic jam behavior?|Concert for the next car|party,hot,city|Entertainment.|Scream into void|adventure,mountains,budget|Let it out.|4-hour Roman history podcast|culture,mild,relax|Learning time.|Eat car snacks|foodie,nature,beach|Desperate times.|Driver handles it while I sleep|luxury,romance,cold|Must be nice.",
    "Pizza topping?|Truffle and mushroom|luxury,culture,city|Fancy fungus.|Shameful pepperoni amount|party,hot,foodie|Greasy classic.|Pineapple.|adventure,beach,mild|Controversial.|Whatever veggies|nature,relax,mountains|Healthy??|Plain cheese 5-year-old|budget,cold,romance|Purist.",
    "Magical wardrobe?|Perfect tailored suit|luxury,city,romance|Sharp.|Endless sweatpants|relax,budget,mild|Comfort king.|Impenetrable armor|adventure,mountains,cold|Battle ready.|Glowing party outfits|party,hot,beach|Rave ready.|Smells like fresh bread|foodie,nature,culture|Edible closet.",
    "Texting style?|One massive paragraph|culture,mild,mountains|Wall of text.|15 messages in a row|party,hot,city|Ding ding ding.|Just 'K.'|cold,budget,relax|Brutal.|Emojis and GIFs only|adventure,beach,nature|Hieroglyphics.|I call.|luxury,romance,foodie|Old school.",
    "Haunted house reaction?|Punch the first ghost|adventure,hot,party|Fight or fight!|Human shield for friends|relax,romance,beach|Protective cry.|Critique special effects|culture,city,mild|'Bad makeup.'|Befriend the demons|nature,mountains,cold|Hug them.|Eat the props|foodie,budget,luxury|Fake eyeballs.",
    "Alien abduction response?|Take me, Earth is ghetto!|adventure,party,nature|Beam me up.|Sell them a timeshare|city,luxury,budget|Hustler.|Space-recipes ask|foodie,culture,mild|Galactic Ramsay.|I have a boyfriend|romance,relax,beach|Rejection.|Scream and throw rocks|hot,mountains,cold|Primal.",
    "Lottery win?|Private island, ban everyone|nature,beach,relax|Zen.|Week-long festival|party,hot,city|Legendary hangover.|Solid gold toilet|luxury,romance,culture|Why not?|Invest in cheese vault|foodie,mountains,mild|Gouda investment.|Lose it in Vegas|adventure,budget,cold|Easy come easy go.",
    "Potato favorite?|Mashed with obscene butter|foodie,relax,romance|Comfort.|Cheese tater tots|party,hot,budget|Drunk food.|Roasted herb potato|culture,mild,luxury|Refined.|Raw potato. Feral.|adventure,nature,mountains|Cook it!|French fries on beach|beach,city,cold|Seagull food.",
    "Unpopular opinion?|Water isn't wet|culture,city,mild|Philosophy.|Pizza is better cold|foodie,budget,relax|Leftover king.|Sleep is a waste|party,hot,adventure|Crash incoming.|Outdoors is overrated|luxury,romance,cold|AC please.|Sand is the worst|mountains,nature,beach|Anakin vibes.",
    "Dance move?|Awkward two-step|mild,relax,budget|Safe.|Drop to floor|party,hot,beach|Knees of steel.|Dad-shuffle|culture,nature,mountains|Classic.|Nod with a drink|city,luxury,cold|Too cool.|Interpretive flailing|adventure,foodie,romance|Danger zone.",
    "Karaoke song?|Tequila.|budget,relax,party|Maximum impact.|Emo anthem|hot,city,adventure|MCR forever.|Whitney ballad I can't hit|romance,luxury,beach|Confidence.|I rap.|culture,mild,nature|Eminem fears you.|Duet both parts|foodie,mountains,cold|Main character.",
    "How to handle inconvenience?|Meditation|relax,mild,nature|Zen.|Vocal complaining|city,hot,culture|Let them know.|Bottle it up for 3 years|cold,mountains,budget|Healthy.|Throw money at it|luxury,romance,party|Must be nice.|Eat feelings|foodie,beach,adventure|Ice cream fix.",
    "Useless superpower?|Invisible when no one looks|budget,relax,culture|Hiding.|Summon a grape|foodie,nature,mild|Nutritious.|Make anyone sneeze|party,hot,adventure|Disruption.|Dry wet socks instantly|cold,mountains,beach|Top tier power.|Make things slightly pricier|luxury,city,romance|Evil.",
    "Minor chaos preference?|6 people cooking|foodie,party,hot|Too many cooks.|Group chat dinner plans|city,mild,culture|'You pick.'|Loose dog in park|nature,beach,adventure|Fenton!|Assemble tent in dark|mountains,budget,cold|Friendship test.|Reality TV reunion|luxury,romance,relax|Screaming."
]

parsed_dynamic_qs = []
for q_str in raw_qs:
    pts = q_str.split("|")
    q_dict = {"q": pts[0], "opts": {}}
    for i in range(1, 16, 3):
        if i+2 < len(pts):
            q_dict["opts"][pts[i]] = {"tags": pts[i+1].split(","), "cheeky": pts[i+2]}
    parsed_dynamic_qs.append(q_dict)

# ---------------------------------------------------------
# 4. LOGIC ENGINE
# ---------------------------------------------------------
opposites = {"hot": "cold", "cold": "hot", "city": "nature", "nature": "city", "beach": "mountains", "mountains": "beach", "adventure": "relax", "relax": "adventure", "luxury": "budget", "budget": "luxury", "party": "relax"}

if 'stage' not in st.session_state:
    st.session_state.stage = 'welcome'
    st.session_state.q_index = 0
    st.session_state.user_tags = Counter()
    st.session_state.available_dests = list(dests.keys())
    st.session_state.chosen_dest = None
    st.session_state.activities = []
    st.session_state.activity_round = 0
    st.session_state.last_cheeky = ""
    st.session_state.unused_qs = list(parsed_dynamic_qs)
    random.shuffle(st.session_state.unused_qs)
    st.session_state.current_q = None

def get_top_dests(n=10):
    scored = []
    for d in st.session_state.available_dests:
        dtags = dests[d]["t"]
        score = sum(st.session_state.user_tags[t] for t in dtags if t in st.session_state.user_tags)
        norm = (score / len(dtags)) + random.uniform(0, 0.05)
        scored.append((norm, d))
    scored.sort(key=lambda x: x[0], reverse=True)
    return [x[1] for x in scored[:n]]

def get_next_question():
    if st.session_state.q_index < 3: return static_qs[st.session_state.q_index]
    if not st.session_state.unused_qs: return None
    top_dests = get_top_dests(10)
    active_tags = {tag for d in top_dests for tag in dests[d]['t']}
    for i, q in enumerate(st.session_state.unused_qs):
        q_tags = {tag for opt in q['opts'].values() for tag in opt['tags']}
        if q_tags.intersection(active_tags): return st.session_state.unused_qs.pop(i)
    return st.session_state.unused_qs.pop(0)

def handle_answer(selected):
    w = st.session_state.current_q["opts"][selected]["tags"]
    for t in w:
        st.session_state.user_tags[t] += 2
        if t in opposites: st.session_state.user_tags[opposites[t]] -= 2
    st.session_state.last_cheeky = st.session_state.current_q["opts"][selected]["cheeky"]
    st.session_state.q_index += 1
    if st.session_state.q_index == 10: st.session_state.stage = 'stick_or_risk'
    elif st.session_state.q_index >= 20 or not st.session_state.unused_qs:
        st.session_state.chosen_dest = get_top_dests(1)[0]
        st.session_state.stage = 'final_match_reveal'
    else: st.session_state.current_q = get_next_question()

# ---------------------------------------------------------
# 5. UI
# ---------------------------------------------------------
if st.session_state.stage == 'welcome':
    set_bg("#1E1E1E", "#00FF7F")
    st.markdown("<br><div class='giant-emoji'>✈️🌍✨</div><h1 style='text-align:center;'>The Perfect Holiday Finder</h1>", unsafe_allow_html=True)
    st.markdown("<div style='background:rgba(255,255,255,0.1);padding:30px;border-radius:20px;text-align:center;'><h3>How it works:</h3><p>1. Answer personality questions.<br>2. Dynamic Vibe Engine searches 100 Viral destinations.<br>3. Stick or Risk at the halfway point.<br>4. Pick your 6-part atmospheric itinerary!</p></div>", unsafe_allow_html=True)
    if st.button("START THE ENGINE! 🚀"):
        st.session_state.current_q = get_next_question()
        st.session_state.stage = 'questions'
        st.rerun()

elif st.session_state.stage == 'questions':
    set_bg("#2C3E50", "#FFFFFF")
    if st.session_state.last_cheeky: st.markdown(f"<div class='cheeky-text'>💬 \"{st.session_state.last_cheeky}\"</div>", unsafe_allow_html=True)
    st.markdown(f"<h1 style='text-align:center;'>Question {st.session_state.q_index+1}: {st.session_state.current_q['q']}</h1>", unsafe_allow_html=True)
    choice = st.radio("👇 Click your vibe:", list(st.session_state.current_q["opts"].keys()))
    if st.button("LOCK IT IN! 🔒➡️"):
        handle_answer(choice)
        st.rerun()

elif st.session_state.stage == 'stick_or_risk':
    best = get_top_dests(1)[0]
    set_bg(dests[best]["c"], "#FFFFFF")
    st.markdown("<h1 style='text-align:center;'>🚨 HALFWAY POINT! 🚨</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.2])
    with c1: safe_image(dests[best]["p"])
    with c2:
        st.markdown(f"<h2>Matching with: <u style='font-size:60px;'>{best}</u></h2><p style='font-size:25px;'>Imagine: {random.choice(dests[best]['e'])}</p><h3>STICK or RISK?</h3><p>(Risking bins this place forever!)</p>", unsafe_allow_html=True)
        if st.button("😍 STICK!"):
            st.session_state.chosen_dest = best
            st.session_state.stage = 'activity_selection'
            st.rerun()
        if st.button("🎲 RISK!"):
            st.session_state.available_dests.remove(best)
            st.session_state.current_q = get_next_question()
            st.session_state.stage = 'questions'
            st.rerun()

elif st.session_state.stage == 'final_match_reveal':
    best = st.session_state.chosen_dest
    set_bg(dests[best]["c"], "#FFFFFF")
    if "cold" in dests[best]["t"]: st.snow()
    else: st.balloons()
    st.markdown("<h1 style='text-align:center;'>🎉 WE FOUND A MATCH! 🎉</h1>", unsafe_allow_html=True)
    safe_image(dests[best]["p"])
    st.markdown(f"<h1 style='text-align:center;font-size:100px;'>{best}!</h1>", unsafe_allow_html=True)
    if st.button("PICK MY ACTIVITIES! ➡️"):
        st.session_state.stage = 'activity_selection'
        st.rerun()

elif st.session_state.stage == 'activity_selection':
    best = st.session_state.chosen_dest
    set_bg(dests[best]["c"], "#FFFFFF")
    rnd = st.session_state.activity_round
    if rnd==0: title, a1, a2 = "🍽️ Food", dests[best]["f"][0], dests[best]["f"][1]
    elif rnd==1: title, a1, a2 = "🍸 Drinks", dests[best]["d"][0], dests[best]["d"][1]
    elif rnd==2: title, a1, a2 = "📸 Cute", dests[best]["cu"][0], dests[best]["cu"][1]
    elif rnd==3: title, a1, a2 = "🔥 Epic 1", dests[best]["e"][0], dests[best]["e"][1]
    elif rnd==4: title, a1, a2 = "🔥 Epic 2", dests[best]["e"][2], dests[best]["e"][3]
    else: title, a1, a2 = "🔥 Epic 3", dests[best]["e"][4], dests[best]["e"][5]
    st.markdown(f"<h1 style='text-align:center;'>{title} (Choice {rnd+1}/6)</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"<div style='background:rgba(0,0,0,0.5);padding:40px;border-radius:20px;height:220px;'><h2>{a1}</h2></div>", unsafe_allow_html=True)
        if st.button("✅ KEEP THIS", key=f"k1_{rnd}"):
            st.session_state.activities.append(a1); st.session_state.activity_round += 1
            if st.session_state.activity_round >= 6: st.session_state.stage = 'final_itinerary'
            st.rerun()
    with c2:
        st.markdown(f"<div style='background:rgba(0,0,0,0.5);padding:40px;border-radius:20px;height:220px;'><h2>{a2}</h2></div>", unsafe_allow_html=True)
        if st.button("✅ KEEP THIS", key=f"k2_{rnd}"):
            st.session_state.activities.append(a2); st.session_state.activity_round += 1
            if st.session_state.activity_round >= 6: st.session_state.stage = 'final_itinerary'
            st.rerun()

elif st.session_state.stage == 'final_itinerary':
    best = st.session_state.chosen_dest
    set_bg(dests[best]["c"], "#FFFFFF")
    st.markdown("<h1 style='text-align:center;'>🎊 PACK YOUR BAGS! 🎊</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1.5])
    with c1: safe_image(dests[best]["p"])
    with c2:
        st.markdown(f"<h2>📍 {best}</h2><h3>Your Itinerary:</h3>", unsafe_allow_html=True)
        for act in st.session_state.activities: st.markdown(f"<div style='background:rgba(255,255,255,0.2);padding:15px;margin-bottom:10px;border-radius:10px;'>🌟 {act}</div>", unsafe_allow_html=True)
    st.markdown("<br><hr>", unsafe_allow_html=True)
    if st.button("CLICK FOR SURPRISE... 👀"):
        st.session_state.stage = 'twist'
        st.rerun()

elif st.session_state.stage == 'twist':
    set_bg("#000000", "#FFFFFF")
    st.markdown("<div class='beating-heart'>❤️</div><h1 style='text-align:center;'>Do you love Damien?</h1>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("YES"):
        st.session_state.ans = 'yes'; st.session_state.stage = 'res'
        st.rerun()
    if c2.button("NO"):
        st.session_state.ans = 'no'; st.session_state.stage = 'res'
        st.rerun()

elif st.session_state.stage == 'res':
    set_bg("#000000", "#FFFFFF")
    st.markdown("<div class='giant-emoji'>❤️</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align:center;color:#FF1493 !important;'>I love you too Katie bear 🐻</h1>", unsafe_allow_html=True)
    if st.session_state.ans == 'no': st.markdown("<h2 style='text-align:center;'>...but enjoy your holiday on your own 😜</h2>", unsafe_allow_html=True)
    else: st.balloons()
