import pandas as pd
import youtube_dl
import csv
from pydub import AudioSegment
import tqdm

# reading csv into new dataframe
df = pd.read_csv("balanced_train_segments.csv") #original csv
df_copy = df.copy()

COUGHING_ID = "  /m/01b_21"


def find_cough_pos(df, wantedId):
    """
    find pos and append the row to initialized df
    return cough positions + non_cough positions (for dataset balancing)
    """
    yt_ids = list()
    strts = list()
    endts = list()
    cough_label = list()
    indices = list()
    # listOfPos used in return
    listOfPos = list()
    posLabels = (df[" positive_labels"])
    tracker = 0
    unknown = "#NAME?"
    for idx, label in enumerate(posLabels):
        #get coughing data ~45 coughing labels
        if(COUGHING_ID == label and df.iloc[idx,0]!=unknown):
            yt_ids.append(df.iloc[idx,0])
            strts.append(df.iloc[idx,1])
            endts.append(df.iloc[idx,2])
            cough_label.append("cough")            
            listOfPos.append(idx+2)
            indices.append(idx+2)
        #get non-coughing data
        elif(tracker < 45 and df.iloc[idx,0]!=unknown):
            yt_ids.append(df.iloc[idx,0])
            strts.append(df.iloc[idx,1])
            endts.append(df.iloc[idx,2])
            cough_label.append("non-cough")
            indices.append(idx+2)
            tracker +=1

    dict_items = {"YT_IDs": yt_ids, "start_time": strts, "end_time": endts, "label": cough_label, "index": indices}

    return listOfPos, dict_items

def download_from_csv(csv_file):
    """
    Downloads 
    Appends Youtube IDs to use in vids_to_clip function
    """
    f = open(csv_file)
    csv_f = csv.reader(f)
    next(csv_f)
    clip_dicts = {}
    for idx, row in enumerate((csv_f)):
        v1, v2, v3, v4 = row[1], row[2], row[3], row[4]
        cargo = download_clip(f"https://www.youtube.com/watch?v={v1}&feature=youtu.be&{v2}&{v3}", f"{v4}_{idx}", v1, row[5])[0]
        clip_dicts[cargo[0]] = cargo[1]
    print("Done downloading!")
    print(clip_dicts)
    return clip_dicts

    
# we need to get the .wav files of the yt videos on memory
def download_clip(url, name, YTID, idx):
    """
    Converts youtube video into a wav file for processing
    """
    outPath = f'/sound_board/{name}__{YTID}.wav'
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': outPath,
        'noplaylist': True,
        'continue_dl': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192', }]
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.cache.remove()
            info_dict = ydl.extract_info(url, download=False)
            ydl.prepare_filename(info_dict)
            ydl.download([url])
            return idx, outPath
    except Exception as e:
        print(e)
        return None
    


def main():
    """
    Calling all functions for data processing
    """
    listOfCoughIndices = find_cough_pos(df_copy, COUGHING_ID)[0]
    item_store = find_cough_pos(df_copy, COUGHING_ID)[1]

    item_df = pd.DataFrame.from_dict(item_store)

    item_df.to_csv("outputTest.csv")
    test_df = pd.DataFrame(listOfCoughIndices, columns=['Cough Video IDs'])
    test_df
    clip_dicts = download_from_csv("outputTest.csv")
    vids_to_clip(clip_dicts)

if __name__ == '__main__':
    main()



