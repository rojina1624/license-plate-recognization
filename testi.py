import cv2
import imutils
import pytesseract
import glob
import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import PhotoImage
import threading
import xlsxwriter

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
root.geometry("700x450")
root.title("Number plate detection by dataset")
array=[]

def outrunner():

    label = tk.Label(root)
    label.grid(row=0, column=3)


    output_label1 = tk.Label(root, text="Plate detected Image =", font=("Arial", 28, "bold"))
    output_label1.grid(row=0, column=0, pady =10)



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
            image=image.resize((250, 200))
            image = ImageTk.PhotoImage(image)

            label.config(image=image)
            label.image = image
            root.update()
            root.after(500)
        
            array.append(plate2)

            output_label = tk.Label(root, text="Number on Plate = "+plate2, font=("Arial", 18, "bold"))
            output_label.grid(row=i, column=0)
            root.update()
            root.after(500, output_label.destroy())
            

            # update the GUI with the output
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

    cap.release()
    cv2.destroyAllWindows()


def make_invisible(widget):
       widget.grid_forget()

but1=ttk.Button(root, text= "Click Here for Dataset",width=50, command=lambda:[outrunner(),make_invisible(but2),make_invisible(but1)])
but1.grid(row = 0, column = 2,padx=200,pady = 100)
but2=ttk.Button(root, text= "Click Here for Real-time",width=50, command=lambda:[inrunner()])
but2.grid(row = 1, column = 2, pady = 5)

root.mainloop()



        
#database
def insert_data(listdata):
    wb = xlsxwriter.Workbook("output1.xlsx")
    ws = wb.add_worksheet()
    row = 0
    col = 0
    for item in listdata:
        ws.write(row, col , item)
        row += 1
        
    wb.close()

insert_data(array)
os.system("output1.xlsx")





