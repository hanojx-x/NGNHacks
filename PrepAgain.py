import os
import csv
import random
import tkinter as tk
from tkinter import ttk

#finds the exact location of the file directory no matter where it is
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) if '__file__' in globals() else os.getcwd()

#map lesson titles to their respective file paths
LESSON_FILES = {"Unit 1 (Number Sense)": os.path.join(BASE_DIR, "mth1w_number_sense.csv"), "Unit 2 (Algebra)": os.path.join(BASE_DIR, "mth1w_algebra_coding.csv"), "Unit 3 (Linear Relations)": os.path.join(BASE_DIR, "mth1w_linear_relations.csv"), "Unit 4 (Geometry)": os.path.join(BASE_DIR, "mth1w_measurement_geometry.csv"), "Unit 5 (Financial Literacy)": os.path.join(BASE_DIR, "mth1w_financial_literacy.csv"), "Unit 6 (Data and Statistics)": os.path.join(BASE_DIR, "mth1w_data_statistics.csv") }

lessons = list(LESSON_FILES.keys())

#returns the values of 10 random questions and their options and answers
def load_random_questions(csv_filepath, num_questions=10):
    #loads all question rows into memory
    with open(csv_filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) #skips the header of the csv file
        rows = list(reader)

    #selects 10 random rows (questions) from the file
    sample = random.sample(rows, min(num_questions, len(rows)))
    questions = [[row[0]] for row in sample]
    options = [row[1:5] for row in sample]
    answers = [[row[5]] for row in sample]

    return questions, options, answers

#opens a new window where the questions are given
def open_question_window():
    #loads random questions from file path
    selected_lesson = lesson_dropdown.get()
    csv_filepath = LESSON_FILES.get(selected_lesson)
    questions, options, answers = load_random_questions(csv_filepath, 10)

    #variables for score and question no.
    q_index = 0
    score = 0
    letter_map = {'a': 1, 'b': 2, 'c': 3, 'd': 4}

    #question window
    new_window = tk.Toplevel(root)
    new_window.title(f"Questions - {selected_lesson}")
    new_window.geometry("500x500")

    #gui labels/inputs
    tk.Label(new_window, text=selected_lesson, font=("Arial", 14, )).pack(pady=10)
    q_num_label = tk.Label(new_window, text="", font=("Arial", 12))
    q_num_label.pack(pady=5)

    prompt_label = tk.Label(new_window, text="", font=("Arial", 13), wraplength=450)
    prompt_label.pack(pady=10)

    options_label = tk.Label(new_window, text="", font=("Arial", 11),)
    options_label.pack(pady=10)

    entry_label = tk.Label(new_window, text="Type a, b, c, or d:", font=("Arial", 10))
    entry_label.pack(pady=5)

    answer_entry = tk.Entry(new_window, font=("Arial", 12), width=5,)
    answer_entry.pack(pady=5)

    feedback_label = tk.Label(new_window, text="", font=("Arial", 11))
    feedback_label.pack(pady=5)

    #displays the current question
    def display_current_question():
        #shows question no.
        q_num_label.config(text=f"Question {q_index + 1} of {len(questions)}")
        prompt_label.config(text=questions[q_index][0])

        #displays options
        opts = options[q_index]
        options_label.config(text=f"a)  {opts[0]}\nb)  {opts[1]}\nc)  {opts[2]}\nd)  {opts[3]}")

        #clears text from previous answer
        answer_entry.delete(0, tk.END)


    def check_and_next(event=None):
        nonlocal q_index, score

        #prompts user for answer
        user_input = answer_entry.get().strip().lower()

        #check if input is valid
        if user_input not in letter_map:
            feedback_label.config(text="Please enter 'a', 'b', 'c', or 'd'.")
            return

        #check correctness
        if letter_map[user_input] == int(answers[q_index][0]):
            score += 1
            feedback_label.config(text="Correct!")
        else:
            feedback_label.config(text=f"Incorrect! The correct answer was {int(answers[q_index][0])}.")
        q_index += 1

        #chooses whether to advance or finish
        if q_index < len(questions):
            display_current_question()
        else:
            prompt_label.config(text=f"Your Score: {score} / {len(questions)}")
            options_label.config(text="")
            q_num_label.config(text="")
            #remove input fields
            entry_label.pack_forget()
            answer_entry.pack_forget()
            submit_btn.pack_forget()

    #answer submit button
    submit_btn = tk.Button(new_window, text="Submit Answer", command=check_and_next, font=("Arial", 10))
    submit_btn.pack(pady=10)

    display_current_question()

#main application window
root = tk.Tk()
root.title("PrepAgain")
root.geometry("500x500")

#home page gui
tk.Label(root, text="Welcome to PrepAgain!", font=("Arial", 14)).pack(pady=(125, 5))
tk.Label(root, text="Select a Lesson:", font=("Arial", 12)).pack(pady=(25, 5))

lesson_dropdown = ttk.Combobox(root, values=lessons, state="readonly", width=30)
lesson_dropdown.current(0)
lesson_dropdown.pack(pady=10)

open_btn = tk.Button(root, text="Start Questions", command=open_question_window, font=("Arial", 10,))
open_btn.pack(pady=20)

#continues main loop
root.mainloop()