# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
# from rev_ai import apiclient
# import time
# from textblob import TextBlob  # For sentiment analysis
# import sys


# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Customer Call Analysis')
#         self.initUI()

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         self.logo = QLabel(self)
#         self.logo.setPixmap(QPixmap('logo.png').scaled(250, 250, Qt.KeepAspectRatio))
#         self.logo.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.logo)

#         self.selectButton = QPushButton('Select Audio for Analysis', self)
#         self.selectButton.clicked.connect(self.load_file)  # Ensure load_file exists
#         self.layout.addWidget(self.selectButton)

#         self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet', self)
#         self.layout.addWidget(self.sentimentLabel)

#         self.actionItemsLabel = QLabel('Action Items from the Call: Not analyzed yet', self)
#         self.layout.addWidget(self.actionItemsLabel)

#         self.actionItemsList = QListWidget(self)
#         self.layout.addWidget(self.actionItemsList)

#     def load_file(self):
#         fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

#         if fname[0]:
#             try:
#                 response = self.send_to_api(fname[0])
#                 sentiment = response.get('sentiment', "Unknown")
#                 transcription = response.get('transcription', "No transcription available")

#                 # Display sentiment with colors
#                 if sentiment == "NEUTRAL":
#                     self.sentimentLabel.setStyleSheet("color: gray")
#                 elif sentiment == "NEGATIVE":
#                     self.sentimentLabel.setStyleSheet("color: red")
#                 else:
#                     self.sentimentLabel.setStyleSheet("color: green")

#                 self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

#                 # Display transcription and action items
#                 self.actionItemsLabel.setText(f"Transcription and Action Items from the Call:")
#                 self.actionItemsList.clear()

#                 # Add transcription first
#                 self.actionItemsList.addItem("**Transcription**:")
#                 self.actionItemsList.addItem(transcription)

#                 # Add a separator
#                 self.actionItemsList.addItem("")

#                 # Add action items
#                 action_items = response.get('action_items', [])
#                 if action_items:
#                     self.actionItemsList.addItem("**Action Items**:")
#                     for item in action_items:
#                         self.actionItemsList.addItem(item)
#                 else:
#                     self.actionItemsList.addItem("No action items found.")

#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

#     # Other methods like send_to_api, analyze_sentiment, and get_action_items go here


#     # def load_file(self):
#     #     fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

#     #     if fname[0]:
#     #         try:
#     #             response = self.send_to_api(fname[0])
#     #             sentiment = response.get('sentiment', "Unknown")

#     #             # Display sentiment with colors
#     #             if sentiment == "NEUTRAL":
#     #                 self.sentimentLabel.setStyleSheet("color: gray")
#     #             elif sentiment == "NEGATIVE":
#     #                 self.sentimentLabel.setStyleSheet("color: red")
#     #             else:
#     #                 self.sentimentLabel.setStyleSheet("color: green")

#     #             self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

#     #             # Display action items
#     #             action_items = response.get('action_items', [])
#     #             self.actionItemsLabel.setText(f"Action Items from the Call: {len(action_items)} found")
#     #             self.actionItemsList.clear()
#     #             for item in action_items:
#     #                 self.actionItemsList.addItem(item)

#     #         except Exception as e:
#     #             QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

#     # def send_to_api(self, file_path):
#     #     try:
#     #         # Submit the audio file to Rev AI
#     #         print("Uploading file for transcription...")
#     #         with open(file_path, 'rb') as file:
#     #             job = self.rev_client.submit_job_local_file(file_path)

#     #         # Poll for job completion
#     #         print("Waiting for transcription to complete...")
#     #         while True:
#     #             job_details = self.rev_client.get_job_details(job.id)
#     #             if job_details.status == "transcribed":
#     #                 break
#     #             elif job_details.status == "failed":
#     #                 print("Transcription failed!")
#     #                 raise Exception("Transcription failed")
#     #             time.sleep(5)  # Check every 5 seconds

#     #         # Fetch the transcript
#     #         transcript_text = self.rev_client.get_transcript_text(job.id)
#     #         print("Transcription completed!")
#     #         print("Transcript:", transcript_text)

#     #         # Analyze sentiment
#     #         sentiment = self.analyze_sentiment(transcript_text)

#     #         # Extract action items
#     #         action_items = self.get_action_items(transcript_text)

#     #         return {
#     #             "sentiment": sentiment,
#     #             "action_items": action_items,
#     #         }
#     #     except Exception as e:
#     #         print("Error in send_to_api:", e)
#     #         raise e
# # def load_file(self):
# #     fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

# #     if fname[0]:
# #         try:
# #             response = self.send_to_api(fname[0])
# #             sentiment = response.get('sentiment', "Unknown")
# #             transcription = response.get('transcription', "No transcription available")

# #             # Display sentiment with colors
# #             if sentiment == "NEUTRAL":
# #                 self.sentimentLabel.setStyleSheet("color: gray")
# #             elif sentiment == "NEGATIVE":
# #                 self.sentimentLabel.setStyleSheet("color: red")
# #             else:
# #                 self.sentimentLabel.setStyleSheet("color: green")

# #             self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

# #             # Display transcription and action items
# #             self.actionItemsLabel.setText(f"Transcription and Action Items from the Call:")
# #             self.actionItemsList.clear()

# #             # Add transcription first
# #             self.actionItemsList.addItem("**Transcription**:")
# #             self.actionItemsList.addItem(transcription)

# #             # Add a separator
# #             self.actionItemsList.addItem("")

# #             # Add action items
# #             action_items = response.get('action_items', [])
# #             if action_items:
# #                 self.actionItemsList.addItem("**Action Items**:")
# #                 for item in action_items:
# #                     self.actionItemsList.addItem(item)
# #             else:
# #                 self.actionItemsList.addItem("No action items found.")

# #         except Exception as e:
# #             QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")


# def send_to_api(self, file_path):
#     try:
#         # Submit the audio file to Rev AI
#         print("Uploading file for transcription...")
#         job = self.rev_client.submit_job_local_file(file_path)

#         # Poll for job completion
#         print("Waiting for transcription to complete...")
#         while True:
#             job_details = self.rev_client.get_job_details(job.id)
#             if job_details.status == "transcribed":
#                 break
#             elif job_details.status == "failed":
#                 print("Transcription failed!")
#                 raise Exception("Transcription failed")
#             time.sleep(5)  # Check every 5 seconds

#         # Fetch the transcript
#         transcript_text = self.rev_client.get_transcript_text(job.id)
#         print("Transcription completed!")

#         # Analyze sentiment
#         sentiment = self.analyze_sentiment(transcript_text)

#         # Extract action items
#         action_items = self.get_action_items(transcript_text)

#         # Return both transcription and analysis results
#         return {
#             "transcription": transcript_text,
#             "sentiment": sentiment,
#             "action_items": action_items,
#         }
#     except Exception as e:
#         print("Error in send_to_api:", e)
#         raise e


#     def analyze_sentiment(self, transcript):
#         try:
#             # Use TextBlob for sentiment analysis
#             sentiment = TextBlob(transcript).sentiment.polarity
#             if sentiment > 0:
#                 return "POSITIVE"
#             elif sentiment < 0:
#                 return "NEGATIVE"
#             else:
#                 return "NEUTRAL"
#         except Exception as e:
#             print("Error in analyze_sentiment:", e)
#             return "NEUTRAL"

#     def get_action_items(self, transcript):
#         try:
#             # Example placeholder logic for extracting action items
#             # Customize as needed for your use case
#             action_items = []
#             lines = transcript.split('\n')
#             for line in lines:
#                 if "action" in line.lower() or "follow-up" in line.lower():
#                     action_items.append(line.strip())
#             return action_items
#         except Exception as e:
#             print("Error in get_action_items:", e)
#             return []

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     ex = MyApp()
#     ex.show()
#     sys.exit(app.exec_())


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
# from rev_ai import RevAiAPIClient  # Import Rev AI client
from rev_ai import RevAiAPI

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Call Analysis')
        self.initUI()
        self.rev_ai_client = RevAiAPI("02ADaw_XB8FloTQqeZ2Ru-Nw_21iGnD4SodfWnnITyvaOEtm4898pge9HeYfx8dxbHpU18x9esqMb00aNFKsLVFPyWffA")  # Replace with your Rev AI API key

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.logo = QLabel(self)
        self.logo.setPixmap(QPixmap('logo.png').scaled(250, 250, Qt.KeepAspectRatio))
        self.logo.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.logo)

        self.selectButton = QPushButton('Select Audio for Analysis', self)
        self.selectButton.clicked.connect(self.load_file)
        self.layout.addWidget(self.selectButton)

        self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet', self)
        self.layout.addWidget(self.sentimentLabel)

        self.actionItemsLabel = QLabel('Transcription and Action Items:', self)
        self.layout.addWidget(self.actionItemsLabel)

        self.actionItemsList = QListWidget(self)
        self.layout.addWidget(self.actionItemsList)

    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

        if fname[0]:
            try:
                response = self.send_to_api(fname[0])
                sentiment = response.get('sentiment', "Unknown")
                transcription = response.get('transcription', "No transcription available")

                # Display sentiment with colors
                if sentiment == "NEUTRAL":
                    self.sentimentLabel.setStyleSheet("color: gray")
                elif sentiment == "NEGATIVE":
                    self.sentimentLabel.setStyleSheet("color: red")
                else:
                    self.sentimentLabel.setStyleSheet("color: green")

                self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

                # Display transcription and action items
                self.actionItemsLabel.setText(f"Transcription and Action Items from the Call:")
                self.actionItemsList.clear()

                # Add transcription first
                self.actionItemsList.addItem("**Transcription**:")
                self.actionItemsList.addItem(transcription)

                # Add a separator
                self.actionItemsList.addItem("")

                # Add action items
                action_items = response.get('action_items', [])
                if action_items:
                    self.actionItemsList.addItem("**Action Items**:")
                    for item in action_items:
                        self.actionItemsList.addItem(item)
                else:
                    self.actionItemsList.addItem("No action items found.")

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

        def send_to_api(self, file_path):
            try:
                # Submit a job
                print("Uploading file for transcription...")
                with open(file_path, 'rb') as audio_file:
                    job = self.rev_ai_client.submit_job_local_file(audio_file)
                
                # Wait for job completion
                while True:
                    job_details = self.rev_ai_client.get_job_details(job.id)
                    if job_details.status == 'completed':
                        break
                    elif job_details.status == 'failed':
                        raise Exception("Transcription job failed.")
                    time.sleep(5)

                # Get transcript
                transcript = self.rev_ai_client.get_transcript(job.id)
                return {"transcription": transcript['text']}
            except Exception as e:
                print(f"Error in send_to_api: {e}")
                return None
    def analyze_sentiment(self, transcript):
        """Mock sentiment analysis."""
        positive_keywords = ["good", "great", "excellent", "positive", "happy"]
        negative_keywords = ["bad", "poor", "negative", "unhappy"]

        positive_count = sum(word in transcript.lower() for word in positive_keywords)
        negative_count = sum(word in transcript.lower() for word in negative_keywords)

        if positive_count > negative_count:
            return "POSITIVE"
        elif positive_count < negative_count:
            return "NEGATIVE"
        else:
            return "NEUTRAL"

    def get_action_items(self, transcript):
        """Mock action item extraction."""
        # For now, simply return placeholder action items
        return [
            "Follow up with the customer about the issue.",
            "Provide a discount for the inconvenience.",
            "Schedule a callback for next week.",
        ]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
