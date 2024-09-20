import re
from datetime import datetime, timedelta

def tokenize(text):
    """Splits text into words based on whitespace and punctuation."""
    tokens = re.findall(r'\b\w+\b', text.lower())
    return tokens

def extract_dates_times(text):
    """Extract dates and times from the text based on improved patterns."""
    dates = []
    times = []

    # Date patterns
    date_patterns = [
        r'\b(\d{4}-\d{2}-\d{2})\b',    # YYYY-MM-DD
        r'\b(\d{2}/\d{2}/\d{4})\b',    # MM/DD/YYYY
        r'\b(\d{1,2}\s+\w+\s+\d{4})\b' # e.g., 5 September 2024
    ]
    # Time patterns
    time_patterns = [
        r'\b(\d{1,2}:\d{2}\s*[APM]{2})\b',  # 2:00 PM or 2:00PM
        r'\b(\d{1,2}\s*[APM]{2})\b',        # 5 PM or 5pm
        r'\b(\d{1,2}\s*[-/]\s*\d{2}\s*[APM]{2})\b' # Handles times like 5-7 PM
    ]

    for pattern in date_patterns:
        dates.extend(re.findall(pattern, text))
    for pattern in time_patterns:
        times.extend(re.findall(pattern, text, re.IGNORECASE))

    lower_text = text.lower()
    if "today" in lower_text:
        dates.append(datetime.now().strftime("%Y-%m-%d"))
    if "tomorrow" in lower_text:
        dates.append((datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d"))

    return dates, times

def extract_task(text):
    """Extract simple task descriptions from the text."""
    tokens = tokenize(text)
    stop_words = {"the", "is", "in", "at", "of", "and", "a", "to", "with"}
    task = ' '.join(token for token in tokens if token not in stop_words)
    return task if task else "No specific task identified"

def main():
    while True:
        user_input = input("Enter a task description (or type 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break
        
        dates, times = extract_dates_times(user_input)
        print(f"Dates found: {dates}")
        print(f"Times found: {times}")
        
        task = extract_task(user_input)
        print(f"Extracted task: {task}")

if __name__ == "__main__":
    main()
