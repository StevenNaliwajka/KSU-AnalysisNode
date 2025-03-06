# Generic_VENV_Manger
https://github.com/StevenNaliwajka/Generic_VENV_Manger  
Builds a VENV and handles running python files within the VENV.
------------------
# Setup.
### 1) Install Project as a Subtree with git.

To integrate this repo into your project.  
Navigate to the location of where you want it in CMD and input a variation of this:
```angular2html
git subtree add --prefix=PATH/TO/FOLDER/Generic_VENV_Manger https://github.com/StevenNaliwajka/Generic_VENV_Manger.git main --squash
```

### 2) Run Setup Python Files to create JSON config.
Two setup files, run one or both.

For Package Install Management:
```angular2html
python3 PATH/TO/Generic_VENV_Manager/VENVSetup/setup_packages_file.py
```

For Runtime Environment Variable Management:
```angular2html
python3 PATH/TO/Generic_VENV_Manager/VENVSetup/setup_run_env_file.py
```

### 3) Final git tracking setup.
Ensure to add 'venv' to ".gitignore" file. In new proj root run:
```angular2html
echo venv >> .gitignore
```
IF you added package install management, force tracking.
```angular2html
git add -f PATH/TO/Generic_VENV_Manger/packages.json
```
SAME for IF you added the Runtime Enviroment Variable Management, force tracking.
```angular2html
git add -f PATH/TO/Generic_VENV_Manager/run_env_var.json
```
### 4) In the future.
To update to the latest version of this repo.
```angular2html
git subtree pull --prefix=PATH/TO/FILE/Generic_VENV_Manger https://github.com/StevenNaliwajka/Generic_VENV_Manger.git main --squash
```
------------------

## Using the tools.
### Create VENV:
Fill out required 'pacakges.json' and/or "run_env_var.json".  
To Generate the VENV, call:    
```angular2html
VENVUtil.setup_venv("~/PATH/TO/ROOT")
```
### Run with VENV:
To run programs with the VENV, call:  
```angular2html
VENVUtil.run_with_venv("~/PATH/TO/ROOT", "~/PATH/TO/PYTHON.PY")
```

Any script being the 'entry point' of the VENV to the program should have before any imports:  
IE: any program that gets called by run_with_venv should always have this codeblock.
```angular2html
import sys
from pathlib import Path

# Dynamically find the project root, required to allow for correct imports.
folder_ct = 2  ### NOT always 2. Change to the qty of folders up before root.
PROJECT_ROOT = Path(__file__).resolve().parents[folder_ct]
sys.path.append(str(PROJECT_ROOT))
```
