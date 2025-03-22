"""
Study plan module to manage Bible reading and memorization plans.
"""

import json
import os
import datetime
from bible_data import format_reference, ALL_BOOKS, get_book_chapters

# Data directory
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(DATA_DIR, exist_ok=True)
PLAN_FILE = os.path.join(DATA_DIR, 'study_plan.json')

# Default study plan
DEFAULT_PLAN = {
    "reading_passages": [
        {"book": "诗篇", "chapter": 1}
    ],
    "memorization_verses": [
        {"book": "约翰福音", "chapter": 3, "verse_start": 16, "verse_end": 16, "custom_text": ""}
    ]
}


class StudyPlan:
    def __init__(self):
        self.reading_passages = []
        self.memorization_verses = []
        self.load_plan()
    
    def load_plan(self):
        """Load study plan from file or create a default one if it doesn't exist."""
        if os.path.exists(PLAN_FILE):
            try:
                with open(PLAN_FILE, 'r', encoding='utf-8') as f:
                    plan_data = json.load(f)
                    self.reading_passages = plan_data.get('reading_passages', [])
                    self.memorization_verses = plan_data.get('memorization_verses', [])
            except:
                # If there's an error loading, use defaults
                self.set_default_plan()
        else:
            # If no file exists, use defaults
            self.set_default_plan()
    
    def set_default_plan(self):
        """Set the default study plan."""
        self.reading_passages = DEFAULT_PLAN['reading_passages']
        self.memorization_verses = DEFAULT_PLAN['memorization_verses']
        self.save_plan()
    
    def save_plan(self):
        """Save the current study plan to file."""
        plan_data = {
            'reading_passages': self.reading_passages,
            'memorization_verses': self.memorization_verses
        }
        
        with open(PLAN_FILE, 'w', encoding='utf-8') as f:
            json.dump(plan_data, f, ensure_ascii=False, indent=2)
    
    def add_reading_passage(self, book, chapter):
        """
        Add a reading passage to the plan.
        
        Args:
            book (str): Bible book name
            chapter (int): Chapter number
        """
        # Validate chapter
        max_chapters = get_book_chapters(book)
        if chapter < 1 or chapter > max_chapters:
            return False
        
        # Check if it already exists
        for passage in self.reading_passages:
            if passage['book'] == book and passage['chapter'] == chapter:
                return False
        
        # Add to plan
        self.reading_passages.append({
            'book': book,
            'chapter': chapter
        })
        
        self.save_plan()
        return True
    
    def remove_reading_passage(self, index):
        """
        Remove a reading passage by index.
        
        Args:
            index (int): Index of the passage to remove
        """
        if 0 <= index < len(self.reading_passages):
            self.reading_passages.pop(index)
            self.save_plan()
            return True
        return False
    
    def add_memorization_verse(self, book, chapter, verse_start, verse_end=None, custom_text=""):
        """
        Add a memorization verse to the plan.
        
        Args:
            book (str): Bible book name
            chapter (int): Chapter number
            verse_start (int): Starting verse number
            verse_end (int, optional): Ending verse number
            custom_text (str, optional): Custom text for the verse if provided by user
        """
        # Validate inputs
        max_chapters = get_book_chapters(book)
        if chapter < 1 or chapter > max_chapters:
            return False
        
        # Simple validation for verses
        if verse_start < 1 or (verse_end is not None and verse_end < verse_start):
            return False
            
        # Add to plan
        self.memorization_verses.append({
            'book': book,
            'chapter': chapter,
            'verse_start': verse_start,
            'verse_end': verse_end,
            'custom_text': custom_text
        })
        
        self.save_plan()
        return True
    
    def remove_memorization_verse(self, index):
        """
        Remove a memorization verse by index.
        
        Args:
            index (int): Index of the verse to remove
        """
        if 0 <= index < len(self.memorization_verses):
            self.memorization_verses.pop(index)
            self.save_plan()
            return True
        return False
    
    def update_verse_text(self, index, custom_text):
        """
        Update the custom text for a memorization verse.
        
        Args:
            index (int): Index of the verse to update
            custom_text (str): Custom text to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        if 0 <= index < len(self.memorization_verses):
            self.memorization_verses[index]['custom_text'] = custom_text
            self.save_plan()
            return True
        return False
    
    def get_daily_reading_passages(self):
        """
        Get the list of reading passages for today.
        
        Returns:
            list: List of reading passage references
        """
        return [
            format_reference(passage['book'], passage['chapter'])
            for passage in self.reading_passages
        ]
    
    def get_daily_memorization_verses(self):
        """
        Get the memorization verse for today based on current date.
        
        Returns:
            dict: A verse reference dictionary
        """
        # If no verses are set, return None
        if not self.memorization_verses:
            return None
            
        # Select verse based on day of year
        today = datetime.datetime.now()
        day_of_year = today.timetuple().tm_yday
        verse_index = (day_of_year - 1) % len(self.memorization_verses)
        
        return self.memorization_verses[verse_index]
        
    def get_all_reading_passages(self):
        """
        Get all reading passages.
        
        Returns:
            list: List of all reading passages
        """
        return self.reading_passages
        
    def get_all_memorization_verses(self):
        """
        Get all memorization verses.
        
        Returns:
            list: List of all memorization verses
        """
        return self.memorization_verses 