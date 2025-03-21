# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
# from rev_ai import apiclient
# import time
# # from textblob import TextBlob  # For sentiment analysis
# import nltk
# from nltk.sentiment.vader import SentimentIntensityAnalyzer  # For sentiment analysis
# import sys
# nltk.download('vader_lexicon')

# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Customer Call Analysis')
#         self.initUI()
#         self.rev_client = apiclient.RevAiAPIClient("02ADaw_XB8FloTQqeZ2Ru-Nw_21iGnD4SodfWnnITyvaOEtm4898pge9HeYfx8dxbHpU18x9esqMb00aNFKsLVFPyWffA")  # Replace with your Rev AI API Key
#         self.sentiment_analyzer = SentimentIntensityAnalyzer()

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         self.logo = QLabel(self)
#         self.logo.setPixmap(QPixmap('logo.png').scaled(250, 250, Qt.KeepAspectRatio))
#         self.logo.setAlignment(Qt.AlignCenter)
#         self.layout.addWidget(self.logo)

#         self.selectButton = QPushButton('Select Audio for Analysis', self)
#         self.selectButton.clicked.connect(self.load_file)
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

#                 # Display sentiment with colors
#                 if sentiment == "NEUTRAL":
#                     self.sentimentLabel.setStyleSheet("color: gray")
#                 elif sentiment == "NEGATIVE":
#                     self.sentimentLabel.setStyleSheet("color: red")
#                 else:
#                     self.sentimentLabel.setStyleSheet("color: green")

#                 self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

#                 # Display action items
#                 action_items = response.get('action_items', [])
#                 self.actionItemsLabel.setText(f"Action Items and Transcription:")
#                 self.actionItemsList.clear()
#                 for item in action_items:
#                     self.actionItemsList.addItem(item)

#             except Exception as e:
#                 QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

#     def send_to_api(self, file_path):
#         try:
#             # Submit the audio file to Rev AI
#             print("Uploading file for transcription...")
#             with open(file_path, 'rb') as file:
#                 job = self.rev_client.submit_job_local_file(file_path)

#             # Poll for job completion
#             print("Waiting for transcription to complete...")
#             while True:
#                 job_details = self.rev_client.get_job_details(job.id)
#                 if job_details.status == "transcribed":
#                     break
#                 elif job_details.status == "failed":
#                     print("Transcription failed!")
#                     raise Exception("Transcription failed")
#                 time.sleep(5)  # Check every 5 seconds

#             # Fetch the transcript
#             transcript_text = self.rev_client.get_transcript_text(job.id)
#             print("Transcription completed!")
#             print("Transcript:", transcript_text)

#             # Analyze sentiment
#             sentiment = self.analyze_sentiment(transcript_text)

#             # Extract action items
#             action_items = [transcript_text]  # Show full transcription in the list
#             action_items += self.get_action_items(transcript_text)  # Add extracted action items

#             return {
#                 "sentiment": sentiment,
#                 "action_items": action_items,
#             }
#         except Exception as e:
#             print("Error in send_to_api:", e)
#             raise e

#     def analyze_sentiment(self, transcript):
#         try:
#             scores = self.sentiment_analyzer.polarity_scores(transcript)
#             print(f"Sentiment Scores: {scores}") 
#             if scores['compound'] >= 0.05:
#                 return "POSITIVE"
#             elif scores['compound'] <= -0.05:
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


from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from rev_ai import apiclient
import time
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
from textblob import TextBlob
import sys

# Download VADER lexicon if not already downloaded
nltk.download('vader_lexicon')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Call Analysis')
        self.initUI()

        # Initialize Rev AI client
        self.rev_client = apiclient.RevAiAPIClient("02jwzVyea_5X7mXLFPfgk6vLNrG7BtbybXDYC8PlDUcxUodUOmtZX_18LhxYX1Q9oL56RaevOL201aeKhtNnVQjYqAI00")  # Replace with your Rev AI API Key

        # Initialize Sentiment Analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

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

        self.actionItemsLabel = QLabel('Action Items from the Call: Not analyzed yet', self)
        self.layout.addWidget(self.actionItemsLabel)

        self.actionItemsList = QListWidget(self)
        self.layout.addWidget(self.actionItemsList)

    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

        if fname[0]:
            try:
                response = self.send_to_api(fname[0])
                sentiment = response.get('sentiment', "Unknown")

                # Display sentiment with colors
                if sentiment == "NEUTRAL":
                    self.sentimentLabel.setStyleSheet("color: gray")
                elif sentiment == "NEGATIVE":
                    self.sentimentLabel.setStyleSheet("color: red")
                else:
                    self.sentimentLabel.setStyleSheet("color: green")

                self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

                # Display action items
                action_items = response.get('action_items', [])
                self.actionItemsLabel.setText(f"Action Items and Transcription:")
                self.actionItemsList.clear()
                for item in action_items:
                    self.actionItemsList.addItem(item)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

    def send_to_api(self, file_path):
        try:
            # Submit the audio file to Rev AI
            print("Uploading file for transcription...")
            with open(file_path, 'rb') as file:
                job = self.rev_client.submit_job_local_file(file_path)

            # Poll for job completion
            print("Waiting for transcription to complete...")
            while True:
                job_details = self.rev_client.get_job_details(job.id)
                if job_details.status == "transcribed":
                    break
                elif job_details.status == "failed":
                    print("Transcription failed!")
                    raise Exception("Transcription failed")
                time.sleep(5)  # Check every 5 seconds

            # Fetch the transcript
            transcript_text = self.rev_client.get_transcript_text(job.id)
            print("Transcription completed!")

            # Analyze sentiment
            sentiment = self.analyze_sentiment(transcript_text)

            # Combine transcription with action items
            action_items = [transcript_text]  # Show full transcription in the list
            action_items += self.get_action_items(transcript_text)  # Add extracted action items

            return {
                "sentiment": sentiment,
                "action_items": action_items,
            }
        except Exception as e:
            print("Error in send_to_api:", e)
            raise e

    def analyze_sentiment(self, transcript):
        try:
            # Use VADER for sentiment analysis
            vader_score = self.sentiment_analyzer.polarity_scores(transcript)['compound']
            print(f"VADER Score: {vader_score}")  # Debugging log

            # Adjusted thresholds for more granular sentiment detection
            if vader_score >= 0.05:
                return "POSITIVE"
            elif vader_score <= -0.05:
                return "NEGATIVE"
            else:
                return "NEUTRAL"

            # Alternatively, use TextBlob to cross-validate sentiment (optional)
            # textblob_sentiment = TextBlob(transcript).sentiment.polarity
            if textblob_sentiment > 0:
                return "POSITIVE"
            elif textblob_sentiment < 0:
                return "NEGATIVE"
            else:
                return "NEUTRAL"
        except Exception as e:
            print("Error in analyze_sentiment:", e)
            return "NEUTRAL"

    def get_action_items(self, transcript):
        try:
            # Example placeholder logic for extracting action items
            # Customize as needed for your use case
            action_items = []
            lines = transcript.split('\n')
            for line in lines:
                if "action" in line.lower() or "follow-up" in line.lower():
                    action_items.append(line.strip())
            return action_items
        except Exception as e:
            print("Error in get_action_items:", e)
            return []

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
