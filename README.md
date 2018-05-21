# ID-Recorgnition-System-Demo
(For paper)

Make sure python3 and MySQL is installed, and ethereum is on before running
Current available client: ganache, geth v1.7.3



# python version: 3.5
brew install python3.5 (or python3)


# ethereum: ganache-cli, geth
1. npm install -g ganache-cli
2. geth v1.7.3


# Database: MySQL
On terminal: mysql -u root -p DBO_BLOCKCHAIN < all.sql
Make sure the schema, DBO_BLOCKCHAIN, is established before import


# Mac settings:
1. python3 -m venv venv
2. source venv/bin/activate
3. pip install -r requirements.txt
4. cd ID-Recorgnition-System-Demo
5. python run.py
6. ( url: localhost:5000/ )



# others
1. Some local settings:

§ config.py:
DEBUG = False

§ instance/config.py:
DEBUG = True
SECRET_KEY = 'dlkfg;dkfjhdjkhsjkhkl'


2. You can run the simulation server of Bank and Education, yet make sure there're user datas respectively. There'll be some fake data your set on the index page.

§ python Department/Finance/Bank.py
§ python Department/Education/Education.py




