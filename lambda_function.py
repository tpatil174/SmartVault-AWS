import boto3
import os
from datetime import datetime

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name='eu-central-1')
    sns = boto3.client('sns', region_name='eu-central-1')
    
    volume_id = 'vol-0c0321488b36afb2a'
    sns_topic_arn = 'arn:aws:sns:eu-central-1:363479758460:SmartVault-Alerts'
    
    try:
        snapshot = ec2.create_snapshot(
            VolumeId=volume_id,
            Description=f'SmartVault automated backup - {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
        
        snapshot_id = snapshot['SnapshotId']
        
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject='SmartVault - Snapshot Created Successfully',
            Message=f'Snapshot {snapshot_id} created successfully for volume {volume_id} at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} UTC.'
        )
        
        return {'statusCode': 200, 'body': f'Snapshot {snapshot_id} created successfully.'}
    
    except Exception as e:
        sns.publish(
            TopicArn=sns_topic_arn,
            Subject='SmartVault - Snapshot FAILED',
            Message=f'Snapshot creation FAILED for volume {volume_id}. Error: {str(e)}'
        )
        raise e
