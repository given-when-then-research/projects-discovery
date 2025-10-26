import os
import sys
from datetime import datetime
from config import env
from miner import CucumberMultiLanguageMiner

def main():
    # Valor padrão
    output_path = "./data/cucumber_repositories.json"

    # Lê argumento --out (com nome e diretório)
    if "--out" in sys.argv:
        idx = sys.argv.index("--out")
        if len(sys.argv) > idx + 1:
            output_path = sys.argv[idx + 1]

    # Separa diretório e nome base
    output_dir = os.path.dirname(output_path)
    base_name = os.path.splitext(os.path.basename(output_path))[0]

    os.makedirs(output_dir, exist_ok=True)

    # Cria timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    final_file = os.path.join(output_dir, f"{base_name}_{timestamp}.json")

    # Executa coleta
    miner = CucumberMultiLanguageMiner(github_token=env.GITHUB_TOKEN)
    results = miner.collect_repositories()
    miner.save_results(results=results, output_file=final_file)

    print("\n🎉 Collection completed successfully!")
    print(f"📁 File saved to: {final_file}")

if __name__ == "__main__":
    main()