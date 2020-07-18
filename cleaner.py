#extract relevant features from audio by downsampling and removing noise
import matplotlib.pyplot as plt
from scipy.io import wavfile
import argparse
import os
from glob import glob
import numpy as np
import pandas as pd
from librosa.core import resample, to_mono
from tqdm import tqdm

def envelope(freq, rate, threshold):
    bolMask = []
    series = pd.Series(freq).apply(np.abs)
    #sliding window basically (window= 10th of a sec) => returns a series
    y_max = series.rolling(window=int(rate/10), min_periods=1, center=True).max()

    for max in y_max:
        if max > threshold:
            bolMask.append(True)
        else:
            bolMask.append(False)
    return bolMask, y_max

def mono_converter(path, sr):
    rate, wav = wavfile.read(path)
    wav = wav.astype(np.float32, order='F')
    try:
        tmp = wav.shape[1]
        wav = to_mono(wav.T)
    except:
        pass
    wav = resample(wav, rate, sr)
    wav = wav.astype(np.int16)
    return sr, wav

def save_sample(sample, rate, target_dir, file, idx):
    file = file.split('.wav')[0]
    outPath = os.path.join(target_dir.split('.')[0], f"{file}_{idx}.wav")
    if(os.path.exists(outPath)):
        return
    wavfile.write(outPath, rate, sample)

def check_dir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    
def split_wavs(args):
    src_root = args.src_root
    dst_root = args.dst_root
    dt = args.delta_time
    #get all wav paths from sub dirs (hence rec is True)
    wav_paths = glob(f"{src_root}/**", recursive=True)
    wav_paths = [x for x in wav_paths if '.wav' in x]
    dirs = os.listdir(src_root)
    for c in dirs:
        target_dir = os.path.join(dst_root, c)
        check_dir(target_dir)
        src_dir = os.path.join(dst_root, c)
        for file in tqdm(os.listdir(src_dir)):
            src_file = os.path.join(src_dir, file)
            rate, wav = mono_converter(src_file, args.sr)
            mask, y_max = envelope(wav, rate, threshold=args.threshold)
            wav = wav[mask]
            #delta sample
            ds = int(dt*rate)

            if(wav.shape[0] < ds):
                sample = np.zeros(shape=(delta_sample,), dtype=np.int16)
                sample[:wav.shape[0]] = wav
                save_sample(sample, rate, target_dir, fn, 0)

            else:
                leftovers = wav.shape[0] % ds
                #arrange => like range but for np
                for idx, i in enumerate(np.arrange(0,wav.shape[0]-leftovers, ds)):
                    strt = int(i)
                    end = int(i+ds)
                    sample = wav[strt:end]
                    save_sample(sample, rate, target_dir, file, cnt)

def test_threshold(args):
    src_root = args.src_root
    wav_paths = glob('{}/**'.format(src_root), recursive=True)
    wav_path = [x for x in wav_paths if args.fn in x]
    if len(wav_path) != 1:
        print('audio file not found for sub-string: {}'.format(args.fn))
        return
    rate, wav = mono_converter(wav_path[0], args.sr)
    mask, env = envelope(wav, rate, threshold=args.threshold)
    plt.style.use('ggplot')
    plt.title('Signal Envelope, Threshold = {}'.format(str(args.threshold)))
    plt.plot(wav[np.logical_not(mask)], color='r', label='remove')
    plt.plot(wav[mask], color='c', label='keep')
    plt.plot(env, color='m', label='envelope')
    plt.grid(False)
    plt.legend(loc='best')
    plt.show()

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Cleaning audio data')
    parser.add_argument('--src_root', type=str, default='wavfiles',
                        help='directory of audio files in total duration')
    parser.add_argument('--dst_root', type=str, default='clean',
                        help='directory to put audio files split by delta_time')
    parser.add_argument('--delta_time', '-dt', type=float, default=1.0,
                        help='time in seconds to sample audio')
    parser.add_argument('--sr', type=int, default=16000,
                        help='rate to downsample audio')

    parser.add_argument('--fn', type=str, default='3a3d0279',
                        help='pick random file to check plot')
    parser.add_argument('--threshold', type=str, default=20,
                        help='threshold magnitude for np.int16 dtype')
    print(parser.parse_known_args())
    #the second value would be a list arguments user may entered that the program doesn't recognize
    args, _ = parser.parse_known_args()
    #test_threshold(args)
    split_wavs(args)
