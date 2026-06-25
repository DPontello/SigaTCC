# SigaTCC — Sistema de Gestão de TCCs

Sistema para gerenciamento de Trabalhos de Conclusão de Curso (TCCs), desenvolvido com **Django REST Framework** no backend e **Vue.js 3** no frontend.

## Tecnologias

| Camada | Tecnologia |
|--------|------------|
| Backend | Python 3.12, Django 6, Django REST Framework |
| Frontend | Vue.js 3, Vue Router, Vite, Chart.js |
| Banco de dados | SQLite |
| Containerização | Docker, Docker Compose |

## Funcionalidades implementadas

- **Dashboard** com gráficos de TCCs por status e por orientador (Chart.js)
- **Listagem e busca** de TCCs com filtros por título, aluno e status
- **Cadastro de TCC** com upload de arquivo PDF
- **Visualização e download** do arquivo PDF na listagem
- **Listagem** de Alunos, Professores, Cursos, Departamentos e Unidades Acadêmicas

---

## Como rodar com Docker (recomendado)

Pré-requisito: [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado e em execução.

```bash
# Sobe o backend (porta 8000) e o frontend (porta 5173)
docker compose up --build
```

Na primeira vez, popule o banco com dados de exemplo:

```bash
docker compose exec backend python load.py
```

Acesse:
- **Frontend:** http://localhost:5173
- **API:** http://localhost:8000/api/

Para parar:

```bash
docker compose down
```

---

## Como rodar sem Docker

### Backend

```bash
# 1. Crie e ative o ambiente virtual
python -m venv venv

# Linux/macOS:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Rode as migrações
python manage.py migrate

# 4. Popule o banco com dados de exemplo
python load.py

# 5. Inicie o servidor
python manage.py runserver
```

API disponível em: http://127.0.0.1:8000/api/

### Frontend

```bash
cd frontend

# 1. Copie o arquivo de variáveis de ambiente
cp .env.example .env
# O arquivo já aponta para http://127.0.0.1:8000/api por padrão

# 2. Instale as dependências
npm install

# 3. Inicie o servidor de desenvolvimento
npm run dev
```

Frontend disponível em: http://localhost:5173

---

## Como popular dados

O script `load.py` na raiz do projeto limpa e repopula o banco com dados fictícios (unidades acadêmicas, departamentos, cursos, professores, alunos e TCCs).

```bash
# Sem Docker:
python load.py

# Com Docker (container em execução):
docker compose exec backend python load.py
```

---

## Endpoints da API

| Recurso | URL |
|---------|-----|
| Unidades Acadêmicas | `GET /api/unidades-academicas/` |
| Departamentos | `GET /api/departamentos/` |
| Cursos | `GET /api/cursos/` |
| Alunos | `GET /api/alunos/` |
| Professores | `GET /api/professores/` |
| TCCs | `GET /api/tccs/` |
| Estatísticas (Dashboard) | `GET /api/tccs/estatisticas/` |

### Status dos TCCs

| Código | Descrição |
|--------|-----------|
| `0` | Em Elaboração |
| `1` | Enviado |
| `2` | Aprovado |
| `3` | Reprovado |

### Upload de arquivo

O campo `arquivo` (PDF) deve ser enviado via `multipart/form-data` no cadastro de TCC.

### Estrutura do endpoint de estatísticas

```json
{
    "total_geral": 10,
    "por_status": {
        "Aprovado": 3,
        "Em Elaboração": 2
    },
    "por_orientador": {
        "Prof. Ana Paula Ribeiro": 4
    }
}
```

---

## Material de apoio

- [Django REST Framework](https://www.django-rest-framework.org/)
- [Vue.js 3](https://vuejs.org/)
- [Vite](https://vite.dev/)
- [Chart.js](https://www.chartjs.org/)
