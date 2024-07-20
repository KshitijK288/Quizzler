import customtkinter as ctk
from PIL import Image, ImageTk
from quiz_brain import QuizBrain

GREEN = "#88D66C"
RED = "#FF7777"
nxt_question = None

class QuizInterface:
    def __init__(self, quiz:QuizBrain,app:ctk.CTk) -> None:
        self.quiz = quiz
        self.app = app

        self.frame = ctk.CTkFrame(self.app, width=260,
                                  height=240,bg_color="#C8ACD6",
                                  fg_color="#433D8B",
                                  corner_radius=20,
                                 )
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        # Label
        long_text = "This is a very long text that should wrap to the next line if it exceeds the specified width. bcbwebfuuuhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh"
        self.question_label = ctk.CTkLabel(self.app, text=long_text, wraplength=200,
                                           font = ("Arial", 20),
                                           text_color="white",
                                           bg_color="#433D8B",
                                           )
        self.question_label.grid(row=0, column=0,padx=10, pady=10)
        # optionA
        self.optionA = ctk.CTkButton(self.app, text="OptionA",
                                     width=260,
                                     height=40,
                                     bg_color="#C8ACD6",
                                     fg_color="#433D8B",
                                     corner_radius=20,
                                     compound="right",
                                     command=self.option_a,
                                     )

        self.optionA.grid(row=1, column=0, padx=20)
        # optionB
        self.optionB = ctk.CTkButton(self.app, text="OptionB",
                                     width=260,
                                     height=40,
                                     bg_color="#C8ACD6",
                                     fg_color="#433D8B",
                                     corner_radius=20,
                                     command=self.option_b,
                                    )
        self.optionB.grid(row=2, column=0, padx=20, pady=10)
        # oprionC
        self.optionC = ctk.CTkButton(self.app, text="OptionC",
                                     width=260,
                                     height=40,
                                     bg_color="#C8ACD6",
                                     fg_color="#433D8B",
                                     corner_radius=20,
                                     command=self.option_c,
                                    )
        self.optionC.grid(row=3, column=0, padx=20)
        # optionD
        self.optionD = ctk.CTkButton(self.app, text="OptionD",
                                     width=260,
                                     height=40,
                                     bg_color="#C8ACD6",
                                     fg_color="#433D8B",
                                     corner_radius=20,
                                     command=self.option_d,
                                    )
        self.optionD.grid(row=4, column=0, padx=20, pady=10)
        

        self.get_nxt_question()

        self.app.mainloop()


    def get_nxt_question(self):
        ls = [self.optionA, self.optionB, self.optionC, self.optionD]
        for i in range(4):
            ls[i].configure(fg_color = "#433D8B")
        
        if self.quiz.still_has_questions():
            question, options = self.quiz.next_question()
            self.question_label.configure(text=question)
            option_a = options[0]
            option_b = options[1]
            option_c = options[2]
            option_d = options[3]

            self.optionA.configure(text=option_a)
            self.optionB.configure(text=option_b)
            self.optionC.configure(text=option_c)
            self.optionD.configure(text=option_d)
        else:
            self.question_label.configure(text="You have reached the end")
            self.optionA.configure(state="disabled")
            self.optionB.configure(state="disabled")
            self.optionC.configure(state="disabled")
            self.optionD.configure(state="disabled")

            self.optionA.configure(text="")
            self.optionB.configure(text="")
            self.optionC.configure(text="")
            self.optionD.configure(text="")

            self.app.after_cancel(nxt_question)

            self.show_final_score()

    def option_a(self):
        self.give_feedback(self.quiz.check_answer(self.optionA.cget("text")))

    def option_b(self):
        self.give_feedback(self.quiz.check_answer(self.optionB.cget("text")))

    def option_c(self):
        self.give_feedback(self.quiz.check_answer(self.optionC.cget("text")))

    def option_d(self):
        self.give_feedback(self.quiz.check_answer(self.optionD.cget("text")))

    def clear_widgets(self):
        for widget in self.app.winfo_children():
            widget.destroy()

    def give_feedback(self,is_correct:bool):
        global nxt_question
        if is_correct:
            self.quiz.score += 1
        
        correct_ans = self.quiz.get_correct_ans()
        ls = [self.optionA, self.optionB, self.optionC, self.optionD]
        for i in range(4):
            if ls[i].cget("text") == correct_ans:
                ls[i].configure(fg_color = GREEN)
            else:
                ls[i].configure(fg_color = RED)

        nxt_question = self.app.after(1000, self.get_nxt_question)

    def show_final_score(self):
        self.clear_widgets()
        self.app.geometry("300x500")

        
        image_path = "end.png"
        pil_image = Image.open(image_path)
        self.tk_image = ImageTk.PhotoImage(pil_image)

        canvas = ctk.CTkCanvas(self.app, width=600, height=500,bg="#C8ACD6", highlightthickness=0)
        canvas.create_image(230, 250,image=self.tk_image)
        canvas.grid(row=0, column=0,columnspan=2)

        self.new_frame = ctk.CTkFrame(self.app, width=100, 
                                height=60,bg_color="#C8ACD6",
                                fg_color="#433D8B",
                                corner_radius=20,
                                )
        self.new_frame.grid(row=1, column=0,pady=20,padx=50)


        self.score = ctk.CTkLabel(self.app, text=f"Score: {self.quiz.score}",
                                    bg_color="#433D8B",
                                    font=("arial",20),
                                    )
        
        self.score.grid(row=1, column=0,pady=20,padx=50)
