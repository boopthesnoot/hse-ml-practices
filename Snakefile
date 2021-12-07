import os
from pathlib import Path

cwd = os.getcwd()

rule all:
    input:
        Path("reports/figures/surv_dist.png"),
        Path("reports/figures/pclass_dist.png"),
        Path("data/results/submissions.csv")

rule preprocess_data:
    input:
        Path("data/raw/train.csv"),
        Path("data/raw/test.csv"),
        directory(Path("data/processed"))
    output:
        # Path("data/processed"),
        Path("reports/figures/pclass_dist.png"),
        Path("reports/figures/surv_dist.png")
    params:
        cli=os.path.join(cwd, Path("workflow/cli.py")),
    shell:
        "echo {params.cli} & echo {input} & python {params.cli} preprocess {input}"


rule predict:
    input:
        directory(Path("data/processed"))
    output:
        Path("data/results/submissions.csv")
    params:
        cli=os.path.join(cwd, Path("workflow/cli.py")),
    shell:
        "echo {output} & python {params.cli} get-prediction {input} {output}"
