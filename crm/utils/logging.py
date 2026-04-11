# import logging
# import os
# from dotenv import load_dotenv

# load_dotenv(dotenv_path=".env.app")


# def get_logger(name="default"):
#     "Получить логгер в зависимости от окружения."
#     if os.getenv("CI") or os.getenv("GITHUB_ACTIONS"):
#         return logging.getLogger(f"ci.{name}")
#     return logging.getLogger(f"log_file.{name}")
