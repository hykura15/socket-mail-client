import json

def load_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def classify_email(email, rules, default_folder):
    for rule in rules:
        if rule['type'] == 'sender' and email['sender'] == rule['value']:
            return rule['folder']
        elif rule['type'] == 'subject' and rule['value'] in email['subject']:
            return rule['folder']
        elif rule['type'] == 'keyword' and rule['value'] in email['content']:
            return rule['folder']
    return default_folder

# Example usage
if __name__ == "__main__":
    config = load_config('config.json')

    sample_email = {
        'sender': 'example@example.com',
        'subject': 'Important Meeting',
        'content': 'Hello, let\'s discuss the important matters in the meeting.'
    }

    folder = classify_email(sample_email, config['rules'], config['default_folder'])

