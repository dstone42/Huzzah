# Set Up

## Installing Postgresql locally
In order to build the local Postgresql database you will need to get your computer set up. There are few ways to install this locally. 

### Apple

#### Installing Homebrew
The first step is installing a package manager to your terminal. The go to for Mac is [Homebrew](https://brew.sh/). You install Homebrew by typing the following command into your terminal (or copy paste to make sure you don't mess it up).

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

This will download and install the manager. Homebrew is extremely useful for installing any number of free and open source tools, many of which are extremely well made. 


### Installing Conda
We installed Anaconda last semester. You can download it from the website, but you can also install it through Hombrew. 

```zsh
brew install --cask anaconda
```
This installs all the terminal commands, as well as the .app file. 

### Setting up a Conda Environement
Python works best is small development environments. Conda can help you with this. To create a new environment:

```zsh
cconda create -n mimic python=3.13.9 
```

This would create an environment called "mimic" which contains python version 3.13.9. You can then activate the conda environment with:

```zsh
conda activate mimic
```

You can deactivate the environment with:

```zsh
conda deactivate mimic
```
### Required Packages

Assuming you're using conda, install the following packages:

[sqlalchemy](https://pypi.org/project/SQLAlchemy/) — Python wrapper for SQL interactions
[pandas](https://pypi.org/project/pandas/) — Our favorite data manipulator
[matplotlib](https://pypi.org/project/matplotlib/) — For nice plots
[seaborn](https://pypi.org/project/seaborn/) — For nicer plots
[psycopg2](https://pypi.org/project/psycopg2/) — Required by SQL alchemy to access Postgresql databases
[jupyter](https://pypi.org/project/jupyter/) — For easy testing and writing of scripts


To install these run the following:

```zsh
conda activate mimic #This makes sure you're installing into the right environment
conda install pandas sqlachemy matplotlib seaborn jupyter
conda install -c conda-forge psycopg2
```

### Installing Postgresql@17
I've installed an am running postgresql@17. It's probably best if we all use the same version if possible, though different computers may have different CPU architecture which may or may not be supported with version 17. 

Install with the folllowing command.

```zsh
brew install postgresql@17
```

Once that is installed, you want to make sure the database service is running:

```zsh
brew services start postgresql@17
```

You will likely need to add this particular version of postgresql to your ```PATH```. If you don't know what that means, it's okay. If you are on a newer Apple computer you can run the following in your terminal:

```zsh
echo 'export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"' >> ~/.zshrc
```

This will write the line ```echo PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"``` to the file ```.zsh```. Your terminal will now find this version of postgresql making the following commands function. By default brew doesn't automatically add postgresql@17 to the ```PATH```. It gets a bit more technical, but this will work. 

### Downloading and installing MIMIC-IV locally

Now that you have brew installed, conda installed, your mimic environment ready, postgresql@17 installed and added to your path, you are ready for the long part.

This information is from the [MIT-LCP](https://github.com/MIT-LCP/mimic-code/tree/main/mimic-iv/buildmimic/postgres) GitHub repository, which is a currated resource of was to deal with the MIMIC series of datasets, including the Google online repo that we've been discussing. 


If you run the following code (assuming you have MIMIC-IV access) it will download the data, create a new postgresql db, create the tables/schema, and then add all the information. It then links all the tables together (remember foreign keys and 1:many relationships?), and then indexes the whole thing.

```<USERNAME>``` is your username for physionet. For example if my username was "stein" I would put the following into my terminal.

```zsh
wget -r -N -c -np --user stein --ask-password https://physionet.org/files/mimiciv/3.1/
```

It will ask for you password after this line. It's your password for physionet.

```zsh
# clone repo
git clone https://github.com/MIT-LCP/mimic-code.git
cd mimic-code
# download data
wget -r -N -c -np --user <USERNAME> --ask-password https://physionet.org/files/mimiciv/3.1/
mv physionet.org/files/mimiciv mimiciv && rmdir physionet.org/files && rm physionet.org/robots.txt && rmdir physionet.org
createdb mimiciv
psql -d mimiciv -f mimic-iv/buildmimic/postgres/create.sql
psql -d mimiciv -v ON_ERROR_STOP=1 -v mimic_data_dir=mimiciv/3.1 -f mimic-iv/buildmimic/postgres/load_gz.sql
psql -d mimiciv -v ON_ERROR_STOP=1 -v mimic_data_dir=mimiciv/3.1 -f mimic-iv/buildmimic/postgres/constraint.sql
psql -d mimiciv -v ON_ERROR_STOP=1 -v mimic_data_dir=mimiciv/3.1 -f mimic-iv/buildmimic/postgres/index.sql
```






