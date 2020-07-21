from stem import Signal
from stem.control import Controller

def switch_ip():
    with Controller.from_port() as controller:
        controller.authenticate()
        controller.signal(Signal.NEWNYM)