import ffmpeg

def convert_to_8bit(input_file, output_file):
    try:
        (
            ffmpeg
            .input(input_file)
            .output(output_file, acodec="pcm_u8", ar="22050")
            .run()
        )
    except Exception as e:
        print(f"Conversion error: {e}")
