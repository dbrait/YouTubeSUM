#!/usr/bin/env python
# coding: utf-8
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from summarizer import Summarizer

import spacy
nlp = spacy.load("en_core_web_sm")

st.title("YouTube Summary Generator")

video_url = st.text_input("Input Video Url", "https://www.youtube.com/watch?v=xJ3e0RDbT1w&t=158s")

def extract_video_id(url):
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    return None

video_id = extract_video_id(video_url)
transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

ratio = st.sidebar.slider("Sentence keep ratio", 0.1, 0.9, 0.3)
min_length = st.sidebar.slider("Minimum Length of Summarization", 50, 99, 50)
max_length = st.sidebar.slider("Maxmium Length of Summarization", 100, 500, 200)
 

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

def sentence_text(text):
	tokens = nlp(text)
	sentences = [sent for sent in tokens.sents]
	sentences = str(sentences)
	punctuated_text = sentences.replace(",", ".")
	return punctuated_text


@st.cache
def bert_model(clean_text):
    model = Summarizer()
    result = model(clean_text, min_length=min_length, max_length=max_length, ratio=ratio)
    summarized_text = "".join(result)
    return summarized_text

full_text = gather_text(transcript_list)
clean_text = process_text(full_text)


def is_text_punctuated(clean_text):
	result = clean_text.count(".")
	if result > 5:
		punctuated_text = clean_text
	else:
		punctuated_text = sentence_text(clean_text)
	return punctuated_text



punctuated_text = is_text_punctuated(clean_text)
summarized_text = bert_model(punctuated_text)


st.header('Summarized text')
summarized_text



