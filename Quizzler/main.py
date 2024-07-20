import random
import customtkinter as ctk
import requests
from PIL import Image ,ImageTk
import html
from question_model import Question
from ui import QuizInterface
from quiz_brain import QuizBrain

all_questions = [] # conatins all the quiz questions.

# available quiz categories.
categories = {    
    "Anime" : 31,
    "Gadgets" : 30,
    "Sports" : 21,
    "Computers" : 18,
}

# category obtained from user(default set to "Anime")
category_text = "Anime"
# difficulty obtained from user(default set to "easy")
difficulty_text = "easy"

def close_window():
    '''Removes all the existing widgets from the window and starts the quiz'''

    global all_questions
    for widget in app.winfo_children():
        widget.destroy()
            
    category_code = categories[category_text]

    parameter = {
        "amount":10,
        "category" : int(category_code),
        "difficulty": difficulty_text,
        "type":"multiple",
    }

    response = requests.get(url = "https://opentdb.com/api.php", params=parameter)
    response.raise_for_status()

    data = response.json()
    new_data = data["results"]


    all_questions = []  

    for questions in new_data:
        option_B = html.unescape(questions["incorrect_answers"][1])
        option_A = html.unescape(questions["incorrect_answers"][0])
        option_C = html.unescape(questions["incorrect_answers"][2])
        option_D = html.unescape(questions["correct_answer"])

        # correct option among all four
        correct_ans = option_D
        # question
        question = html.unescape(questions["question"])
        # options list
        ls = [option_A, option_B, option_C, option_D]
        random.shuffle(ls)
        new_question = Question(question=question, options=ls, answer=correct_ans)
        all_questions.append(new_question)

    quiz = QuizBrain(all_questions)
    ui = QuizInterface(quiz,app)

def get_c_text(selected_val):
    '''Assigns the value in option menu to category text.'''
    global category_text 
    category_text = selected_val

def get_diff_text(selected_val):
    '''Assigns the value in option menu to difficulty text.'''
    global difficulty_text
    difficulty_text = selected_val

app = ctk.CTk()
app.geometry("300x500")
app.title("Quizzler")
app.resizable(False, False) 
app.config(bg="#C8ACD6")
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ls = [key for (key, value) in categories.items()]
diff_ls = ["easy", "medium", "hard"]

# adding quiz graphic.
image_path = "quiz.jpg"
pil_image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(pil_image)

# adding canvas for the quiz start graphic.
canvas = ctk.CTkCanvas(app, width=600, height=500,bg="#C8ACD6", highlightthickness=0)
canvas.create_image(210, 250,image=tk_image)
canvas.grid(row=0, column=0)

# adding option for category and difficulty.
options_c = ctk.CTkOptionMenu(app, values=ls, fg_color="#433D8B", bg_color="#C8ACD6", command=get_c_text)
options_c.grid(row=1,column=0,pady=20)

options_diff = ctk.CTkOptionMenu(app, values=diff_ls, fg_color="#433D8B", bg_color="#C8ACD6", command=get_diff_text)
options_diff.grid(row=2,column=0,pady=20)

# adding labels
label_c = ctk.CTkLabel(app, text="Select Category:",fg_color="#C8ACD6",
                       bg_color="#C8ACD6",font=("arial",17),
                       text_color="#433D8B",
                       )
label_c.grid(row=1,column=0,sticky="w")

label_diff = ctk.CTkLabel(app, text="Select Difficulty:",fg_color="#C8ACD6",
                          bg_color="#C8ACD6",font=("arial",17),
                          text_color="#433D8B",
                          )
label_diff.grid(row=2,column=0,sticky="w")

# start button
start = ctk.CTkButton(app, text="Start", bg_color="#C8ACD6",fg_color="#433D8B",command=close_window)
start.grid(row=3,column=0)

app.mainloop()





