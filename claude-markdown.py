import json
import markdown
import os
import datetime
import argparse
import html
def convert_to_markdown(json_data, output_dir, organize_by_date):
    """
    Converts the JSON chat log data into Markdown format and writes each conversation to a separate file.
    
    Args:
    json_data (dict): The JSON chat log data.
    output_dir (str): The directory where the Markdown files will be written.
    organize_by_date (bool): Whether to organize files into subfolders by last updated date.
    """

    tz_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    conversations = []
    for conversation in json_data:
        created = datetime.datetime.strptime(conversation["created_at"], tz_format)
        updated = datetime.datetime.strptime(conversation["updated_at"], tz_format)
        conversations.append({
            'uuid': conversation['uuid'],
            'name': conversation['name'],
            'created': created.strftime('%m/%d/%y'),
            'updated': updated.strftime('%m/%d/%y'),
        })

    conversations.sort(key=lambda x: datetime.datetime.strptime(x['updated'], '%m/%d/%y'), reverse=True)
    conversation_list_markdown = generate_conversation_list_markdown(conversations)
    with open(os.path.join(output_dir, 'conversation_list.md'), 'w', encoding='utf-8') as file:
        file.write(conversation_list_markdown)

    for conversation in json_data:
        conversation_markdown = generate_conversation_markdown(conversation)
        folder_path = get_folder_path(conversation, output_dir, organize_by_date)
        filename = f"{conversation['uuid']}.md"
        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
            file.write(conversation_markdown)

def generate_conversation_list_markdown(conversations):
    markdown_data = "# Conversation List\n\n"
    markdown_data += "| Conversation Name | Last Update | Created |\n"
    markdown_data += "| --- | --- | --- |\n"
    for conversation in conversations:
        markdown_data += f"| [{conversation['name']}]({conversation['uuid']}.md) | {conversation['updated'].replace('/', '-')} | {conversation['created'].replace('/', '-')} |\n"
    return markdown_data

def generate_conversation_markdown(conversation):
    tz_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    conversation_markdown = f"# {conversation['name']}\n\n"
    created = datetime.datetime.strptime(conversation["created_at"], tz_format)
    conversation_markdown += f"Created: {created.strftime('%m/%d/%y %H:%M')}\n"
    updated = datetime.datetime.strptime(conversation["updated_at"], tz_format)
    conversation_markdown += f"Updated: {updated.strftime('%m/%d/%y %H:%M')}\n\n"
    for message in conversation['chat_messages']:
        created_at = datetime.datetime.strptime(message['created_at'], tz_format)
        sender_uuid = message['sender']
        conversation_markdown += f"{created_at.strftime('%m/%d/%y %H:%M')} - **{sender_uuid}** :\n"
        conversation_markdown += message['text'].replace("\n", "\n    ") + "\n\n"
        if message['attachments']:
            conversation_markdown += "Attachments:\n"
            for attachment in message['attachments']:
                conversation_markdown += f"  * {attachment['file_name']} ({attachment['file_size']} bytes)\n"
                conversation_markdown += f"    {attachment['extracted_content'].replace('\n', '\n    ')}\n\n"
        if message['files']:
            conversation_markdown += "Files:\n"
            for file in message['files']:
                conversation_markdown += f"  * {file['file_name']}\n"
    return conversation_markdown

def get_folder_path(conversation, output_dir, organize_by_date):
    if organize_by_date:
        folder_name = conversation['updated_at'][:7]  # YYYY-MM
        folder_path = os.path.join(output_dir, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        return folder_path
    else:
        return output_dir

def main():
    parser = argparse.ArgumentParser(description='Convert chat log data to Markdown format')
    parser.add_argument('--organize-by-date', action='store_true', help='Organize files into subfolders by last updated date')
    args = parser.parse_args()

    data_dir = 'data'
    json_file = os.path.join(data_dir, 'conversations.json')

    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    markdown_dir = os.path.join(data_dir, 'conversations_markdown')
    convert_to_markdown(json_data, markdown_dir, args.organize_by_date)


if __name__ == "__main__":
    main()
