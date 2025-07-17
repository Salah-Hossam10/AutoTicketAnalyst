import json
import openai
import os
from typing import List, Dict, Any, Optional

class SupportTicketClassifier:
    """
    A class to classify support tickets using a dynamic category hierarchy and Azure OpenAI analysis.
    """
    
    def __init__(self):
        self.client = openai.AzureOpenAI(
            api_key="api_key",
            api_version="api_version", 
            azure_endpoint="azure_endpoint"
        )

    def load_categories(self, categories_file: str) -> List[Dict[str, Any]]:
        """
        Load and validate the categories from a JSON file.
        """
        try:
            with open(categories_file, 'r') as f:
                categories = json.load(f)
                
            if not isinstance(categories, list):
                raise ValueError("Categories file should contain a JSON array")
                
            return categories
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in categories file: {e}")
        except FileNotFoundError:
            raise ValueError(f"Categories file not found: {categories_file}")
    
    def load_ticket(self, ticket_file: str) -> str:
        """
        Load the ticket description from a text file.
        """
        try:
            with open(ticket_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            raise ValueError(f"Ticket file not found: {ticket_file}")
    
    def _build_category_prompt(self, categories: List[Dict[str, Any]]) -> str:
        """
        Build the category description part of the prompt.
        """
        prompt_parts = []
        
        def build_category_tree(category: Dict[str, Any], level: int = 0) -> str:
            indent = "  " * level
            parts = [f"{indent}- {category['value']}"]
            if 'description' in category:
                parts.append(f" ({category['description']})")
            
            if 'subcategories' in category:
                for subcat in category['subcategories']:
                    parts.append("\n" + build_category_tree(subcat, level + 1))
            
            return "".join(parts)
        
        for category in categories:
            prompt_parts.append(build_category_tree(category))
        
        return "\n".join(prompt_parts)
    
    def classify_ticket(
        self, 
        ticket_content: str, 
        categories: List[Dict[str, Any]],
        model: str = "gpt-4o"  
    ) -> Dict[str, List[List[str]]]:
        """
        Classify a support ticket using the provided categories.
        """
        category_prompt = self._build_category_prompt(categories)
        
        system_prompt = f"""
        You are an expert support ticket classifier. Your task is to analyze support tickets 
        and categorize them according to the following category hierarchy:
        
        {category_prompt}
        
        Rules:
        1. Analyze the ticket thoroughly and identify ALL relevant categories and subcategories
        2. For each identified aspect, provide the FULL PATH from top-level category to most specific subcategory
        3. Only use categories and subcategories that are explicitly defined in the hierarchy
        4. If no categories match, return an empty list
        5. Be as specific as possible - always go to the deepest matching subcategory
        6. Return your response as a JSON object with a single key "analysis_results" containing a list of lists
           (each inner list represents one category path)
        
        Example output format:
        {{
          "analysis_results": [
            ["Issue Type", "Bug"],
            ["Priority", "High", "Performance"],
            ["Component", "Frontend"]
          ]
        }}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": ticket_content}
                ],
                response_format={"type": "json_object"},
                temperature=0.1
            )
            
            result = json.loads(response.choices[0].message.content)
            
            if not isinstance(result, dict) or "analysis_results" not in result:
                raise ValueError("Invalid response format from API")
                
            if not isinstance(result["analysis_results"], list):
                raise ValueError("analysis_results should be a list")
                
            for item in result["analysis_results"]:
                if not isinstance(item, list):
                    raise ValueError("Each analysis result should be a list")
                    
            return result
            
        except Exception as e:
            raise ValueError(f"API call failed: {e}")
    
    def process_ticket(
        self, 
        ticket_file: str, 
        categories_file: str,
        output_file: Optional[str] = None,
        model: str = "gpt-4o"  
    ) -> Dict[str, List[List[str]]]:
        """
        Complete pipeline to load files, classify ticket, and return/print results.
        """
        try:
            categories = self.load_categories(categories_file)
            ticket_content = self.load_ticket(ticket_file)
            
            results = self.classify_ticket(ticket_content, categories, model)
            
            if output_file:
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
                print(f"Results saved to {output_file}")
            else:
                print(json.dumps(results, indent=2))
                
            return results
            
        except ValueError as e:
            print(f"Error: {e}")
            raise

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Support Ticket Classifier using Azure OpenAI")
    parser.add_argument("ticket_file", help="Path to the ticket text file")
    parser.add_argument("categories_file", help="Path to the JSON categories file")
    parser.add_argument("--output", help="Optional output file path")
    parser.add_argument("--model", default="gpt-4o", 
                       help="Azure OpenAI deployment name (default: gpt-4o)")
    
    args = parser.parse_args()
    
    classifier = SupportTicketClassifier()
    classifier.process_ticket(
        args.ticket_file, 
        args.categories_file, 
        args.output,
        args.model
    )

if __name__ == "__main__":
    main()
