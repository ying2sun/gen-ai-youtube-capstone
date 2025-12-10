import requests

class VideoSummarizer:
    def __init__(self, api_key: str, apify_token: str):
        self.api_key = api_key
        self.apify_token = apify_token

    def _get_video_id(self, url: str) -> str | None:
        if "v=" in url:
            return url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in url:
            return url.split("youtu.be/")[1].split("?")[0]
        return None

    def get_transcript(self, video_url: str):
        api_url = (
            f"https://api.apify.com/v2/acts/insight_api_labs~youtube-transcript/"
            f"run-sync-get-dataset-items?token={self.apify_token}"
        )

        payload = {
            "video_urls": [
                {
                    "url": video_url,
                    "method": "GET"
                }
            ]
        }

        try:
            response = requests.post(api_url, json=payload)
            response.raise_for_status()
            data = response.json()

            if not data or not isinstance(data, list):
                return None, "Unexpected response format."

            item = data[0]

            # Choose best transcript source
            transcript = (
                item.get("transcriptWithTimestamps")
                or item.get("transcript")
                or None
            )

            if not transcript:
                return None, f"No transcript found. Keys available: {list(item.keys())}"

            # transcript either list or string
            if isinstance(transcript, str):
                full_text = transcript
            elif isinstance(transcript, list):
                full_text = " ".join(seg.get("text", "") for seg in transcript)
            else:
                return None, "Unsupported transcript type."

            return full_text, None

        except Exception as e:
            return None, f"Error retrieving transcript: {e}"

    def summarize_text(self, text: str) -> str:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "HTTP-Referer": "http://localhost",
            "X-Title": "YouTube Summarizer"
        }

        payload = {
            "model": "openai/gpt-oss-20b:free",
            "messages": [
                {"role": "system", "content": "You are a concise summarization assistant."},
                {"role": "user", "content": f"Summarize this transcript into 4–6 sentences:\n\n{text}"}
            ],
            "max_tokens": 250
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        return result["choices"][0]["message"]["content"]

    def generate_summary(self, video_url: str):
        transcript, error = self.get_transcript(video_url)
        if error:
            return f"Error retrieving transcript: {error}"

        return self.summarize_text(transcript[:4000])
