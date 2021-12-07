import sys

sys.path.append("/Users/mikhaillebedev/study/hse-ml-practices/")

import click
import src


@click.group()
def cli():
    pass


@cli.command()
@click.argument("path_to_train", type=click.Path())
@click.argument("path_to_test", type=click.Path())
@click.argument("path_to_outdir", type=click.Path())
def preprocess(path_to_train, path_to_test, path_to_outdir):
    src.preprocess(path_to_train, path_to_test, path_to_outdir)


@cli.command()
@click.argument("path_to_dir", type=click.Path())
@click.argument("path_to_out", type=click.Path())
def get_prediction(path_to_dir, path_to_out):
    src.get_prediction(path_to_dir, path_to_out)


if __name__ == "__main__":
    cli()
