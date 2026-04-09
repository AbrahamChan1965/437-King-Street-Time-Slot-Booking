#!/usr/bin/env python3
"""Create a 1080p MP4 music video from an audio track and background image."""

from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
)


def build_video(
    audio_path: str = "song.mp3",
    image_path: str = "background.jpg",
    output_path: str = "output.mp4",
    title: str = "Tyre: Silk & Cedar",
    fps: int = 30,
) -> None:
    """Render a 1920x1080 video matching the audio duration."""
    audio_clip = AudioFileClip(audio_path)

    canvas_size = (1920, 1080)
    duration = audio_clip.duration

    # Scale image to fill 1080p while preserving aspect ratio, then center-crop.
    background = (
        ImageClip(image_path)
        .resize(height=canvas_size[1])
        .set_duration(duration)
        .crop(width=canvas_size[0], height=canvas_size[1], x_center="center", y_center="center")
    )

    # Fallback base layer in case the source image has transparency.
    base_layer = ColorClip(size=canvas_size, color=(0, 0, 0), duration=duration)

    text_overlay = (
        TextClip(
            title,
            fontsize=60,
            color="white",
            stroke_color="black",
            stroke_width=2,
            method="caption",
            size=(canvas_size[0] - 120, None),
        )
        .set_duration(duration)
        .set_position(("center", canvas_size[1] - 130))
    )

    final = CompositeVideoClip([base_layer, background, text_overlay], size=canvas_size).set_audio(audio_clip)

    final.write_videofile(
        output_path,
        fps=fps,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True,
    )

    final.close()
    audio_clip.close()


if __name__ == "__main__":
    build_video()
