import os
from moviepy.video.io.VideoFileClip import VideoFileClip

def convert_mp4_to_wav(input_file, output_file):
    video_clip = VideoFileClip(input_file)
    audio_clip = video_clip.audio
    audio_clip.write_audiofile(output_file)
    audio_clip.close()

def convert_all_mp4_to_wav(directory):
    # Membuat folder 'Audio' di dalam folder input_directory
    output_directory = os.path.join(directory, "Audio")
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created folder: {output_directory}")

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.mp4'):
                mp4_path = os.path.join(root, file)

                # Menentukan nama file output di folder 'Audio'
                wav_filename = os.path.splitext(file)[0] + '.wav'
                wav_path = os.path.join(output_directory, wav_filename)

                print(f"Converting: {mp4_path} => {wav_path}")
                try:
                    convert_mp4_to_wav(mp4_path, wav_path)
                except Exception as e:
                    print(f"Failed to convert {mp4_path}: {e}")

if __name__ == "__main__":
    # Path ke folder di komputer kamu
    input_directory = r"D:\Akademik Polban\Tugas Akhir Telekomunikasi\Pro\Normalisasi_Dataset\Data Test\Pengujian"

    if not os.path.isdir(input_directory):
        print(f"Invalid directory path: {input_directory}")
    else:
        print(f"Processing folder: {input_directory}")
        convert_all_mp4_to_wav(input_directory)
        print(f"Conversion completed for: {input_directory}")