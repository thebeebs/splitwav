from pydub import AudioSegment
from io import BytesIO
from pydub.silence import split_on_silence
import base64
import os

with open(os.environ['inputBlob'], "rb") as wav_file:
    sound = AudioSegment.from_file(wav_file, format="wav")
    chunks = split_on_silence(
        sound,
        # split on silences longer than 1000ms (1 sec)
        min_silence_len=100,
        # anything under -50 dBFS is considered silence
        silence_thresh=-50, 
        # keep 200 ms of leading/trailing silence
        keep_silence=200
    )

    # now recombine the chunks so that the parts are at least 2 minutes
    target_length = 120 * 1000
    output_chunks = [chunks[0]]
    for chunk in chunks[1:]:
        if len(output_chunks[-1]) < target_length:
            output_chunks[-1] += chunk
        else:
            # if the last output chunk is longer than the target length,
            # we can start a new one
            output_chunks.append(chunk)


    for index in range(len(output_chunks)):
        output_chunks[index].export(os.environ['part' + str(index + 1)], format="wav")
