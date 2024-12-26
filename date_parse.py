import dateparser

# Example user input
user_input = "The meeting is tomorrow at 3PM."
user_input = user_input.split(" ")
# Parse the date/time from the text
for s in user_input:
    parsed_date = dateparser.parse(s)
    print("Parsed Date:", parsed_date)
