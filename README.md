## O que é o buscaDOE
O buscaDOE é um pequeno projeto, ainda em desenvolvimento, feito em Python para a busca de termos em arquivos PDF.

## Motivo para o desenvolvimento do projeto
Ele foi criado para suprir a necessidade de verificar se certos termos estavam presentes em um Diário Oficial que é publicado em PDF. Caso os termos sejam encontrados é enviada uma mensagem para um chatbot do telegram informando as páginas em que os termos foram encontrados.

## O que está sendo utilizado no projeto
É utilizada a biblioteca tesseract-ocr, versão 4.0, para a conversão de arquivos PDF com imagens em texto.

O uso do tesseract-ocr fez-se necessário pois os arquivos PDF são compostos por imagens.

O tesseract-ocr é uma ferramenta OCR gratuíta e de código-aberto.

O passo-a-passo para instalar o tesseract-ocr no Linux, Windows ou MacOS podem ser verificados na [wiki do projeto](https://tesseract-ocr.github.io/tessdoc/Installation.html)

Outros links do projeto tesseract-ocr:
- [Documentação](https://tesseract-ocr.github.io/tessdoc/)
- [Repositório do projeto](https://github.com/tesseract-ocr/)

Utilizar o Tesseract portuguese language trained data
- Baixar o arquivo: **[por.traineddata](https://github.com/tesseract-ocr/tessdata/blob/main/por.traineddata)** e copiar para a pasta: `/usr/share/tesseract-ocr/4.00/tessdata`.


### Exemplo de instalação em Ubuntu Linux

#### Pacotes necessários
> **OBS:** Necessário python3.8 ou superior
```shell
sudo apt install poppler-utils tesseract-ocr python3-pip git
```

#### Baixando o projeto direto do repositório e instalando as dependências
```shell
# Baixar o projeto
git clone https://gitlab.com/francinaldo/buscadoe.git

# Acessar a pasta do projeto
cd buscadoe

# Instalar as dependencias
pip install -r requirements.txt
```

#### Criar o arquivo .env onde serão armazenadas o TOKEN e o RECEIVER_ID do Telegram
```shell
# Criar o arquivo .env
touch .env
```
O arquivo ficará conforme a estrutura abaixo
```
# Telegram Bot Credentials
TOKEN='TELEGRAM_TOKEN'
RECEIVE_ID=TELEGRAM_RECEIVE_ID
```

#### Como criar uma chatbot no Telegram
- https://canaltech.com.br/apps/como-criar-um-bot-no-telegram-botfather/
- https://www.youtube.com/watch?v=WyJM2ckBgMs&themeRefresh=1


## Exemplo DOEPB
#### Inserir os termos a serem buscados no arquivo `doepb.py` na linha, separados por vírgula:
```
search_terms = ["Term 1", "Term 2", "Term ..."]
```
#### Executar o arquivo `doepb.py`
```shell
python3 doepb.py
```
