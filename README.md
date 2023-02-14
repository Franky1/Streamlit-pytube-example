# Streamlit pytube example project

A small example project to demonstrate how to use **pytube** together with streamlit.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)

## Resources

### Python Libraries

- streamlit
  - <https://streamlit.io/>
  - <https://docs.streamlit.io/>
- pytube
  - <https://github.com/pytube/pytube>
- yt-dlp
  - *predecessor of youtube-dl*
  - <https://github.com/yt-dlp/yt-dlp>
- youtube-dl
  - *seems to be not maintained anymore*
  - <https://github.com/ytdl-org/youtube-dl>
- ffmpeg-python
  - *wrapper for ffmpeg*
  - <https://github.com/kkroening/ffmpeg-python>
- sponsorblock.py
  - <https://github.com/wasi-master/sponsorblock.py>
- unidecode
  - <https://github.com/avian2/unidecode>
- fabric
  - <https://www.fabfile.org/>
- Paramiko
  - <https://github.com/paramiko/paramiko>
- AsyncSSH
  - <https://github.com/ronf/asyncssh>
- pysftp
  - *outdated*
  - <https://pysftp.readthedocs.io>
  - <https://sftptogo.com/blog/python-sftp/>

## ToDo

- [ ] Test it on Windows
- [ ] Before downloading, get the available stream formats first
- [ ] Add option to download the audio/video in different formats
- [ ] Add a progress bar for the download
- [ ] Make the download button disabled while downloading
- [ ] Accumulate the downloaded file in the temp folder
- [ ] Download the accumulated files as a zip file
- [ ] Add error handling and make it more robust
- [ ] Add options for file naming based on the video title, author, date, etc.
- [ ] Try other libraries e.g. `yt-dlp`
- [ ] Add cutting out the ads with sponsorblock
- [ ] Add multi column layout
- [ ] Add file transfer option with sftp, scp, etc.

## Status

> Work in progress. Not finished yet. Don't use it.
> Last changed: 2023-02-14
