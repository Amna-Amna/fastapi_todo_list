import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from the project root .env file if present
env_path = Path(__file__).parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

DB_PASSWORD = os.getenv("DB_PASSWORD", "amnatelerelation123098")
DB_NAME = os.getenv("DB_NAME", "todoapplicationdatabase")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_USER = os.getenv("DB_USER", "root")

SECRET_KEY = os.getenv("SECRET_KEY", "pWgOD4aqUO4L3geaTVmv9sH7Gh4rlmbqjly-qkegf8FTOfp2Dnnxig3mzGyxQNhaw2ZCPCDenZIiXEPEaqTPyg")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

