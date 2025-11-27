# YouTube Video Summarization via Knowledge Distillation and RAG

## Project Overview

This repository hosts the implementation of a scalable AI system designed to generate abstractive summaries for YouTube video transcripts. Addressing the challenges of processing long-form unstructured audio-visual data, this project employs a **Knowledge Distillation** framework. We utilize a high-capacity Large Language Model (Gemini 2.0Flash) to generate a synthetic "Gold Standard" dataset, which is subsequently used to fine-tune a computationally efficient **Flan-T5** model.

The system integrates principles from **Retrieval-Augmented Generation (RAG)** for context management and demonstrates a viable pipeline for democratizing video intelligence with low inference costs.

## App


## Human Evaluation


## Technical Objectives

1.  **Abstractive Summarization:** Move beyond extractive methods to generate coherent, synthesized paragraphs that capture the core narrative.
2.  **Cost Efficiency:** Replace reliance on continuous, expensive API calls to proprietary LLMs with a fine-tuned, locally deployable Small Language Model (SLM).
3.  **Data Engineering:** Overcome the lack of labeled training data through the engineering of a synthetic dataset generation pipeline.

## Repository Structure

The project directory is organized as follows:

* **src/**: Contains the production-ready source code for the inference engine and the `VideoSummarizer` class.
* **notebooks/**: Includes Jupyter notebooks documenting the experimental process, including data ETL, RAG prototyping, evaluation and model training workflows.
* **data/**: The derived dataset (`gold_dataset_merged_final.csv`) is included.
* **app/**: Lists all files for api calls and the application.
* **reports/**: Contains the final project report detailing the methodology, error analysis, and conclusions.
* **images/**: Stores data visualizations generated during the evaluation phase, such as performance metrics and embedding comparisons.
* **requirements.txt**: Lists all Python dependencies required to reproduce the environment.

## Methodology

The development process followed a four-stage pipeline:

1.  **Data Acquisition & Preprocessing:**
    Utilization of the `jamescalam/youtube-transcriptions` dataset. The pipeline handles text cleaning, concatenation based on video IDs, and tokenization.

2.  **RAG Prototype (Phase I):**
    Initial implementation using FAISS vector stores and `sentence-transformers` to retrieve relevant transcript chunks. While effective for QA, this approach highlighted limitations in global narrative summarization, prompting a shift to fine-tuning.

3.  **Knowledge Distillation (Phase II):**
    Deployment of a robust data pipeline to interact with the Gemini API, generating approximately 300 high-quality summary-transcript pairs. This synthetic dataset served as the ground truth for student model training.

4.  **Supervised Fine-Tuning:**
    Fine-tuning of the `google/flan-t5-base` model using the generated dataset. Training employed mixed-precision (FP16) and optimized hyperparameters to ensure convergence within limited GPU resources.

## Performance Evaluation

We evaluated the model using both lexical and semantic metrics:

* **Lexical Overlap (ROUGE):** The model achieved ROUGE-1 scores averaging 0.20. This relatively low score is attributed to the vocabulary divergence between the teacher (Gemini) and student (Flan-T5) models.
* **Semantic Similarity:** Analysis using Cosine Similarity on vector embeddings reveals scores between 0.60 and 0.80. This significant metric demonstrates that the model successfully captures the semantic meaning and narrative structure of the videos, despite using different phrasing than the ground truth.

## Execution Instructions

### Prerequisites
* Python 3.8 or higher
* GPU support is recommended for efficient model inference (e.g., NVIDIA CUDA).

### 1. Installation
Clone the repository and install the necessary dependencies listed in `requirements.txt`.

```
git clone https://github.com/sokkerstar123/Capstone.git
cd Capstone
pip install -r requirements.txt
```

### 2. Model Weight Configuration
Due to GitHub's file size limitations, the fine-tuned model weights are hosted externally.
* **Action Required:** Download the model package from [https://drive.google.com/file/d/1Cz60JtJpdVMrFds9RI6-9LgIqQ44rIJo/view?usp=drive_link](https://drive.google.com/file/d/1Cz60JtJpdVMrFds9RI6-9LgIqQ44rIJo/view?usp=drive_link).
* **Setup:** Unzip the downloaded file and ensure the directory `final_flan_t5_model` is placed in the root of this project repository.

### 3. Generating Summaries (Inference)
To run the summarizer on a new video, you can use the provided script in the `src` directory or write a simple Python script as follows:

```
from src.video_summarizer import VideoSummarizer

# Initialize the model
# Ensure 'final_flan_t5_model' exists in your current directory
summarizer = VideoSummarizer(model_path="./final_flan_t5_model")

# Run inference
url = "https://www.youtube.com/watch?v=VIDEO_ID"   # Remember to replace `VIDEO_ID`
summary = summarizer.generate_summary(url)
print(summary)
```

### 4. Reproducing Results and Figures
To reproduce the figures and evaluation metrics found in the final report:
1. Navigate to the `notebooks/` directory.
2. Open `final_analysis_and_plots.ipynb` using Jupyter Notebook or Google Colab. （TBA）
3. Execute the cells sequentially. Note that the training dataset (`gold_dataset_merged_final.csv`) must be present in the correct path as defined in the notebook.


## Data Access Statement

### 1. Source Data
This project utilizes the **YouTube Transcriptions** dataset hosted on Hugging Face.
* **Dataset Name:** `jamescalam/youtube-transcriptions`
* **Access:** Publicly available via the Hugging Face Datasets library.
* **URL:** https://huggingface.co/datasets/jamescalam/youtube-transcriptions
* **Ownership & License:** Data ownership resides with the original content creators on YouTube. This dataset is provided for research/educational purposes under the terms specified by the repository maintainer.

### 2. Derived Data (Synthetic Training Set)
To facilitate knowledge distillation, we generated a synthetic dataset containing "Gold Standard" summaries.
* **Method:** Generated using Google's Gemini 2.0 Pro API based on the source transcripts.
* **Availability:** The derived dataset (`gold_dataset_merged_final.csv`) is included in this repository for reproducibility: [https://github.com/sokkerstar123/Capstone/blob/main/data/gold_dataset_merged_final.csv](https://github.com/sokkerstar123/Capstone/blob/main/data/gold_dataset_merged_final.csv).
* **Terms of Use:** This derived data is intended solely for academic research and verifying the results of this project.

### 3. Model Weights
The fine-tuned model weights (`final_flan_t5_model`) are hosted externally due to file size limitations.
* **Access:** [https://drive.google.com/file/d/1Cz60JtJpdVMrFds9RI6-9LgIqQ44rIJo/view?usp=drive_link](https://drive.google.com/file/d/1Cz60JtJpdVMrFds9RI6-9LgIqQ44rIJo/view?usp=drive_link)
* **License:** The model is a derivative of `google/flan-t5-base` (Apache 2.0 License).

## License and Attribution

* **Code Attribution:** Certain segments of the RAG retrieval logic and text preprocessing were adapted from open-source documentation (e.g., Hugging Face Tutorials, YouTube Transcript API docs). These segments are explicitly marked with in-line attributions within the source code files.
* **License:** This project is licensed under the MIT License.

---
*This project was submitted in partial fulfillment of the requirements for the Master of Applied Data Science (MADS) program.*
