root@ELK-PROD:~# crontab -l


#crontab for elk Index-backup -> s3 s3://bucketname/elk/prod-elk/ @1:50 AM daily
30 13 * * * /root/index-backup/backup.sh >> /root/index-backup/log/backup.log 2>&1
