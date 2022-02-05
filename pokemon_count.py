import PySimpleGUI as sg
from multiprocessing import Process
import pygame


EXIT = False

def updateScreen():
    layout = [
           [sg.Text("", size=(40, 1), key='-TEXT-')],
           [sg.Button("Sair")]
           ]

    window = sg.Window("Title", layout, finalize=True)  
    while True:
        try:
            event, values = window.read(timeout=10)
            value = readvalue('count.txt')
            window.Element('-TEXT-').update(value)
            if event == "Sair" or event == sg.WIN_CLOSED:
                print("Saindo")
                EXIT = True
                break
        except:
            print("Saindo")
            break 




def contador():
    pygame.init()

    j = pygame.joystick.Joystick(0)
    j.init()
    count = 0
    filename = 'count.txt'
    r2_press = False
    r2_x = False
    inc = 1
    r2_press = False
    r2_x = False
    try:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.JOYBUTTONDOWN:
                    if j.get_button(5):
                        count = readvalue(filename)
                        value = count + inc
                        writevalue(filename, value)
                        print("count:",value)
                    elif j.get_button(15):
                        print("Começando nova run:")
                        print('count: 0')
                        writevalue(filename, 0)
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 5:
                        if r2_press == False and round(event.value,2) > 0.81:
                            r2_press = True
                            count = readvalue(filename)
                            value = count + inc
                            writevalue(filename, value)
                            print("count:",value)
                        elif round(event.value,2) <= 0.81:
                            r2_press = False
                            r2_x = False
                elif event.type == pygame.JOYBUTTONDOWN:
                    if r2_x == False  and event.button == 0 and r2_press == True:
                        count = readvalue(filename)
                        value = count - inc
                        writevalue(filename, value)
                        print("count:",value)
                        r2_x = True
            if EXIT:
                j.quit()
                print("EXITING NOW")
                break

    except KeyboardInterrupt:
        print("EXITING NOW")
        j.quit()

def writevalue(filename ,value):
    f = open("count.txt", 'w')
    f.write(str(value))
    f.close()

def readvalue(filename):
    f = open("count.txt", 'r')
    value = int(f.read())
    f.close()
    return value


#f = open("count.txt", 'r+')


if __name__ == "__main__":

    p1 = Process(target=updateScreen)
    p2 = Process(target=contador)
    p2.start()
    p1.start()
    p1.join()
    p2.terminate()
    p2.join()

    
    