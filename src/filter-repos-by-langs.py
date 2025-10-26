import json
import argparse
from typing import List, Dict, Any

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Carrega o arquivo JSON."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json_file(data: Dict[str, Any], filepath: str) -> None:
    """Salva os dados em um arquivo JSON."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def filter_by_languages(data: Dict[str, Any], languages: List[str]) -> Dict[str, Any]:
    """
    Filtra o dataset mantendo apenas as linguagens especificadas.
    
    Args:
        data: Dicionário com os dados do dataset
        languages: Lista de linguagens para manter (ex: ['nodejs', 'java', 'python'])
    
    Returns:
        Dataset filtrado
    """
    filtered_data = data.copy()
    
    # Filtra os repositórios
    if 'repositories' in filtered_data:
        original_repos = filtered_data['repositories']
        filtered_repos = {
            lang: repos for lang, repos in original_repos.items() 
            if lang in languages
        }
        filtered_data['repositories'] = filtered_repos
    
    # Reconstrói metadata apenas com os campos necessários
    if 'metadata' in filtered_data:
        new_metadata = {}
        
        # Calcula total de repositórios únicos
        if 'repositories' in filtered_data:
            total_repos = sum(len(repos) for repos in filtered_data['repositories'].values())
            new_metadata['total_unique_repositories'] = total_repos
        elif 'total_unique_repositories' in filtered_data['metadata']:
            new_metadata['total_unique_repositories'] = filtered_data['metadata']['total_unique_repositories']
        
        # Filtra a distribuição de linguagens
        if 'language_distribution' in filtered_data['metadata']:
            original_distribution = filtered_data['metadata']['language_distribution']
            filtered_distribution = {
                lang: count for lang, count in original_distribution.items() 
                if lang in languages
            }
            new_metadata['language_distribution'] = filtered_distribution
        
        # Substitui metadata pelo novo (apenas com os 2 campos)
        filtered_data['metadata'] = new_metadata
    
    return filtered_data

def main():
    parser = argparse.ArgumentParser(
        description='Filtra dataset JSON por linguagens específicas',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  # Filtrar apenas nodejs e java
  python filter_dataset.py input.json -l nodejs java -o filtered_output.json
  
  # Filtrar apenas python e go
  python filter_dataset.py input.json --languages python go --output filtered_output.json
  
  # Filtrar múltiplas linguagens
  python filter_dataset.py input.json -l nodejs java ruby
        """
    )
    
    parser.add_argument(
        'input_file',
        help='Caminho do arquivo JSON de entrada'
    )
    
    parser.add_argument(
        '-l', '--languages',
        nargs='+',
        required=True,
        help='Lista de linguagens para manter (ex: nodejs java python)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='filtered_dataset.json',
        help='Caminho do arquivo JSON de saída (padrão: filtered_dataset.json)'
    )
    
    parser.add_argument(
        '--show-available',
        action='store_true',
        help='Mostra as linguagens disponíveis no dataset'
    )
    
    args = parser.parse_args()
    
    # Carrega o dataset
    print(f"📂 Carregando dataset de: {args.input_file}")
    data = load_json_file(args.input_file)
    
    # Mostra linguagens disponíveis se solicitado
    if args.show_available:
        if 'metadata' in data and 'language_distribution' in data['metadata']:
            available_langs = list(data['metadata']['language_distribution'].keys())
            print(f"\n🔍 Linguagens disponíveis no dataset:")
            for lang in available_langs:
                count = data['metadata']['language_distribution'][lang]
                print(f"  - {lang}: {count} repositórios")
        return
    
    # Filtra os dados
    print(f"🔧 Filtrando por linguagens: {', '.join(args.languages)}")
    filtered_data = filter_by_languages(data, args.languages)
    
    # Salva o resultado
    save_json_file(filtered_data, args.output)
    print(f"✅ Dataset filtrado salvo em: {args.output}")
    
    # Mostra estatísticas
    if 'metadata' in filtered_data:
        print(f"\n📊 Estatísticas do dataset filtrado:")
        if 'total_unique_repositories' in filtered_data['metadata']:
            print(f"  - Total de repositórios: {filtered_data['metadata']['total_unique_repositories']}")
        if 'language_distribution' in filtered_data['metadata']:
            print(f"  - Distribuição por linguagem:")
            for lang, count in filtered_data['metadata']['language_distribution'].items():
                print(f"    • {lang}: {count}")

if __name__ == '__main__':
    main()