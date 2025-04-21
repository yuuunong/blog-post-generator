import os 
import boto3
from dotenv import load_dotenv


def __set_api_key():
    GROQ_API_KEY = os.environ.get('GROQ_API_KEY', None)

    if not GROQ_API_KEY:
        ssm = boto3.client('ssm')
        parameter = ssm.get_parameter(Name='/CICD/BLOG-POST-GENERATOR/GROQ_API_KEY', WithDecryption=True)
        os.environ['GROQ_API_KEY'] = parameter['Parameter']['Value']


def init_chatbot():
    load_dotenv()
    __set_api_key()


