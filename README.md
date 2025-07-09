# FastAPI Local Setup for Windows

Este guia fornece instruções passo a passo para configurar e executar uma aplicação FastAPI localmente em um computador Windows.

## 📋 Pré-requisitos

- Windows 10 ou superior
- Acesso à internet para downloads
- Privilégios de administrador (para instalação do Python)

## 🚀 Instalação

### 1. Instalar Python

1. Acesse o site oficial: [python.org](https://www.python.org/downloads/)
2. Baixe a versão mais recente do Python (3.7 ou superior)
3. Execute o instalador
4. **IMPORTANTE**: Marque a opção "Add Python to PATH" durante a instalação
5. Verifique a instalação executando no prompt de comando:
   ```bash
   python --version
   ```

### 2. Criar e Ativar Ambiente Virtual

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto:

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
venv\Scripts\activate

# Para desativar (quando necessário)
deactivate
```

### 3. Instalar Dependências

Com o ambiente virtual ativado, instale FastAPI e Uvicorn:

```bash
pip install -r requirements.txt
```

Para desenvolvimento, você também pode instalar dependências opcionais:

```bash
pip install "fastapi[all]"
```

## 📁 Estrutura do Projeto

Crie a seguinte estrutura de pastas:

```
projeto-fastapi/
├── main.py
├── requirements.txt
├── README.md
└── venv/
└── src/
```

## 🏃‍♂️ Executando a Aplicação

### Método 1: Usando Uvicorn (Recomendado)

```bash
uvicorn main:app --reload
```

### Método 2: Executando o arquivo Python diretamente

```bash
python main.py
```

### Opções de Configuração

Você pode personalizar a execução com as seguintes opções:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Parâmetros:**
- `--reload`: Reinicia automaticamente quando há mudanças no código
- `--host 0.0.0.0`: Permite acesso de outros dispositivos na rede local
- `--port 8000`: Define a porta (8000 é padrão)
- `--workers 4`: Define o número de workers (para produção)

## 🌐 Acessando a Aplicação

Após executar a aplicação, você pode acessar:

- **API Principal**: [http://localhost:8000](http://localhost:8000)
- **Documentação Interativa (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Documentação Alternativa (ReDoc)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📦 Gerenciamento de Dependências

### Gerar arquivo requirements.txt

```bash
pip freeze > requirements.txt
```

### Instalar dependências de um requirements.txt

```bash
pip install -r requirements.txt
```

## 🛠️ Comandos Úteis

### Verificar logs em tempo real
A aplicação mostrará logs no terminal, incluindo:
- Requisições HTTP recebidas
- Erros e exceções
- Informações de debug

### Parar a aplicação
Pressione `Ctrl+C` no terminal para parar o servidor.

### Verificar se a porta está em uso
```bash
netstat -ano | findstr :8000
```

## 🔧 Solução de Problemas

### Erro: Python não é reconhecido como comando
- Reinstale o Python marcando "Add Python to PATH"
- Ou adicione manualmente o Python ao PATH do sistema

### Erro: Porta já em uso
- Mude a porta: `uvicorn main:app --port 8001`
- Ou finalize o processo que está usando a porta

### Erro: ModuleNotFoundError
- Certifique-se de que o ambiente virtual está ativado
- Reinstale as dependências: `pip install fastapi uvicorn`

## 📚 Próximos Passos

1. **Adicionar autenticação**: Implemente JWT ou OAuth2
2. **Banco de dados**: Integre com SQLAlchemy e PostgreSQL/MySQL
3. **Testes**: Adicione testes unitários com pytest
4. **Docker**: Containerize a aplicação
5. **Deploy**: Faça deploy em serviços como Heroku, AWS, ou Google Cloud

## 🤝 Contribuindo

1. Faça fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas e suporte:
- Documentação oficial: [FastAPI Docs](https://fastapi.tiangolo.com/)
- GitHub Issues: [Reporte bugs aqui](https://github.com/seu-usuario/seu-projeto/issues)
- Comunidade: [FastAPI Discord](https://discord.gg/VQjSZaeJmf)

---

**Desenvolvido com ❤️ usando FastAPI**