# -*- coding: utf-8 -*-

"""
Webotron: Deploy websites with aws.

Webotron automates the process of deploying static web pages into AWS
- Configure AWS S3 buckets
    - Create them
    - Set them up for static website hosting
    - Synching the contest of a local directory with S3 bucket
- Configure DNS with AWS Route 53
"""

import boto3
import click

from bucket import BucketManager

session = boto3.Session()
bucket_manager = BucketManager(session)


@click.group()
def cli():
    """Webtron deploys websites to AWS."""
    pass


@cli.command('list-buckets')
def list_buckets():
    """List all s3 buckets."""
    for bucket in bucket_manager.all_buckets():
        print(bucket)


@cli.command('list-bucket-objects')
@click.argument('bucket')
def list_bucket_objects(bucket):
    """List objects in s3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)


@cli.command('setup-bucket')
@click.argument('bucket')
def setup_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_policy(s3_bucket)
    bucket_manager.configure_website(s3_bucket)

    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname, bucket):
    """Sync contest of PATHNAME to BUCKET."""
    s3_bucket = bucket_manager.s3.Bucket(bucket)
    bucket_manager.sync(pathname, bucket)


if __name__ == '__main__':
    cli()
