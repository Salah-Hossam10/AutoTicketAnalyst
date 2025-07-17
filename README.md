# Support Ticket Classification AI

## 📌 Overview
An automated system that classifies IT support tickets using Azure OpenAI's GPT-4o, dynamically categorizing issues based on customizable taxonomies.

## 🚀 Features
- **Comprehensive Classification**:
  - Identifies primary issue type (Bug/Feature/Docs)
  - Detects priority level with subcategories
  - Recognizes affected components
- **Dynamic Taxonomy**:
  - Loads category structures from JSON
  - Supports unlimited nesting levels
- **Production-Ready Output**:
  ```json
  {
    "analysis_results": [
      ["Issue Type", "Bug"],
      ["Priority", "High", "Performance"],
      ["Component", "Mobile"]
    ]
  }

## ⚙️ Installation
pip install openai python-dotenv

## 🏃‍♂️ Usage
python app.py [TICKET_FILE] [CATEGORIES_FILE] --model [DEPLOYMENT_NAME]

## Example
python app.py issue.txt categories.json --model gpt-4o --output results.json
