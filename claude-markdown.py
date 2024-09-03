import json
import markdown
import os
import datetime
import argparse
import html
def convert_to_markdown(json_data, users_data, output_dir, use_full_name, organize_by_date):
    """
    Converts the JSON chat log data into Markdown format and writes each conversation to a separate file.
    
    Args:
    json_data (dict): The JSON chat log data.
    users_data (dict): The JSON users data.
    output_dir (str): The directory where the Markdown files will be written.
    use_full_name (bool): Whether to use the user's full name from the users.json file.
    """

    tz_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    users_map = {user['uuid']: user['full_name'] for user in users_data}

    conversations = []
    for conversation in json_data:
        created = datetime.datetime.strptime(conversation["created_at"], tz_format)
        updated = datetime.datetime.strptime(conversation["updated_at"], tz_format)
        conversations.append({
            'uuid': conversation['uuid'],
            'name': html.escape(conversation['name']),
            'created': created.strftime('%m/%d/%y'),
            'updated': updated.strftime('%m/%d/%y'),
        })

    conversations.sort(key=lambda x: x['updated'], reverse=True)

    markdown_data = "# Conversation List\n\n"
    markdown_data += "| Conversation Name | Last Update | Created |\n"
    markdown_data += "| --- | --- | --- |\n"
    for conversation in conversations:
        markdown_data += f"| [{html.escape(conversation['name'])}]({conversation['uuid']}.md) | {conversation['updated']} | {conversation['created']} |\n"

    with open(os.path.join(output_dir, 'conversation_list.md'), 'w', encoding='utf-8') as file:
        file.write(markdown_data)

    for conversation in json_data:
        conversation_markdown_data = f"# {html.escape(conversation['name'])}\n\n"
        created = datetime.datetime.strptime(conversation["created_at"], tz_format)
        conversation_markdown_data += f"Created: {created.strftime('%m/%d/%y %H:%M:%S')}\n"
        updated = datetime.datetime.strptime(conversation["updated_at"], tz_format)
        conversation_markdown_data += f"Updated: {updated.strftime('%m/%d/%y %H:%M:%S')}\n\n"
        for message in conversation['chat_messages']:
            created_at = datetime.datetime.strptime(message['created_at'], tz_format)
            sender_uuid = message['sender']
            if use_full_name and sender_uuid in users_map:
                conversation_markdown_data += f"{created_at.strftime('%m/%d/%y %H:%M:%S')} - **{users_map[sender_uuid]}** :\n"
            else:
                conversation_markdown_data += f"{created_at.strftime('%m/%d/%y %H:%M:%S')} - **{sender_uuid}** :\n"
            conversation_markdown_data += html.escape(message['text'].replace("\n", "\n    ")) + "\n\n"
            if message['attachments']:
                conversation_markdown_data += "Attachments:\n"
                for attachment in message['attachments']:
                    conversation_markdown_data += f"  * {attachment['file_name']} ({attachment['file_size']} bytes)\n"
                    conversation_markdown_data += f"    {attachment['extracted_content'].replace('\n', '\n    ')}\n\n"
            if message['files']:
                conversation_markdown_data += "Files:\n"
                for file in message['files']:
                    conversation_markdown_data += f"  * {file['file_name']}\n"
        
        # Logic for Organize by Date
        if organize_by_date:
            folder_name = conversation['updated_at'][:10]  # YYYY-MM-DD
            folder_path = os.path.join(output_dir, folder_name)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        else:
            folder_path = output_dir        
        
        
        filename = f"{conversation['uuid']}.md"
        with open(os.path.join(folder_path, filename), 'w', encoding='utf-8') as file:
            file.write(conversation_markdown_data)

def main():
    parser = argparse.ArgumentParser(description='Convert chat log data to Markdown format')
    parser.add_argument('--use-full-name', action='store_true', help='Use the user\'s full name from the users.json file')
    parser.add_argument('--organize-by-date', action='store_true', help='Organize files into subfolders by last updated date')
    args = parser.parse_args()

    data_dir = 'data'
    json_file = os.path.join(data_dir, 'conversations.json')
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)
    
    users_file = os.path.join(data_dir, 'users.json')
    with open(users_file, 'r', encoding='utf-8') as file:
        users_data = json.load(file)
    
    markdown_dir = os.path.join(data_dir, 'conversations_markdown')
    convert_to_markdown(json_data, users_data, markdown_dir, args.use_full_name, args.organize_by_date)


if __name__ == "__main__":
    main()
