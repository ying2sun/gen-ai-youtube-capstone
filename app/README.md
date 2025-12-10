# YouTube Summarizer

**University of Michigan Capstone Project**  
**Team Candles**

## Overview

YouTube Summarizer is an AI-powered web application that generates concise summaries of YouTube videos. Users paste a YouTube URL and receive a short, readable summary of the video’s content in seconds.

## Live Demo

You can access the deployed web application here:

- https://team-candlestyt.lovable.app/

## Features

- 🎥 **Instant Summaries** – Paste any YouTube URL to get an AI-generated summary  
- 🎨 **University of Michigan Themed** – Custom design featuring Maize and Blue colors  
- ⚡ **Real-time Processing** – Handles long-running API requests with clear user feedback  
- 📋 **Copy to Clipboard** – Easily copy summaries for later use or note-taking  
- 🌐 **Responsive Design** – Works seamlessly on desktop and mobile devices  

## Technology Stack

- **Frontend**: React, TypeScript, Vite  
- **UI Framework**: shadcn-ui components with Tailwind CSS  
- **Backend**: Lovable Cloud (Supabase) with Edge Functions  
- **AI Processing**: External summarization API  

## Getting Started

### Prerequisites

- Node.js & npm ([install with nvm](https://github.com/nvm-sh/nvm#installing-and-updating))

### Installation

1. Clone the repository:
   ```sh
   git clone <YOUR_GIT_URL>
   cd <YOUR_PROJECT_NAME>
   ```

2. Install dependencies:
   ```sh
   npm install
   ```

3. Start the development server:
   ```sh
   npm run dev
   ```

## How It Works

1. The user enters a YouTube URL in the input field.  
2. The frontend sends the URL to a Supabase Edge Function.  
3. The Edge Function forwards the request to the external summarization API with the appropriate authentication.  
4. The AI service processes the video (via its transcript) and generates a summary.  
5. The summary is returned to the frontend and displayed to the user, with a copy-to-clipboard option.

## API Integration

The application integrates with an external summarization API:

- **Endpoint**: `http://34.229.218.179:8000/summarize`  
- **Method**: `POST`  
- **Authentication**: API key via header  
- **Timeout**: 2 minutes (to account for long processing times on longer videos)  

## Running the Summarization API on AWS

The summarization API is designed to run on the AWS instance at:

```text
34.229.218.179
```

### Environment Setup

1. Connect to the AWS instance (for example, via SSH).  
2. Activate the Python virtual environment:

   ```bash
   source /venv/bin/activate
   ```

   Ensure that all required dependencies have been installed in this environment (for example, via `pip install -r requirements.txt`).

### Starting the API Service

With the virtual environment active, start the API using Uvicorn:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000
```

This command:

- Serves the FastAPI (or compatible) application defined in `api.py`  
- Binds to all interfaces on the instance (`0.0.0.0`)  
- Exposes the service on port `8000`, which is used by the frontend at the `/summarize` endpoint  

Verify that:

- Port `8000` is open in the AWS security group / firewall settings  
- Any required environment variables (e.g., API keys, configuration values) are set before running the service  

## Project Structure

```text
├── src/
│   ├── components/        # Reusable UI components
│   ├── pages/             # Page components
│   ├── integrations/      # Supabase client configuration
│   └── index.css          # Global styles and design tokens
├── supabase/
│   └── functions/         # Edge functions for backend logic
└── public/                # Static assets
```

## Deployment

This project is deployed on Lovable. To publish updates:

1. Click the **Publish** button in the Lovable editor.  
2. Click **Update** to deploy frontend changes.  
3. Backend changes (Supabase Edge Functions) are deployed automatically as part of the Lovable workflow.  

The external summarization API must be running on the AWS instance (as described above) for the application to function end-to-end.

## Team

**Team Candles** – University of Michigan Capstone Project

## License

Built with [Lovable](https://lovable.dev)
