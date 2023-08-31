import numpy as np
ARRAY=[]
# Define the evaluation metric (accuracy for binary classification)
def accuracy(y_true, y_pred):
    correct = np.sum(y_true == y_pred)
    return correct / len(y_true)

# Load the dataset (assuming X is the input data and y is the ground truth labels)
X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
y = np.array(['MH20EE7598', 'DL10CE4581', 'aEX52ULB', 'MISSRY', '208LHI2467', 'aSS', 'WH20EJ0365', '48007', 'V8LUV', 'MH1407T8831', 'MHO2FE8819', 'MH13AZ9256', 'a', 
'MH20DV2363', '', 'RKOSYFT', 'MH20DV2366', 'MH12DE1433', 'GJO5JA1143', '', 'TC157123', 'KL2645009', 'TC157123', 'TSO7FX3534', 'KEG10A2555', 'M66YOB', '', 'KAO3MG2784', '15LK10898', '', '', 'KLO2BM4659', 'P03TC4945', 'CZ20FSE', '', 'BN4001YOTAPH9810916666Sy', 'CGO4MF2250', '', 'MH27BE8570', 'KN05MK4498'])

# Make predictions using your model (assuming y_pred is the predicted labels)
y_pred = np.array(ARRAY)
# Calculate accuracy for the entire dataset
acc = accuracy(y, y_pred)
print('Accuracy: {:.2f}%'.format(acc * 100))


    # def insert_data(listdata):
#     wb = xlsxwriter.Workbook("output1.xlsx")
#     ws = wb.add_worksheet()
#     row = 0
#     col = 0
#     for item in listdata:
#         ws.write(row, col , item)
#         row += 1
        
#     wb.close()

# insert_data(array)
# os.system("output1.xlsx")

