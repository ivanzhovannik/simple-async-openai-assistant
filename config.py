from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="ASYNC_OPENAI_ASSISTANT",
    settings_files=["settings.yaml", ".secrets.yaml"],
    merge_enabled=True,
)