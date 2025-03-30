# Totymark

Sistema de mensagens em tempo real usando Flutter Web e FastAPI.

## Requisitos

- Python 3.8+
- MongoDB
- Flutter SDK
- Node.js (para desenvolvimento)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/totymark.git
cd totymark
```

2. Instale as dependências do Python:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
- Copie o arquivo `.env.example` para `.env`
- Ajuste as variáveis conforme necessário

4. Inicie o MongoDB:
```bash
sudo service mongodb start
```

5. Inicie o servidor backend:
```bash
python main.py
```

O servidor estará rodando em `http://localhost:8000`

## Documentação da API

A documentação da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Estrutura do Projeto

```
totymark/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── (arquivos Flutter)
├── .env
└── README.md
```

## Contribuindo

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request 