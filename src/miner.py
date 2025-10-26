from typing import Dict, Set, Tuple, List
from dataclasses import dataclass
from collections import defaultdict
import os
import json
from datetime import datetime
from pathlib import Path
from api.github import ApiGithub
from constants.improved_searches import improved_searches
import time
from github import RateLimitExceededException

import logging

from datetime import datetime

from pathlib import Path

def setup_logging(log_dir: str = "logs"):
    """Setup logging configuration with both file and console output"""
    Path(log_dir).mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = Path(log_dir) / f"projects_discovery_{timestamp}.txt"

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    return log_file

@dataclass
class Repository:
    full_name: str
    html_url: str
    stargazers_count: int
    languages: Set[str]
    found_by_queries: List[str]
    found_by_code_search: bool = False

    def __hash__(self):
        return hash(self.full_name)

    def __eq__(self, other):
        return isinstance(other, Repository) and self.full_name == other.full_name

class CucumberMultiLanguageMiner:
    def __init__(self, github_token: str, log_dir: str = "logs", log_level: int = logging.INFO):
        """
        Usando PyGithub
        """
        # Setup logging
        self.log_file = setup_logging(log_dir=log_dir)
        self.logger = logging.getLogger(self.__class__.__name__)

        try:
            self.github = ApiGithub(github_token=github_token).api
            self.user = self.github.get_user()
            self.logger.info(f"Authenticated as: {self.user.login}")
        except Exception as e:
            self.logger.exception("Failed to authenticate with GitHub API")
            raise

        # constantes para busca
        self.implementation_patterns = improved_searches

        # Para tracking de duplicatas
        self.all_repositories: Dict[str, Repository] = {}
        self.query_stats = defaultdict(int)
        self.code_search_stats = defaultdict(int)

        # Mapeamento correto de linguagens para GitHub Code Search
        self.language_mapping = {
            'nodejs': ['javascript', 'typescript'],  # Node.js usa JS/TS
            'java': ['java'],
            'ruby': ['ruby'],
            'go': ['go'],
            'kotlin': ['kotlin'],
            'php': ['php'],
            'scala': ['scala'],
            'cpp': ['cpp', 'c++'],
            'android': ['java', 'kotlin'],  # Android usa Java/Kotlin
            'lua': ['lua'],
            'ocaml': ['ocaml']
        }

        # Queries específicas para busca de código
        self.code_search_patterns = self._get_code_search_patterns()

    def _get_code_search_patterns(self) -> Dict[str, List[Dict]]:
        """
        Define padrões específicos para busca de código com linguagens corretas
        """
        return {
            'nodejs': [
                {'pattern': '"@cucumber/cucumber"', 'languages': ['javascript', 'typescript']},
                {'pattern': '"cucumber-js"', 'languages': ['javascript', 'typescript']},
                {'pattern': 'require @cucumber', 'languages': ['javascript']},
                {'pattern': 'import @cucumber', 'languages': ['javascript', 'typescript']},
                {'pattern': 'cucumberOpts', 'languages': ['javascript', 'typescript']},
                {'pattern': 'filename:cucumber.config.js', 'languages': ['javascript']},
                {'pattern': 'filename:package.json "@cucumber"', 'languages': ['json']}
            ],
            'java': [
                {'pattern': 'import io.cucumber', 'languages': ['java']},
                {'pattern': '@CucumberOptions', 'languages': ['java']},
                {'pattern': 'RunWith Cucumber', 'languages': ['java']},
                {'pattern': 'cucumber-junit', 'languages': ['java']},
                {'pattern': 'CucumberFeature', 'languages': ['java']},
                {'pattern': 'filename:pom.xml cucumber', 'languages': ['xml']},
                {'pattern': 'filename:build.gradle cucumber', 'languages': ['gradle']}
            ],
            'ruby': [
                {'pattern': 'require cucumber', 'languages': ['ruby']},
                {'pattern': 'Cucumber::', 'languages': ['ruby']},
                {'pattern': 'cucumber-rails', 'languages': ['ruby']},
                {'pattern': 'World cucumber', 'languages': ['ruby']},
                {'pattern': 'filename:Gemfile cucumber', 'languages': ['ruby']}
            ],
            'go': [
                {'pattern': 'import godog', 'languages': ['go']},
                {'pattern': 'godog.Suite', 'languages': ['go']},
                {'pattern': '"github.com/cucumber/godog"', 'languages': ['go']},
                {'pattern': 'filename:go.mod godog', 'languages': ['go-mod']}
            ],
            'kotlin': [
                {'pattern': 'import io.cucumber', 'languages': ['kotlin']},
                {'pattern': '@CucumberOptions', 'languages': ['kotlin']},
                {'pattern': 'cucumber-java', 'languages': ['kotlin']}
            ],
            'scala': [
                {'pattern': 'import cucumber', 'languages': ['scala']},
                {'pattern': 'cucumber-scala', 'languages': ['scala']},
                {'pattern': 'filename:build.sbt cucumber', 'languages': ['scala']}
            ],
            'cpp': [
                {'pattern': 'cucumber-cpp', 'languages': ['cpp', 'c++']},
                {'pattern': '#include.*cucumber', 'languages': ['cpp', 'c++']},
                {'pattern': 'filename:CMakeLists.txt cucumber', 'languages': ['cmake']}
            ],
            'lua': [
                {'pattern': 'cucumber-lua', 'languages': ['lua']},
                {'pattern': 'require.*cucumber', 'languages': ['lua']}
            ],
            'ocaml': [
                {'pattern': 'cucumber.ml', 'languages': ['ocaml']},
                {'pattern': 'open Cucumber', 'languages': ['ocaml']}
            ]
        }

    def wait_for_rate_limit(self) -> None:
        """
        Aguarda se o limite de taxa for excedido
        """
        try:
            limits = self.github.get_rate_limit()

            # verifica o tempo limite para busca
            if limits.search.remaining == 0:
                reset_timestamp = limits.search.reset.timestamp()
                sleep_time = reset_timestamp - datetime.now().timestamp()

                if sleep_time > 0:
                    self.logger.warning(f"Rate limit exceeded. Waiting for {sleep_time:.2f} seconds...")
                    time.sleep(sleep_time + 1)
        except Exception:
            self.logger.exception("Error while checking rate limit")
            # Se não conseguir checar limites, aguardar um tempo conservador
            time.sleep(10)

    def collect_repositories(self) -> Dict[str, Set[Tuple[str, str, int]]]:
        """
        Coleta repositórios usando busca de repositórios + busca de código
        """
        self.logger.info("🔍 Phase 1: Repository Search")
        self._collect_from_repository_search()

        #print("\n🔍 Phase 2: Code Search")
        #self._collect_from_code_search()

        # Converte para o formato original
        results = {}
        for lang in self.implementation_patterns.keys():
            lang_repos = set()
            for repo in self.all_repositories.values():
                if lang in repo.languages:
                    lang_repos.add((repo.full_name, repo.html_url, repo.stargazers_count))
            results[lang] = lang_repos
            self.logger.info(f"Final count for {lang}: {len(lang_repos)} unique repositories")

        return results

    def _collect_from_repository_search(self):
        """
        Busca usando a API de repositórios (método original)
        """
        for lang, config in self.implementation_patterns.items():
            self.logger.info(f"Collecting repositories for: {lang}")

            for query in config['search_queries']:
                try:
                    self.wait_for_rate_limit()
                    search_result = self.github.search_repositories(
                        query=query, sort='stars', order='desc')

                    repos_found_this_query = 0
                    for repo in search_result:
                        repos_found_this_query += 1
                        self._process_repository(repo, lang, f"repo:{query}")

                    self.query_stats[f"{lang}:{query}"] = repos_found_this_query
                    self.logger.info(f"  Repo Query '{query}': {repos_found_this_query} repos")

                except RateLimitExceededException:
                    self.logger.warning(f"Rate limit hit while searching {lang}. Waiting...")
                    self.wait_for_rate_limit()
                except Exception:
                    self.logger.exception(f"Error with repo query '{query}'")
                    continue

    def _collect_from_code_search(self):
        """
        Busca usando a API de código com linguagens corretas
        """
        for lang, patterns in self.code_search_patterns.items():
            self.logger.info(f"Code search for: {lang}")

            for pattern_config in patterns:
                pattern = pattern_config['pattern']
                languages = pattern_config['languages']

                for github_lang in languages:
                    try:
                        self.wait_for_rate_limit()

                        # Constrói a query corretamente
                        if pattern.startswith('filename:'):
                            # Para busca de arquivos específicos
                            query = f'{pattern}'
                        else:
                            # Para busca de código com linguagem
                            query = f'{pattern} language:{github_lang}'

                        self.logger.info(f"  Executing: {query}")

                        code_results = self.github.search_code(
                            query=query,
                            sort='indexed'
                        )

                        repos_found_this_query = 0
                        processed_repos = set()

                        for code_file in code_results:
                            repo = code_file.repository
                            if repo.full_name not in processed_repos:
                                repos_found_this_query += 1
                                processed_repos.add(repo.full_name)
                                self._process_repository_from_code(repo, lang, f"code:{pattern}:{github_lang}", code_file)

                        query_key = f"{lang}:{pattern}:{github_lang}"
                        self.code_search_stats[query_key] = repos_found_this_query
                        self.logger.info(f"    Found {repos_found_this_query} repos")

                        # Pausa mais longa para code search (mais restritivo)
                        time.sleep(2)

                    except RateLimitExceededException:
                        self.logger.warning(f"Rate limit hit during code search for {lang}. Waiting...")
                        self.wait_for_rate_limit()
                    except Exception:
                        self.logger.exception(f"    Error with code query '{query}'")
                        continue

    def _process_repository_from_code(self, repo, language: str, query: str, code_file):
        """
        Processa repositório encontrado via busca de código
        """
        full_name = repo.full_name

        if full_name in self.all_repositories:
            existing_repo = self.all_repositories[full_name]
            existing_repo.languages.add(language)
            existing_repo.found_by_queries.append(f"{language}:{query}")
            existing_repo.found_by_code_search = True
            self.logger.debug(f"Updated existing repo (code) {full_name}: added language {language}")
        else:
            new_repo = Repository(
                full_name=full_name,
                html_url=repo.html_url,
                stargazers_count=repo.stargazers_count,
                languages={language},
                found_by_queries=[f"{language}:{query}"],
                found_by_code_search=True
            )
            self.all_repositories[full_name] = new_repo
            self.logger.debug(f"Added new repo (code) {full_name} for language {language}")

    def _process_repository(self, repo, language: str, query: str):
        """
        Processa repositório encontrado via busca de repositórios (método original)
        """
        full_name = repo.full_name

        if full_name in self.all_repositories:
            existing_repo = self.all_repositories[full_name]
            existing_repo.languages.add(language)
            existing_repo.found_by_queries.append(f"{language}:{query}")
            self.logger.debug(f"Updated existing repo {full_name}: added language {language}")
        else:
            new_repo = Repository(
                full_name=full_name,
                html_url=repo.html_url,
                stargazers_count=repo.stargazers_count,
                languages={language},
                found_by_queries=[f"{language}:{query}"],
                found_by_code_search=False
            )
            self.all_repositories[full_name] = new_repo
            self.logger.debug(f"Added new repo {full_name} for language {language}")

    def get_duplicate_analysis(self) -> Dict:
        """
        Análise expandida incluindo estatísticas de busca por código
        """
        multi_language_repos = []
        multi_query_repos = []
        code_search_only_repos = []

        for repo in self.all_repositories.values():
            if len(repo.languages) > 1:
                multi_language_repos.append(repo)
            if len(repo.found_by_queries) > 1:
                multi_query_repos.append(repo)
            if repo.found_by_code_search and not any('repo:' in query for query in repo.found_by_queries):
                code_search_only_repos.append(repo)

        return {
            'total_unique_repositories': len(self.all_repositories),
            'multi_language_count': len(multi_language_repos),
            'multi_query_count': len(multi_query_repos),
            'code_search_only_count': len(code_search_only_repos),
            'code_search_discoveries': len([r for r in self.all_repositories.values() if r.found_by_code_search]),
            'multi_language_repos': multi_language_repos[:10],
            'code_search_only_repos': code_search_only_repos[:10],
            'query_stats': dict(self.query_stats),
            'code_search_stats': dict(self.code_search_stats),
            'language_distribution': self._get_language_distribution()
        }

    def _get_language_distribution(self) -> Dict[str, int]:
        """
        Conta quantos repos únicos por linguagem
        """
        distribution = defaultdict(int)
        for repo in self.all_repositories.values():
            for lang in repo.languages:
                distribution[lang] += 1
        return dict(distribution)

    def save_results(self, results: Dict[str, Set[Tuple[str, str, int]]], output_file: str = 'data/cucumber_repositories.json'):
        """
        Salvamento com informações expandidas sobre busca por código
        """
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        analysis = self.get_duplicate_analysis()

        output = {
            'timestamp': datetime.utcnow().isoformat(),
            'user': self.user.login,
            'metadata': {
                'total_unique_repositories': len(self.all_repositories),
                'multi_language_count': analysis['multi_language_count'],
                'multi_query_count': analysis['multi_query_count'],
                'code_search_discoveries': analysis['code_search_discoveries'],
                'code_search_only_count': analysis['code_search_only_count'],
                'language_distribution': analysis['language_distribution'],
                'collection_summary': {
                    'total_repo_queries_executed': len(self.query_stats),
                    'total_code_queries_executed': len(self.code_search_stats),
                    'most_effective_repo_queries': sorted(
                        self.query_stats.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:5],
                    'most_effective_code_queries': sorted(
                        self.code_search_stats.items(),
                        key=lambda x: x[1],
                        reverse=True
                    )[:5]
                }
            },
            'repositories': {
                lang: [
                    {
                        'name': name,
                        'url': url,
                        'stars': stars,
                        'found_in_languages': list(self.all_repositories[name].languages) if name in self.all_repositories else [lang],
                        'found_by_queries': len(self.all_repositories[name].found_by_queries) if name in self.all_repositories else 1,
                        'found_by_code_search': self.all_repositories[name].found_by_code_search if name in self.all_repositories else False,
                        'discovery_method': 'code_search_only' if (name in self.all_repositories and
                                                                 self.all_repositories[name].found_by_code_search and
                                                                 not any('repo:' in q for q in self.all_repositories[name].found_by_queries)) else 'repository_search'
                    } for name, url, stars in sorted(repos, key=lambda x: x[2], reverse=True)
                ] for lang, repos in results.items()
            }
        }

        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(output, f, indent=2, ensure_ascii=False)
            self.logger.info(f"✅ Results saved to {output_file}")
        except Exception:
            self.logger.exception(f"Failed to write results to {output_file}")
            raise

        self.print_collection_summary()

    def print_collection_summary(self):
        """
        Resumo expandido com estatísticas de busca por código
        """
        analysis = self.get_duplicate_analysis()

        self.logger.info("="*70)
        self.logger.info("CUCUMBER REPOSITORIES COLLECTION SUMMARY (HYBRID SEARCH)")
        self.logger.info("="*70)
        self.logger.info(f"📊 Total unique repositories found: {analysis['total_unique_repositories']}")
        self.logger.info(f"🔄 Repositories found in multiple languages: {analysis['multi_language_count']}")
        self.logger.info(f"🔍 Repositories found by multiple queries: {analysis['multi_query_count']}")
        self.logger.info(f"💻 Repositories discovered via code search: {analysis['code_search_discoveries']}")
        self.logger.info(f"🎯 Repositories found ONLY via code search: {analysis['code_search_only_count']}")

        self.logger.info("📈 Language distribution:")
        for lang, count in sorted(analysis['language_distribution'].items(), key=lambda x: x[1], reverse=True):
            self.logger.info(f"   {lang:>12}: {count:>4} repositories")

        if analysis['code_search_only_repos']:
            self.logger.info("💎 Top repositories found ONLY via code search:")
            for i, repo in enumerate(analysis['code_search_only_repos'][:5], 1):
                langs = ', '.join(sorted(repo.languages))
                self.logger.info(f"   {i}. {repo.full_name} ({repo.stargazers_count:,} ⭐) - [{langs}]")

        self.logger.info("🎯 Most effective repository queries:")
        top_repo_queries = sorted(analysis['query_stats'].items(), key=lambda x: x[1], reverse=True)[:3]
        for i, (query, count) in enumerate(top_repo_queries, 1):
            if ':' in query:
                lang, q = query.split(':', 1)
                self.logger.info(f"   {i}. {lang}: '{q}' → {count} repos")

        self.logger.info("💻 Most effective code queries:")
        top_code_queries = sorted(analysis['code_search_stats'].items(), key=lambda x: x[1], reverse=True)[:3]
        for i, (query, count) in enumerate(top_code_queries, 1):
            if ':' in query:
                parts = query.split(':', 2)
                if len(parts) >= 2:
                    lang = parts[0]
                    pattern = parts[1] if len(parts) == 2 else f"{parts[1]}:{parts[2]}"
                    self.logger.info(f"   {i}. {lang}: '{pattern}' → {count} repos")

        # Estatísticas de efetividade
        total_repo_results = sum(analysis['query_stats'].values())
        total_code_results = sum(analysis['code_search_stats'].values())
        total_before_dedup = total_repo_results + total_code_results
        total_after_dedup = analysis['total_unique_repositories']
        dedup_saved = total_before_dedup - total_after_dedup

        if dedup_saved > 0:
            self.logger.info("✨ Hybrid search effectiveness:")
            self.logger.info(f"   Repository search results: {total_repo_results:,}")
            self.logger.info(f"   Code search results: {total_code_results:,}")
            self.logger.info(f"   Total before dedup: {total_before_dedup:,}")
            self.logger.info(f"   Unique repositories: {total_after_dedup:,}")
            self.logger.info(f"   Duplicates removed: {dedup_saved:,} ({dedup_saved/total_before_dedup*100:.1f}% reduction)")
            self.logger.info(f"   Code search bonus: {analysis['code_search_only_count']} exclusive discoveries")