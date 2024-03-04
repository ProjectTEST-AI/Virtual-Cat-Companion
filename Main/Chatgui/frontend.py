import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.clock import Clock
from threading import Thread
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.graphics import Color, Rectangle
import requests

kivy.require('2.0.0')  # Replace with your current kivy version!

# Change the color of the window background
Window.clearcolor = (0.2, 0.2, 0.2, 1)

# Set window size
Window.size = (500, 650)

class ChatMessage(BoxLayout):
    def __init__(self, message, is_user=True, **kwargs):
        super(ChatMessage, self).__init__(**kwargs)
        self.orientation = 'horizontal' if is_user else 'horizontal'
        self.size_hint_y = None
        self.height = 100  # Increase height for better visibility

        # Update the styling for the chat bubble
        bubble = BoxLayout(orientation='vertical', padding=10, size_hint_y=None)
        bubble.bind(minimum_height=bubble.setter('height'))

        # Create the label for the message text with word wrapping
        message_label = Label(text=message, markup=True, halign='left', valign='middle', size_hint_y=None)
        message_label.bind(width=lambda *x: message_label.setter('text_size')(message_label, (self.width - 100, None)),
                           texture_size=lambda *x: message_label.setter('height')(message_label, message_label.texture_size[1]))
        message_label.text_size = (self.width - 100, None)
        bubble.add_widget(message_label)

        # Decide which image to use based on who is sending the message
        img_source = 'user.png' if is_user else 'ai.png'

        # Create the Image widget and add it to the layout
        image = Image(source=img_source, size_hint=(None, 1), width=50)

        if is_user:
            self.add_widget(image)
            self.add_widget(bubble)
        else:
            self.add_widget(bubble)
            self.add_widget(image)

        # Add a background color to the chat bubble
        with bubble.canvas.before:
            Color(rgba=(0.3, 0.3, 0.3, 1) if is_user else (0.1, 0.1, 0.1, 1))
            self.rect = Rectangle(size=bubble.size, pos=bubble.pos)

        bubble.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ChatInterface(BoxLayout):
    def __init__(self, **kwargs):
        super(ChatInterface, self).__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = 10
        self.padding = [10, 10, 10, 10]

        # BoxLayout to contain the chat history
        self.chat_history_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.chat_history_layout.bind(minimum_height=self.chat_history_layout.setter('height'))

        # Scrollable view for chat history
        self.chat_history = ScrollView(size_hint=(1, 0.8), do_scroll_x=False)
        self.chat_history.add_widget(self.chat_history_layout)
        self.add_widget(self.chat_history)

        # User input
        self.user_input = TextInput(size_hint=(1, 0.1), multiline=False)
        self.user_input.bind(on_text_validate=self.on_enter)
        self.add_widget(self.user_input)

        # Send button
        send_button = Button(text="Send", size_hint=(1, 0.1))
        send_button.bind(on_press=self.on_send_press)
        self.add_widget(send_button)

    def on_enter(self, instance):
        self.send_message_to_ai()

    def on_send_press(self, instance):
        self.send_message_to_ai()

    def update_chat_history(self, message, is_user=True):
        # Call this method from the main thread
        chat_message = ChatMessage(message, is_user=is_user)
        self.chat_history_layout.add_widget(chat_message)
        # Scroll to the latest message
        self.chat_history.scroll_to(chat_message)
        
    def send_message_to_ai(self):
        user_message = self.user_input.text
        self.user_input.text = ''
        if user_message:
            self.update_chat_history(user_message)
            # Use a thread to avoid freezing the UI
            Thread(target=self.call_virtual_cat_companion, args=(user_message,)).start()

    def call_virtual_cat_companion(self, user_input):
        try:
            response = requests.post('http://localhost:5000/ask', json={'input': user_input}).json()
            # Schedule the message update to happen on the main thread
            Clock.schedule_once(lambda dt: self.update_chat_history(response['response'], is_user=False))
        except requests.RequestException as e:
            # Handle connection error
            print(f"Error: {e}")

    def build(self):
        # Set the background color for the entire layout
        with self.canvas.before:
            Color(rgba=(0.05, 0.05, 0.05, 1))  # Dark background color
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(pos=self.update_rect, size=self.update_rect)
        return super(ChatInterface, self).build()

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class VirtualCatApp(App):
    def build(self):
        self.title = 'VirtualCat'  # Set a title for the window
        return ChatInterface()

if __name__ == "__main__":
    VirtualCatApp().run()