import os 
import sys 

import requests
from moviepy.editor import VideoFileClip, concatenate_videoclips
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)


class Rickroller:
    """
    Rickroller class, contains everything required for generating rickrolls
    """

    def make(self, clip_path: str, output_path="output.mp4"):
        """
        Generates the rickroll itself. Essentially just concatenates the
        video clips together.
        :param clip_path: The path to the video clip to be used.
        :param output_path: The path to the output file. Default is output.mp4
        :return: None
        """
        rickroll = VideoFileClip("rickroll.mp4")

        # Check if clip_path is a URL, if yes, downloads it and changes the clip_path
        clip_path = self.__download_if_url(clip_path)

        clip2 = VideoFileClip(clip_path)
        clip2 = clip2.subclip(0, clip2.duration - 15)

        # We only want the first 15 seconds
        rickroll = rickroll.subclip(0.5, 15).resize(width=clip2.w)

        # Concatenate the two clips
        final_clip = concatenate_videoclips([clip2, rickroll], method="compose")

        final_clip.write_videofile(output_path)


    def __do_download(self, url) -> str:
        """
        The function that actually does the downloading part.
        Uses rich progress bar to show the progress.

        param url: The URL to download
        :return: The path to the downloaded file.
        """

        progress = Progress(
            TextColumn("[bold blue]{task.fields[filename]}", justify="right"),
            BarColumn(bar_width=None),
            "[progress.percentage]{task.percentage:>3.1f}%",
            "•",
            DownloadColumn(),
            "•",
            TransferSpeedColumn(),
            "•",
            TimeRemainingColumn(),
        )
        task_id = progress.add_task(url, filename="Rickroll.mp4")
        progress.console.log("Downloading {}".format(url))

        with progress:

            r = requests.get(url, stream=True)

            # Getting the content length to be marked as the total length of the download
            total = int(r.headers.get("content-length"), 0)
            with open(url.split("/")[-1], "wb") as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        progress.update(task_id, total=total, completed=f.tell())
        
        progress.console.log("Download complete")

        # This returns the filepath of downloaded
        return url.split("/")[-1]
        

    def __download_if_url(self, url: str):
        """
        Checks if it's a URL, if yes, downloads it.
        :return: None
        """
        if url.startswith("http"):
            url = self.__do_download(url)
        
        return url

if __name__ == "__main__":
    rickroller = Rickroller()

    # Can be used as a standalone script
    rickroller.make(sys.argv[1])