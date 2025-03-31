# Guia de Uso - Totymark API

## 📋 Índice
1. [Introdução](#introdução)
2. [Endpoints Disponíveis](#endpoints-disponíveis)
3. [Como Usar](#como-usar)
4. [Exemplos Práticos](#exemplos-práticos)
5. [Respostas e Códigos](#respostas-e-códigos)

## 🚀 Introdução
O Totymark é um sistema de mensagens em tempo real que permite a comunicação entre usuários através de uma API REST. Este guia mostrará como usar todos os endpoints disponíveis.

## 🔌 Endpoints Disponíveis

### 1. Página Inicial
- **URL**: `/`
- **Método**: GET
- **Descrição**: Retorna informações básicas sobre a API
- **Autenticação**: Não

### 2. Autenticação
- **URL**: `/token`
- **Método**: POST
- **Descrição**: Gera um token de acesso para o usuário
- **Autenticação**: Não
- **Corpo da Requisição**:
  ```json
  {
    "username": "seu_usuario",
    "password": "sua_senha"
  }
  ```

### 3. Usuários
#### Criar Usuário
- **URL**: `/users`
- **Método**: POST
- **Descrição**: Cria um novo usuário no sistema
- **Autenticação**: Não
- **Corpo da Requisição**:
  ```json
  {
    "username": "novo_usuario",
    "email": "email@exemplo.com",
    "password": "senha123"
  }
  ```

#### Listar Usuários
- **URL**: `/users`
- **Método**: GET
- **Descrição**: Lista todos os usuários cadastrados
- **Autenticação**: Sim (Token JWT)

### 4. Mensagens
#### Enviar Mensagem
- **URL**: `/messages`
- **Método**: POST
- **Descrição**: Envia uma nova mensagem
- **Autenticação**: Sim (Token JWT)
- **Corpo da Requisição**:
  ```json
  {
    "content": "Conteúdo da mensagem",
    "sender_id": "id_do_remetente",
    "type": "text"  // text, pix, notification
  }
  ```

#### Listar Mensagens
- **URL**: `/messages`
- **Método**: GET
- **Descrição**: Lista todas as mensagens
- **Autenticação**: Sim (Token JWT)

### 5. Verificação de Saúde
- **URL**: `/health`
- **Método**: GET
- **Descrição**: Verifica o status da API
- **Autenticação**: Não

## 📝 Como Usar

### 1. Criando um Usuário
```bash
curl -X POST "http://127.0.0.1:8081/users" \
-H "Content-Type: application/json" \
-d '{
    "username": "marcos",
    "email": "mpcambiaghi80@hotmail.com",
    "password": "Mark28803345"
}'
```

### 2. Obtendo um Token de Acesso
```bash
curl -X POST "http://127.0.0.1:8081/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=marcos&password=Mark28803345"
```

### 3. Enviando uma Mensagem
```bash
curl -X POST "http://127.0.0.1:8081/messages" \
-H "Authorization: Bearer seu_token_aqui" \
-H "Content-Type: application/json" \
-d '{
    "content": "Olá, tudo bem?",
    "sender_id": "id_do_remetente",
    "type": "text"
}'
```

### 4. Enviando uma Notificação de PIX
```bash
curl -X POST "http://127.0.0.1:8081/messages" \
-H "Authorization: Bearer seu_token_aqui" \
-H "Content-Type: application/json" \
-d '{
    "content": "PIX recebido: R$ 100,00",
    "sender_id": "id_do_remetente",
    "type": "pix"
}'
```

### 5. Listando Mensagens
```bash
curl -X GET "http://127.0.0.1:8081/messages" \
-H "Authorization: Bearer seu_token_aqui"
```

## 🎯 Exemplos Práticos

### Fluxo Completo de Uso

1. **Criar Usuário**
```bash
curl -X POST "http://127.0.0.1:8081/users" \
-H "Content-Type: application/json" \
-d '{
    "username": "marcos",
    "email": "mpcambiaghi80@hotmail.com",
    "password": "Mark28803345"
}'
```

2. **Fazer Login**
```bash
curl -X POST "http://127.0.0.1:8081/token" \
-H "Content-Type: application/x-www-form-urlencoded" \
-d "username=marcos&password=Mark28803345"
```

3. **Enviar Mensagem**
```bash
curl -X POST "http://127.0.0.1:8081/messages" \
-H "Authorization: Bearer seu_token_aqui" \
-H "Content-Type: application/json" \
-d '{
    "content": "Teste de mensagem!",
    "sender_id": "id_do_remetente",
    "type": "text"
}'
```

4. **Ver Mensagens**
```bash
curl -X GET "http://127.0.0.1:8081/messages" \
-H "Authorization: Bearer seu_token_aqui"
```

## 📊 Respostas e Códigos

### Códigos de Status
- **200**: Sucesso
- **201**: Criado com sucesso
- **400**: Erro de requisição
- **401**: Não autorizado
- **403**: Proibido
- **404**: Não encontrado
- **500**: Erro interno do servidor

### Exemplo de Resposta de Sucesso
```json
{
    "status": "success",
    "data": {
        "id": "123",
        "content": "Mensagem de teste",
        "timestamp": "2024-03-31T12:00:00",
        "type": "text"
    }
}
```

### Exemplo de Resposta de Erro
```json
{
    "status": "error",
    "message": "Usuário não encontrado"
}
```

## 🔒 Segurança
- Todas as senhas são armazenadas com hash
- Autenticação via JWT
- Tokens expiram após 30 minutos
- Endpoints protegidos requerem token válido

## 📱 Interface Web
A documentação interativa da API está disponível em:
- Swagger UI: http://127.0.0.1:8081/docs
- ReDoc: http://127.0.0.1:8081/redoc 