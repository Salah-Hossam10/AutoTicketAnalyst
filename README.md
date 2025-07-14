# Support Ticket Classification AI

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Azure OpenAI](https://img.shields.io/badge/Azure_OpenAI-GPT4o-purple.svg)

An AI-powered system for automatically classifying support tickets using Azure OpenAI's GPT-4o model.

## Features

- 🚀 Automatic classification of support tickets
- 🔍 Multi-label categorization (identifies all relevant categories)
- ⚙️ Dynamic category loading from JSON configuration
- 📊 Structured JSON output with detailed analysis

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/support-ticket-ai.git
   cd support-ticket-ai
Install dependencies:

bash
pip install openai python-dotenv
Usage
Basic Command
bash
python app.py issue.txt categories.json --model gpt-4o
Options
Parameter	Description	Example
ticket_file	Path to ticket text file	issue.txt
categories_file	Path to categories JSON file	categories.json
--model	Azure OpenAI deployment name	gpt-4o (required)
--output	Optional output file path	results.json
Example Output
Results are saved in results.json with the following format:

json
{
  "analysis_results": [
    ["Issue Type", "Bug"],
    ["Priority", "High", "Performance"],
    ["Component", "Mobile"]
  ]
}
Configuration
Edit categories.json to customize your classification taxonomy

Ensure your Azure OpenAI credentials are properly configured

Sample Files
Example ticket: issue.txt

Category definition: categories.json
