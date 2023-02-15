import re
import tempfile
import uuid
from io import BytesIO
from pathlib import Path

import pandas as pd
import streamlit as st
from pytube import YouTube


# set basic streamlit page config
st.set_page_config(page_title="Youtube Download", page_icon="🎵",
                layout="centered", initial_sidebar_state="collapsed")

# apply custom css if needed
# with open('utils/style.css') as css:
#     st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


@st.cache_data
def make_safe_filename_re(s: str) -> str:
    return re.sub(r'[^\x00-\x7f]', '_', s).strip("_").replace("__", "_").replace("__", "_")


# convert string to a safe filename
@st.cache_data
def make_safe_filename(s: str) -> str:
    def safe_char(c):
        if c.isalnum():
            return c
        else:
            return "_"
    return "".join(safe_char(c) for c in s).strip("_").replace("__", "_").replace("__", "_")


@st.cache_data
def get_youtube_metadata(url: str) -> dict:
    '''Get youtube video metadata and return it as dict
    '''
    videodata = {'exception': None}
    try:
        youtube_video = YouTube(url)
    except Exception as e:
        videodata['exception'] = e
    else:
        videodata['title'] = youtube_video.title
        videodata['author'] = youtube_video.author
        videodata['length'] = youtube_video.length
        videodata['views'] = youtube_video.views
        videodata['publish_date'] = youtube_video.publish_date
        videodata['streams'] = youtube_video.streams.asc()
    return videodata


@st.cache_data
def download_video_to_file(url: str, tmpdirname: Path) -> tuple(str, Path):
    '''Download video to file and return title and file path
    param url: youtube url
    param tmpdirname: path to temp dir
    '''
    youtube_video = YouTube(url)
    title = youtube_video.title
    video = youtube_video.streams.filter(progressive="True", file_extension="mp4").order_by('resolution').desc()[0]
    filename = make_safe_filename(title)
    file_path = tmpdirname.joinpath(f"{filename}.mp4")
    video.download(filename=file_path)
    # TODO: add exception handling here
    return title, file_path


@st.cache_data
def download_video_to_buffer(url: str) -> tuple(str, str, BytesIO):
    '''Download video to buffer and return title, filename and buffer
    param url: youtube url
    '''
    buffer = BytesIO()
    youtube_video = YouTube(url)
    title = youtube_video.title
    video = youtube_video.streams.filter(progressive="True", file_extension="mp4").order_by('resolution').desc()[0]
    filename = make_safe_filename(title)
    video.stream_to_buffer(buffer)
    # TODO: add exception handling here
    return title, filename, buffer


@st.cache_data
def download_audio_to_file(url: str, tmpdirname: Path) -> tuple(str, Path):
    '''Download audio to file and return title and file path
    param url: youtube url
    param tmpdirname: path to temp dir
    '''
    youtube_video = YouTube(url)
    title = youtube_video.title
    audio = youtube_video.streams.get_audio_only()
    filename = make_safe_filename(title)
    file_path = tmpdirname.joinpath(f"{filename}.mp3")
    audio.download(filename=file_path)
    # TODO: add exception handling here
    return title, file_path


@st.cache_data
def download_audio_to_buffer(url: str) -> tuple(str, str, BytesIO):
    '''Download audio to buffer and return title, filename and buffer
    param url: youtube url
    '''
    buffer = BytesIO()
    youtube_video = YouTube(url)
    title = youtube_video.title
    audio = youtube_video.streams.get_audio_only()
    filename = make_safe_filename(title)
    audio.stream_to_buffer(buffer)
    # TODO: add exception handling here
    return title, filename, buffer


# FIXME: this is maybe not working on windows due to issues with TemporaryDirectory()
@st.cache_data
def make_tempdir() -> Path:
    '''Make temp dir for each user session and return path to it
    '''
    if 'tempfiledir' not in st.session_state:
        tempfiledir = Path(tempfile.gettempdir())
        tempfiledir = tempfiledir.joinpath(f"streamlit_{uuid.uuid4()}")   # make unique subdir
        tempfiledir.mkdir(parents=True, exist_ok=True)  # make dir if not exists
        st.session_state['tempfiledir'] = tempfiledir
    return st.session_state['tempfiledir']


# make pandas dataframe from video metadata
@st.cache_data
def get_dataframe_from_metadata(_videodata, url=None) -> pd.DataFrame:
    del _videodata['streams']
    del _videodata['exception']
    del _videodata['views']
    _videodata_list = [_videodata]
    return pd.DataFrame(_videodata_list).set_index('title')


# make pandas dataframe from list of streams
@st.cache_data
def make_dataframe_from_streams(_streams, url=None) -> pd.DataFrame:
    rows = list()
    for stream in _streams:
        row = stream.__dict__
        del row['_monostate']
        del row['url']
        rows.append(row)
    return pd.DataFrame.from_dict(data=rows).set_index('itag')


def main():
    tmpdirname = make_tempdir()
    st.title("Download Audio from Youtube 🎵")
    url = st.text_input("Paste Youtube URL here:")
    if url:
        videodata = get_youtube_metadata(url)
        # TODO: add exception handling here
        st.subheader("Metadata")
        # st.write({key: videodata[key] for key in videodata if key != 'streams'})
        df_metadata = get_dataframe_from_metadata(videodata.copy(), url=url)
        st.write(df_metadata)
        st.subheader("Streams")
        df_streams = make_dataframe_from_streams(videodata.get('streams').fmt_streams.copy(), url=url)
        st.write(df_streams)
        # st.write(videodata.get('streams').fmt_streams[0].__dict__)
        title_vid, data_file_path = download_audio_to_file(url, tmpdirname)
        print(f"data_file_path: {data_file_path}")
        st.subheader("Title")
        st.info(title_vid)
        file_name = data_file_path.name
        st.subheader("File Name")
        st.info(file_name)
        with open(data_file_path, "rb") as f:
            buffer = f.read()
        st.subheader("Download Audio File")
        st.download_button(
            label="Download mp3",
            data=buffer,
            file_name=file_name,
            mime="audio/mpeg")


if __name__ == "__main__":
    main()
