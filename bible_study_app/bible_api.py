"""
Bible API module to fetch Bible verses from online sources.
"""

import requests
import json
import os
import time
from urllib.parse import quote

# Set fallback data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
CACHE_FILE = os.path.join(DATA_DIR, 'verse_cache.json')

# Initialize cache
if os.path.exists(CACHE_FILE):
    try:
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            verse_cache = json.load(f)
    except:
        verse_cache = {}
else:
    verse_cache = {}

# 本地经文库 - 提供一些常用经文作为备选
LOCAL_VERSES = {
    # 约翰福音
    "约翰福音_3_16": "神爱世人，甚至将他的独生子赐给他们，叫一切信他的，不致灭亡，反得永生。",
    "约翰福音_14_6": "耶稣说：'我就是道路、真理、生命；若不借着我，没有人能到父那里去。'",
    "约翰福音_10_10": "盗贼来，无非要偷窃，杀害，毁坏；我来了，是要叫羊得生命，并且得的更丰盛。",
    "约翰福音_15_5": "我是葡萄树，你们是枝子。常在我里面的，我也常在他里面，这人就多结果子；因为离了我，你们就不能做什么。",
    
    # 诗篇
    "诗篇_23_1": "耶和华是我的牧者，我必不至缺乏。",
    "诗篇_1_1_2": "不从恶人的计谋，不站罪人的道路，不坐亵慢人的座位，惟喜爱耶和华的律法，昼夜思想，这人便为有福。",
    "诗篇_119_105": "你的话是我脚前的灯，是我路上的光。",
    "诗篇_46_10": "你们要休息，要知道我是神！我必在外邦中被尊崇，在遍地上也被尊崇。",
    "诗篇_37_4": "又要以耶和华为乐，他就将你心里所求的赐给你。",
    
    # 罗马书
    "罗马书_8_28": "我们晓得万事都互相效力，叫爱神的人得益处，就是按他旨意被召的人。",
    "罗马书_12_2": "不要效法这个世界，只要心意更新而变化，叫你们察验何为神的善良、纯全、可喜悦的旨意。",
    "罗马书_5_8": "惟有基督在我们还作罪人的时候为我们死，神的爱就在此向我们显明了。",
    "罗马书_10_9": "你若口里认耶稣为主，心里信神叫他从死里复活，就必得救。",
    
    # 腓立比书
    "腓立比书_4_13": "我靠着那加给我力量的，凡事都能做。",
    "腓立比书_4_6_7": "应当一无挂虑，只要凡事借着祷告、祈求和感谢，将你们所要的告诉神。神所赐出人意外的平安，必在基督耶稣里保守你们的心怀意念。",
    "腓立比书_4_19": "我的神必照他荣耀的丰富，在基督耶稣里使你们一切所需用的都充足。",
    
    # 耶利米书
    "耶利米书_29_11": "耶和华说：我知道我向你们所怀的意念是赐平安的意念，不是降灾祸的意念，要叫你们末后有指望。",
    
    # 箴言
    "箴言_3_5_6": "你要专心仰赖耶和华，不可倚靠自己的聪明。在你一切所行的事上都要认定他，他必指引你的路。",
    "箴言_16_9": "人心筹算自己的道路，惟耶和华指引他的脚步。",
    "箴言_15_1": "回答柔和，使怒消退；言语暴戾，触动怒气。",
    
    # 马太福音
    "马太福音_11_28": "凡劳苦担重担的人可以到我这里来，我就使你们得安息。",
    "马太福音_5_16": "你们的光也当这样照在人前，叫他们看见你们的好行为，便将荣耀归给你们在天上的父。",
    "马太福音_28_19_20": "所以，你们要去，使万民作我的门徒，奉父、子、圣灵的名给他们施洗。凡我所吩咐你们的，都教训他们遵守，我就常与你们同在，直到世界的末了。",
    
    # 以赛亚书
    "以赛亚书_40_31": "但那等候耶和华的必从新得力，他们必如鹰展翅上腾，他们奔跑却不困倦，行走却不疲乏。",
    "以赛亚书_41_10": "你不要害怕，因为我与你同在；不要惊惶，因为我是你的神。我必坚固你，我必帮助你，我必用我公义的右手扶持你。",
    "以赛亚书_53_5": "哪知他为我们的过犯受害，为我们的罪孽压伤。因他受的刑罚，我们得平安；因他受的鞭伤，我们得医治。",
    
    # 约翰一书
    "约翰一书_1_9": "我们若认自己的罪，神是信实的，是公义的，必要赦免我们的罪，洗净我们一切的不义。",
    "约翰一书_4_19": "我们爱，因为神先爱我们。",
    
    # 哥林多前书
    "哥林多前书_13_4_7": "爱是恒久忍耐，又有恩慈；爱是不嫉妒；爱是不自夸，不张狂，不做害羞的事，不求自己的益处，不轻易发怒，不计算人的恶，不喜欢不义，只喜欢真理；凡事包容，凡事相信，凡事盼望，凡事忍耐。",
    "哥林多前书_10_13": "你们所遇见的试探，无非是人所能受的。神是信实的，必不叫你们受试探过于所能受的；在受试探的时候，总要给你们开一条出路，叫你们能忍受得住。",
    
    # 加拉太书
    "加拉太书_5_22_23": "圣灵所结的果子，就是仁爱、喜乐、和平、忍耐、恩慈、良善、信实、温柔、节制。这样的事没有律法禁止。",
    "加拉太书_2_20": "我已经与基督同钉十字架，现在活着的不再是我，乃是基督在我里面活着；并且我如今在肉身活着，是因信神的儿子而活；他是爱我，为我舍己。",
    
    # 希伯来书
    "希伯来书_4_14_16": "我们既然有一位已经升入高天尊荣的大祭司，就是神的儿子耶稣，便当持定所承认的道。因我们的大祭司并非不能体恤我们的软弱，他也曾凡事受过试探，与我们一样，只是他没有犯罪。所以，我们只管坦然无惧地来到施恩的宝座前，为要得怜恤，蒙恩惠，作随时的帮助。",
    "希伯来书_11_1": "信就是所望之事的实底，是未见之事的确据。",
    "希伯来书_12_1_2": "我们既有这许多的见证人，如同云彩围着我们，就当放下各样的重担，脱去容易缠累我们的罪，存心忍耐，奔那摆在我们前头的路程，仰望为我们信心创始成终的耶稣。他因那摆在前面的喜乐，就轻看羞辱，忍受了十字架的苦难，便坐在神宝座的右边。",
    "希伯来书_13_5": "你们存心不可贪爱钱财，要以自己所有的为足；因为主曾说：'我总不撇下你，也不丢弃你。'"
}


def save_cache():
    """Save the verse cache to disk."""
    try:
        with open(CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(verse_cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving cache: {str(e)}")


def get_verse(book, chapter, verse_start, verse_end=None):
    """
    Get Bible verse text from API or cache.
    
    Args:
        book (str): Bible book name
        chapter (int): Chapter number
        verse_start (int): Starting verse number
        verse_end (int, optional): Ending verse number
        
    Returns:
        str: The verse text
    """
    # Create a cache key
    if verse_end:
        cache_key = f"{book}_{chapter}_{verse_start}_{verse_end}"
    else:
        cache_key = f"{book}_{chapter}_{verse_start}"
        
    # Check cache first
    if cache_key in verse_cache:
        return verse_cache[cache_key]
    
    # Check local verse library
    if cache_key in LOCAL_VERSES:
        verse_text = LOCAL_VERSES[cache_key]
        verse_cache[cache_key] = verse_text
        save_cache()
        return verse_text
        
    # Similar keys in local verse library
    similar_key = None
    for key in LOCAL_VERSES.keys():
        if key.startswith(f"{book}_{chapter}_"):
            similar_key = key
            break
    
    # Format reference for API request
    if verse_end:
        reference = f"{book} {chapter}:{verse_start}-{verse_end}"
    else:
        reference = f"{book} {chapter}:{verse_start}"
    
    # Try to get from API
    try:
        # Using API
        verse_text = get_from_api(book, chapter, verse_start, verse_end, reference)
        
        if verse_text and not verse_text.startswith("Error"):
            # Cache result
            verse_cache[cache_key] = verse_text
            save_cache()
            return verse_text
            
        # If API failed, use our backup approach
        if similar_key:
            return LOCAL_VERSES[similar_key]
            
        # If no similar verse found, provide a default response
        fallback_text = f"经文 {reference} 暂时无法获取，请稍后再试。"
        verse_cache[cache_key] = fallback_text
        save_cache()
        return fallback_text
    
    except Exception as e:
        # If API failed, use our backup approach
        if similar_key:
            return LOCAL_VERSES[similar_key]
            
        # If no similar verse found, provide a default response
        fallback_text = f"经文 {reference} 暂时无法获取：{str(e)}"
        return fallback_text


def get_from_api(book, chapter, verse_start, verse_end, reference):
    """Try to get verse from external API"""
    try:
        # Using the GetBible API
        encoded_ref = quote(reference)
        url = f"https://getbible.net/json?passage={encoded_ref}&version=cns"
        
        response = requests.get(url, timeout=10)
        
        # Check if valid JSON response
        if response.status_code == 200:
            text = response.text
            if not text:
                return None
                
            # Handle JSONP format
            if text.startswith('(') and text.endswith(')'):
                text = text[1:-1]
            
            # Parse JSON
            try:
                data = json.loads(text)
                
                # Extract verse text
                verse_text = ""
                
                if 'book' in data:
                    book_data = data['book']
                    chapter_data = book_data[0]['chapter']
                    
                    verses = []
                    for verse_num, verse_info in chapter_data.items():
                        if 'verse' in verse_info:
                            verses.append(verse_info['verse'])
                    
                    verse_text = " ".join(verses)
                    return verse_text
                    
                return None
            except json.JSONDecodeError:
                return None
        else:
            return None
    
    except Exception:
        # API call failed
        return None


def get_chapter(book, chapter):
    """
    Get an entire Bible chapter.
    
    Args:
        book (str): Bible book name
        chapter (int): Chapter number
        
    Returns:
        str: Reference text for the chapter
    """
    # For chapters, we just return the reference
    return f"{book} {chapter}" 