# romantic-quest_main
import anthropic
import os
from datetime import datetime
from fpdf import FPDF
import argparse
from google import genai


def create_message_with_reasoning_claude(prompt, output_dir="outputs"):
    """
    Create a message using Claude with reasoning mode enabled and export to txt and pdf

    Args:
        prompt (str): The prompt to send to Claude
        output_dir (str): Directory to save output files

    Returns:
        dict: The message response from Claude
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Initialize the client
    client = anthropic.Anthropic(
        # defaults to os.environ.get("ANTHROPIC_API_KEY")
    )

    # Create timestamp for filenames
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"{output_dir}/claude_response_{timestamp}"

    # Create the message with reasoning mode enabled
    message = client.messages.create(
        model="claude-3-7-sonnet-20250219",
        max_tokens=2024,
        messages=[{"role": "user", "content": prompt}],
        system="To answer this question, use reasoning mode to think through the answer step by step.",
        thinking={"type": "enabled", "budget_tokens": 1024},
    )
    print(message.content)
    print("Thinking block")
    print(message.content[0])
    print("----------------")
    print("Text block:")
    print(message.content[1].text)
    print("----------------")
    response_text = message.content[1].text

    # Save to text file
    with open(f"{filename_base}.txt", "w", encoding="utf-8") as txt_file:
        txt_file.write(response_text)

    # Save to PDF
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Split text into lines to handle line breaks
    lines = response_text.split("\n")
    for line in lines:
        # Add wrapped text
        pdf.multi_cell(0, 10, line)

    pdf.output(f"{filename_base}.pdf")
    ### markdown zu pdf
    print(f"Response saved to {filename_base}.txt and {filename_base}.pdf")

    return message


# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a sonnet using Claude.")
    parser.add_argument(
        "--prompt",
        type=str,
        default="I would like a sonnet about love",
        help="Prompt to send",
    )
    parser.add_argument(
        "--model", type=str, default="claude-3-7-sonnet-20250219", help="Model to use"
    )
    parser.add_argument(
        "--use_reasoning", action="store_true", help="Use reasoning mode"
    )
    args = parser.parse_args()
    prompt = args.prompt
    model = args.model
    if model == "claude-3-7-sonnet-20250219":
        message = create_message_with_reasoning_claude(prompt)
    print(message.content[0].text)
