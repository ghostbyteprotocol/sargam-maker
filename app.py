import streamlit as st
import subprocess
import os
import librosa
import numpy as np

st.set_page_config(page_title="Sargam Video Maker", layout="centered")
st.title("🎵 নিখুঁত সরগম পিচ ভিডিও মেকার")

uploaded_file = st.file_uploader("তোর গানের ফাইল আপলোড কর (MP3/WAV)", type=["mp3", "wav"])

if uploaded_file is not None:
    with open("input_song.mp3", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio("input_song.mp3")
    
    if st.button("ভিডিও তৈরি কর (Render 60fps)"):
        with st.spinner("Manim দিয়ে ফ্রেম-বাই-ফ্রেম নিখুঁত ভিডিও তৈরি হচ্ছে... ১-২ মিনিট অপেক্ষা কর..."):
            
            manim_code = """
from manim import *
import librosa
import numpy as np

class SargamScene(Scene):
    def construct(self):
        y, sr = librosa.load("input_song.mp3", duration=30) # প্রথম ৩০ সেকেন্ডের জন্য
        duration = librosa.get_duration(y=y, sr=sr)
        
        f0, _, _ = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C6'))
        times = librosa.times_like(f0, sr=sr)
        
        axes = Axes(
            x_range=[0, duration, 2],
            y_range=[100, 600, 100],
            x_length=11,
            y_length=5.5,
            axis_config={"color": GREY_B}
        )
        
        points = [axes.c2p(t, freq) for t, freq in zip(times, f0) if not np.isnan(freq)]
        
        graph = VMobject(color="#00FFCC", stroke_width=5)
        if len(points) > 1:
            graph.set_points_smoothly(points)
            
        self.add_sound("input_song.mp3")
        self.add(axes)
        self.play(Create(graph), run_time=duration, rate_func=linear)
        self.wait(0.5)
"""
            with open("render_script.py", "w") as f:
                f.write(manim_code)
                
            # Manim রেন্ডার কমান্ড (720p 60fps দ্রুত ও নিখুঁত আউটপুটের জন্য)
            subprocess.run(["manim", "-pqm", "--fps", "60", "render_script.py", "SargamScene"])
            
            video_path = "media/videos/render_script/720p60/SargamScene.mp4"
            if os.path.exists(video_path):
                st.success("ভিডিও একদম রেডি!")
                st.video(video_path)
                with open(video_path, "rb") as file:
                    st.download_button(
                        label="⬇️ ভিডিও ডাউনলোড কর (MP4)",
                        data=file,
                        file_name="perfect_sargam.mp4",
                        mime="video/mp4"
                    )
            else:
                st.error("কোথাও একটা সমস্যা হয়েছে, আবার চেষ্টা কর।")
