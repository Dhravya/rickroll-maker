from moviepy.editor import VideoFileClip, concatenate_videoclips


class Rickroller:

    @staticmethod
    def clip_maker(clip_path: str, output_path="output.mp4"):
        rickroll = VideoFileClip("rickroll.mp4")

        clip2 = VideoFileClip(clip_path)
        clip2 = clip2.subclip(0, clip2.duration - 15)

        # Get the 15 seconds only
        rickroll = rickroll.subclip(0.5, 15).resize(width=clip2.w)

        # Concatenate the two clips
        final_clip = concatenate_videoclips([clip2, rickroll], method="compose")

        final_clip.write_videofile(output_path)


if __name__ == "__main__":
    Rickroller().clip_maker(
        r"C:\Users\dhrav\Pictures\274309341_124665780124890_905868432853985379_n.mp4"
    )
