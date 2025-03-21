# # from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
# # from PyQt5.QtGui import QPixmap
# # from PyQt5.QtCore import Qt
# # from rev_ai import apiclient
# # import time
# # # from textblob import TextBlob  # For sentiment analysis
# # import nltk
# # from nltk.sentiment.vader import SentimentIntensityAnalyzer  # For sentiment analysis
# # import sys
# # nltk.download('vader_lexicon')

# # class MyApp(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle('Customer Call Analysis')
# #         self.initUI()
# #         self.rev_client = apiclient.RevAiAPIClient("02ADaw_XB8FloTQqeZ2Ru-Nw_21iGnD4SodfWnnITyvaOEtm4898pge9HeYfx8dxbHpU18x9esqMb00aNFKsLVFPyWffA")  # Replace with your Rev AI API Key
# #         self.sentiment_analyzer = SentimentIntensityAnalyzer()

# #     def initUI(self):
# #         self.layout = QVBoxLayout()
# #         self.setLayout(self.layout)

# #         self.logo = QLabel(self)
# #         self.logo.setPixmap(QPixmap('logo.png').scaled(250, 250, Qt.KeepAspectRatio))
# #         self.logo.setAlignment(Qt.AlignCenter)
# #         self.layout.addWidget(self.logo)

# #         self.selectButton = QPushButton('Select Audio for Analysis', self)
# #         self.selectButton.clicked.connect(self.load_file)
# #         self.layout.addWidget(self.selectButton)

# #         self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet', self)
# #         self.layout.addWidget(self.sentimentLabel)

# #         self.actionItemsLabel = QLabel('Action Items from the Call: Not analyzed yet', self)
# #         self.layout.addWidget(self.actionItemsLabel)

# #         self.actionItemsList = QListWidget(self)
# #         self.layout.addWidget(self.actionItemsList)

# #     def load_file(self):
# #         fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

# #         if fname[0]:
# #             try:
# #                 response = self.send_to_api(fname[0])
# #                 sentiment = response.get('sentiment', "Unknown")

# #                 # Display sentiment with colors
# #                 if sentiment == "NEUTRAL":
# #                     self.sentimentLabel.setStyleSheet("color: gray")
# #                 elif sentiment == "NEGATIVE":
# #                     self.sentimentLabel.setStyleSheet("color: red")
# #                 else:
# #                     self.sentimentLabel.setStyleSheet("color: green")

# #                 self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

# #                 # Display action items
# #                 action_items = response.get('action_items', [])
# #                 self.actionItemsLabel.setText(f"Action Items and Transcription:")
# #                 self.actionItemsList.clear()
# #                 for item in action_items:
# #                     self.actionItemsList.addItem(item)

# #             except Exception as e:
# #                 QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

# #     def send_to_api(self, file_path):
# #         try:
# #             # Submit the audio file to Rev AI
# #             print("Uploading file for transcription...")
# #             with open(file_path, 'rb') as file:
# #                 job = self.rev_client.submit_job_local_file(file_path)

# #             # Poll for job completion
# #             print("Waiting for transcription to complete...")
# #             while True:
# #                 job_details = self.rev_client.get_job_details(job.id)
# #                 if job_details.status == "transcribed":
# #                     break
# #                 elif job_details.status == "failed":
# #                     print("Transcription failed!")
# #                     raise Exception("Transcription failed")
# #                 time.sleep(5)  # Check every 5 seconds

# #             # Fetch the transcript
# #             transcript_text = self.rev_client.get_transcript_text(job.id)
# #             print("Transcription completed!")
# #             print("Transcript:", transcript_text)

# #             # Analyze sentiment
# #             sentiment = self.analyze_sentiment(transcript_text)

# #             # Extract action items
# #             action_items = [transcript_text]  # Show full transcription in the list
# #             action_items += self.get_action_items(transcript_text)  # Add extracted action items

# #             return {
# #                 "sentiment": sentiment,
# #                 "action_items": action_items,
# #             }
# #         except Exception as e:
# #             print("Error in send_to_api:", e)
# #             raise e

# #     def analyze_sentiment(self, transcript):
# #         try:
# #             scores = self.sentiment_analyzer.polarity_scores(transcript)
# #             print(f"Sentiment Scores: {scores}") 
# #             if scores['compound'] >= 0.05:
# #                 return "POSITIVE"
# #             elif scores['compound'] <= -0.05:
# #                 return "NEGATIVE"
# #             else:
# #                 return "NEUTRAL"
# #         except Exception as e:
# #             print("Error in analyze_sentiment:", e)
# #             return "NEUTRAL"

# #     def get_action_items(self, transcript):
# #         try:
# #             # Example placeholder logic for extracting action items
# #             # Customize as needed for your use case
# #             action_items = []
# #             lines = transcript.split('\n')
# #             for line in lines:
# #                 if "action" in line.lower() or "follow-up" in line.lower():
# #                     action_items.append(line.strip())
# #             return action_items
# #         except Exception as e:
# #             print("Error in get_action_items:", e)
# #             return []

# # if __name__ == '__main__':
# #     app = QApplication(sys.argv)
# #     ex = MyApp()
# #     ex.show()
# #     sys.exit(app.exec_())


# from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
# from PyQt5.QtGui import QPixmap
# from PyQt5.QtCore import Qt
# from rev_ai import apiclient
# import time
# from nltk.sentiment.vader import SentimentIntensityAnalyzer
# import nltk
# from textblob import TextBlob
# import sys

# # Download VADER lexicon if not already downloaded
# nltk.download('vader_lexicon')

# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Customer Call Analysis')
#         self.initUI()

#         # Initialize Rev AI client
#         self.rev_client = apiclient.RevAiAPIClient("02jwzVyea_5X7mXLFPfgk6vLNrG7BtbybXDYC8PlDUcxUodUOmtZX_18LhxYX1Q9oL56RaevOL201aeKhtNnVQjYqAI00")  # Replace with your Rev AI API Key

#         # Initialize Sentiment Analyzer
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

#             # Analyze sentiment
#             sentiment = self.analyze_sentiment(transcript_text)

#             # Combine transcription with action items
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
#             # Use VADER for sentiment analysis
#             vader_score = self.sentiment_analyzer.polarity_scores(transcript)['compound']
#             print(f"VADER Score: {vader_score}")  # Debugging log

#             # Adjusted thresholds for more granular sentiment detection
#             if vader_score >= 0.08:
#                 return "POSITIVE"
#             elif vader_score <= -0.01:
#                 return "NEGATIVE"
#             else:
#                 return "NEUTRAL"

#             # Alternatively, use TextBlob to cross-validate sentiment (optional)
#             # textblob_sentiment = TextBlob(transcript).sentiment.polarity
#             if textblob_sentiment > 0:
#                 return "POSITIVE"
#             elif textblob_sentiment < 0:
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



# previous UI

 # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle('Customer Call Analysis')
    #     self.initUI()

    #     # Initialize Rev AI client
    #     self.rev_client = apiclient.RevAiAPIClient("02jwzVyea_5X7mXLFPfgk6vLNrG7BtbybXDYC8PlDUcxUodUOmtZX_18LhxYX1Q9oL56RaevOL201aeKhtNnVQjYqAI00")  # Replace with your Rev AI API Key

    #     # Initialize Hugging Face Sentiment Analysis Pipeline
    #     self.sentiment_pipeline = pipeline("sentiment-analysis")  # Uses a default sentiment analysis model

    # def initUI(self):
    #     self.layout = QVBoxLayout()
    #     self.setLayout(self.layout)

    #     self.logo = QLabel(self)
    #     # self.logo.setPixmap(QPixmap('logo.png').scaled(250, 250, Qt.KeepAspectRatio))
    #     self.logo.setAlignment(Qt.AlignCenter)
    #     self.layout.addWidget(self.logo)

    #     self.selectButton = QPushButton('Select Audio for Analysis', self)
    #     self.selectButton.clicked.connect(self.load_file)
    #     self.layout.addWidget(self.selectButton)

    #     self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet', self)
    #     self.layout.addWidget(self.sentimentLabel)

    #     self.actionItemsLabel = QLabel('Action Items from the Call: Not analyzed yet', self)
    #     self.layout.addWidget(self.actionItemsLabel)

    #     self.actionItemsList = QListWidget(self)
    #     self.layout.addWidget(self.actionItemsList)

# our main code:

# # by aditya and rudrax
# from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox, QWidget, QFrame
# from PyQt5.QtGui import QFont, QPixmap
# from PyQt5.QtCore import Qt
# from rev_ai import apiclient
# import time
# from transformers import pipeline  # Hugging Face Sentiment Analysis Pipeline
# import sys



# class MyApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle('Customer Call Analysis')
#         # self.setFixedSize(600, 600)  # Set a fixed window size
#         self.initUI()

#         # Initialize Rev AI client
#         self.rev_client = apiclient.RevAiAPIClient(
#             "02jwzVyea_5X7mXLFPfgk6vLNrG7BtbybXDYC8PlDUcxUodUOmtZX_18LhxYX1Q9oL56RaevOL201aeKhtNnVQjYqAI00"
#         )  # Replace with your Rev AI API Key

#         # Initialize Hugging Face Sentiment Analysis Pipeline
#         self.sentiment_pipeline = pipeline("sentiment-analysis")  # Uses a default sentiment analysis model

#     def initUI(self):
#         self.layout = QVBoxLayout()
#         self.setLayout(self.layout)

#         # Header Section
#         header_layout = QVBoxLayout()
#         header_label = QLabel('Customer Call Analysis')
#         header_label.setFont(QFont('MONTSERRAT', 20, QFont.ExtraBold))
#         header_label.setAlignment(Qt.AlignCenter)
#         header_label.setStyleSheet("color: ##693278; margin-bottom: 10px;")
#         header_layout.addWidget(header_label)

#         self.logo = QLabel(self)
#         # self.logo.setPixmap(QPixmap('logo.png').scaled(100, 100, Qt.KeepAspectRatio))  # Optional: Add a logo
#         self.logo.setAlignment(Qt.AlignCenter)
#         header_layout.addWidget(self.logo)

#         self.layout.addLayout(header_layout)

#         # Horizontal Separator
#         separator = QFrame()
#         separator.setFrameShape(QFrame.HLine)
#         separator.setFrameShadow(QFrame.Sunken)
#         self.layout.addWidget(separator)

#         # File Selection Section
#         file_layout = QVBoxLayout()
#         self.selectButton = QPushButton('Select Audio for Analysis')
#         self.selectButton.setFont(QFont('Ubuntu', 12, QFont.Bold))
#         self.selectButton.setStyleSheet("background-color: #8c39a3; color: #eacef2; padding: 8px; border-radius: 5px;")
#         self.selectButton.clicked.connect(self.load_file)
#         self.layout.addWidget(self.selectButton)

#         # Sentiment Analysis Display
#         self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet')
#         self.sentimentLabel.setFont(QFont('Ubuntu', 12, QFont.Bold))
#         self.sentimentLabel.setStyleSheet("margin-top: 20px; color: #6b4475;")
#         self.layout.addWidget(self.sentimentLabel)

#         # Action Items Section
#         self.actionItemsLabel = QLabel('Action Items from the Call: Not analyzed yet')
#         self.actionItemsLabel.setFont(QFont('Ubuntu', 12, QFont.Bold))
#         self.actionItemsLabel.setStyleSheet("margin-top: 20px; color: #583561;")
#         self.layout.addWidget(self.actionItemsLabel)

#         self.actionItemsList = QListWidget(self)
#         self.actionItemsList.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px;")
#         self.layout.addWidget(self.actionItemsList)

#         # Footer Section
#         footer_label = QLabel("Rudrax and Aditya")
#         footer_label.setFont(QFont('Arial', 10, QFont.StyleItalic))
#         footer_label.setAlignment(Qt.AlignCenter)
#         footer_label.setStyleSheet("margin-top: 20px; color: #8a7f8d;")
#         self.layout.addWidget(footer_label)


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

#             # Analyze sentiment
#             sentiment = self.analyze_sentiment_transformers(transcript_text)

#             # Combine transcription with action items
#             action_items = [transcript_text]  # Show full transcription in the list
#             action_items += self.get_action_items(transcript_text)  # Add extracted action items

#             return {
#                 "sentiment": sentiment,
#                 "action_items": action_items,
#             }
#         except Exception as e:
#             print("Error in send_to_api:", e)
#             raise e

#     def analyze_sentiment_transformers(self, transcript):
#         try:
#             # Use Hugging Face Transformers for sentiment analysis
#             result = self.sentiment_pipeline(transcript[:1024])  # Truncate to 512 characters if too long
#             print(f"Hugging Face Sentiment Result: {result}")  # Debugging log
#             sentiment_label = result[0]['label'].upper()  # Ensure case consistency
#             sentiment_score = result[0]['score']  # Optional: Use score for more logic

#             sentiment_label = result[0]['label']  # Example: "LABEL_0" or "LABEL_1"
#             if sentiment_label == "POSITIVE":
#                 return "POSITIVE"
#             elif sentiment_label == "NEGATIVE":
#                 return "NEGATIVE"
#             else:
#                 return "NEUTRAL"
#         except Exception as e:
#             print("Error in analyze_sentiment_transformers:", e)
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







# extra

from PyQt5.QtWidgets import (
    QApplication, QLabel, QVBoxLayout, QPushButton, QFileDialog, QListWidget, QMessageBox, QWidget, QFrame
)
from PyQt5.QtGui import QFont                            
from PyQt5.QtCore import Qt
from rev_ai import apiclient
import time
from transformers import pipeline  # Hugging Face Sentiment Analysis Pipeline
import sys


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Emotion Speech Analysis')
        self.initUI()


        self.rev_client = apiclient.RevAiAPIClient(
            "02jwzVyea_5X7mXLFPfgk6vLNrG7BtbybXDYC8PlDUcxUodUOmtZX_18LhxYX1Q9oL56RaevOL201aeKhtNnVQjYqAI00"
        )

        self.sentiment_pipeline = pipeline("sentiment-analysis") 

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Header Section
        header_layout = QVBoxLayout()
        header_label = QLabel('Emotion Speech Analysis')
        header_label.setFont(QFont('MONTSERRAT', 20, QFont.ExtraBold))
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setStyleSheet("color: ##693278; margin-bottom: 10px;")
        header_layout.addWidget(header_label)

        self.logo = QLabel(self)
        self.logo.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.logo)

        self.layout.addLayout(header_layout)

        # Horizontal Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setFrameShadow(QFrame.Sunken)
        self.layout.addWidget(separator)

        # File Selection Section
        file_layout = QVBoxLayout()
        self.selectButton = QPushButton('Select Audio for Analysis')
        self.selectButton.setFont(QFont('Ubuntu', 12, QFont.Bold))
        self.selectButton.setStyleSheet("background-color: #8c39a3; color: #eacef2; padding: 8px; border-radius: 5px;")
        self.selectButton.clicked.connect(self.load_file)
        self.layout.addWidget(self.selectButton)

        # Sentiment Analysis Display
        self.sentimentLabel = QLabel('Overall Sentiment Analysis: Not analyzed yet')
        self.sentimentLabel.setFont(QFont('Ubuntu', 12, QFont.Bold))
        self.sentimentLabel.setStyleSheet("margin-top: 20px; color: #6b4475;")
        self.layout.addWidget(self.sentimentLabel)

        # Action Items Section
        self.actionItemsLabel = QLabel('Action Items from the Call: Not analyzed yet')
        self.actionItemsLabel.setFont(QFont('Ubuntu', 12, QFont.Bold))
        self.actionItemsLabel.setStyleSheet("margin-top: 20px; color: #583561;")
        self.layout.addWidget(self.actionItemsLabel)

        self.actionItemsList = QListWidget(self)
        self.actionItemsList.setStyleSheet("border: 1px solid #BDC3C7; padding: 10px;")
        self.layout.addWidget(self.actionItemsList)

        # Footer Section
        footer_label = QLabel("Rudrax and Aditya")
        footer_label.setFont(QFont('Arial', 10, QFont.StyleItalic))
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("margin-top: 20px; color: #8a7f8d;")
        self.layout.addWidget(footer_label)
    def load_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Select Audio for Analysis')

        if fname[0]:
            try:
                response = self.send_to_api(fname[0])
                sentiment = response.get('sentiment', "Unknown")

                # Display sentiment
                if sentiment == "NEUTRAL":
                    self.sentimentLabel.setStyleSheet("color: gray")
                elif sentiment == "NEGATIVE":
                    self.sentimentLabel.setStyleSheet("color: red")
                else:
                    self.sentimentLabel.setStyleSheet("color: green")

                self.sentimentLabel.setText(f"Overall Sentiment Analysis: {sentiment}")

                # Display action items
                self.actionItemsLabel.setText("Action Items from the Call: Analyzed")
                action_items = response.get('action_items', [])
                self.actionItemsList.clear()
                for item in action_items:
                    self.actionItemsList.addItem(item)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

    def send_to_api(self, file_path):
        try:
            print("Uploading file for transcription...")
            with open(file_path, 'rb') as file:
                job = self.rev_client.submit_job_local_file(file_path)

            print("Waiting for transcription to complete...")
            while True:
                job_details = self.rev_client.get_job_details(job.id)
                if job_details.status == "transcribed":
                    break
                elif job_details.status == "failed":
                    raise Exception("Transcription failed")
                time.sleep(5)

            transcript_text = self.rev_client.get_transcript_text(job.id)
            print("Transcription completed!")

            sentiment = self.analyze_sentiment_transformers(transcript_text)
            action_items = [transcript_text] + self.get_action_items(transcript_text)

            return {
                "sentiment": sentiment,
                "action_items": action_items,
            }
        except Exception as e:
            print("Error in send_to_api:", e)
            raise e

    def analyze_sentiment_transformers(self, transcript):
        try:
            # Split transcript into chunks of 512 characters for analysis
            chunks = [transcript[i:i + 512] for i in range(0, len(transcript), 512)]
            sentiments = []

            for chunk in chunks:
                result = self.sentiment_pipeline(chunk)
                sentiments.append(result[0])  # Append sentiment result for each chunk

            # Debug
            print("Chunk-wise Sentiment Results:", sentiments)

            # Aggregate sentiment results
            positive_count = sum(1 for s in sentiments if s['label'] == 'POSITIVE' and s['score'] > 0.5)
            negative_count = sum(1 for s in sentiments if s['label'] == 'NEGATIVE' and s['score'] > 0.7)
            neutral_count = len(sentiments) - (positive_count + negative_count)


            print(f"Positive: {positive_count}, Negative: {negative_count}, Neutral: {neutral_count}")

            if positive_count > negative_count:
                return "POSITIVE"
            elif negative_count > positive_count:
                return "NEGATIVE"
            else:
                return "NEUTRAL"
        except Exception as e:
            print("Error in analyze_sentiment_transformers:", e)
            return "NEUTRAL"

    def get_action_items(self, transcript):
        try:
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

