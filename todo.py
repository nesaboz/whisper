# TODO 

def State(Enum):
    idle = 0
    started_listening = 1
    started_processing = 2


@async
def start_listening():
    print("Start listening asynchronously")
    # start listening 


def stop_listening():
    print("Stop listening")
    

def pressed(state):
    if state == 0:
        start_listening()
        state = 1
    elif state == 1:
        stop_listening()
        state = 2
        processing()   # start this asynchronously
    elif state == 2:
        state = 0
        print("Stop processing")
    return state


@async
def processing():
    # this is timed operation (<30sec)
    some_operation()
    # when done
    state = 0


def main():
    state = 0
    while True:
        if button_pressed():
            state = pressed(state)
        sleep(0.05)