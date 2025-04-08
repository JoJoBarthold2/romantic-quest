# romantic-quest_main
import anthropic
import os
from datetime import datetime
from fpdf import FPDF
import argparse
from google import genai
from google.genai import types
import google.api_core.exceptions
import logging

logging.basicConfig(level=logging.INFO)

def save_to_txt_and_pdf(text, filename_base):
    """
    Save the text to both txt and pdf files.

    Args:
        text (str): The text to save
        filename_base (str): Base filename for the output files
    """
    # Save to txt file
    with open(f"{filename_base}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(text)
    str_bytes = text.encode('utf-8')         # Convert string to UTF-8 bytes
    decoded_str = str_bytes.decode('latin-1')    # Decode as ISO-8859-1 (mimics utf8_decode)

    # Save to pdf file
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, decoded_str)
    pdf.output(f"{filename_base}.pdf")

def create_message_with_reasoning_claude(prompt, output_dir="outputs", system_prompt="You are an experienced writer that writes dark romance novels.", max_tokens=2024):
    """
    Create a message using Claude with reasoning mode enabled and export to txt and pdf

    Args:
        prompt (str): The prompt to send to Claude
        output_dir (str): Directory to save output files

    Returns:
        dict: The message response from Claude
    """
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize the client
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )

    # Create timestamp for filenames
   
    timestamp = datetime.now().strftime("%d_%m_%Y_%Hh_%Mmin")
    filename_base = f"{output_dir}/claude_response_{timestamp}"
    system_prompt =  "To fulfill this task, use reasoning mode to think through the answer step by step. " + system_prompt
    logging.info(f"System prompt: {system_prompt}")
    logging.info(f"Max tokens: {max_tokens}")
    # Create the message with reasoning mode enabled
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
        system= system_prompt,
        thinking={"type": "enabled", "budget_tokens": 1024},
    )
    logging.info(f"Claude response: {message}")
    #logging.info(f"Output tokens: {message.content[]}")
    save_to_txt_and_pdf(message.content[1].text, filename_base)
    return message



def create_book_with_gemini(prompt, output_dir="outputs", system_prompt="You are an experienced writer that writes dark romance novels."):
    """
    Create a book using Gemini and export to txt and pdf

    Args:
        prompt (str): The prompt to send to Gemini
        output_dir (str): Directory to save output files

    Returns:
        dict: The message response from Gemini
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    api_key = os.environ.get("GEMINI_API_KEY")
    # Initialize the client
    client = genai.Client(
      api_key=  api_key
    )

    # Create timestamp for filenames
    timestamp = datetime.now().strftime("%d_%m_%Y_%Hh_%Mmin")
    filename_base = f"{output_dir}/gemini_response_{timestamp}"

    
 

    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=prompt,
    config= types.GenerateContentConfig(
        system_instruction=system_prompt),
        )

    logging.info(f"Gemini response: {response}")

    logging.info(f"Gemini response text: {response.text}")

    save_to_txt_and_pdf(response.text, filename_base)
    return response


    

    


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate text using Claude and/or Gemini.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="I would like a sonnet about love",
        help="Prompt to send to the model(s)",
    )
    parser.add_argument(
        "--claude", action="store_true", help="Call Claude to generate a response"
    )
    parser.add_argument(
        "--gemini", action="store_true", help="Call Gemini to generate a response"
    )
    parser.add_argument(
        "--claude_model",
        type=str,
        default="claude-3-7-sonnet-20250219",
        help="Claude model to use",
    )
    parser.add_argument(
        "--gemini_model",
        type=str,
        default="gemini-pro",
        help="Gemini model to use",
    )
    parser.add_argument(
        "--use_reasoning",
        action="store_true",
        help="Use reasoning mode for Claude (if called)",
    )
    parser.add_argument("--max_tokens", type=int, default=2024, help="Max tokens for the model")
    parser.add_argument("--system_prompt", type=str, default="You are an experienced writer that writes dark romance novels in german. You are eager to write your new book. You take care to create a consitent narrative. You don't refrain from writing about sexual themes when necessary. However you keep it tasteful.", help="System prompt for the model")
    parser.add_argument( "--debug", action="store_true", help="Enable debug mode"
    )
    args = parser.parse_args()
    prompt = args.prompt
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    logging.debug(f"Prompt: {prompt}")
    if args.claude:
        if args.claude_model == "claude-3-7-sonnet-20250219":
            claude_response = create_message_with_reasoning_claude(prompt, output_dir="outputs", system_prompt=args.system_prompt, max_tokens=args.max_tokens)
            

    if args.gemini:
       create_book_with_gemini(prompt)