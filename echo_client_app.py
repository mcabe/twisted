#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.relativelayout import RelativeLayout
install_twisted_reactor()


#A simple Client that send messages to the echo server
from twisted.internet import reactor, protocol

class EchoClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_connection(self.transport)

    def dataReceived(self, data):
        self.factory.app.print_message(data)

class EchoFactory(protocol.ClientFactory):
    protocol = EchoClient
    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        self.app.print_message("connection lost")

    def clientConnectionFailed(self, conn, reason):
        self.app.print_message("connection failed")


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.selectableview import SelectableView

# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None



    def build(self):
        root = self.setup_gui()
        self.username = ""
        #self.connect_to_server()
        return root

    def setup_gui(self):
        self.usern = TextInput(size_hint_y=0.1, multiline=False, text="your name here...")
        self.connectbutton = Button(size_hint_y=0.1, text="Connect", on_press=self.svr_con)
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        self.label2 = Label(text='Users...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.scroll = ScrollView(do_scroll_y=True, do_scroll_x=False, size=(250, 320))
        self.scroll2 = ScrollView(do_scroll_y=True, do_scroll_x=False, size=(250, 320))
        #self.onlineusers = ScrollView(do_scroll=True)
        self.scroll.add_widget(self.label)
        self.scroll2.add_widget(self.label2)
        self.layout.add_widget(self.usern)
        self.layout.add_widget(self.connectbutton)
        self.layout.add_widget(self.scroll)
        self.layout.add_widget(self.scroll2)
        self.layout.add_widget(self.textbox)
        return self.layout

    def svr_con(self, instance):
        #def connect_to_server(self):
            #print self.n.text
        reactor.connectTCP('localhost', 8000, EchoFactory(self))
        self.username = self.usern.text
        print self.username

    def on_connection(self, connection):
        self.connection = connection
        self.connection.write(str(self.username+"#Connect$"))
        self.print_message("connected successfully!--from client")

    def send_message(self, *args):
        msg = self.textbox.text
        if msg and self.connection:
            self.connection.write(str(self.username+"#"+self.textbox.text))
            self.textbox.text = ""
            self.label.text += "You wrote: "+"'"+msg+"'"+"\n"

    def print_message(self, msg):
        self.label.text += msg + "\n"


class User():
    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    TwistedClientApp().run()
