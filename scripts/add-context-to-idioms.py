#!/usr/bin/env python3
"""
Add context fields to idioms using Cerebras LLM.
"""
import json
import os
import sys
import time
from typing import Dict, List, Optional
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_idioms(filepath: str) -> List[str]:
    """Load idioms from JSON file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_idioms_with_context(filepath: str, idioms_with_context: List[Dict[str, str]]) -> None:
    """Save idioms with context to JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(idioms_with_context, f, ensure_ascii=False, indent=2)

def generate_context(client: Cerebras, idiom_entry: str, model: str = "qwen-3-32b") -> Optional[str]:
    """Generate context for a single idiom using Cerebras API."""
    # Parse the idiom and definition
    parts = idiom_entry.split(": ", 1)
    if len(parts) != 2:
        return None
    
    chinese_idiom, definition = parts
    
    prompt = f"""For the Chinese idiom "{chinese_idiom}" which means "{definition}", 
provide a general description of situations where this idiom would apply (2-3 sentences). 
Make it broad enough to cover various scenarios, not just one specific example.
Focus on the core meaning and patterns rather than specific instances.
Do not include the Chinese idiom in your response.
Provide only the context description without any thinking process or tags.

Example: Instead of "A company refuses to update old software", say "When someone or something remains fixed in established patterns and resists any form of change or modernization, regardless of the context or benefits of updating."
"""
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that provides clear, concise responses without showing your thinking process."
                },
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            max_tokens=150,
            temperature=0.7,
        )
        
        context = chat_completion.choices[0].message.content.strip()
        
        # Clean up any thinking tags if present
        if "<think>" in context:
            # Extract text after thinking process
            parts = context.split("</think>")
            if len(parts) > 1:
                context = parts[-1].strip()
            else:
                # If no closing tag, try to extract meaningful content
                context = context.split("<think>")[0].strip()
        
        # If context is empty after cleaning, return a generic message
        if not context:
            context = "Context could not be generated properly. Please try again."
        
        return context
    except Exception as e:
        print(f"Error generating context for '{chinese_idiom}': {e}")
        return None

def process_idioms(input_file: str, output_file: str, api_key: str, 
                  model: str = "qwen-3-32b", batch_size: int = 10,
                  delay_seconds: float = 0.5, limit: Optional[int] = None) -> None:
    """Process idioms file and add context fields."""
    # Initialize Cerebras client
    client = Cerebras(api_key=api_key)
    
    # Load idioms
    print(f"Loading idioms from {input_file}...")
    idiom_entries = load_idioms(input_file)
    
    # Apply limit if specified
    if limit:
        idiom_entries = idiom_entries[:limit]
        print(f"Processing first {limit} idioms for testing")
    
    total_idioms = len(idiom_entries)
    print(f"Found {total_idioms} idioms to process")
    
    # Process idioms
    idioms_with_context = []
    
    for i, idiom_entry in enumerate(idiom_entries):
        # Parse existing entry
        parts = idiom_entry.split(": ", 1)
        if len(parts) != 2:
            print(f"Skipping invalid entry: {idiom_entry}")
            continue
        
        chinese_idiom, definition = parts
        
        # Generate context
        print(f"Processing {i+1}/{total_idioms}: {chinese_idiom}")
        context = generate_context(client, idiom_entry, model)
        
        # Create new entry with context
        entry = {
            "idiom": chinese_idiom,
            "definition": definition,
            "context": context if context else "Context generation failed"
        }
        idioms_with_context.append(entry)
        
        # Save progress periodically
        if (i + 1) % batch_size == 0:
            print(f"Saving progress... ({i+1}/{total_idioms})")
            save_idioms_with_context(output_file, idioms_with_context)
        
        # Rate limiting
        if i < total_idioms - 1:  # Don't delay after last item
            time.sleep(delay_seconds)
    
    # Final save
    print(f"Saving final results to {output_file}...")
    save_idioms_with_context(output_file, idioms_with_context)
    print(f"Successfully processed {len(idioms_with_context)} idioms!")

def main():
    # Check for API key
    api_key = os.environ.get("CEREBRAS_API_KEY")
    if not api_key:
        print("Error: CEREBRAS_API_KEY environment variable not set")
        print("Please set it with: export CEREBRAS_API_KEY='your-api-key'")
        sys.exit(1)
    
    # File paths
    input_file = "data/idioms-and-definitions.json"
    output_file = "data/idiom-definition-context.json"
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    # Check for test mode
    test_mode = "--test" in sys.argv
    limit = 5 if test_mode else None
    
    if test_mode:
        print("Running in TEST MODE - processing only first 5 idioms")
        output_file = "data/idioms-with-context-test.json"
    
    # Process idioms
    process_idioms(
        input_file=input_file,
        output_file=output_file,
        api_key=api_key,
        model="qwen-3-32b",
        batch_size=10,  # Save progress every 10 idioms
        delay_seconds=0.5,  # Small delay between API calls
        limit=limit
    )

if __name__ == "__main__":
    main()