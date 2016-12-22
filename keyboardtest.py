import keyboard
import time

def read_file():
    a = []
    b = input()
    while b != 'EOF':
        a.append(b.split(' '))
        b = input()
    return a


if __name__ == '__main__':
    list_of_note = read_file()
    last_time = float(list_of_note[0][0])
    #print(last_time)
    keyboard.wait('space')
    for i in list_of_note:
        #print(float(i[0])+0.033 ,i[1] ,i[2])
        time.sleep(float(i[0]) - last_time)
        last_time = float(i[0])
        if i[2] == 'p':
            keyboard.press_and_release(i[1])
        elif i[2] == 'h':
            keyboard.press(i[1])
        elif i[2] == 'r':
            keyboard.release(i[1])
