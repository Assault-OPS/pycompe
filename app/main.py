import kivy
import requests.exceptions
from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import RoundedRectangle,Color
from kivy.lang import Builder
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager,Screen, FadeTransition, SlideTransition
from kivy.uix.popup import Popup
from tkinter import filedialog
from requests import get,post
from io import BytesIO
from pdfdocument.document import PDFDocument
from random import shuffle

#initialize kivy version
kivy.require('2.1.0')

ip = "127.0.0.1"
url = f"http://{ip}:5000/api/v3?full=true"


#Builder.load_file('appstyle.kv')

window = Window

class MyPopup(Popup):
    def __init__(self,title,text,**kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.size_hint = (0.5,0.3)
        self.title = title
        self.content = Label(text=text)
        self.opacity = 0.75

    def open(self, *_args, **kwargs):
        super().open()

#custom button
class MyButton(Button):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.font_name = 'fonts/AGENCYR'
        self.font_size = 20
        self.size_hint_y = None
        self.height = 50
        self.size_hint_x = None
        self.width = 200
        self.background_color[3] = 0.5
        
            

#custom text input
class MyTextInput(TextInput):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.foreground_color = (1,1,1,0.75)
        self.background_color = (0,0,0,0.5)
        self.size_hint = (None,None)
        self.height = 30
        self.width = 200



class SelectFilePopup:
    def __init__(self,title,initialdir):
        self.title = title
        self.path = None
        self.initialdir = initialdir

    def open_file(self):
        self.path = filedialog.askopenfilename(
            initialdir=self.initialdir,
            title=self.title,
            filetypes=(("PNG Files","*.png"),("JPG Files","*.jpg"))
        )

    def open_docx(self):
        self.path = filedialog.askopenfilename(
            initialdir=self.initialdir,
            title=self.title,
            filetypes=(("Word Files","*.docx"),("Word Files","*.docx"))
        )

    def open_dir(self):
        self.path = filedialog.askdirectory(
            initialdir=self.initialdir,
            title=self.title
        )
        return self.path

    def getDir(self):
        return self.path


class Interface(GridLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 1
        with self.canvas.before:
            self.bg = Image(source='assets/background.jpg').texture
            self.rect = Rectangle(texture=self.bg, pos=self.pos, size=self.size)
            self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self,*args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class LoginPage(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.LoginLayout = GridLayout(cols=2) # Layout for the Login page
        self.mainLayout = BoxLayout() # Layout for the main stuff
        self.Layout2 = AnchorLayout()
        self.Layout3 = GridLayout(
            size_hint_y=None,
            height=120,
            size_hint_x=None,
            width=300,
            spacing=10
        )
        self.cols = 2
        self.Layout2.orientation = 'vertical'
        self.Layout2.cols = 3
        self.Layout3.cols = 2
        self.Layout3.add_widget(Label(
            text="Enter Username ".upper(),
            font_size=25,
            font_name='fonts/AGENCYR'
        )
        )
        self.usernameInp = MyTextInput(multiline=False)
        self.Layout3.add_widget(self.usernameInp)
        self.Layout3.add_widget(Label(
            text="Enter Password ".upper(),
            font_size=25,
            font_name='fonts/AGENCYR'
        )
        )
        self.passwordInp = MyTextInput(multiline=False, password=True)
        self.Layout3.add_widget(self.passwordInp)
        self.loginButton = MyButton(
            text='LOGIN',
            background_color=(0, 1, 0, 0.5)
        )
        self.skipButton = MyButton(
            text='SKIP LOGIN'
        )
        self.loginButton.bind(on_release=self.switch_layout)
        self.skipButton.bind(on_release=self.switch_layout)
        self.Layout3.add_widget(self.loginButton)
        self.Layout3.add_widget(self.skipButton)
        self.Layout2.add_widget(self.Layout3)
        self.LoginLayout.add_widget(self.Layout2)
        self.LoginLayout.add_widget(
            Label(
                text="intelliDoc",
                font_size=50,
                font_name='fonts/BAUHS93.otf'
            )
        )
        self.add_widget(self.LoginLayout)

    def switch_layout(self,*args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'main'

class MainScreen(Screen):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.CenterLayout = FloatLayout()
        #self.MainLayout = BoxLayout(orientation='vertical', spacing=10)
        StartButton = MyButton(
            text='START SCANNING',
            background_color=(0, 1, 0, 0.5),
            pos_hint={'center_x':0.5,'center_y':0.6}
        )
        SettingButton = MyButton(
            text='Settings',
            background_color=(1,1,1,0.5),
            pos_hint={'center_x':0.5,'center_y':0.5}
        )
        ReturnButton = MyButton(
            text='Log out',
            background_color=(1, 0, 0, 0.5),
            pos_hint={'center_x':0.5,'center_y':0.4}
        )
        StartButton.bind(on_release=self.switch_to_ScanScreen)
        ReturnButton.bind(on_release=self.switch_to_LoginScreen)
        SettingButton.bind(on_release=self.switch_to_SettingScreen)
        self.CenterLayout.add_widget(StartButton)
        self.CenterLayout.add_widget(SettingButton)
        self.CenterLayout.add_widget(ReturnButton)
        self.add_widget(self.CenterLayout)

    def switch_to_LoginScreen(self, *args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'login'

    def switch_to_SettingScreen(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'setting'

    def switch_to_ScanScreen(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'scan'


class SettingScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text='COMING SOON'))
        self.BackButton = MyButton(
            text = 'BACK'
        )
        self.BackButton.bind(on_release=self.switch_to_MainScreen)
        self.add_widget(self.BackButton)

    def switch_to_MainScreen(self,*args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'


class ScanScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.Layout = BoxLayout(padding=30)
        self.ButtonsLayout = FloatLayout()
        self.imagedisplay = None
        self.GenerateButton = None
        self.jsondata = None
        self.RealBrowseButton = MyButton(
            text="BROWSE FILE",
            pos_hint={'center_x':0.5,'center_y':0.6},
            background_color=(1,1,0,0.5)
        )
        self.BrowseButton = MyButton(
            text="SCAN IMAGE",
            pos_hint={'center_x':0.5,'center_y':0.6},
            background_color=(1,1,0,0.5)
        )
        self.TextButton = MyButton(
            text="TEXT PROMPT",
            pos_hint={'center_x':0.5,'center_y':0.5},
            background_color=(1,1,0,0.5)

        )
        self.DocxButton = MyButton(
            text="DOCUMENT FILE",
            pos_hint={'center_x':0.5,'center_y':0.4},
            background_color=(1,1,0,0.5)

        )
        self.BackButton = MyButton(
            text="CANCEL",
            background_color=(1,0,0,0.5)
        )
        self.BrowseButton.bind(on_release=self.Work)
        self.TextButton.bind(on_release=self.switch_to_TextInput)
        self.DocxButton.bind(on_release=self.switch_to_docx)
        self.BackButton.bind(on_release=self.switch_to_MainScreen)
        self.ButtonsLayout.add_widget(self.BrowseButton)
        self.ButtonsLayout.add_widget(self.TextButton)
        self.ButtonsLayout.add_widget(self.DocxButton)
        self.ButtonsLayout.add_widget(self.BackButton)
        self.Layout.add_widget(self.ButtonsLayout)
        self.add_widget(self.Layout)

    def switch_to_MainScreen(self,*args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'
        if self.imagedisplay is not None:
            self.Layout.remove_widget(self.imagedisplay)
        if self.GenerateButton is not None:
            self.ButtonsLayout.remove_widget(self.GenerateButton)
            self.ButtonsLayout.remove_widget(self.BrowButton)
            self.GenerateButton = None
        self.ButtonsLayout.clear_widgets()
        self.ButtonsLayout.add_widget(self.BrowseButton)
        self.ButtonsLayout.add_widget(self.TextButton)
        self.ButtonsLayout.add_widget(self.DocxButton)
        self.ButtonsLayout.add_widget(self.BackButton)

    def switch_to_TextInput(self,*args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'text'

    def Work(self,*args):
        filename = ScanScreen.askfile()
        if filename != '':
            try:
                if self.imagedisplay is not None:
                    self.Layout.remove_widget(self.imagedisplay)
                if self.GenerateButton is None:
                    self.ButtonsLayout.remove_widget(self.BrowseButton)
                    self.ButtonsLayout.remove_widget(self.TextButton)
                    self.ButtonsLayout.remove_widget(self.DocxButton)
                    self.BrowButton = MyButton(
                        text='BROWSE FILE',
                        pos_hint={'center_x':0.5,'center_y':0.6},
                        background_color=(0,1,1,0.5)
                    )
                    self.GenerateButton = MyButton(
                        text='GENERATE QNA',
                        pos_hint={'center_x':0.5,'center_y':0.5},
                        background_color=(0,1,1,0.5)
                    )
                    self.GenerateButton.bind(
                        on_release=lambda instance: Clock.schedule_once(lambda unknown:self.ProcessDocument(url,filename,'img'))
                    )
                    self.BrowButton.bind(on_release=self.Work)
                    self.ButtonsLayout.add_widget(self.GenerateButton)
                    self.ButtonsLayout.add_widget(self.BrowButton)
                self.imagedisplay = Image(source=filename,pos_hint={'center_x':0.5,'center_y':0.5})
                self.Layout.add_widget(self.imagedisplay)
            except AttributeError:
                pass
    
    def switch_to_docx(self,*args):
        filename = ScanScreen.askdocx()
        if filename != '':
            try:
                if self.imagedisplay is not None:
                    self.Layout.remove_widget(self.imagedisplay)
                if self.GenerateButton is None:
                    self.ButtonsLayout.remove_widget(self.BrowseButton)
                    self.ButtonsLayout.remove_widget(self.TextButton)
                    self.ButtonsLayout.remove_widget(self.DocxButton)
                    self.BrowButton = MyButton(
                        text='BROWSE FILE',
                        pos_hint={'center_x':0.5,'center_y':0.6},
                        background_color=(0,1,1,0.5)
                    )
                    self.GenerateButton = MyButton(
                        text='GENERATE QNA',
                        pos_hint={'center_x':0.5,'center_y':0.5},
                        background_color=(0,1,1,0.5)
                    )
                    self.GenerateButton.bind(
                        on_release=lambda instance: Clock.schedule_once(lambda unknown:self.ProcessDocument(url,filename,'docx'))
                    )
                    self.BrowButton.bind(on_release=self.switch_to_docx)
                    self.ButtonsLayout.add_widget(self.GenerateButton)
                    self.ButtonsLayout.add_widget(self.BrowButton)
                self.imagedisplay = Image(source='assets/docx.png',pos_hint={'center_x':0.5,'center_y':0.5})
                self.Layout.add_widget(self.imagedisplay)
            except AttributeError:
                pass

    @staticmethod
    def askfile():
        popup = SelectFilePopup("Select Image","/")
        popup.open_file()
        return popup.getDir()
    
    @staticmethod
    def askdocx():
        popup = SelectFilePopup("Select Document File","/")
        popup.open_docx()
        return popup.getDir()

    @staticmethod
    def askdir():
        popup = SelectFilePopup("Select Directory","/")
        return popup.open_dir()

    @staticmethod
    def pdf_gen(data):
        f = BytesIO()
        pdf = PDFDocument(f)
        pdf.init_report()
        pdf.h1('MCQ Questions:')
        for index, i in enumerate(data.get('mc_qs').get('questions'), 1):
            pdf.p(f"{index}. {i.get('question_statement')}")
            int_list = [j for j in i.get('options')]
            int_list.append(i.get('answer'))
            shuffle(int_list)
            pdf.p(f"• {' • '.join(int_list)}\n")
        pdf.h1('Answers: ')
        for index, i in enumerate(data.get('mc_qs').get('questions'), 1):
            pdf.p(f"{index}. {i.get('answer')}")
        pdf.p("\n")
        pdf.h1('Single Questions:')
        for index, i in enumerate(data.get('short_qs').get('questions'), 1):
            pdf.p(f"{index}. {i.get('Question')}")
        pdf.p("\n")
        pdf.h1('Answers: ')
        for index, i in enumerate(data.get('short_qs').get('questions'), 1):
            pdf.p(f"{index}. {i.get('Answer')}")
        pdf.p("\n")
        pdf.h1('Extracted Text:')
        pdf.p(f"{data.get('text')['input_text']}")
        pdf.generate()
        dir = ScanScreen.askdir()
        with open(f'{dir}/doc.pdf', 'wb') as file:
            file.write(f.getvalue())
    
    @staticmethod
    def ConnectServer(server_url,files=None,_type=None):
        print(_type)
        if _type!='text':
            r = post(server_url+f"&type={_type}",files={'file':open(files,'rb')})
        else:
            r = post(server_url+f"&type={_type}",json={'text':files})
        return r.json()
    

    def ProcessDocument(self,server_url,filepath,_type):
        try:
            self.jsondata = self.ConnectServer(server_url,filepath,_type)
            self.pdf_gen(self.jsondata)
            popup = MyPopup("Success","Document generated successfully.",title_color=(0,1,0,1))
            popup.open()
            self.ButtonsLayout.add_widget(self.BrowseButton)
            self.ButtonsLayout.add_widget(self.TextButton)
            self.ButtonsLayout.add_widget(self.DocxButton)
            self.switch_to_MainScreen()
        except requests.exceptions.ConnectionError:
            popup = MyPopup("Error","Unable to connect to the server. Please try again later.",title_color=(1,0,0,1))
            popup.open()
            self.switch_to_MainScreen()
            return
        except PermissionError:
            popup = MyPopup("Error","Cannot write file: Permission denied.",title_color=(1,0,0,1))
            popup.open()
            self.switch_to_MainScreen()
        except Exception as e:
            raise e

class TextScreen(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.Layout = BoxLayout(orientation='vertical')
        txtinp = TextInput(
            multiline=True,
            size_hint=(1,1),
            foreground_color=(1, 1, 1, 0.75),
            background_color=(0, 0, 0, 0.5)
        )
        self.GenerateButton = MyButton(
            text='GENERATE QNA',
            pos_hint={'center_x':0.5,'center_y':0.5},
            background_color=(0,1,1,0.5)
        )

        self.GenerateButton.bind(
            on_release=lambda instance: Clock.schedule_once(lambda unknown:self.ProcessDocument(url,txtinp.text,'text'))
        )
        self.Layout2 = FloatLayout()
        self.BackButton = MyButton(
            text="CANCEL",
            background_color=(1,0,0,0.5)
        )
        self.BackButton.bind(on_release=self.switch_to_ScanScreen)
        self.Layout2.add_widget(self.BackButton)
        self.Layout.add_widget(txtinp)
        self.Layout.add_widget(self.GenerateButton)
        self.Layout.add_widget(self.Layout2)
        self.add_widget(self.Layout)

    def switch_to_ScanScreen(self, *args):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'scan'
    def switch_to_MainScreen(self,*args):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main'
    def ProcessDocument(self,server_url,filepath,_type,*args):
        try:
            self.jsondata = ScanScreen.ConnectServer(server_url,filepath,_type)
            ScanScreen.pdf_gen(self.jsondata)
            popup = MyPopup("Success","Document generated successfully.",title_color=(0,1,0,1))
            popup.open()
            # self.ButtonsLayout.add_widget(self.BrowseButton)
            # self.ButtonsLayout.add_widget(self.TextButton)
            # self.ButtonsLayout.add_widget(self.DocxButton)
            self.switch_to_ScanScreen()
        except requests.exceptions.ConnectionError:
            popup = MyPopup("Error","Unable to connect to the server. Please try again later.",title_color=(1,0,0,1))
            popup.open()
            self.switch_to_MainScreen()
            return
        except PermissionError:
            popup = MyPopup("Error","Cannot write file: Permission denied.",title_color=(1,0,0,1))
            popup.open()
            self.switch_to_MainScreen()
        except Exception as e:
            raise e


class MyApp(App):
    def build(self):
        self.title = 'intelliDoc'
        ParentLayout = Interface()
        screen_manager = ScreenManager()
        loginScreen = LoginPage(name='login')
        mainScreen = MainScreen(name='main')
        mainSettingScreen = SettingScreen(name='setting')
        scanScreen = ScanScreen(name='scan')
        textScreen = TextScreen(name='text')
        screen_manager.add_widget(loginScreen)
        screen_manager.add_widget(mainScreen)
        screen_manager.add_widget(mainSettingScreen)
        screen_manager.add_widget(scanScreen)
        screen_manager.add_widget(textScreen)
        ParentLayout.add_widget(screen_manager)
        return ParentLayout


# starting app
app = MyApp()

if __name__ == '__main__':
    app.run()
