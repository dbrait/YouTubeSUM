#!/usr/bin/env python
# coding: utf-8

from youtube_transcript_api import YouTubeTranscriptApi
from summarizer import Summarizer


video_id = 'kEMJRjEdNzM&list=PLoROMvodv4rOhcuXMZkNm7j3fVwBBY42z&index=2'
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
 
#with open('your_file.txt', 'w') as f:
#    for item in transcript_list:
#        f.write("%s\n" % item)


def gather_text(transcript_list):
    full_text = []
    length = len(transcript_list)
    for i in range(length):
        t = transcript_list[i]["text"]
        full_text.append(t)
    return full_text


def process_text(full_text):
    clean_text = "".join(map(str, full_text))
    return clean_text


def bert_model(clean_text):
    model = Summarizer()
    result = model(clean_text, min_length=60, max_length=500, ratio=0.2)
    summarized_text = "".join(result)
    return summarized_text


full_text = gather_text(transcript_list)
clean_text = process_text(full_text)
print(bert_model(clean_text))



