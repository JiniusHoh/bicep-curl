# import cv2
# import mediapipe as mp
# import numpy as np
# import streamlit as st
# from gtts import gTTS
# import base64
# from webcam import webcam


# def autoplay_audio(file_path):
#     with open(file_path, "rb") as f:
#         data = f.read()
#     b64 = base64.b64encode(data).decode()
#     return b64

# def create_audio_html(b64_data):
#     html_string = f"""
#         <audio controls autoplay="true">
#             <source src="data:audio/mp3;base64,{b64_data}" type="audio/mp3">
#         </audio>
#     """
#     return html_string


# # Initialize MediaPipe's drawing utilities and pose module
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return int(angle)

# def app():
#     st.set_page_config(layout="wide")  # Set the layout to wide
#     st.title("Left Bicep Curl Exercise")
#     remind_text = "Make sure to allow access to your camera and speaker. Refresh the website if there is a lag."
#     st.markdown(remind_text)  # Display remark below the frame
#     remark_text = "If there is no autoplay sound, press the most bottom audio play button once to autoplay the feedback sound. Might need some time to start autoplay the feedback sound."
#     st.markdown(remark_text)  # Display remark below the frame

#     # GIF placeholder
#     gif_path = 'bicep_curl.gif'  # Replace with the path to your GIF file
#     # CSS to control the size of the GIF
#     st.markdown(
#         """
#         <style>
#         .small-gif {
#             width: 1000px;
#             height: auto;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )
#     gif_placeholder = st.empty()

#     start_button = st.button('Start Exercise')


#     if start_button:
#         gif_placeholder.empty()  # Clear the GIF
#         stframe = st.empty()

#         # cap = cv2.VideoCapture(0)
#         captured_image = webcam()

#         # Set initial values for stage and counter
#         counter = 0
#         stage = "down"
#         sequence_stage = "Initial"
#         feedback_status = ""
#         last_feedback = ""

#         def play_audio(feedback_text, filename):
#             tts = gTTS(feedback_text)
#             tts.save(filename)
#             audio_file = filename

#             b64_data = autoplay_audio(audio_file)
#             html_content = create_audio_html(b64_data)
#             st.markdown(html_content, unsafe_allow_html=True)

#         with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
#             while captured_image is True:
#                 ret, frame = captured_image.read()
#                 if not ret:
#                     break

#                 image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB for processing
#                 image.flags.writeable = False

#                 results = pose.process(image)

#                 image.flags.writeable = True
#                 image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)  # Convert back to BGR for OpenCV

#                 try:
#                     landmarks = results.pose_landmarks.landmark

#                     shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
#                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#                     elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
#                                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#                     wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
#                                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

#                     angle = calculate_angle(shoulder, elbow, wrist)

#                     if angle > 160 and sequence_stage != "Bicep Curl":
#                         sequence_stage = "Straighten Arms"
#                         stage = "down"
#                         feedback_status = "Arms straightened. Go to curl."
#                     elif sequence_stage == "Straighten Arms" and angle < 110 and stage == "down":
#                         sequence_stage = "Bicep Curl"
#                         stage = "up"
#                         counter += 1
#                         print(counter)

#                     # Update feedback status on each frame
#                     if sequence_stage == "Bicep Curl":
#                         if angle < 45:
#                             feedback_status = "Lower down your arm."
#                             filename = 'lower_arm.mp3'
#                         elif 45 <= angle <= 65:
#                             feedback_status = "Good Curl!"
#                             filename = 'goodcurl.mp3'
#                         # elif 65 < angle <= 105:
#                         #     feedback_status = "Raise up your arm."
#                         #     filename = 'raise_arm.mp3'
#                         elif angle > 160 and stage == "up":
#                             sequence_stage = "Straighten Arms"
#                             stage = "down"
#                             feedback_status = "Arms straightened. Go to curl."
#                             last_feedback = feedback_status
#                             continue  # Skip the rest of the loop

#                         # Only give feedback if it's different from the last feedback given
#                         if feedback_status != last_feedback:
#                             play_audio(feedback_status, filename)
#                             last_feedback = feedback_status

#                     # Ensure the left elbow landmark is detected
#                     if landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.5:
#                         # Get the left elbow landmark coordinates
#                         left_elbow_x = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image.shape[1])
#                         left_elbow_y = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image.shape[0])

#                         # Display the angle value near the left elbow position
#                         cv2.putText(image, str(angle),
#                                     (left_elbow_x, left_elbow_y),  # Use left elbow coordinates
#                                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#                     # Adjust sequence stage text
#                     cv2.putText(image, f"Stage: {sequence_stage}",
#                                 (10, image.shape[0] - 55),  # Position at the left bottom corner
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

#                     # Adjust feedback status text
#                     cv2.putText(image, f"Feedback: {feedback_status}",
#                                 (10, image.shape[0] - 20),  # Position above the sequence stage text
#                                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

#                 except Exception as e:
#                     print(e)
#                     pass

#                 cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
#                 cv2.putText(image, 'REPS', (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 1, 0), 1, cv2.LINE_AA)
#                 cv2.putText(image, str(counter), (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#                 cv2.putText(image, 'STAGE', (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
#                 cv2.putText(image, stage, (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

#                 # Draw landmarks and connections
#                 mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                             mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
#                                             mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

#                 # Resize the image to make it larger
#                 image = cv2.resize(image, (1200, 800))  # Resize the image

#                 stframe.image(image, channels="BGR")  # Display RGB frame

#         # captured_image.release()

#     else:
#         gif_html = f"""
#         <div style="text-align: center;">
#             <img src="data:image/gif;base64,{base64.b64encode(open(gif_path, "rb").read()).decode()}" class="small-gif">
#         </div>
#         """
#         st.markdown(gif_html, unsafe_allow_html=True)
#         st.markdown('**Perfect angle for a bicep curl is 45 degree to 60 degree.**')
#         st.markdown('**Try now with your left arm! Make sure to show your upper body with your left arm into your webcam.**')

# if __name__ == '__main__':
#     app()


# import cv2
# import mediapipe as mp
# import numpy as np
# import streamlit as st
# from gtts import gTTS
# import base64
# from streamlit_webrtc import webrtc_streamer, RTCConfiguration
# import av

# def autoplay_audio(file_path):
#     with open(file_path, "rb") as f:
#         data = f.read()
#     b64 = base64.b64encode(data).decode()
#     return b64

# def create_audio_html(b64_data):
#     html_string = f"""
#         <audio controls autoplay="true">
#             <source src="data:audio/mp3;base64,{b64_data}" type="audio/mp3">
#         </audio>
#     """
#     return html_string

# # Initialize MediaPipe's drawing utilities and pose module
# mp_drawing = mp.solutions.drawing_utils
# mp_pose = mp.solutions.pose

# def calculate_angle(a, b, c):
#     a = np.array(a)
#     b = np.array(b)
#     c = np.array(c)

#     radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
#     angle = np.abs(radians * 180.0 / np.pi)

#     if angle > 180.0:
#         angle = 360 - angle

#     return int(angle)

# class VideoProcessor:
#     def __init__(self):
#         self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
#         self.counter = 0
#         self.stage = "down"
#         self.sequence_stage = "Initial"
#         self.feedback_status = ""
#         self.last_feedback = ""

#     def play_audio(self, feedback_text, filename):
#         tts = gTTS(feedback_text)
#         tts.save(filename)
#         audio_file = filename

#         b64_data = autoplay_audio(audio_file)
#         html_content = create_audio_html(b64_data)
#         st.markdown(html_content, unsafe_allow_html=True)

#     def recv(self, frame):
#         frm = frame.to_ndarray(format="bgr24")
#         image = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
#         results = self.pose.process(image)

#         image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
#         try:
#             landmarks = results.pose_landmarks.landmark

#             shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
#                         landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
#             elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
#                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
#             wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
#                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

#             angle = calculate_angle(shoulder, elbow, wrist)

#             if angle > 160 and self.sequence_stage != "Bicep Curl":
#                 self.sequence_stage = "Straighten Arms"
#                 self.stage = "down"
#                 self.feedback_status = "Arms straightened. Go to curl."
#             elif self.sequence_stage == "Straighten Arms" and angle < 110 and self.stage == "down":
#                 self.sequence_stage = "Bicep Curl"
#                 self.stage = "up"
#                 self.counter += 1
#                 print(self.counter)

#             if self.sequence_stage == "Bicep Curl":
#                 if angle < 45:
#                     self.feedback_status = "Lower down your arm."
#                     filename = 'lower_arm.mp3'
#                 elif 45 <= angle <= 65:
#                     self.feedback_status = "Good Curl!"
#                     filename = 'goodcurl.mp3'
#                 elif angle > 160 and self.stage == "up":
#                     self.sequence_stage = "Straighten Arms"
#                     self.stage = "down"
#                     self.feedback_status = "Arms straightened. Go to curl."
#                     self.last_feedback = self.feedback_status
#                     return av.VideoFrame.from_ndarray(frm, format='bgr24')

#                 if self.feedback_status != self.last_feedback:
#                     self.play_audio(self.feedback_status, filename)
#                     self.last_feedback = self.feedback_status

#             if landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.5:
#                 left_elbow_x = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image.shape[1])
#                 left_elbow_y = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image.shape[0])

#                 cv2.putText(image, str(angle),
#                             (left_elbow_x, left_elbow_y),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

#             cv2.putText(image, f"Stage: {self.sequence_stage}",
#                         (10, image.shape[0] - 55),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                        
#             cv2.putText(image, f"Feedback: {self.feedback_status}",
#                         (10, image.shape[0] - 20),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                        
#         except Exception as e:
#             print(e)

#         cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
#         cv2.putText(image, 'REPS', (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 1, 0), 1, cv2.LINE_AA)
#         cv2.putText(image, str(self.counter), (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
#         cv2.putText(image, 'STAGE', (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
#         cv2.putText(image, self.stage, (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
#         mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
#                                     mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
#                                     mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

#         image = cv2.resize(image, (1200, 800))
        
#         return av.VideoFrame.from_ndarray(image, format='bgr24')

# def app():
#     st.set_page_config(layout="wide")
#     st.title("Left Bicep Curl Exercise")
#     remind_text = "Make sure to allow access of your camera and speaker. Refresh (or press key 'R') the website if there is a lag."
#     st.markdown(remind_text)
#     remark_text = "If there is autoplay sound, press the most bottom audio play button once to autoplay the feedback sound. Might need some time to start autoplay the feedback sound."
#     st.markdown(remark_text)

#     webrtc_ctx = webrtc_streamer(
#         key="full-body-detection",
#         video_processor_factory=VideoProcessor,
#         rtc_configuration=RTCConfiguration(
#             {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
#         ),
#         media_stream_constraints={"video": True, "audio": False},
#         async_processing=True,
#     )

# if __name__ == '__main__':
#     app()

import cv2
import mediapipe as mp
import numpy as np
import streamlit as st
from gtts import gTTS
import base64
from streamlit_webrtc import webrtc_streamer, RTCConfiguration
import av
import time


# def autoplay_audio(file_path):
#     with open(file_path, "rb") as f:
#         data = f.read()
#     b64 = base64.b64encode(data).decode()
#     return b64

# def create_audio_html(b64_data):
#     html_string = f"""
#         <audio controls autoplay="true">
#             <source src="data:audio/mp3;base64,{b64_data}" type="audio/mp3">
#         </audio>
#     """
#     return html_string

# def play_audio(feedback_text, filename):
#     tts = gTTS(feedback_text)
#     tts.save(filename)
#     audio_file = filename

#     b64_data = autoplay_audio(audio_file)
#     html_content = create_audio_html(b64_data)
#     st.markdown(html_content, unsafe_allow_html=True)
# def play_audio(feedback_text, filename):
#     tts = gTTS(feedback_text)
    
#     # Set filename based on feedback_text
#     if feedback_text == "Lower down your arm.":
#         filename = 'lower_arm.mp3'
#     elif feedback_text == "Good Curl!":
#         filename = 'goodcurl.mp3'
    
#     tts.save(filename)  # Save the audio file
#     audio_file = filename

#     b64_data = autoplay_audio(audio_file)
#     html_content = create_audio_html(b64_data)
#     st.markdown(html_content, unsafe_allow_html=True)


# Initialize MediaPipe's drawing utilities and pose module
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return int(angle)

class VideoProcessor:
    def __init__(self):
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.counter = 0
        self.stage = "down"
        self.sequence_stage = "Initial"
        self.feedback_status = ""  # Define feedback_status attribute
        self.last_feedback = ""

    def recv(self, frame):

        self.feedback_status = ""
        self.last_feedback = ""

        frm = frame.to_ndarray(format="bgr24")
        image = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image)

        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark

            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle > 160 and self.sequence_stage != "Bicep Curl":
                self.sequence_stage = "Straighten Arms"
                self.stage = "down"
                self.feedback_status = "Arms straightened. Go to curl."
            elif self.sequence_stage == "Straighten Arms" and angle < 110 and self.stage == "down":
                self.sequence_stage = "Bicep Curl"
                self.stage = "up"
                self.counter += 1
                print(self.counter)

            if self.sequence_stage == "Bicep Curl":
                if angle < 45:
                    self.feedback_status = "Lower down your arm."
                    # filename = 'lower_arm.mp3'
                    self.last_feedback = self.feedback_status
                    # print("Lower down")

                elif 45 <= angle <= 65:
                    self.feedback_status = "Good Curl!"
                    # filename = 'goodcurl.mp3'
                    self.last_feedback = self.feedback_status
                    # print("Good curl")
    
                elif angle > 160 and self.stage == "up":
                    self.sequence_stage = "Straighten Arms"
                    self.stage = "down"
                    self.feedback_status = "Arms straightened. Go to curl."
                    self.last_feedback = self.feedback_status

                # if self.feedback_status != self.last_feedback:
                #     self.play_audio(self.feedback_status, filename)
                #     self.last_feedback = self.feedback_status

            if landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].visibility > 0.5:
                left_elbow_x = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * image.shape[1])
                left_elbow_y = int(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * image.shape[0])

                cv2.putText(image, str(angle),
                            (left_elbow_x, left_elbow_y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

            cv2.putText(image, f"Stage: {self.sequence_stage}",
                        (10, image.shape[0] - 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                        
            cv2.putText(image, f"Feedback: {self.feedback_status}",
                        (10, image.shape[0] - 20),
                                  cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, cv2.LINE_AA)
                        
        except Exception as e:
            print(e)

        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        cv2.putText(image, 'REPS', (15, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 1, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(self.counter), (30, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(image, 'STAGE', (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, self.stage, (100, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2),
                                    mp_drawing.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2))

        image = cv2.resize(image, (1200, 800))
        
        return av.VideoFrame.from_ndarray(image, format='bgr24')
    
    def get_feedback_status(self):
        return self.feedback_status

def app():
    st.set_page_config(layout="wide")
    st.title("Left Bicep Curl Exercise")
    remind_text = "Make sure to allow access of your camera and speaker. Refresh (or press key 'R') the website if there is a lag."
    st.markdown(remind_text)
    remark_text = "If there is autoplay sound, press the most bottom audio play button once to autoplay the feedback sound. Might need some time to start autoplay the feedback sound."
    st.markdown(remark_text)


    # webrtc_ctx = webrtc_streamer(
    #     key="full-body-detection",
    #     video_processor_factory=VideoProcessor,
    #     rtc_configuration=RTCConfiguration(
    #         {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    #     ),
    #     media_stream_constraints={"video": True, "audio": False},
    #     async_processing=True,
    # )

    webrtc_ctx = webrtc_streamer(
        key="full-body-detection",
        video_processor_factory=VideoProcessor,
        rtc_configuration=RTCConfiguration(
            {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        ),
        media_stream_constraints={"video": {"frameRate": {"ideal": 15}}, "audio": False},
        video_html_attrs={
            "style": {"width": "50%", "margin": "0 auto", "border": "5px purple solid"},
            "controls": False,
            "autoPlay": True,
        },
        audio_html_attrs={
            "autoPlay": True,
        },
        async_processing=True,
    )

    video_processor = VideoProcessor()

    last_feedback = ""
    # filename = ""

    # if webrtc_ctx.video_processor:
    #     video_processor = webrtc_ctx.video_processor
    #     while True:
    #         feedback_status = video_processor.get_feedback_status()
    #         print(f"Latest feedback status: {feedback_status}")
    #         # Do whatever you want with the feedback_status here

    # if webrtc_ctx.video_processor:
    #     video_processor = webrtc_ctx.video_processor
    #     while True:
    #         feedback_status = video_processor.get_feedback_status()
    #         # print(f"Latest Update: {feedback_status}")
    #         if feedback_status == "Lower down your arm.":
    #             if feedback_status != last_feedback:
    #                 st.audio('lower_arm.mp3', autoplay = True)
    #                 last_feedback = feedback_status
    #             # filename = 'lower_arm.mp3'
    #         elif feedback_status == "Good Curl!":
    #             if feedback_status != last_feedback:
    #                 st.audio('goodcurl.mp3', autoplay=True)
    #                 last_feedback = feedback_status
        # Only give feedback if it's different from the last feedback given
            # if feedback_status != last_feedback:
            #     st.audio(filename, autoplay=True)
            #     # play_audio(feedback_status, filename)
            #     last_feedback = feedback_status

if __name__ == '__main__':
    app()
