from dynaconf import Dynaconf

config_root = "config"

settings = Dynaconf(
    envvar_prefix="ASYNC_OPENAI_ASSISTANT",
    settings_files=["settings.yaml", ".secrets.yaml"],
    merge_enabled=True,
)