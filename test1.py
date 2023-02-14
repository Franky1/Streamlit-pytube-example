import re
from io import BytesIO
from pathlib import Path

import streamlit as st
from pytube import YouTube

st.set_page_config(page_title="Download Video", page_icon="🎵",
                layout="centered", initial_sidebar_state="collapsed")


@st.cache_data(show_spinner=False)
def download_video_to_buffer(url):
    buffer = BytesIO()
    youtube_video = YouTube(url)
    video = youtube_video.streams.filter(
        progressive="True", file_extension="mp4").order_by('resolution').desc()
    video_720p = video[0]
    default_filename = youtube_video.title
    default_filename = re.sub(r'[^\x00-\x7f]', '', default_filename).strip()  # remove special characters
    video_720p.stream_to_buffer(buffer)
    return default_filename, buffer


def main():
    st.title("Download video from Youtube")
    url = st.text_input("Insert Youtube URL:")
    if url:
        with st.spinner("Downloading Video Stream from Youtube..."):
            default_filename, buffer = download_video_to_buffer(url)
        st.subheader("Video Title")
        st.write(default_filename)
        title_vid = Path(default_filename).with_suffix(".mp4").name
        st.subheader("Watch the Video")
        st.video(buffer, format='video/mp4')
        st.subheader("Download Video File")
        st.download_button(
            label="Download mp4",
            data=buffer,
            file_name=title_vid,
            mime="video/mpeg")


if __name__ == "__main__":
    main()
