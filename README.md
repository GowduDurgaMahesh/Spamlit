# SpamLit

SpamLit is a machine-learning-based spam message detection system designed to classify messages as **Spam** or **Legitimate (Ham)** using Natural Language Processing (NLP).

The project uses **TF-IDF text feature extraction** with a **Linear Support Vector Machine (LinearSVC)** classifier to analyze message patterns and identify potentially unwanted or suspicious messages.

## Features

- Spam and legitimate message classification
- TF-IDF feature extraction
- LinearSVC machine-learning classifier
- Real-time message analysis
- Benchmark spam and legitimate messages
- Original message inspection
- Classification confidence indicator
- Character and word statistics
- Model and vectorizer information
- Technical model inspection
- Professional dark-themed Streamlit interface
- Responsive web interface

## Technology Stack

- **Python**
- **Streamlit**
- **Scikit-learn**
- **Pandas**
- **Joblib**
- **TF-IDF**
- **LinearSVC**
- **Jupyter Notebook**

## How It Works

```text
Message Input
     ↓
Text Processing
     ↓
TF-IDF Vectorization
     ↓
LinearSVC Classifier
     ↓
Classification
     ↓
Spam / Legitimate
     ↓
Result & Analysis