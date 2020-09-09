#!/usr/bin/env python
# coding: utf-8
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from summarizer import Summarizer
from urllib.parse import urlparse, parse_qs

from string import punctuation
from collections import Counter

st.title("YouTube Summary Generator")

video_url = st.text_input("input video url", "")

def extract_video_id(url):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail?
    return None

video_id = extract_video_id(video_url)
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)


ratio = st.sidebar.slider("Sentence keep ratio", 0.1, 0.9, 0.3)
min_length = st.sidebar.slider("Minimum Length of Summarization", 50, 99, 50)
max_length = st.sidebar.slider("Maxmium Length of Summarization", 100, 500, 200)
 
#with open('your_file.txt', 'w') as f:
#    for item in transcript_list:
#        f.write("%s\n" % item)

@st.cache
def gather_text(transcript_list):
    full_text = []
    length = len(transcript_list)
    for i in range(length):
        t = transcript_list[i]["text"]
        full_text.append(t + " ")
    return full_text

@st.cache
def process_text(full_text):
    clean_text = "".join(map(str, full_text))
    return clean_text

@st.cache
def bert_model(clean_text):
    model = Summarizer()
    result = model(clean_text, min_length=min_length, max_length=max_length, ratio=ratio)
    summarized_text = "".join(result)
    return summarized_text

full_text = gather_text(transcript_list)
clean_text = process_text(full_text)
summarized_text = bert_model(clean_text)


st.header('Summarized text'), summarized_text



