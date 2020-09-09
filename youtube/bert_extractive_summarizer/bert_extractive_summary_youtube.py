#!/usr/bin/env python
# coding: utf-8
#pip install youtube_transcript_api
#pip install bert-extractive-summarizer

from youtube_transcript_api import YouTubeTranscriptApi
from summarizer import Summarizer

#fill in with video
def video(id="2B9b9mUPJik&list=PL851F45079A91C3F2"):
    video_id = id
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    #print(transcript_list[0])
    #print(transcript_list[1])
    #print(transcript_list[2])

    with open('your_file.txt', 'w') as f:
        for item in transcript_list:
            f.write("%s\n" % item)


def process_text(transcript_list):
    full_text = []
    length = len(transcript_list)
    for i in range(length):
        t = transcript_list[i]["text"]
        full_text.append(t)
        #print(transcript_list[0]["text"])
        full_text = ''.join(map(str, full_text))

def bert_model(full_text):
    #f = full_text
    model = Summarizer()
    result = model(full_text, min_length=60, max_length=500, ratio=0.2)
    summarized_text = "".join(result)


print(summarized_text)





