from __future__ import annotations
import yaml


def extend_env(base, env):
    base_conda = base.get("conda", [])
    base_pip = base.get("pip", [])
    conda = env.get("conda", [])
    pip = env.get("pip", [])
    conda.extend(base_conda)
    pip.extend(base_pip)
    return {"pip": list(sorted(set(pip))), "conda": list(sorted(set(conda)))}


# thanks to https://github.com/yaml/pyyaml/issues/234#issuecomment-765894586
class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def dump_env(env_dir, name, env, vim=True):
    """take my garbo dict of env and put in the conda forge format

    Parameters
    ----------
    name : str
    env : dict
    vim : boolean
        If True also generate a vim version with jupyterlab vim plugins
    """
    conda = list(env.get("conda", []))
    pip = list(env.get("pip", []))

    dependencies = list(conda)
    dependencies.append({"pip": pip})

    env = {"name": name, "channels": ["conda-forge"], "dependencies": dependencies}
    with open(env_dir / (name + ".yaml"), "w") as f:
        yaml.dump(env, f, Dumper=Dumper)

    if vim:
        dependencies = list(conda) + ["jupyterlab-vim"]
        pip.append("jupyterlab-vimrc")
        dependencies.append({"pip": pip})

        env = {"name": name, "channels": ["conda-forge"], "dependencies": dependencies}
        with open(env_dir / (name + "-vim.yaml"), "w") as f:
            yaml.dump(env, f, Dumper=Dumper)
