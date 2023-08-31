from .resources import RESOURCES
from . import assets
from dagster import Definitions
from dagster import load_assets_from_package_module

assets = load_assets_from_package_module(package_module=assets)
# all_assets = [*api]

deployment_name = "local"

defs = Definitions(
    assets=[*assets],
    resources= resources.RESOURCES[deployment_name],
)