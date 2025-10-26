# Projects Discovery — GitHub Miner

Ferramenta em Python para **descoberta e mineração de repositórios GitHub** que utilizam **Cucumber / BDD**, com suporte a filtragem por linguagens específicas e exportação de datasets customizados.

---

## 🚀 Instalação

Clone este repositório e crie um ambiente virtual:

```bash
python3 -m venv venv
source venv/bin/activate
````

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuração

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Abra o arquivo `.env` e **adicione seu token do GitHub**:

```env
GITHUB_TOKEN=seu_token_aqui
```

> 💡 Você pode gerar um token pessoal em
> [https://github.com/settings/tokens](https://github.com/settings/tokens)

---

## 🧩 Execução da Coleta

Para iniciar a coleta de repositórios:

```bash
make
```

O processo realiza a busca, coleta os metadados e salva o resultado em `./data/cucumber_repositories.json`.

---

## 🔍 Filtragem de Datasets

Após a coleta, é possível **filtrar os resultados** por linguagens específicas:

```bash
make filter
```

Por exemplo, para manter apenas projetos em **Ruby, Java e Nodejs**, ajuste o filtro no script principal antes de rodar.