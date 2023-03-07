
import os
import sys
# need pip3 install openai first
import openai
import configparser

COMMIT_MSG_FILE = sys.argv[1]

# get current branch diff
def get_diff():
    """
        Get the diff of the current branch
    """
    return os.popen("git diff").read()
current_commit_file_content = open(COMMIT_MSG_FILE, 'r').read()

CONFIG_DIR = os.getenv("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
API_KEYS_LOCATION = os.path.join(CONFIG_DIR, "openaiapirc")

def create_template_ini_file():
    # """
    # If the ini file does not exist create it and add the organization_id and
    # secret_key
    # """
    """
    If the ini file does not exist create it and add the secret_key
    """
    if not os.path.isfile(API_KEYS_LOCATION):
        with open(API_KEYS_LOCATION, "w") as f:
            f.write("[openai]\n")
            # f.write("organization_id=\n")
            f.write("secret_key=\n")

        print("OpenAI API config file created at {}".format(API_KEYS_LOCATION))
        print("Please edit it and add your organization ID and secret key")
        print(
            "If you do not yet have an organization ID and secret key, you\n"
            "need to register for OpenAI Codex: \n"
            "https://openai.com/blog/openai-codex/"
        )
        sys.exit(1)


def initialize_openai_api():
    """
    Initialize the OpenAI API
    """
    # Check if file at API_KEYS_LOCATION exists
    create_template_ini_file()
    config = configparser.ConfigParser()
    config.read(API_KEYS_LOCATION)

    # openai.organization_id = config["openai"]["organization_id"].strip('"').strip("'")
    openai.api_key = config["openai"]["secret_key"].strip('"').strip("'")

initialize_openai_api()

messages = [
{'role': 'system', 'content': 'You are a helpful assistant writes short git commit messages.'},
{'role': 'user', 'content': f'{get_diff()}\n\nWrite the commit message.'},
]

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    # model="text-davinci-003",
  messages=messages,
)

response_text = response["choices"][0]["message"]['content']

content_whole_file = response_text + current_commit_file_content

with open(COMMIT_MSG_FILE, 'w') as f:
    f.write(content_whole_file)
