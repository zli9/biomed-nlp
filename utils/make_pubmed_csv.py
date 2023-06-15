import os
from collections import namedtuple
from typing import List

import click
import pandas as pd
from tqdm import tqdm


@click.group()
def cli():
    """Functions to generate dataset"""


@cli.command()
@click.argument("input-dir")
@click.argument("output-dir")
def convert_to_csv(input_dir:str, output_dir:str):
    """Convert train/dev/test documents to CSV file

    Args:

        input_dir (str): Path to folder with train/dev/test files
        output_dir (str): Path where the output files should be
    """

    dfs = []
    for file in os.listdir(input_dir):
        input_path = os.path.join(input_dir, file)
        output_path = os.path.join(output_dir, file.replace("txt", "csv"))
        print(f"Convert {input_path} to {output_path}.")

        instances = []
        with open(input_path, "r") as f:
            for line in tqdm(f.readlines(), desc="Process document"):
                if line.startswith("###") or len(line.strip()) == 0:
                    next
                else:
                    label, text = line.split("\t")
                    instances.append({
                        "sentence": text,
                        "label": label
                    })
        tmp_df = pd.DataFrame(instances)
        tmp_df.to_csv(output_path, index=False)
        dfs.append(tmp_df)

    pd.concat(dfs).to_csv(os.path.join(output_dir, "whole.csv"), index=False)


if __name__ == "__main__":
    cli()
