import streamlit as st
import random
import urllib.parse
from collections import Counter

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


raw_dests = [
    # ASIA (25)
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
    "Singapore|hot,city,luxury,foodie|#8B008B|singapore marina bay sands supertrees|Eat $300 Chili Crab at a luxury seafood house|Eat 3 Michelin-star Chicken Rice at a hawker centre|Drink the original Singapore Sling at the Raffles Hotel|Craft cocktails in a hidden speakeasy|Walk through the glowing Supertree Grove|Explore the indoor waterfall at the Jewel airport|Swim in the Marina Bay Sands infinity pool 57th floor|Take a night safari to see nocturnal predators|Shop in insanely massive luxury mega-malls|Ride the Singapore Flyer observation wheel|Bungee jump on Sentosa Island|Watch the Formula 1 Night Race",
    "Hanoi (Vietnam)|hot,city,culture,foodie,budget|#556B2F|hanoi vietnam busy streets motorbikes|Gourmet French-Vietnamese fusion|Eat $1 Pho sitting on a tiny plastic stool|Drink viral Egg coffee in a hidden narrow cafe|Drink Bia Hoi fresh beer for 20 cents|Dodge thousands of motorbikes to cross the street|Watch a traditional Water Puppet show|Take a luxury overnight junk boat cruise in Ha Long Bay|Trek the terraced rice fields of Sapa|Crawling through the Cu Chi tunnels|Take a sleeper train down the coast|Eat Banh Mi from a street cart|Explore the massive ancient cave of Son Doong",
    "Ha Long Bay (Vietnam)|hot,nature,relax,romance|#20B2AA|ha long bay vietnam limestone boats|Gourmet seafood on a luxury wooden junk boat|Eat fresh spring rolls|Drink cocktails on the top deck at sunset|Drink strong Vietnamese drip coffee|Take a bamboo rowboat through floating fishing villages|Explore the massive Sung Sot cave|Kayak silently through the towering limestone karsts|Take a seaplane flight over the emerald waters|Swim in isolated hidden coves|Take a Tai Chi class on the deck at dawn|Squid fishing at midnight|Hike to the top of Titop Island for a panoramic view",
    "Palawan (Philippines)|hot,beach,nature,adventure,budget|#00CED1|palawan philippines limestone lagoons|Fresh lobster cooked on a remote island|Eat Adobo and Lechon roast pig|Rum cocktails out of a pineapple|Drink Red Horse beer by a beach bonfire|Take a tiny outrigger boat to a hidden lagoon|Find a totally deserted white sand beach|Paddle deep into the massive Underground River cave|Island hop through the breathtaking Bacuit Archipelago|Scuba dive WWII Japanese shipwrecks in Coron|Zipline between two islands over the ocean|Kayak through secret emerald lagoons|Camp on a deserted island like Survivor",
    "Siargao (Philippines)|hot,beach,adventure,party|#3CB371|siargao philippines surfing palm trees|Gourmet smoothie bowls at a trendy cafe|Eat fresh Kinilaw (Filipino ceviche)|Drink cheap rum at a massive jungle party|Drink fresh coconut water|Swing from a rope into the Maasin River|Drive a scooter through thousands of palm trees|Surf the legendary Cloud 9 barrel waves|Island hop to Naked Island (just a sandbar)|Explore the glowing Sugba Lagoon|Party all night at the viral General Luna clubs|Wakeboard across the pristine ocean|Cliff jump into the Magpupungko rock pools",
    "Taipei (Taiwan)|mild,city,foodie,culture|#D2691E|taipei taiwan night market 101 tower|Soup dumplings at the original Din Tai Fung|Eat Stinky Tofu at a chaotic night market|High mountain Oolong tea ceremony|Drink absurdly sugary Boba Bubble Tea|Release a glowing paper lantern in Shifen|Ride the Maokong glass-bottom gondola|Take the ultra-fast elevator up Taipei 101|Soak in the Beitou thermal hot springs|Hike Elephant Mountain for the perfect city view|Explore the stunning Taroko Gorge marble canyons|Eat literally everything at Shilin Night Market|Scooter road trip along the dramatic east coast",
    "Luang Prabang (Laos)|hot,culture,nature,relax|#8B4513|luang prabang laos monks temples waterfalls|Luxury French-Lao fusion dining|Eat spicy Laap and sticky rice|Drink Beerlao by the Mekong river|Drink fresh sugar cane juice|Give alms to the hundreds of monks at dawn|Shop the vibrant night market|Swim in the spectacular multi-tiered Kuang Si Falls|Take a slow boat down the Mekong River|Explore the Pak Ou caves filled with Buddha statues|Take an organic rice farming masterclass|Bathe elephants in the river|Get a traditional Lao herbal sauna and massage",
    "Jaipur (India)|hot,city,culture,romance|#FF4500|jaipur india pink city palaces desert|Royal Rajasthani Thali in a converted palace|Eat ultra-spicy Laal Maas curry|Cocktails on a palace rooftop|Drink fresh Lassi from a clay pot|Explore the insanely intricate Hawa Mahal Palace of Winds|Get a traditional Henna tattoo|Take a hot air balloon over the desert forts|Ride a jeep up to the massive Amber Fort|Sleep like royalty in an actual Maharaja's palace|Spot wild Bengal Tigers in Ranthambore on safari|Shop for precious gems and textiles|Watch a snake charmer in the street markets",
    "Maldives|hot,beach,relax,luxury,romance|#00CED1|maldives overwater bungalow crystal ocean|Dine in an all-glass underwater restaurant|Have a private beach BBQ cooked by a personal chef|Champagne delivered to your pool via floating tray|Drink coconut cocktails on a deserted sandbank|Slide directly from your overwater bungalow into the ocean|Night swim with glowing bioluminescent plankton|Take a private seaplane over the gorgeous atolls|Scuba dive with massive gentle Manta Rays|Go deep sea fishing for Yellowfin Tuna|Take a submarine tour of the vibrant coral reefs|Couples spa day on a glass floor over the ocean|Watch an outdoor movie at a jungle cinema",

    # AMERICAS (25)
    "New York City (USA)|mild,cold,city,foodie,luxury,culture|#4682B4|new york city times square skyline|Eat the viral Suprême croissant at Lafayette|Eat a massive greasy $2 slice of NY pizza|Martinis in a high-end hidden speakeasy|Drink cheap beers at a gritty Brooklyn dive bar|Take mind-bending photos in the SUMMIT One Vanderbilt|Ice skate in Central Park|Take a helicopter doors-off tour over Manhattan|Watch a smash-hit Broadway musical from VIP seats|Attend a crazy underground warehouse party in Brooklyn|Go on a massive shopping spree on 5th Avenue|Eat a massive pastrami sandwich at Katz's Deli|Walk the High Line elevated park at sunset",
    "Los Angeles (USA)|hot,city,beach,party,luxury|#FF1493|los angeles hollywood palm trees sunset|Eat at the viral Erewhon bakery|Eat tacos from a street truck at 2 AM|Drink insanely expensive green juice|Drink cocktails on a West Hollywood rooftop|Hike to the Hollywood sign|Rollerblade down Venice Beach|Take a VIP studio backlot tour|Surf the waves in Malibu|Drive a convertible down the Pacific Coast Highway|Party with celebrities in Beverly Hills|Shop on Rodeo Drive|Take a helicopter tour over the mansions",
    "San Francisco (USA)|mild,city,foodie,culture,adventure|#1E90FF|san francisco golden gate bridge cable car|10-course Michelin star tasting menu in Soma|Eat Clam Chowder out of a massive sourdough bowl|Wine tasting trip to Napa Valley via private limo|Drink Irish Coffees at the Buena Vista|Hang off the side of a moving Cable Car|Have a picnic at the Painted Ladies|Take a terrifying midnight Alcatraz ghost tour|Bike across the Golden Gate Bridge|Skydive directly over the Bay|Hike among massive Redwoods in Muir Woods|Eat giant burritos in the Mission District|Sail a catamaran under the Golden Gate Bridge",
    "Miami (USA)|hot,beach,party,luxury|#FF1493|miami south beach neon palm trees|Luxury stone crab dining at Joe's|Eat authentic Cuban sandwiches in Little Havana|Champagne on a mega-yacht|Drink mojitos at a salsa club|Rollerblade down Ocean Drive in neon gear|Look at street art in Wynwood Walls|Party until 6 AM at a massive club like E11EVEN|Ride an airboat through the Everglades looking for alligators|Charter a private yacht to the Bahamas|Drive a neon Lamborghini down South Beach|Deep sea fishing for Marlin|Attend an exclusive Art Basel party",
    "Oahu (Hawaii)|hot,beach,city,adventure|#1E90FF|oahu hawaii waikiki beach surfing|Eat luxury Japanese fusion at Nobu|Eat fresh Poke bowls from a local grocery store|Drink Mai Tais at the Royal Hawaiian|Drink Kona brewing beer on the beach|Visit the historic Pearl Harbor memorial|Eat Dole Whip at the pineapple plantation|Surf massive winter waves on the North Shore|Hike the terrifying Haiku Stairs (Stairway to Heaven)|Shark cage diving in the open ocean|Helicopter tours over the volcanic craters|Attend a massive traditional Luau fire show|Skydive over the crystal clear ocean",
    "Kauai (Hawaii)|hot,nature,adventure,relax|#006400|kauai hawaii napali coast cliffs|Luxury oceanfront dining|Eat massive colorful Shave Ice|Drink tropical cocktails out of a pineapple|Drink local Hawaiian coffee|Hike the breathtaking Waimea Canyon|Take a doors-off Helicopter over Jurassic Park falls|Sail a catamaran along the dramatic Na Pali coast|Kayak the Wailua River to hidden waterfalls|Zipline over the lush valleys|Surf the warm waves|Scuba dive with sea turtles|Off-roading in a 4x4 through the mud",
    "Yellowstone (USA)|cold,mild,nature,adventure|#A0522D|yellowstone geyser bison nature|Gourmet game meat at a luxury lodge|Eat campfire chili out of a tin can|Craft beer tasting in a cowboy saloon|Drink cowboy coffee boiled over a fire|Watch Old Faithful erupt on schedule|Spot adorable bear cubs through binoculars|Snowmobile through the park in dead of winter|Spot packs of wild wolves in the Lamar Valley|Hike around the neon-colored Grand Prismatic Spring|Camp deep in grizzly bear country|Fly fish in freezing crystal-clear rivers|Whitewater raft down the Snake River",
    "Banff (Canada)|cold,mountains,nature,adventure|#2F4F4F|banff canada lake louise mountains snow|Fine dining at the Fairmont Chateau Lake Louise|Eat massive plates of Canadian Poutine|Drink ice wine from the local vineyards|Sip hot chocolate while ice skating|Rent a clear glass canoe on the turquoise Lake Louise|Soak in the Banff Upper Hot Springs|Take a helicopter tour over the massive Canadian Rockies|Hike to the spectacular Plain of Six Glaciers|Ski world-class powder at Sunshine Village|Ice climb up a frozen waterfall in Johnston Canyon|Spot massive wild Grizzly Bears|Take the steep gondola up Sulphur Mountain",
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

    # EUROPE (25)
    "Paris (France)|mild,city,culture,foodie,luxury,romance|#C71585|paris eiffel tower sunset romance|Wait in line for Cedric Grolet’s viral fruit illusion pastries|Eat the famous hot chocolate and mont blanc at Angelina|Champagne at the very top of the Eiffel Tower|Drink inside a secret speakeasy behind a washing machine|Take photos in a vintage Fotoautomat booth in Montmartre|Have a chic picnic at Place Vosges|Take a Dior Spa cruise down the Seine River|VIP skip-the-line night tour of the Louvre|Explore the underground bone Catacombs|Dine on the glass-roofed Bustronome double-decker bus|Take a croissant-making masterclass|Attend a cabaret show at the Moulin Rouge",
    "Rome (Italy)|mild,hot,city,culture,foodie|#A0522D|rome colosseum ancient sunset|Build your own custom Tiramisu at the viral Pompi|Massive slice of Roman pizza al taglio|Vintage Barolo wine tasting in an ancient cellar|Drink an Aperol Spritz overlooking Piazza Navona|Throw a coin in the Trevi Fountain at midnight|Eat gelato on the Spanish Steps|Take a pasta making class at a viral Frascati farmhouse|Attend a Gladiator training school on the Appian Way|Take a private after-hours tour of the Sistine Chapel|Ride a Vespa through the chaotic Roman traffic|Explore the ancient crypts made entirely of human bones|Helicopter tour over the ancient ruins",
    "Amalfi Coast (Italy)|hot,beach,foodie,luxury,romance|#FF8C00|amalfi coast cliffside colorful houses|Eat lemon sorbet served inside a massive hollowed-out lemon|Eat lunch at the viral La Tagliata overlooking the cliffs|Limoncello tasting straight from a lemon farm|Drink Prosecco on a private vintage wooden boat|Shop for handmade leather sandals in Positano|Take a vintage Vespa tour along the coastal roads|Swim into the sparkling Blue Grotto sea cave|Take a helicopter tour of Mount Vesuvius|Hike the breathtaking Path of the Gods|Take a private cooking class in a cliffside villa|Charter a luxury yacht to the island of Capri|Jump off the cliffs into the Mediterranean",
    "Venice (Italy)|mild,city,romance,culture|#008080|venice canals gondola sunset romance|Romantic seafood dinner on a floating terrace|Venetian tapas in a crowded local bacaro|Bellinis at the famous Harry's Bar|Spritz in St. Mark's Square listening to the orchestra|Get lost in the tiny alleyways|Watch a glassblower in Murano|Private sunset Gondola ride with a serenader|Attend a masquerade ball in a grand palazzo|Kayak through the quiet hidden canals|VIP tour of the Doge's Palace secret passages|Take a water taxi across the lagoon at high speed|Make your own authentic Carnival mask",
    "Cinque Terre (Italy)|mild,hot,beach,culture|#DC143C|cinque terre italy colorful houses cliff|Eat authentic pesto pasta invented right here|Eat fried seafood out of a paper cone|Taste Sciacchetrà sweet wine|Drink Aperol Spritz on a cliffside terrace|Take the scenic train between the 5 colorful villages|Hike the coastal trails with insane ocean views|Charter a private boat to sail past the colorful cliffs|Cliff jump into the Mediterranean Sea|Take a pesto-making masterclass|Scuba dive in the protected marine park|Watch the sunset from the viral Nessun Dorma restaurant|Explore the terraced vineyards on the cliffs",
    "Swiss Alps (Switzerland)|cold,mountains,adventure,luxury,nature|#8B0000|swiss alps matterhorn snow cabin|Eat fondue inside a literal igloo|Eat at the viral Aescher cliff restaurant built into the rock|Drink Dom Pérignon in an outdoor heated jacuzzi|Drink hot spiced Glühwein by a roaring fire|Build a snowman overlooking the Matterhorn|Ride a horse-drawn sleigh through the village|Ride the Gelmerbahn Europe's steepest open-air funicular|Helicopter drop-off for extreme off-piste skiing|Paraglide over the snowy peaks|Ice climb up a frozen waterfall|Ride the panoramic Glacier Express train|Bungee jump off a dam like James Bond",
    "Hallstatt (Austria)|cold,mountains,nature,romance|#4682B4|hallstatt austria lake mountains fairytale|Eat gourmet Austrian Schnitzel|Eat fresh lake trout|Drink local Austrian beer|Drink hot cocoa overlooking the fairytale lake|Rent a swan boat on the crystal clear water|Wander the perfectly preserved alpine village|Take the funicular up to the ancient salt mines|Walk out onto the terrifying Skywalk viewing platform|Explore the eerie Dachstein Giant Ice Cave|Hike the dramatic Dachstein mountain range|Take a helicopter tour over the Austrian Alps|Visit the incredibly creepy Bone House (Beinhaus)",
    "Vienna (Austria)|mild,city,culture,romance|#FFD700|vienna austria palaces music|Gourmet Wiener Schnitzel|Eat a slice of the famous Sachertorte|Sip elegant Viennese coffee in a grand cafe|Drink local Gruner Veltliner wine in a vineyard|Watch the Lipizzaner dancing horses|Ride the giant historic Ferris wheel|Attend a grand ball in a tuxedo/gown|Listen to Mozart performed in a golden hall|Tour the massive Schönbrunn Palace|Visit the creepy catacombs of St. Stephen's|Take a horse-drawn fiaker ride at night|Sail the Danube river",
    "London (UK)|mild,cold,city,culture,party|#191970|london big ben red bus thames|Eat afternoon tea at Sketch (viral pink room)|Eat in the Coppa Club glass igloos overlooking Tower Bridge|Drink cocktails at the eccentric Alchemist bar|Drink pints of ale in a 400-year-old tavern|Feed the pelicans in St. James's Park|Browse quirky antiques at Portobello Road|VIP pod on the London Eye with champagne|Take a terrifying Jack the Ripper night walking tour|Climb completely over the top of the O2 Arena|Attend a smash-hit West End theatre premiere|Speedboat down the River Thames at 40mph|Tour the hidden underground Churchill War Rooms",
    "Scottish Highlands (UK)|cold,mild,mountains,nature,adventure|#2E8B57|scottish highlands castle loch fog mountains|Gourmet venison at a luxury castle|Eat traditional Haggis Neeps and Tatties|Taste 50-year-old single malt Scotch whisky|Drink pints of heavy ale in a 16th-century inn|Spot highland cows (hairy coos)|Search the loch for the Loch Ness Monster|Sleep in a massive historic haunted castle|Ride the real Hogwarts Express steam train|Hike the dramatic ridges of Glencoe|Sea kayak with wild seals|Off-road in a Land Rover through the mud|Learn archery and falconry on a noble estate",
    "Barcelona (Spain)|hot,city,beach,party,culture|#DC143C|barcelona sagrada familia colorful gaudi|Eat Avant-garde molecular gastronomy|Eat endless massive pans of seafood Paella|Sangria tasting on a luxury rooftop|Cava in a historic underground cellar|Find the hidden mosaics in Park Güell|Watch street performers on La Rambla|Sail a catamaran on the Mediterranean at sunset|VIP tour of the unfinished Sagrada Familia|Attend a live passionate Flamenco show|Helicopter ride over the coastline|Dance until 6 AM at a massive beach club|Take a hot air balloon over Catalonia",
    "Ibiza (Spain)|hot,beach,party,luxury|#FF1493|ibiza beach party neon sunset ocean|VIP dining at a superclub|Eat fresh grilled octopus at a quiet hidden cove|Bottle service with sparklers at Pacha|Drink Hierbas liqueur at a bohemian beach shack|Shop at the hippie markets|Watch the sunset at Es Vedra with bongos|Dance until 8 AM with the world's biggest DJs|Charter a luxury yacht to Formentera|Cliff jump into the crystal clear Mediterranean|Parasail high above the party beaches|Explore hidden sea caves on a paddleboard|Attend an exclusive secret villa afterparty",
    "Seville (Spain)|hot,city,culture,romance|#FF8C00|seville spain moorish architecture orange trees|Gourmet Andalusian tapas|Eat Churros con Chocolate|Drink Sherry wine|Drink Tinto de Verano|Walk through the massive Plaza de España|Smell the orange trees in the courtyards|Explore the stunning Royal Alcázar palace|Watch a deeply passionate Flamenco performance in a tiny cave|Walk the wooden Metropol Parasol at sunset|Take a carriage ride through the old town|Attend the wild Feria de Abril festival|Take a boat cruise down the Guadalquivir river",
    "Amsterdam (Netherlands)|mild,city,culture,party|#FF4500|amsterdam canals bicycles sunset|Gourmet Dutch tasting menu in a greenhouse|Eat hot Stroopwafels fresh off the iron|Heineken VIP brewing experience|Jenever tasting in a dimly lit 17th-century tasting room|Browse the floating flower market|Have a picnic in Vondelpark|Rent a private canal boat with endless drinks|Cycle through the tulip fields of Keukenhof|Explore the secret annex of Anne Frank|Party at a massive underground techno warehouse|Tour the bizarre and wild Red Light District|Eat a massive wheel of authentic Gouda cheese",
    "Iceland|cold,nature,adventure,relax|#0B3D91|iceland northern lights glacier waterfalls|High-end Nordic tasting menu|Try fermented shark and a street hot dog|Brennivín shots in an ice bar|Blue lagoon cocktails floating in thermal water|Pet fluffy Icelandic horses|Search for hidden elf houses in the rocks|Explore deep inside a glittering blue Ice Cave|Snowmobile across a massive glacier|Chase the Northern Lights in a Super-Jeep|Snorkel between two tectonic plates in freezing water|Hike up to a live flowing volcano|Walk behind the roaring Seljalandsfoss waterfall",
    "Tromso (Norway)|cold,nature,adventure,mountains|#000033|tromso norway snowy fjords aurora|Arctic fine dining with king crab|Eat dried fish like a true Viking|Taste Aquavit in the world's northernmost brewery|Drink hot toddies on a silent electric whale watching boat|Sleep in a viral glass igloo under the Northern Lights|Warm up by a fire in a cozy candlelit cafe|Chase the Northern Lights in the arctic wilderness|Whale watch for massive Orcas in the fjords|Dog sled across the frozen tundra with Siberian Huskies|Snowshoe through silent snowy valleys|Feed reindeer with indigenous Sami people|Ride the Fjellheisen cable car for sunset views",
    "Svalbard (Norway)|cold,nature,adventure,mountains|#E0FFFF|svalbard polar bears arctic ice|Gourmet dining at the edge of the world|Eat freeze-dried expedition meals in a tent|Champagne tasting in a coal miner's cellar|Drink pure melted glacier water|Mail a letter from the world's northernmost post office|Spot arctic foxes playing in the snow|Armed expedition to safely spot wild Polar Bears|Explore the Global Seed Vault|Snowmobile to an abandoned Soviet ghost town|Ice cave inside a massive glacier|Kayak in freezing waters past walruses|Experience 24 hours of total darkness or sunlight",
    "Santorini (Greece)|hot,beach,relax,luxury,romance|#00008B|santorini white houses blue domes sunset|Private clifftop dining with fresh lobster|Eat a massive Gyros from a bustling local taverna|Wine tasting in a volcanic cave vineyard|Drink cocktails on a luxury catamaran at sunset|Do the viral Flying Dress photoshoot on the white roofs|Wander the white cobblestone streets of Oia|Sail a yacht to the volcanic hot springs|Scuba dive in the deep caldera|Take a helicopter ride over the Greek Islands|Rent ATVs to explore hidden black sand beaches|Explore the ancient ruins of Akrotiri|Jump off the cliffs at Amoudi Bay",
    "Mykonos (Greece)|hot,beach,party,luxury|#00BFFF|mykonos windmills party beach|Luxury seafood at Nammos|Eat Gyros on the street|Champagne bottle service at a beach club|Drink Ouzo shots|Take photos with the iconic windmills|Wander the alleys of Little Venice|Party until 8 AM at massive beach clubs|Charter a luxury yacht|Scuba dive the crystal clear reefs|Take a helicopter to Santorini|Windsurf the breezy ocean|Host a private villa party",
    "Dubrovnik (Croatia)|hot,beach,city,culture|#D2691E|dubrovnik croatia kings landing walls sea|Upscale Mediterranean dining on the cliffs|Eat black squid ink risotto in the old town|Cocktails at a bar literally clinging to the cliffside|Local Rakija shots with a fisherman|Find the Game of Thrones Walk of Shame steps|Pet the hundreds of street cats|Walk the massive ancient city walls at sunset|Sea kayak to the cursed island of Lokrum|Take a cable car up Mount Srd for insane views|Sail the Elaphiti Islands on a pirate ship|Cliff jump at Buza Bar|Zipline over the coastal mountains",
    "Plitvice Lakes (Croatia)|mild,nature,relax|#32CD32|plitvice lakes croatia waterfalls green clear|Gourmet Croatian forest dining|Eat fresh trout|Drink local Croatian wine|Drink cold Ozujsko beer|Walk the endless wooden boardwalks over the lakes|Take stunning photos of the massive waterfalls|Hike the extensive national park trails|Row a wooden boat across the pristine upper lakes|Take a panoramic train ride through the forest|Explore the hidden Barac Caves nearby|Rent bicycles to explore the surrounding villages|Zipline across the nearby Korana river canyon",
    "Prague (Czechia)|cold,mild,city,culture,party|#B22222|prague charles bridge castle sunset|Fine dining overlooking the Vltava river|Eat a massive roasted pork knuckle in a beer hall|Drink absurdly cheap world-class Pilsner|Absinthe tasting in a dark gothic basement|Watch the medieval Astronomical Clock chime|Walk the Charles Bridge at dawn|Take a ghost and legends night tour|Shoot AK-47s at an underground range|Bathe in a literal tub of dark beer at a Beer Spa|Cruise the river on a jazz boat|Attend a classical concert in a 14th-century church|Explore a nuclear bunker from the Cold War",
    "Budapest (Hungary)|cold,city,party,relax|#B22222|budapest parliament river baths|Gourmet Goulash at a high-end restaurant|Eat sweet Chimney cake on the street|Drink Palinka fruit brandy|Drink Unicum herbal liqueur|Soak in the massive outdoor Szechenyi Thermal Baths|Walk the iconic Chain Bridge|Party in the wild eclectic Ruin Pubs|Take a nighttime river cruise past the glowing Parliament|Explore the spooky Buda Castle labyrinth|Go caving under the city streets|Take a helicopter tour over the Danube|Do an intense Escape room",
    "Copenhagen (Denmark)|cold,city,foodie,culture|#4682B4|copenhagen nyhavn boats bikes|Eat at Noma (world's best restaurant)|Eat Smorrebrod open sandwiches|Drink Carlsberg beer at the brewery|Taste Aquavit|Ride the wooden rollercoasters at Tivoli Gardens|Walk the colorful Nyhavn harbor|Rent a boat and drive it through the canals yourself|Explore the hippie commune of Christiania|Cycle the entire city like a local|Bathe in the freezing harbor baths|Take a helicopter tour|Tour the massive Renaissance castles",
    "Lapland (Finland)|cold,nature,adventure,relax|#F0F8FF|lapland snow igloo northern lights reindeer|Luxury Arctic tasting menu|Hearty Reindeer stew cooked over a campfire|Cloudberry liquor in an ice glass|Hot cocoa while wrapped in reindeer hides|Meet the real Santa Claus|Feed wild gentle reindeer|Sleep in a viral glass igloo under the Northern Lights|Drive a team of huskies on a sled through the forest|Take an icebreaker cruise and swim in the freezing sea|Snowmobile across massive frozen lakes|Ice fishing and cook your catch|Get whipped with birch branches in a traditional sauna",

    # AFRICA & MIDDLE EAST (15)
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

    # OCEANIA (10)
    "Great Barrier Reef (Australia)|hot,beach,nature,adventure|#00CED1|great barrier reef coral ocean turtle|Luxury seafood buffet on a catamaran|Eat Barramundi fish and chips on the beach|Champagne on a remote sand cay|Drink Bundaberg Rum|Take a glass-bottom boat tour|Find Nemo in the sea anemones|Scuba dive the largest most vibrant coral reef on earth|Take a scenic helicopter flight over the Heart Reef|Skydive over the reef and land on the beach|Sleep overnight on a pontoon floating on the reef|Sail the beautiful Whitsunday Islands|Bungee jump in the nearby Daintree Rainforest",
    "Australian Outback (Uluru)|hot,nature,adventure,culture|#B8860B|uluru outback red dirt kangaroo sunset|Gourmet Sounds of Silence dinner under the stars|Eat Kangaroo or Emu steak cooked on a BBQ|Drink cold beer out of an esky|Drink Billy Tea boiled over a campfire|Watch the massive Uluru rock change colors at sunset|Learn to throw a returning Boomerang|Sleep in a swag bedroll under a billion stars|Take a helicopter ride over the red desert|Hike the massive dome-shaped Kata Tjuta rocks|Learn Aboriginal Dreamtime stories from indigenous elders|Off-road in a massive 4x4 across the dunes|Ride a camel through the outback at dawn",
    "Queenstown (New Zealand)|mild,cold,mountains,adventure,party|#556B2F|queenstown new zealand mountains lake extreme|Fine dining accessible only by a steep gondola|Eat the world-famous massive Fergburger|Taste world-class Pinot Noir in Central Otago|Drink shots in an ice bar made of glaciers|Ride the Luge go-karts down the mountain|Soak in the private cliffside Onsen Hot Pools|Bungee jump off the Kawarau Bridge where the sport was invented|Jet boat at 90km/h through narrow shallow river canyons|Skydive over the breathtaking Remarkables mountain range|Helicopter ski on untouched alpine powder|Hike the brutal rewarding Ben Lomond track|Paraglide off a mountain over the town",
    "Milford Sound (New Zealand)|cold,nature,mountains,adventure,relax|#2F4F4F|milford sound new zealand fjords waterfalls|Gourmet lunch on a luxury nature cruise|Eat a classic Kiwi meat pie on the bus ride in|Drink hot tea while getting sprayed by a waterfall|Drink Speights beer in a cozy pub|Spot playful Kea alpine parrots|See wild dolphins swimming alongside your boat|Cruise through the majestic towering fjords and waterfalls|Take a scenic flight over the dramatic Southern Alps|Kayak silently through the massive fjords|Hike the multi-day world-famous Milford Track|Scuba dive in the dark deep fjord waters to see black coral|Explore the glowworm caves in nearby Te Anau",
    "Bora Bora (French Polynesia)|hot,beach,relax,luxury,romance|#00BFFF|bora bora tropical island luxury overwater bungalow|Private dinner served on the beach surrounded by tiki torches|Eat Tahitian Poisson Cru raw fish in coconut milk|Drink cocktails out of a freshly cut coconut|Drink Hinano Tahiti beer on a boat|Get a traditional Polynesian flower crown|Have breakfast delivered to your bungalow by canoe|Sleep in a massive `$2000/night overwater bungalow|Swim with friendly reef sharks and stingrays|Take a helicopter ride around Mount Otemanu|Jet ski across the impossibly blue lagoon|Attend an intense Polynesian fire dancing show|Scuba dive outside the reef for lemon sharks",
    "Sydney (Australia)|mild,hot,city,beach,party|#1E90FF|sydney opera house harbour bridge ocean|Fine dining inside the Sydney Opera House sails|Eat a classic Aussie meat pie with ketchup|Cocktails at a rooftop bar overlooking the Harbour|Drink pints of Victoria Bitter at a local pub|Pet Kangaroos and Koalas at the zoo|Take the scenic ferry to Manly Beach|Climb the massive arch of the Sydney Harbour Bridge|Surf the famous waves at Bondi Beach|Sail a yacht around the spectacular Sydney Harbour|Take a seaplane to a luxury waterside restaurant|Party at the massive Mardi Gras festival|Scuba dive with Grey Nurse Sharks in Manly",
    "Melbourne (Australia)|mild,city,culture,foodie|#4682B4|melbourne city street art coffee|10-course tasting menu at Attica|Eat incredible Asian-fusion in Chinatown|Drink world-class flat white coffee in a hidden laneway|Drink craft beer in a trendy rooftop bar|Wander the vibrant graffiti-filled Hosier Lane|Watch the little penguins parade at Phillip Island|Drive the spectacular Great Ocean Road to the 12 Apostles|Attend a massive deafening AFL footy match|Explore the hidden underground speakeasies|Take a hot air balloon over the Yarra Valley vineyards|Go surfing at Bells Beach|Hike the rugged Grampians National Park",
    "Fiji|hot,beach,nature,adventure,culture|#3CB371|fiji tropical jungle beach beautiful ocean|Eat Lovo meat and veggies cooked in an earth oven|Eat Kokoda Fijian ceviche|Attend a traditional Kava drinking ceremony|Drink Fiji Bitter beer on the beach|Take a mud bath in the Sabeto Hot Springs|Listen to the locals sing traditional farewell songs|Scuba dive the colorful Great Astrolabe Reef|Whitewater raft the spectacular Upper Navua River|Zipline through the dense jungle canopy|Take a seaplane to the remote Yasawa Islands|Surf the massive world-class Cloudbreak wave|Island hop on a luxury catamaran",
    "Samoa|hot,beach,adventure,culture|#3CB371|samoa tropical ocean trench|Eat a massive traditional Umu feast|Eat crispy Taro root chips|Drink Vailima beer|Drink Kava with the village chief|Swim in the spectacular To Sua Ocean Trench|Watch the massive Alofaaga blowholes erupt|Surf the uncrowded pristine reef breaks|Jungle trek to hidden massive waterfalls|Watch a terrifying traditional Fire Knife dance|Scuba dive the untouched coral reefs|Stay in a traditional open-air Fale on the beach|Slide down the natural Papaseea sliding rocks",
    "Rotorua (New Zealand)|mild,nature,adventure,culture|#8B4513|rotorua new zealand geysers mud pools maori|Eat traditional Maori Hangi cooked underground by geothermal heat|Eat a classic Kiwi pavlova|Drink local craft beer|Drink Sauvignon Blanc from Marlborough|Watch the massive Pohutu Geyser erupt|Soak in the colorful geothermal mud pools|Zipline through the massive ancient Redwood forest|Whitewater raft down the highest commercially rafted waterfall in the world|Roll down a hill inside a giant inflatable Zorb ball|Learn the fierce Haka dance at a Maori village|Mountain bike the world-class Whakarewarewa trails|Luge down the mountain track at high speeds"
]

dests = {}
for row in raw_dests:
    parts = row.split("|")
    dests[parts[0]] = {
        "t": parts[1].split(","), "c": parts[2], "p": parts[3],
        "f": [parts[4], parts[5]], "d": [parts[6], parts[7]], "cu": [parts[8], parts[9]],
        "e": [parts[10], parts[11], parts[12], parts[13], parts[14], parts[15]]
    }

static_qs = [
    {"q": "First things first. What is your absolute ideal climate? ☀️❄️", "opts": {
        "Roasting hot. Bake me like a potato.": {"tags": ["hot"], "cheeky": "Factor 50 sunscreen required. We are chasing the sun."},
        "Brisk, freezing, and covered in snow.": {"tags": ["cold"], "cheeky": "Elsa vibes. The cold never bothered you anyway."},
        "Mild, breezy, and perfect for a light jacket.": {"tags": ["mild"], "cheeky": "Ah, the Goldilocks zone. Not too hot, not too cold."}
    }},
    {"q": "What is the desired pace for this trip? 🏃‍♂️🧘‍♀️", "opts": {
        "Extreme adventure. I want to risk my life.": {"tags": ["adventure", "mountains"], "cheeky": "Adrenaline junkie confirmed. Hope your insurance is paid up."},
        "Total relaxation. I want to forget my own name.": {"tags": ["relax", "beach"], "cheeky": "Brain empty. Vibes only. Let's chill."},
        "Chaos, culture, and non-stop exploring.": {"tags": ["city", "culture"], "cheeky": "You're going to need a vacation to recover from this holiday."},
        "Partying until the sun comes up.": {"tags": ["party"], "cheeky": "Sleep is for the weak. Let's rage."}
    }},
    {"q": "What is your budget/travel style? 💸🎒", "opts": {
        "Unlimited wealth. Spoil me absolutely rotten.": {"tags": ["luxury"], "cheeky": "Sugar daddy vibes. Let's drain the bank account."},
        "A mix of cheap street food and one fancy splurge.": {"tags": ["foodie", "culture"], "cheeky": "Sensible, yet indulgent. The perfect balance."},
        "I just need a tent, some rice, and good vibes.": {"tags": ["budget", "nature"], "cheeky": "Dirt cheap and loving it. Nature is free."}
    }}
]

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
    "What’s your preferred method of escaping a bad date?|'I need to go to the bathroom' climbs out window|adventure,party,nature|The classic Houdini exit.|Faking an emergency phone call|city,mild,culture|Smooth, if a bit cliché.|Just telling them 'No vibes' and leaving|hot,budget,mountains|Brutal honesty. Respect.|Having my butler fake a ransom note|luxury,romance,relax|Expensive, but effective.|I don't escape, I just make it worse on purpose|foodie,beach,cold|You woke up and chose violence.",
    "You find a time machine. First stop?|Dinosaurs. I want to ride a T-Rex.|nature,adventure,hot|You will absolutely be eaten.|The roaring 1920s for a wild party|party,city,luxury|Gatsby vibes. Don't drink the bathtub gin.|To last Tuesday so I can eat that one pizza again|foodie,relax,budget|Priorities. I respect it.|Ancient Rome to watch the gladiators|culture,mild,mountains|Blood, sand, and sandals.|The future, to see what robots look like|cold,beach,romance|Shiny and chrome.",
    "Your aesthetic as a teenager?|Too much eyeliner and emotional rock music|city,party,cold|It wasn't a phase, mom!|Neon everything. I glowed in the dark.|hot,beach,adventure|A walking highlighter.|Preppy, clean, and terrifyingly organized|luxury,mild,culture|Future CEO energy.|I just wore whatever was on the floor|budget,nature,relax|Resourceful and lazy.|Camo print. I was preparing for war.|mountains,nature,foodie|Ready for the apocalypse.",
    "What is your signature cocktail ingredient?|Something that's currently on fire|party,adventure,hot|Eyebrows are overrated anyway.|Gold leaf flakes|luxury,city,romance|Tastes like nothing, costs $`50.|Just give me a beer in a can|budget,beach,nature|Keep it simple, keep it cheap.|Whatever the bartender is experimenting with|culture,foodie,mild|A true connoisseur of chaos.|Ice. Lots of ice.|cold,mountains,relax|Brain freeze incoming.",
    "What do you do when the WiFi goes down?|Panic. Cry. Refresh. Repeat.|city,luxury,party|The withdrawal symptoms are kicking in.|Read a physical book like a 19th-century peasant|culture,mild,romance|Ah, the smell of old paper.|Go outside and touch grass|nature,mountains,adventure|Nature? What are the graphics like?|Take a very long nap|relax,beach,cold|Rebooting your own system.|Cook an elaborate 5-course meal|foodie,hot,budget|Chopping onions to hide the tears.",
    "What is your role in a heist movie?|The mastermind in the tailored suit|luxury,city,culture|Looking sharp while stealing art.|The chaotic explosives expert|adventure,party,hot|Boom goes the dynamite!|The getaway driver eating a sandwich|foodie,budget,beach|Snacks are essential for crime.|The acrobat dodging lasers|mountains,nature,mild|Flexible and stressed.|The decoy who just causes a massive distraction|romance,relax,cold|A drama queen, but useful.",
    "Ideal sandwich architecture?|Meat, cheese, bread. No nonsense.|mountains,budget,cold|A structural purist.|14 different ingredients that require a jaw dislocation|foodie,adventure,party|A delicious mess.|Avocado, sprouts, and artisanal sourdough|culture,mild,city|Very trendy. Very expensive.|Just a hot dog. (Yes, it's a sandwich)|beach,hot,nature|Controversial, but I'll allow it.|Truffle mayo and gold leaf on brioche|luxury,romance,relax|Bougie bread.",
    "How do you pack a suitcase?|Throw everything in 10 minutes before the flight|adventure,party,hot|Living on the absolute edge.|Vacuum-sealed, color-coordinated bags|city,culture,luxury|You scare me, but I'm impressed.|I only bring a toothbrush and buy clothes there|budget,beach,nature|Minimalist nomad.|I pack 14 outfits for a 3-day trip|romance,relax,mild|You never know if there will be a gala!|I force someone else to pack it for me|cold,mountains,foodie|Delegation is a skill.",
    "Reaction to finding `$100 on the ground?|Buy a round of shots for strangers|party,city,hot|The life of the party!|Invest it immediately|culture,mild,luxury|Boring, but financially responsible.|Eat the most expensive steak in town|foodie,romance,relax|Treat yo' self!|Stash it in my mattress|budget,mountains,cold|Paranoia pays off.|Buy a weird sword online|adventure,nature,beach|Because why not?",
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

parsed_dynamic_qs = []
for q_str in raw_qs:
    parts = q_str.split("|")
    q_dict = {"q": parts[0], "opts": {}}
    for i in range(1, 16, 3):
        if i+2 < len(parts):
            q_dict["opts"][parts[i]] = {"tags": parts[i+1].split(","), "cheeky": parts[i+2]}
    parsed_dynamic_qs.append(q_dict)

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
    st.session_state.unused_qs = list(parsed_dynamic_qs)
    random.shuffle(st.session_state.unused_qs)
    st.session_state.current_q = None

def set_stage(new_stage):
    st.session_state.stage = new_stage

def extract_animals(dest_data):
    text = " ".join(dest_data["f"] + dest_data["d"] + dest_data["cu"] + dest_data["e"]).lower()
    text += " " + dest_data["p"].lower()
    possible_animals = [
        "panda", "macaque", "deer", "monkey", "snow monkey", "crab", "octopus",
        "elephant", "dog", "cat", "tiger", "shark", "whale", "ray", "dolphin",
        "fish", "jellyfish", "sea turtle", "turtle", "sloth", "bison", "bear", "grizzly",
        "wolf", "penguin", "guanaco", "llama", "flamingo", "booby", "iguana",
        "alpaca", "condor", "horse", "camel", "leopard", "lion", "cheetah",
        "rhino", "tortoise", "chameleon", "lemur", "kangaroo", "emu", "koala",
        "dragon", "fox", "walrus", "reindeer", "husky", "seagull", "pelican",
        "pig", "squid", "marlin", "stingray", "macaw", "parrot"
    ]
    found = set()
    for a in possible_animals:
        if a in text:
            found.add(a.title())
    return list(found)

def get_top_dests(n=10):
    scored = []
    for d in st.session_state.available_dests:
        dtags = dests[d]["t"]
        score = sum(st.session_state.user_tags[t] for t in dtags if t in st.session_state.user_tags)
        # Using pure raw score prevents smaller-tag locations like Cinque Terre from having an unfair mathematical advantage
        norm = score + random.uniform(0, 0.5)
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

    # Triggers straight to final match after hitting the set amount of questions
    if st.session_state.q_index >= 20 or not st.session_state.unused_qs:
        st.session_state.chosen_dest = get_top_dests(1)[0]
        set_stage('final_match_reveal')
    else:
        st.session_state.current_q = get_next_question()

def pick_activity(act):
    st.session_state.activities.append(act)
    st.session_state.activity_round += 1
    if st.session_state.activity_round >= 6:
        set_stage('final_itinerary')


if st.session_state.stage == 'welcome':
    set_bg("#1E1E1E", "#00FF7F")
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("<div class='giant-emoji'>✈️🌍✨</div>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 65px; font-weight: 900;'>The Perfect Holiday Finder</h1>", unsafe_allow_html=True)

    st.markdown("""
    <div style='background-color: rgba(255,255,255,0.1); padding: 30px; border-radius: 20px; text-align: center; margin: 20px auto; max-width: 800px;'>
    <h3 style='margin-bottom: 20px;'>How the Vibe Engine works:</h3>
    <p style='font-size: 22px;'>1. Our engine actively searches <b>100 globally balanced holidays</b> (including viral hidden gems).</p>
    <p style='font-size: 22px;'>2. It asks 3 Macro Questions, then <b>dynamically funnels</b> opaque personality questions based on your remaining matches.</p>
    <p style='font-size: 22px;'>3. You will pick your ultimate 6-part atmospheric itinerary!</p>
    <p style='font-size: 22px;'>4. Finally, view your 3-page personalized travel guide.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.button("START THE ENGINE! 🚀", on_click=lambda: setattr(st.session_state, 'current_q', get_next_question()) or set_stage('questions'))
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

    st.markdown("<h1 style='text-align: center; font-size: 70px; font-weight: 900;'>🎒 PACK YOUR BAGS! 🎒</h1>", unsafe_allow_html=True)
    st.markdown(f"<h2 style='text-align: center; font-size: 50px; text-decoration: underline;'>📍 {best_dest}</h2>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # 3-Page layout requirement via Streamlit Tabs
    tab1, tab2, tab3 = st.tabs(["🗺️ Your Itinerary", "📸 Scenic Pictures", "🐾 Popular Activities & Animals"])

    with tab1:
        st.markdown("<h3>Your Ultimate Hand-Picked Itinerary:</h3>", unsafe_allow_html=True)
        for act in st.session_state.activities:
            st.markdown(f"<div style='background-color: rgba(255,255,255,0.25); padding: 20px; margin-bottom: 15px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'><h3 style='margin:0;'>🌟 {act}</h3></div>", unsafe_allow_html=True)

    with tab2:
        st.markdown("<h3>Scenic Views of Your Destination</h3>", unsafe_allow_html=True)
        safe_image(dest_data["p"])
        safe_image(dest_data["p"] + " beautiful landscape panoramic view")
        safe_image(dest_data["p"] + " beautiful local scenery sunlight")

    with tab3:
        st.markdown("<h3>Other Popular Local Activities</h3>", unsafe_allow_html=True)
        all_acts = dest_data["f"] + dest_data["d"] + dest_data["cu"] + dest_data["e"]
        unpicked = [a for a in all_acts if a not in st.session_state.activities]
        for a in unpicked:
            st.markdown(f"<li style='font-size: 20px;'>{a}</li>", unsafe_allow_html=True)

        st.markdown("<h3 style='margin-top: 30px;'>Animals You Might Spot</h3>", unsafe_allow_html=True)
        animals = extract_animals(dest_data)
        if animals:
            for animal in animals:
                st.markdown(f"<li style='font-size: 20px;'>🐾 {animal}</li>", unsafe_allow_html=True)
        else:
            st.markdown("<li style='font-size: 20px;'>🐾 Native wildlife, local birds, and friendly street animals.</li>", unsafe_allow_html=True)


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
