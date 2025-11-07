# Projects Discovery — GitHub Miner

A Python tool for **discovering and mining GitHub repositories** that use **Cucumber / BDD**, with support for language-specific filtering and export of customized datasets.

---

## Installation

Clone this repository and create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

---

## Configuration

Create the `.env` file from the example:

```bash
cp .env.example .env
```

Open the `.env` file and **add your GitHub token**:

```env
GITHUB_TOKEN=your_token_here
```

> You can generate a personal token at
> [https://github.com/settings/tokens](https://github.com/settings/tokens)

---

## Data Collection

To start collecting repositories:

```bash
make
```

The process will search, gather metadata, and save the results in `./data/cucumber_repositories.json`.

---

## Dataset Filtering

After the collection step, you can **filter the gathered repositories** to keep only those written in specific programming languages.

Before running the filter command, remember to **update the dataset filename** generated in the previous step — it includes a timestamp in its name, for example:

```
./data/cucumber_repositories_2025-10-26_19-59-35.json
```

Update your filtering script or configuration to reference this exact filename.

Then, run:

```bash
make filter
```

By default, the filter can be customized to include only certain languages.
For instance, to keep repositories written in **Ruby, Java, and NodeJS**, adjust the language filter in the main script before executing the command.