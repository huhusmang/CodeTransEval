from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # openai
    openai_api_key: str

    # MiniMax
    minimax_group_id: str
    minimax_secret_key: str

    # Qwen
    qwen_api_key: str

    # Wenxin
    wenxin_api_key: str
    wenxin_secret_key: str

    # Spark
    spark_app_id: str
    spark_api_key: str
    spark_api_secret: str

    # Zhipu
    zhipu_api_key: str


settings = Settings()
