import cv2
import numpy as np
import pytesseract
import glob
import os
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import PhotoImage
import threading
import xlsxwriter
import datetime

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# # you can convert any dataset images into jpeg format
# folder_path = "Dataset2"
# converted_folder_path = "Dataset"

# if not os.path.exists(converted_folder_path):
#     os.makedirs(converted_folder_path)

# for image_file in os.listdir(folder_path):
#     try:
#         image = Image.open(os.path.join(folder_path, image_file))
#         image.save(os.path.join(converted_folder_path, os.path.splitext(image_file)[0] + ".jpeg"), "JPEG")
#     except Exception as e:
#         print("Error in converting image : ", image_file, e)


root = tk.Tk()
root.configure(bg='#5E5E5E')
root.geometry("1000x550")
root.title("License plate detection")


       
style = ttk.Style()
style.configure('TButton', font=('calibri', 18), foreground="lightgray", background="steel blue", borderwidth=10, relief='solid')
style.map('TButton', foreground=[('pressed', 'white'), ('active', 'black')], background=[('pressed', '!disabled', 'blue'), ('active', 'gray')])


output1 = tk.Label(root, text="<License plate recognition by ZARS/>", font=("CG Times", 28, "bold"), fg="white", bg="black")
# output1.grid(row=0, column=4)
output1.place(relx=.5,rely=.1,anchor=CENTER)


array=[]
array1=[]


def Acc():    
    def accuracy(y_true, y_pred):
        correct = np.sum(y_true == y_pred)
        return correct / len(y_true)

    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    y = np.array(['MH20EE7598', 'DL10CE4581', 'EX52ULB', 'MISSRY', '208LHI2467', 'TS0964745', 'MH20EJ0365', '48007', 'V8LUV', 'MH1407T8831', 'MHO2FE8819', 'MH13AZ9256', 'MH53674', 
    'MH20DV2363', 'GJ8964645', 'RKOSYFT', 'MH20DV2366', 'MH12DE1433', 'GJO5JA1143', 'DK9835435', 'TC157123', 'KL2645009', 'TC157123', 'TSO7FX3534', 'KEG10A2555', 'M66YOB', 'MH09BJ93753', 'KAO3MG2784', '15LK10898', 'MH76MN8942', 'MH09MD2531S', 'KLO2BM4659', 'P03TC4945', 'CZ20FSE', 'PK76354343', 'BN4001YOTA', 'CGO4MF2250', 'MHJT4563752', 'MH27BE8570', 'KN05MK4498'])

    y_pred = np.array(array)

    # accuracy
    acc = accuracy(y, y_pred)
    print('Accuracy: {:.2f}%'.format(acc * 100))





def outrunner():

    label = tk.Label(root, bg="gray50")
    # label.grid(row=5, column=10, rowspan=15, columnspan=15, padx=10, pady=10, sticky='nw')
    label.place(relx=.5,rely=.5,anchor= CENTER)


    output_label1 = tk.Label(root, text="Dataset method", font=("Arial", 28, "bold"))
    # output_label1.grid(row=0, column=0)
    output_label1.place(relx=.5,rely=.1,anchor= CENTER)



    dir = os.path.dirname(__file__)
    # image_name = os.listdir('Dataset')
    # array=[]

    def runner():
        for image in glob.glob(dir+"/Dataset/*.jpeg") :
            
            image=cv2.imread(image)
            # image3 = imutils.resize(image, width=300)
            # cv2.imshow("original image", image)
            cv2.waitKey(500)
            
            image9 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # cv2.imshow("greyed image", gray_image)
            # cv2.waitKey(0)
            
            gray_image = cv2.bilateralFilter(image9, 11, 17, 17) 
            # cv2.imshow("smoothened image", gray_image)
            # cv2.waitKey(0)

            edged = cv2.Canny(gray_image, 30, 200) 
            # cv2.imshow("edged image", edged)
            # cv2.waitKey(0)

            cnts,new = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            image1=image.copy()
            cv2.drawContours(image1,cnts,-1,(0,255,0),3)
            # cv2.imshow("contours",image1)
            # cv2.waitKey(0)

            cnts = sorted(cnts, key = cv2.contourArea, reverse = True) [:30]
            screenCnt = 0
            image2 = image.copy()
            cv2.drawContours(image2,cnts,-1,(0,255,0),3)
            # cv2.imshow("Top 30 contours",image2)
            # cv2.waitKey(0)
            
            i = 7
            for c in cnts:
                    perimeter = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.018 * perimeter, True)
                    if len(approx) == 4: 
                            screenCnt = approx
                            x,y,w,h = cv2.boundingRect(c) 
                            new_img=image[y:y+h,x:x+w]
                            cv2.imwrite('./'+str(i)+'.png',new_img)
                            # i+=1
                            break
            try:          
                cv2.drawContours(image, [screenCnt.astype(int)], -1, (0, 255, 0), 3)
            # cv2.imshow("image with detected license plate", image)
            # cv2.waitKey(0)
            except AttributeError:
                print("cannot detect the vehicle")

            Cropped_loc = './7.png'
            # cv2.imshow("cropped", cv2.imread(Cropped_loc))
            plate = pytesseract.image_to_string(Cropped_loc, lang='eng')
            
            # to remove gap between plate numbers signs
            plate2 = ''.join(letter for letter in plate if letter.isalnum())
            
            def remove(plate2):
                return plate2.replace(" " , "")

            plate2 = plate2.strip()
            print(remove(plate2))
        
            
            image = Image.fromarray(image)
            image=image.resize((450, 300), Image.ANTIALIAS)
            image = ImageTk.PhotoImage(image)

            label.config(image=image)
            label.image = image
            root.update()
            root.after(500)
        
            array.append(plate2)

            output_label = tk.Label(root, text="Number on Plate : "+plate2, font=("Arial", 22, "bold"), fg="white", bg="black")
            # output_label.grid(row=20, column=10, pady=10, sticky='s')
            output_label.place(relx=.5,rely=.85,anchor= CENTER)
            root.update()
            root.after(500, output_label.destroy())
            

            # update the GUI with the output
            root.update_idletasks()


    console_thread = threading.Thread(target=runner)
    console_thread.start()




def inrunner():
    
    label1 = tk.Label(root, bg="gray50")
    label1.place(relx=.5,rely=.5,anchor= CENTER)
    
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
       widget.place_forget()
       
       

but1=ttk.Button(root, text= "--> Click Here for Dataset <--",width=50, command=lambda:[outrunner(),make_invisible(but2),make_invisible(but1),make_invisible(output1)])
# but1.grid(row = 1, column = 4,padx=200,pady = 100)
but1.place(height=75,relx=.5,rely=.35,anchor= CENTER)

but2=ttk.Button(root, text= "--> Click Here for Real-time <--",width=50, command=lambda:[inrunner()])
# but2.grid(row = 2, column = 4, pady = 5)
but2.place(height=75,relx=.5,rely=.6,anchor= CENTER)

root.mainloop()



Acc();      

    
#database
def Data_set(listdata):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output2.xlsx"
    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet()
    row = 0
    col = 0
    for item in listdata:
        # Add current date and time to each row of data
        now = datetime.datetime.now()
        date= now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        ws.write(row, col, date)
        ws.write(row, col+1, time)
        ws.write(row, col+2, item)
        row += 1
        
    wb.close()
    
    # Open the saved Excel fil
    if len(array) == 0:
        print("ntg")
    else:
        os.system(filename)

Data_set(array)


def Real_time(listdata):
    now = datetime.datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"output1.xlsx"
    wb = xlsxwriter.Workbook(filename)
    ws = wb.add_worksheet()
    row = 0
    col = 0
    for item in listdata:
        # Add current date and time to each row of data
        now = datetime.datetime.now()
        date= now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        ws.write(row, col, date)
        ws.write(row, col+1, time)
        ws.write(row, col+2, item)
        row += 1
        
    wb.close()
    
    # Open the saved Excel file
    if len(array1) == 0:
        print("ntg")
    else:
        os.system(filename)
    
Real_time(array1)




