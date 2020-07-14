import pandas as pd

df = pd.read_csv("balanced_train_segments.csv") #original csv
df_copy = df.copy()

COUGHING_ID = "  /m/01b_21"


def find_cough_pos(df, wantedId):
    listOfPos = list()
    result = df.isin([wantedId])
    seriesId = result.any()

    print(result[1179:1190], seriesId[1179:1190])

    #List of columns that have the wanted ids
    columnNames = list(seriesId[seriesId == True].index)

    for col in columnNames:
        rows = list(result[col][result[col] == True].index)
        for row in rows:
            listOfPos.append(row)
        
    return listOfPos

listOfCoughIndices = find_cough_pos(df_copy, COUGHING_ID)

print(f"Cough IDs: {listOfCoughIndices}")


test_df = pd.DataFrame(listOfCoughIndices, columns=['Cough Video IDs'])
test_df


#following line outputs same as listOfCoughIndices but formatted
#find_cough_pos(df_copy, COUGHING_ID)




