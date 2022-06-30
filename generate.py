from __future__ import annotations

import yaml
from pathlib import Path

from funcs import extend_env, dump_env

envs = {}
base_dir = Path(__file__).parent
env_dir = base_dir / "envs"
env_dir.mkdir(parents=True, exist_ok=True)
with open(base_dir / "definitions.yaml") as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

for name, env_info in data.items():
    info = {k: v for d in env_info for k, v in d.items()}
    if name == "base":
        envs["base"] = {"conda": info.get("conda", []), "pip": info.get("pip", [])}
    if "based-on" in info:
        env = info
        for base in list(info["based-on"]):
            info = extend_env(envs[base], info)
        envs[name] = info


for name, env in envs.items():
    dump_env(env_dir, name, env, vim=True)
    dump_env(env_dir, name, env, vim=False)
