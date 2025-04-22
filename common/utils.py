import os 
import boto3
from dotenv import load_dotenv


def __set_api_key():
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)

    if not GROQ_API_KEY:
        ssm = boto3.client('ssm')

        # Groq API Key
        parameter = ssm.get_parameter(Name='/CICD/BLOG-POST-GENERATOR/GROQ_API_KEY', WithDecryption=True)
        os.environ['GROQ_API_KEY'] = parameter['Parameter']['Value']

        # Langchain API Key
        parameter = ssm.get_parameter(Name='/CICD/BLOG-POST-GENERATOR/LANGCHAIN_API_KEY', WithDecryption=True)
        os.environ['LANGCHAIN_API_KEY'] = parameter['Parameter']['Value']
        os.environ['LANGCHAIN_PROJECT'] = 'blog-post-generator'
        os.environ['LANGCHAIN_TRACING_V2'] = 'true'
        os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'


def init_chatbot():
    load_dotenv()
    __set_api_key()


