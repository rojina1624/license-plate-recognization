import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import cv2
import numpy as np
import pytesseract
import threading
import glob

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

root = tk.Tk()
root.geometry("1100x550")
root.title("License plate detection")

style = ttk.Style()
style.configure('TButton', font=('calibri',20,'bold'),borderwidth = '4')

array=[]
array1=[]

def Acc():    
    def accuracy(y_true, y_pred):
        correct = np.sum(y_true == y_pred)
        return correct / len(y_true)

    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    y = np.array(['MH20EE7598', 'DL10CE4581', 'EX52ULB', 'MISSRY', '208LHI2467', 'TS0964745', 'MH20EJ0365', '48007', 'V8LUV', 'MH1407T8831', 'MHO2FE8819', 'MH13AZ9256', 'MH53674', 'MH20DV2363', 'GJ8964645', 'RKOSYFT', 'MH20DV2366', 'MH12DE1433', 'GJO5JA1143', 'DK9835435', 'TC157123', 'KL2645009', 'TC157123', 'TSO7FX3534', 'KEG10A2555', 'M66YOB', 'MH09BJ93753', 'KAO3MG2784', '15LK10898', 'MH76MN8942', 'MH09MD2531S', 'KLO2BM4659', 'P03TC4945', 'CZ20FSE', 'PK76354343', 'BN4001YOTA', 'CGO4MF2250', 'MHJT4563752', 'MH27BE8570', 'KN05MK4498'])

    y_pred = np.array(array)

    # accuracy
    acc = accuracy(y, y_pred)
    print('Accuracy: {:.2f}%'.format(acc * 100))


def outrunner():
    label = tk.Label(root)
    label.grid(row=5, column=14)

    output_label1 = tk.Label(root, text="Image :", font=("Arial", 28, "bold"))
    output_label1.grid(row=0, column=5)

    dir = os.path.dirname(__file__)

    def runner():
        for image in glob.glob(dir+"/Dataset/*.jpeg"):
            image=cv2.imread(image)
            cv2.waitKey(500)

            image9 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            gray_image = cv2.bilateralFilter(image9, 11, 17, 17)

            edged = cv2.Canny(gray_image, 30, 200)

            cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            image1=image.copy()
            cv2.drawContours(image1,cnts,-1,(0,255,0),3)

            cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
            screenCnt = 0
            image2 = image.copy()
            cv2.drawContours(image2,cnts,-1,(0,255,0),3)

            i = 7
            for c in cnts:
                perimeter = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
                if len(approx) == 4:
                    screenCnt = approx
                    x,y,w,h = cv2.boundingRect(c)
                    new_img=image[y:y+h,x:x+w]
                    cv2.imwrite('./'+str(i)+'.png',new_img)
                    break
            try:          
                cv2.drawContours(image, [screenCnt.astype(int)], -1, (0, 255, 0), 3)
            except AttributeError:
                print("cannot detect the vehicle")

            Cropped_loc = './7.png'
            plate = pytesseract.image_to_string(Cropped_loc, lang='eng')

            # to remove gap between plate numbers signs
            plate2 = ''.join(letter for letter in plate if letter.isalnum())

            def remove(plate2):
                return plate2.replace("" , "")

            plate2 = plate2.strip()
            print(remove(plate2))

            image = Image.fromarray(image)
            image=image.resize((450, 300))
            image = ImageTk.PhotoImage(image)

            label.config(image=image)
            label.image = image
            root.update()
            root.after(500)

            array.append(plate2)

            output_label = tk.Label(root, text="Number on Plate : "+plate2, font=("Arial", 22, "bold"))
            output_label.grid(row=20, column=15)
            root.update()
            root.after(500, output_label.destroy())

            root.update_idletasks()

    console_thread = threading.Thread(target=runner)
    console_thread.start()


def inrunner():
    cap = cv2.VideoCapture(0)

    while(True):
        ret,image = cap.read()
        cv2.imshow("original image", image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.bilateralFilter(gray_image, 11, 17, 17)

        edged = cv2.Canny(gray_image, 30, 200)

        cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        image1=image.copy()
        cv2.drawContours(image1,cnts,-1,(0,255,0),3)

        cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
        screenCnt = 0
        image2 = image.copy()
        cv2.drawContours(image2,cnts,-1,(0,255,0),3)

        i=7
        for c in cnts:
            perimeter = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
            if len(approx) == 4:
                screenCnt = approx
                x,y,w,h = cv2.boundingRect(c)
                new_img=image[y:y+h,x:x+w]
                cv2.imwrite('./'+str(i)+'.png',new_img)
                i+=1
                break
        try:          
            cv2.drawContours(image, [screenCnt.astype(int)], -1, (0, 255, 0), 3)

        except AttributeError:
            print("cannot detect the vehicle")

        Cropped_loc = './7.png'

        plate = pytesseract.image_to_string(Cropped_loc, lang='eng')

        plate2 = ''.join(letter for letter in plate if letter.isalnum())

        def remove(plate2):
            return plate2.replace(" " , "")

        plate2 = plate2.strip()
        print(remove(plate2))

        if len(plate2)==10 or len(plate2)==9 or len(plate2)==8:
            array1.append(plate2)
            root.destroy()
            break

    cap.release()
    cv2.destroyAllWindows()

def make_invisible(widget):
    widget.grid_forget()

but1=ttk.Button(root, text= "Click Here for Dataset",width=50, command=lambda:[outrunner(),make_invisible(but2),make_invisible(but1)])
but1.grid(row = 0, column = 4,padx=200,pady = 100)

but2=ttk.Button(root, text= "Click Here for Real-time",width=50, command=lambda:[inrunner()])
but2.grid(row = 1, column = 4, pady = 5)

root.mainloop()