from dotenv import dotenv_values
import re


class ConfigService:

    def __init__(self):
        self.config = dotenv_values(".env")

    def get_logs_dir(self):
        return self.config["LOGS_DIR"]

    def get_database_url(self):
        print(self.config["DATABASE_URL"])
        return self.config["DATABASE_URL"]

    def get_database_port(self):
        pattern = r":[0-9]+"
        matches = re.findall(pattern, self.get_database_url())
        length = len(matches)
        if length > 0:
            return int(matches[length - 1].split(":")[1])

        raise ValueError("Port not found in the database url")

    def get_openai_token(self) -> str:
        return self.config["OPENAI_TOKEN"]

    def get_server_uri(self):
        return self.config["SERVER_URI"]

    def get_env(self):
        return self.config["ENV"]

    def get_sentry_dsn(self):
        return self.config["SENTRY_PYTHON_DSN"]

    def get_default_max_reads(self):
        return 50

    def is_docs_enabled(self) -> bool:
        if self.config["ENABLE_DOCS"].lower() in ['yes', 'true']:
            return True
        return False

    def get_temp_dir(self):
        return self.config["TEMP_DIR"]

    def get_documents_batch_size(self):
        return int(self.config["DOCUMENTS_BATCH_SIZE"])

    def get_auth_cookie_name(self):
        return "auth-cookie"

    def get_SSL_certificate(self):
        return self.config.get("SSL_CERTFILE", "")

    def get_SSL_key(self):
        return self.config.get("SSL_KEYFILE", "")
