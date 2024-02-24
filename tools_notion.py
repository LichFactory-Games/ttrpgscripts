import os
import re

def combine_markdown_files(input_dir, output_file):
    """
    Combines all Markdown files in the specified directory into a single file,
    excluding the output file if it exists in the same directory. It also removes
    Markdown link formatting, converting links from [link text](URL) to just link text
    and removing any Markdown file references within parentheses.

    Args:
    input_dir (str): The directory containing Markdown files to combine.
    output_file (str): The path to the output file where the combined content will be saved.
    """
    combined_content = ""
    for filename in os.listdir(input_dir):
        file_path = os.path.join(input_dir, filename)
        # Check if the file is a Markdown file and not the output file
        if filename.endswith('.md') and file_path != output_file:
            with open(file_path, 'r', encoding='utf-8') as file:
                combined_content += file.read() + "\n\n"
    
    # Remove Markdown links, converting [link text](URL) to just link text
    combined_content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', combined_content)
    # Remove Markdown file references
    combined_content = re.sub(r'\([^\s]+\.md\)', '', combined_content)
    
    # Write the combined content to the output file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_content)

def adjust_markdown_header_levels(file_path, adjustment):
    """
    Adjusts the level of all headers in a Markdown file.

    Args:
    file_path (str): The path to the Markdown file to be modified.
    adjustment (int): The number of levels to adjust the headers by. Positive to increase levels, negative to decrease.
    """
    if adjustment == 0:
        return  # No adjustment needed

    # Read the original content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Define a function to use in the re.sub replacement
    def adjust_header(match):
        header_level = len(match.group(1))  # Determine the original level of the header
        new_level = max(1, header_level + adjustment)  # Calculate the new level, ensuring it's at least 1
        return '#' * new_level + ' ' + match.group(2)  # Return the adjusted header

    # Use a regular expression to find headers and adjust their levels
    adjusted_content = re.sub(r'^(#{1,6})\s+(.*)', adjust_header, content, flags=re.MULTILINE)

    # Write the adjusted content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(adjusted_content)

def remove_markdown_headers_of_level(file_path, level):
    """
    Removes all headers of a specific level from a Markdown file.

    Args:
    file_path (str): The path to the Markdown file to be modified.
    level (int): The level of headers to remove (1 for #, 2 for ##, etc.).
    """
    # Construct the header pattern to match based on the specified level
    header_pattern = f'^({"#" * level})\\s+.*$'

    # Read the original content of the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.readlines()

    # Use a list comprehension to filter out the specified level headers
    adjusted_content = [line for line in content if not re.match(header_pattern, line)]

    # Write the adjusted content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines(adjusted_content)


if __name__ == "__main__":
    
    # Example usage
    input_directory = r"C:\Users\mathg\Desktop\Notion_Markdown\Tales of Orinthia f20c8bf900e440ed966f1919912ddede\Characters da77c631f3b44322b8de3c359180ca5a\Characters 57540f38a6a040b6a4cec727baf96770"
    output_file_path = r"C:\Users\mathg\Desktop\characters.md"
    combine_markdown_files(input_directory, output_file_path)
    
    # remove_markdown_headers_of_level(output_file_path, 2)
    
    adjust_markdown_header_levels(output_file_path, 1)
