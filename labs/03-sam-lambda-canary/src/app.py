import os


def handler(event, context):
    version = os.environ.get("APP_VERSION", "?")
    mode = os.environ.get("MODE", "ok")
    is_healthcheck = isinstance(event, dict) and event.get("healthcheck") is True

    if mode == "break-all":
        raise RuntimeError(f"version {version} is completely broken")
    if mode == "break-real" and not is_healthcheck:
        raise RuntimeError(f"version {version} fails for real traffic")

    return {"statusCode": 200, "body": f"hello from version {version}"}
