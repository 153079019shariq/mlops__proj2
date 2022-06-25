#!/usr/bin/env python
import pandas as pd
import argparse
import logging
import wandb


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)
    
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)
    

    ######################
    # YOUR CODE HERE     #
    ######################
    # Drop outliers
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()
    # Convert last_review to datetime
    df['last_review'] = pd.to_datetime(df['last_review'])
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
      args.output_artifact,
      type=args.output_type,
      description=args.output_description,
      )
    artifact.add_file(args.output_artifact)
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Input file name", 
        required=True
    )


    parser.add_argument(
        "--output_artifact", 
        type=str, 
        help="Output file name",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="clean_sample",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="Data with outliers and null values removed ",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=int, 
        help="Minimum threshold below which it is  considered as outlier",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type= int, 
        help="Maximum threshold above which it is considered as outlier",
        required=True
    )


    args = parser.parse_args()

    go(args)
