import random
import json
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
from kivy.uix.popup import Popup

questions = [
    {"question": "What do you like to do on weekends?", "image": "images/question1.png",
     "options": ["Hiking", "Reading", "Watching Movies"]},
    {"question": "What's your favorite color?", "image": "images/question2.png", "options": ["Red", "Blue", "Green"]},
    {"question": "What's your ideal vacation?", "image": "images/question3.png",
     "options": ["Beach", "Mountains", "City"]},
    {"question": "What's your favorite type of music?", "image": "images/question4.png",
     "options": ["Rock", "Classical", "Pop"]},
    {"question": "Which pet do you prefer?", "image": "images/question5.png", "options": ["Dog", "Cat", "Fish"]},
    {"question": "What's your favorite season?", "image": "images/question6.png",
     "options": ["Summer", "Winter", "Spring"]},
    {"question": "What's your favorite meal of the day?", "image": "images/question7.png",
     "options": ["Breakfast", "Lunch", "Dinner"]},
    {"question": "What's your preferred mode of transportation?", "image": "images/question8.png",
     "options": ["Car", "Bicycle", "Walking"]},
    {"question": "What's your favorite hobby?", "image": "images/question9.png",
     "options": ["Painting", "Writing", "Gardening"]},
    {"question": "What's your favorite genre of movies?", "image": "images/question10.png",
     "options": ["Action", "Comedy", "Drama"]},
]


class QuizWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = random.sample(questions, len(questions))
        self.current_question_index = 0
        self.answers = []
        self.display_question()

    def display_question(self):
        self.clear_widgets()

        question = self.questions[self.current_question_index]

        question_label = Label(text=question['question'], size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0.6})
        question_image = Image(source=question['image'], size_hint=(1, 0.4), pos_hint={'x': 0, 'y': 0.2})

        self.add_widget(question_label)
        self.add_widget(question_image)

        for idx, option in enumerate(question['options']):
            button = Button(text=option, size_hint=(0.3, 0.1), pos_hint={'x': 0.35, 'y': 0.1 - idx * 0.12})
            button.bind(on_release=self.record_answer)
            self.add_widget(button)

        sound = SoundLoader.load('sounds/question.mp3')
        if sound:
            sound.play()

    def record_answer(self, instance):
        self.answers.append(instance.text)
        self.current_question_index += 1

        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.display_result()

    def display_result(self):
        self.clear_widgets()

        result_label = Label(text="You are a Right Triangle!", size_hint=(1, 0.2), pos_hint={'x': 0, 'y': 0.6})
        result_image = Image(source="images/result_triangle.png", size_hint=(1, 0.4), pos_hint={'x': 0, 'y': 0.2})

        self.add_widget(result_label)
        self.add_widget(result_image)

        sound = SoundLoader.load('sounds/result.mp3')
        if sound:
            sound.play()

        save_button = Button(text="Save Result", size_hint=(0.3, 0.1), pos_hint={'x': 0.35, 'y': 0.1})
        save_button.bind(on_release=self.save_result)
        self.add_widget(save_button)

    def save_result(self, instance):
        result_data = {
            "answers": self.answers,
            "result": "Right Triangle"
        }
        with open("result.json", "w") as f:
            json.dump(result_data, f)
        popup = Popup(title='Result Saved', content=Label(text='Your result has been saved!'), size_hint=(0.5, 0.5))
        popup.open()


class QuizApp(App):
    def build(self):
        return QuizWidget()


if __name__ == '__main__':
    QuizApp().run()
