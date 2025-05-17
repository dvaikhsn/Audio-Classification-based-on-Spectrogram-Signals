import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
import numpy as np
import librosa
from skimage.transform import resize
from tensorflow.keras.models import load_model
from moviepy.video.io.VideoFileClip import VideoFileClip
import plotly.graph_objs as go
import os
import uuid

# Fungsi untuk mengekstrak audio dari video
def extract_audio_from_video(video_path):
    with VideoFileClip(video_path) as video:
        audio = video.audio
        audio_path = "extracted_audio.wav"
        audio.write_audiofile(audio_path)
    return audio_path

# Fungsi untuk mengubah audio jadi spektrogram
def audio_to_spectrogram(audio_path, target_shape=(128, 88)):
    audio_data, sample_rate = librosa.load(audio_path, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=audio_data, sr=sample_rate)
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)
    spectrogram_resized = resize(spectrogram_db, target_shape)
    spectrogram_resized = np.expand_dims(spectrogram_resized, axis=-1)
    return spectrogram_resized

# Fungsi klasifikasi video
def classify_video(video_path, model):
    audio_path = extract_audio_from_video(video_path)
    spectrogram = audio_to_spectrogram(audio_path)
    spectrogram = np.expand_dims(spectrogram, axis=0)
    prediction = model.predict(spectrogram)
    predicted_class = np.argmax(prediction)
    class_names = ["Audio Smash", "Audio Dropshot"]
    os.remove(audio_path)  # hapus audio setelah klasifikasi
    return class_names[predicted_class], prediction[0][predicted_class]

# Load model
model = load_model('Final_1.h5')

# App initialization
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1("SISTEM KLASIFIKASI GERAK PUKULAN BADMINTON", 
                style={'color': 'white', 'textAlign': 'center', 'padding': '10px'})
    ], style={'backgroundColor': '#4a4a4a', 'marginBottom': '20px'}),
    
    # Main Content
    html.Div([
        # Left Column - Video Upload and Display
        html.Div([
            html.H3("Video", style={'textAlign': 'center'}),
            dcc.Upload(
                id='upload-video',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select a Video File')
                ]),
                style={
                    'width': '90%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px auto'
                },
                multiple=False
            ),
            html.Div(id='video-display', style={'margin': '20px auto', 'textAlign': 'center'})
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
        
        # Right Column - Results
        html.Div([
            # Spectrogram Section
            html.Div([
                html.H3("Spektrogram Audio", style={'textAlign': 'center'}),
                dcc.Graph(id='spectrogram-plot', 
                          style={'height': '300px', 'margin': '10px auto'})
            ], style={'border': '1px solid #ddd', 'padding': '10px', 'marginBottom': '20px'}),
            
            # Prediction Results Section
            html.Div([
                html.H3("Hasil Prediksi", style={'textAlign': 'center'}),
                html.Div(id='prediction-result', 
                         style={
                             'textAlign': 'center', 
                             'fontSize': '20px',
                             'padding': '20px',
                             'backgroundColor': '#f5f5f5',
                             'borderRadius': '5px',
                             'margin': '10px'
                         })
            ], style={'border': '1px solid #ddd', 'padding': '10px'})
        ], style={'width': '45%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'})
    ], style={'width': '90%', 'margin': '0 auto'})
])

# Callback
@app.callback(
    [Output('video-display', 'children'),
     Output('prediction-result', 'children'),
     Output('spectrogram-plot', 'figure')],
    [Input('upload-video', 'contents')]
)
def update_output(video_content):
    if video_content is not None:
        try:
            # Decode dan simpan video
            content_type, content_string = video_content.split(',')
            video_data = base64.b64decode(content_string)
            video_path = f'uploaded_{uuid.uuid4().hex}.mp4'  # pakai UUID supaya beda tiap upload
            with open(video_path, 'wb') as f:
                f.write(video_data)
            
            # Menampilkan video
            encoded_video = base64.b64encode(open(video_path, 'rb').read())
            video_player = html.Video(
                src='data:video/mp4;base64,{}'.format(encoded_video.decode()),
                controls=True,
                style={'width': '90%', 'height': 'auto', 'margin': '10px auto'}
            )

            # Prediksi
            result, confidence = classify_video(video_path, model)

            # Membuat spektrogram
            audio_path = extract_audio_from_video(video_path)
            spectrogram = audio_to_spectrogram(audio_path)
            fig = go.Figure(data=go.Heatmap(
                z=spectrogram.squeeze(), 
                colorscale='Viridis',
                colorbar=dict(title='dB')
            ))
            fig.update_layout(
                title='',
                xaxis_title='Time',
                yaxis_title='Frequency',
                margin=dict(l=50, r=50, b=50, t=30),
                height=280
            )

            # Hapus file sementara
            os.remove(video_path)
            os.remove(audio_path)

            # Prediksi teks
            prediction_text = [
                html.P(f"Jenis Pukulan: {result}", style={'fontWeight': 'bold'}),
                html.P(f"Tingkat Akurasi: {confidence*100:.2f}%")
            ]

            return video_player, prediction_text, fig
        except Exception as e:
            print(f"Error di callback: {e}")
            return html.Div("Error processing video"), f"Terjadi error: {e}", go.Figure()

    return "", "", go.Figure()

# Run 
if __name__ == '__main__':
    app.run(debug=True)