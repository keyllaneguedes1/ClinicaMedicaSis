# Clínica Médica - Sistema de Gestão

Sistema web desenvolvido para gerenciar uma clínica médica, permitindo o controle de pacientes, médicos, consultas, pagamentos e geração de logs automáticos no banco de dados.

##  Tecnologias Utilizadas

- **Python 3.10**
- **Flask** (framework web)
- **SQLAlchemy** (ORM)
- **MySQL 8** (banco de dados relacional)
- **Bootstrap 5** (interface responsiva)
- **Jinja2** (templates HTML)
- **HTML5 & CSS3**

##  Funcionalidades

- Cadastro, edição, visualização e exclusão de:
  - Pacientes
  - Médicos
  - Consultas
  - Pagamentos
  - Exames
  - Receitas
- Relacionamento entre tabelas com uso de JOINs
- Geração de logs automáticos com triggers no banco de dados
- Visualização de relatórios e histórico de ações
- Interface responsiva com navegação intuitiva

##  Estrutura do Projeto

```
clinica_medica/
│
├── app/
│   ├── static/              # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/           # Templates HTML com Jinja2
│   ├── models/              # Definição das tabelas e classes com SQLAlchemy
│   ├── routes/              # Arquivos com as rotas (Flask Blueprints)
│   ├── factories/           # Factories para instanciar objetos
│   ├── facades/             # Padrão Facade para lógica de negócio
│   └── __init__.py          # Inicialização do app Flask
│
├── migrations/              # Arquivos de controle de migrações
├── run.py                   # Arquivo principal para rodar o app
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo
```

## 🛠️ Como Rodar o Projeto

### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/clinica_medica.git
cd clinica_medica
```

### 2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# ou
source venv/bin/activate  # Linux/Mac
```

### 3. Instale as dependências:

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados MySQL:

- Crie um banco chamado `clinica_medica`
- Atualize o arquivo de configuração (ex: `Config` no `__init__.py`) com o usuário e senha do seu MySQL

### 5. Execute as migrações:

```bash
flask db init
flask db migrate
flask db upgrade
```

### 6. Rode o servidor Flask:

```bash
python run.py
```

Acesse em: [http://localhost:5000](http://localhost:5000)

## Recursos Avançados

- **Padrões de Projeto**:
  - Factory: criação de objetos (ex: médicos e pacientes)
  - Facade: encapsulamento da lógica de negócio
- **Banco de Dados**:
  - Procedures e Triggers
  - Transactions e Views
  - Relatórios com JOINs e filtros
- **Logs de Ações**:
  - Logs automáticos de inserções em consultas (`AFTER INSERT`)

## Licença

Este projeto foi elaborado com propósito avaliativo para a disciplina de Banco de Dados II.
