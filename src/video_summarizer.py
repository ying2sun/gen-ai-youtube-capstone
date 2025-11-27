import torch
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from youtube_transcript_api import YouTubeTranscriptApi

class VideoSummarizer:
    """
    A class to handle YouTube video transcription and summarization using a fine-tuned Flan-T5 model.
    """

    def __init__(self, model_path):
        """
        Initialize the summarizer by loading the model and tokenizer.

        Args:
            model_path (str): Path to the directory containing the saved model and tokenizer.
                              This should be the unzipped folder of 'final_flan_t5_model'.
        """
        print(f"[INFO] Loading model artifacts from {model_path}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load model from {model_path}. Ensure the directory exists and contains model files.") from e
        
        # specific handling for GPU availability
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self.model.to(self.device)
        print(f"[INFO] Model loaded successfully on {self.device.upper()}.")

    def _get_video_id(self, url):
        """
        Extracts the video ID from a YouTube URL.

        Args:
            url (str): The full YouTube URL.

        Returns:
            str: The extracted video ID, or None if extraction fails.
        """
        video_id = None
        if "v=" in url:
            video_id = url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
        return video_id

    def get_transcript(self, video_url):
        """
        Retrieves and concatenates the transcript for a given YouTube video.

        Args:
            video_url (str): The URL of the YouTube video.

        Returns:
            tuple: (full_transcript_text, error_message)
        """
        video_id = self._get_video_id(video_url)
        
        if not video_id:
            return None, "Invalid YouTube URL format."

        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            # Combine all text segments into a single string
            full_text = " ".join([t['text'] for t in transcript_list])
            return full_text, None
        except Exception as e:
            return None, str(e)

    def _preprocess_text(self, text):
        """
        Cleans and truncates the input text to fit the model's context window.

        Args:
            text (str): Raw transcript text.

        Returns:
            str: Preprocessed text ready for tokenization.
        """
        if not text:
            return ""
        
        # Normalize whitespace
        clean_text = text.replace("\n", " ")
        
        # Truncate text to approximately 4000 characters to fit within the 1024 token limit.
        # Note: We purposely retain the introductory text as it often contains the topic statement.
        return clean_text[:4000]

    def generate_summary(self, video_url):
        """
        Main pipeline to generate a summary for a specific video URL.

        Args:
            video_url (str): The YouTube video URL.

        Returns:
            str: The generated abstractive summary.
        """
        # 1. Retrieve Transcript
        transcript, error = self.get_transcript(video_url)
        if error:
            return f"Error retrieving transcript: {error}"

        # 2. Preprocess
        cleaned_text = self._preprocess_text(transcript)
        input_string = "summarize: " + cleaned_text

        # 3. Tokenize
        inputs = self.tokenizer(
            input_string, 
            return_tensors="pt", 
            max_length=1024, 
            truncation=True
        ).to(self.device)

        # 4. Generate Summary
        # Parameters are tuned for stability (beams=4) and conciseness (length_penalty=2.0)
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=150,
                min_length=40,
                num_beams=4,
                length_penalty=2.0,
                no_repeat_ngram_size=3,
                early_stopping=True
            )

        # 5. Decode and Post-process
        summary = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Capitalize the first letter for readability
        if summary:
            summary = summary[0].upper() + summary[1:]
            
        return summary

# Example execution block
if __name__ == "__main__":
    # Path configuration: update this to point to the unzipped model directory
    MODEL_DIR = "final_flan_t5_model"
    
    try:
        summarizer = VideoSummarizer(MODEL_DIR)
        
        # Example Test
        test_url = "https://www.youtube.com/watch?v=jNQXAC9IVRw"
        print(f"Processing URL: {test_url}")
        
        result = summarizer.generate_summary(test_url)
        print("-" * 50)
        print("Generated Summary:")
        print(result)
        print("-" * 50)
        
    except Exception as ex:
        print(f"[ERROR] Initialization failed: {ex}")
