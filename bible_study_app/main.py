#!/usr/bin/env python
"""
Main application file for the Bible Study App.
This provides a GUI for setting and viewing daily Bible reading and memorization.
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedTk
import datetime
from dateutil.relativedelta import relativedelta

import bible_data
from bible_api import get_verse
from study_plan import StudyPlan

class BibleStudyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("每日灵修程序")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Load study plan
        self.study_plan = StudyPlan()
        
        # Get current time and day of year
        self.current_time = datetime.datetime.now()
        self.day_of_year = self.current_time.timetuple().tm_yday
        
        # Setup UI
        self.setup_ui()
        
        # Update content
        self.update_daily_content()
        
        # Update time every second
        self.update_time()
        
    def setup_ui(self):
        """Set up the user interface."""
        # Create notebook with tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create frames for tabs
        self.daily_frame = ttk.Frame(self.notebook)
        self.setup_frame = ttk.Frame(self.notebook)
        
        # Add frames to notebook
        self.notebook.add(self.daily_frame, text="每日灵修")
        self.notebook.add(self.setup_frame, text="设置")
        
        # Setup daily tab
        self.setup_daily_tab()
        
        # Setup settings tab
        self.setup_settings_tab()
    
    def setup_daily_tab(self):
        """Set up the daily tab UI."""
        # Time and day frame
        time_frame = ttk.Frame(self.daily_frame)
        time_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Time label
        self.time_label = ttk.Label(
            time_frame, 
            font=("Arial", 14)
        )
        self.time_label.pack(side=tk.LEFT)
        
        # Day of year label
        self.day_label = ttk.Label(
            time_frame,
            font=("Arial", 14)
        )
        self.day_label.pack(side=tk.RIGHT)
        
        # Separator
        ttk.Separator(self.daily_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Reading passages frame
        reading_frame = ttk.LabelFrame(self.daily_frame, text="今日阅读经文")
        reading_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Reading passages list
        self.reading_list = tk.Listbox(
            reading_frame,
            font=("Arial", 12),
            height=5
        )
        self.reading_list.pack(fill=tk.X, padx=10, pady=10)
        
        # Separator
        ttk.Separator(self.daily_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, padx=10, pady=5)
        
        # Memorization verse frame
        mem_frame = ttk.LabelFrame(self.daily_frame, text="今日背诵经文")
        mem_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Memorization reference
        self.mem_ref_label = ttk.Label(
            mem_frame,
            font=("Arial", 14, "bold"),
            anchor=tk.CENTER
        )
        self.mem_ref_label.pack(fill=tk.X, padx=10, pady=10)
        
        # Memorization text
        self.mem_text = tk.Text(
            mem_frame,
            font=("Arial", 12),
            wrap=tk.WORD,
            height=10
        )
        self.mem_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.mem_text.config(state=tk.DISABLED)
    
    def setup_settings_tab(self):
        """Set up the settings tab UI."""
        # Create two frames - one for reading and one for memorization
        settings_paned = ttk.PanedWindow(self.setup_frame, orient=tk.HORIZONTAL)
        settings_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Reading settings frame
        reading_frame = ttk.LabelFrame(settings_paned, text="阅读经文设置")
        
        # Reading list frame
        reading_list_frame = ttk.Frame(reading_frame)
        reading_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Reading passages list with scrollbar
        self.setup_reading_list = tk.Listbox(
            reading_list_frame,
            font=("Arial", 12),
            height=10
        )
        reading_scrollbar = ttk.Scrollbar(reading_list_frame, orient=tk.VERTICAL, command=self.setup_reading_list.yview)
        self.setup_reading_list.configure(yscrollcommand=reading_scrollbar.set)
        
        reading_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.setup_reading_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Reading controls frame
        reading_controls = ttk.Frame(reading_frame)
        reading_controls.pack(fill=tk.X, padx=10, pady=10)
        
        # Book selection
        ttk.Label(reading_controls, text="选择书卷:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.reading_book_var = tk.StringVar()
        self.reading_book_combo = ttk.Combobox(reading_controls, textvariable=self.reading_book_var, values=bible_data.ALL_BOOKS)
        self.reading_book_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.reading_book_combo.bind("<<ComboboxSelected>>", self.update_chapter_values)
        
        # Chapter selection
        ttk.Label(reading_controls, text="选择章节:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.reading_chapter_var = tk.IntVar()
        self.reading_chapter_combo = ttk.Combobox(reading_controls, textvariable=self.reading_chapter_var)
        self.reading_chapter_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Add and Remove buttons
        btn_frame = ttk.Frame(reading_controls)
        btn_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=10)
        
        ttk.Button(btn_frame, text="添加", command=self.add_reading_passage).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="删除", command=self.remove_reading_passage).pack(side=tk.LEFT, padx=5)
        
        # Memorization settings frame
        mem_frame = ttk.LabelFrame(settings_paned, text="背诵经文设置")
        
        # Memorization list frame
        mem_list_frame = ttk.Frame(mem_frame)
        mem_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Memorization verses list with scrollbar
        self.setup_mem_list = tk.Listbox(
            mem_list_frame,
            font=("Arial", 12),
            height=10
        )
        mem_scrollbar = ttk.Scrollbar(mem_list_frame, orient=tk.VERTICAL, command=self.setup_mem_list.yview)
        self.setup_mem_list.configure(yscrollcommand=mem_scrollbar.set)
        
        mem_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.setup_mem_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Memorization controls frame
        mem_controls = ttk.Frame(mem_frame)
        mem_controls.pack(fill=tk.X, padx=10, pady=10)
        
        # Book selection
        ttk.Label(mem_controls, text="选择书卷:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.mem_book_var = tk.StringVar()
        self.mem_book_combo = ttk.Combobox(mem_controls, textvariable=self.mem_book_var, values=bible_data.ALL_BOOKS)
        self.mem_book_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        self.mem_book_combo.bind("<<ComboboxSelected>>", self.update_mem_chapter_values)
        
        # Chapter selection
        ttk.Label(mem_controls, text="选择章节:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.mem_chapter_var = tk.IntVar()
        self.mem_chapter_combo = ttk.Combobox(mem_controls, textvariable=self.mem_chapter_var)
        self.mem_chapter_combo.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Verse selection
        verse_frame = ttk.Frame(mem_controls)
        verse_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W+tk.E)
        
        ttk.Label(verse_frame, text="开始经节:").pack(side=tk.LEFT, padx=5)
        self.mem_verse_start_var = tk.IntVar(value=1)
        self.mem_verse_start_entry = ttk.Entry(verse_frame, textvariable=self.mem_verse_start_var, width=5)
        self.mem_verse_start_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(verse_frame, text="结束经节:").pack(side=tk.LEFT, padx=5)
        self.mem_verse_end_var = tk.IntVar(value=1)
        self.mem_verse_end_entry = ttk.Entry(verse_frame, textvariable=self.mem_verse_end_var, width=5)
        self.mem_verse_end_entry.pack(side=tk.LEFT, padx=5)
        
        # Add and Remove buttons
        mem_btn_frame = ttk.Frame(mem_controls)
        mem_btn_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        
        ttk.Button(mem_btn_frame, text="添加", command=self.add_memorization_verse).pack(side=tk.LEFT, padx=5)
        ttk.Button(mem_btn_frame, text="删除", command=self.remove_memorization_verse).pack(side=tk.LEFT, padx=5)
        
        # Add frames to paned window
        settings_paned.add(reading_frame, weight=1)
        settings_paned.add(mem_frame, weight=1)
        
        # Load current settings
        self.load_settings()
    
    def update_time(self):
        """Update the time display."""
        self.current_time = datetime.datetime.now()
        self.day_of_year = self.current_time.timetuple().tm_yday
        
        # Format the time string
        time_str = self.current_time.strftime("%Y年%m月%d日 %H:%M:%S")
        self.time_label.config(text=time_str)
        
        # Format the day of year
        day_str = f"今年第 {self.day_of_year} 天"
        self.day_label.config(text=day_str)
        
        # Schedule the next update
        self.root.after(1000, self.update_time)
    
    def update_daily_content(self):
        """Update the daily content based on the study plan."""
        # Clear current content
        self.reading_list.delete(0, tk.END)
        
        # Add reading passages
        for passage in self.study_plan.get_daily_reading_passages():
            self.reading_list.insert(tk.END, passage)
        
        # Get memorization verse for today
        verse = self.study_plan.get_daily_memorization_verses()
        if verse:
            # Format reference
            book = verse['book']
            chapter = verse['chapter']
            verse_start = verse['verse_start']
            verse_end = verse['verse_end']
            
            if verse_end:
                ref = f"{book} {chapter}:{verse_start}-{verse_end}"
            else:
                ref = f"{book} {chapter}:{verse_start}"
            
            self.mem_ref_label.config(text=ref)
            
            # Get verse text
            verse_text = get_verse(book, chapter, verse_start, verse_end)
            
            # Display verse text
            self.mem_text.config(state=tk.NORMAL)
            self.mem_text.delete(1.0, tk.END)
            self.mem_text.insert(tk.END, verse_text)
            self.mem_text.config(state=tk.DISABLED)
        else:
            self.mem_ref_label.config(text="未设置背诵经文")
            self.mem_text.config(state=tk.NORMAL)
            self.mem_text.delete(1.0, tk.END)
            self.mem_text.insert(tk.END, "请在设置选项卡添加经文进行背诵。")
            self.mem_text.config(state=tk.DISABLED)
    
    def load_settings(self):
        """Load current settings into the UI."""
        # Load reading passages
        self.setup_reading_list.delete(0, tk.END)
        
        for passage in self.study_plan.get_all_reading_passages():
            book = passage['book']
            chapter = passage['chapter']
            self.setup_reading_list.insert(tk.END, f"{book} {chapter}")
        
        # Load memorization verses
        self.setup_mem_list.delete(0, tk.END)
        
        for verse in self.study_plan.get_all_memorization_verses():
            book = verse['book']
            chapter = verse['chapter']
            verse_start = verse['verse_start']
            verse_end = verse['verse_end']
            
            if verse_end:
                self.setup_mem_list.insert(tk.END, f"{book} {chapter}:{verse_start}-{verse_end}")
            else:
                self.setup_mem_list.insert(tk.END, f"{book} {chapter}:{verse_start}")
    
    def update_chapter_values(self, event=None):
        """Update chapter values based on selected book."""
        book = self.reading_book_var.get()
        if book:
            num_chapters = bible_data.get_book_chapters(book)
            self.reading_chapter_combo.config(values=list(range(1, num_chapters + 1)))
            self.reading_chapter_var.set(1)
    
    def update_mem_chapter_values(self, event=None):
        """Update memorization chapter values based on selected book."""
        book = self.mem_book_var.get()
        if book:
            num_chapters = bible_data.get_book_chapters(book)
            self.mem_chapter_combo.config(values=list(range(1, num_chapters + 1)))
            self.mem_chapter_var.set(1)
    
    def add_reading_passage(self):
        """Add a reading passage to the study plan."""
        book = self.reading_book_var.get()
        chapter = self.reading_chapter_var.get()
        
        if not book:
            messagebox.showerror("错误", "请选择一本书卷")
            return
        
        if not chapter:
            messagebox.showerror("错误", "请选择一个章节")
            return
        
        # Add to plan
        success = self.study_plan.add_reading_passage(book, chapter)
        
        if success:
            messagebox.showinfo("成功", f"已添加 {book} {chapter} 到阅读计划")
            self.load_settings()
            self.update_daily_content()
        else:
            messagebox.showerror("错误", "无法添加阅读章节，可能已存在或是无效章节")
    
    def remove_reading_passage(self):
        """Remove a reading passage from the study plan."""
        selected = self.setup_reading_list.curselection()
        
        if not selected:
            messagebox.showerror("错误", "请选择要删除的阅读章节")
            return
        
        # Remove from plan
        index = selected[0]
        success = self.study_plan.remove_reading_passage(index)
        
        if success:
            messagebox.showinfo("成功", "已从阅读计划中删除所选章节")
            self.load_settings()
            self.update_daily_content()
        else:
            messagebox.showerror("错误", "无法删除所选章节")
    
    def add_memorization_verse(self):
        """Add a memorization verse to the study plan."""
        book = self.mem_book_var.get()
        chapter = self.mem_chapter_var.get()
        verse_start = self.mem_verse_start_var.get()
        verse_end = self.mem_verse_end_var.get()
        
        if not book:
            messagebox.showerror("错误", "请选择一本书卷")
            return
        
        if not chapter:
            messagebox.showerror("错误", "请选择一个章节")
            return
        
        if not verse_start:
            messagebox.showerror("错误", "请输入开始经节")
            return
        
        # If verse_end is the same as verse_start, just use verse_start
        if verse_end == verse_start:
            verse_end = None
        
        # Add to plan
        success = self.study_plan.add_memorization_verse(book, chapter, verse_start, verse_end)
        
        if success:
            if verse_end:
                messagebox.showinfo("成功", f"已添加 {book} {chapter}:{verse_start}-{verse_end} 到背诵计划")
            else:
                messagebox.showinfo("成功", f"已添加 {book} {chapter}:{verse_start} 到背诵计划")
            
            self.load_settings()
            self.update_daily_content()
        else:
            messagebox.showerror("错误", "无法添加背诵经文，可能是无效章节或经节")
    
    def remove_memorization_verse(self):
        """Remove a memorization verse from the study plan."""
        selected = self.setup_mem_list.curselection()
        
        if not selected:
            messagebox.showerror("错误", "请选择要删除的背诵经文")
            return
        
        # Remove from plan
        index = selected[0]
        success = self.study_plan.remove_memorization_verse(index)
        
        if success:
            messagebox.showinfo("成功", "已从背诵计划中删除所选经文")
            self.load_settings()
            self.update_daily_content()
        else:
            messagebox.showerror("错误", "无法删除所选经文")


def main():
    # Create data directory if it doesn't exist
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Create themed Tk instance
    root = ThemedTk(theme="arc")
    
    # Create application
    app = BibleStudyApp(root)
    
    # Start the main loop
    root.mainloop()


if __name__ == "__main__":
    main() 