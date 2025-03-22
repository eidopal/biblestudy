"""
Bible data utility module that provides book names and chapter counts.
"""

# Bible books with their chapter counts
BIBLE_BOOKS = {
    # Old Testament
    "创世记": 50,
    "出埃及记": 40,
    "利未记": 27,
    "民数记": 36,
    "申命记": 34,
    "约书亚记": 24,
    "士师记": 21,
    "路得记": 4,
    "撒母耳记上": 31,
    "撒母耳记下": 24,
    "列王纪上": 22,
    "列王纪下": 25,
    "历代志上": 29,
    "历代志下": 36,
    "以斯拉记": 10,
    "尼希米记": 13,
    "以斯帖记": 10,
    "约伯记": 42,
    "诗篇": 150,
    "箴言": 31,
    "传道书": 12,
    "雅歌": 8,
    "以赛亚书": 66,
    "耶利米书": 52,
    "耶利米哀歌": 5,
    "以西结书": 48,
    "但以理书": 12,
    "何西阿书": 14,
    "约珥书": 3,
    "阿摩司书": 9,
    "俄巴底亚书": 1,
    "约拿书": 4,
    "弥迦书": 7,
    "那鸿书": 3,
    "哈巴谷书": 3,
    "西番雅书": 3,
    "哈该书": 2,
    "撒迦利亚书": 14,
    "玛拉基书": 4,
    
    # New Testament
    "马太福音": 28,
    "马可福音": 16,
    "路加福音": 24,
    "约翰福音": 21,
    "使徒行传": 28,
    "罗马书": 16,
    "哥林多前书": 16,
    "哥林多后书": 13,
    "加拉太书": 6,
    "以弗所书": 6,
    "腓立比书": 4,
    "歌罗西书": 4,
    "帖撒罗尼迦前书": 5,
    "帖撒罗尼迦后书": 3,
    "提摩太前书": 6,
    "提摩太后书": 4,
    "提多书": 3,
    "腓利门书": 1,
    "希伯来书": 13,
    "雅各书": 5,
    "彼得前书": 5,
    "彼得后书": 3,
    "约翰一书": 5,
    "约翰二书": 1,
    "约翰三书": 1,
    "犹大书": 1,
    "启示录": 22
}

# List of book names in canonical order
OLD_TESTAMENT = [
    "创世记", "出埃及记", "利未记", "民数记", "申命记",
    "约书亚记", "士师记", "路得记", "撒母耳记上", "撒母耳记下",
    "列王纪上", "列王纪下", "历代志上", "历代志下", "以斯拉记",
    "尼希米记", "以斯帖记", "约伯记", "诗篇", "箴言",
    "传道书", "雅歌", "以赛亚书", "耶利米书", "耶利米哀歌",
    "以西结书", "但以理书", "何西阿书", "约珥书", "阿摩司书",
    "俄巴底亚书", "约拿书", "弥迦书", "那鸿书", "哈巴谷书",
    "西番雅书", "哈该书", "撒迦利亚书", "玛拉基书"
]

NEW_TESTAMENT = [
    "马太福音", "马可福音", "路加福音", "约翰福音", "使徒行传",
    "罗马书", "哥林多前书", "哥林多后书", "加拉太书", "以弗所书",
    "腓立比书", "歌罗西书", "帖撒罗尼迦前书", "帖撒罗尼迦后书", "提摩太前书",
    "提摩太后书", "提多书", "腓利门书", "希伯来书", "雅各书",
    "彼得前书", "彼得后书", "约翰一书", "约翰二书", "约翰三书",
    "犹大书", "启示录"
]

ALL_BOOKS = OLD_TESTAMENT + NEW_TESTAMENT

def get_book_chapters(book_name):
    """
    Get the number of chapters in a given book.
    
    Args:
        book_name (str): Name of the Bible book
        
    Returns:
        int: Number of chapters in the book
    """
    return BIBLE_BOOKS.get(book_name, 0)

def format_reference(book, chapter, verse_start=None, verse_end=None):
    """
    Format a Bible reference.
    
    Args:
        book (str): Book name
        chapter (int): Chapter number
        verse_start (int, optional): Starting verse
        verse_end (int, optional): Ending verse
        
    Returns:
        str: Formatted reference
    """
    if verse_start is None:
        return f"{book} {chapter}"
    elif verse_end is None:
        return f"{book} {chapter}:{verse_start}"
    else:
        return f"{book} {chapter}:{verse_start}-{verse_end}" 