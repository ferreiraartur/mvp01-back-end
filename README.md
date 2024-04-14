
# Criar ambiente virtual

python -m venv env

# Ative o ambiente 
# Utilizando o S.O. Linux 

```
$ source <venv>/bin/activate
```

# Utilizando o S.O. Windows
```
usando o cmd.exe C:\> <venv>\Scripts\activate.bat
usando o PS C:\> <venv>\Scripts\Activate.ps1
```

# Segue o link da documentação caso tenha algum problema 
# https://docs.python.org/3/library/venv.html
# https://virtualenv.pypa.io/en/latest/installation.html


# Instale as bibliotecas
```
(env)$ pip install -r requirements.txt
```

# Sobe o serviço
```
(env)$ flask run --host 0.0.0.0 --port 5000
```


