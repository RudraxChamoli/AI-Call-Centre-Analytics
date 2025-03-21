from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QListWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
import assemblyai as aai


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Customer Call Analysis')
        self.initUI()

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
                self.actionItemsLabel.setText(f"Action Items from the Call: {len(action_items)} found")
                self.actionItemsList.clear()
                for item in action_items:
                    self.actionItemsList.addItem(item)

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to process audio: {e}")

    def send_to_api(self, file_path):
        try:
            aai.settings.api_key = "32f91b76f351492680f915add87ccfc1"

            FILE_URL = "https://assembly.ai/wildfires.mp3"

            # Initialize transcriber and request transcription
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(
                file_path,
                aai.TranscriptionConfig(sentiment_analysis=True)
            )

            # Debug transcript
            print("Transcript object:", transcript)

            # Analyze sentiment and extract action items
            sentiment = self.analyze_sentiment(transcript)
            action_items = self.get_action_items(transcript)

            return {
                "sentiment": sentiment,
                "action_items": action_items.split('\n'),
            }
        except Exception as e:
            print("Error in send_to_api:", e)
            raise e

    def analyze_sentiment(self, transcript):
        try:
            all_sentiment_scores = [
                sentiment.sentiment for sentiment in transcript.sentiment_analysis
            ]
            sentiments_count = {
                "POSITIVE": all_sentiment_scores.count("POSITIVE"),
                "NEGATIVE": all_sentiment_scores.count("NEGATIVE"),
            }

            if sentiments_count["POSITIVE"] > sentiments_count["NEGATIVE"]:
                return "POSITIVE"
            elif sentiments_count["POSITIVE"] < sentiments_count["NEGATIVE"]:
                return "NEGATIVE"
            else:
                return "NEUTRAL"
        except AttributeError as e:
            print("Error in analyze_sentiment:", e)
            return "NEUTRAL"

    def get_action_items(self, transcript):
        try:
            result = transcript.lemur.action_items(
                context="This is a transcript of a call between a customer and a call center agent.",
                answer_format="**<topic header>**\n<relevant action items>\n",
            )
            return result.response
        except Exception as e:
            print("Error in get_action_items:", e)
            return "No action items found"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
