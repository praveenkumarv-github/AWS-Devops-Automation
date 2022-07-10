#!/bin/bash
curl -s localhost:9200/_aliases?pretty=true | awk -F\" '!/aliases/ && $2 != "" {print $2}' > /root/index-backup/indexlst/indexlst_$(date +%F).txt
start=$(date +%s -d '-11 days')
filename=/root/index-backup/indexlst/indexlst_$(date +%F).txt
while read p; do
        creatationdate=$(curl -s -XGET localhost:9200/_cat/indices/$p?h=creation.date.string | cut -d "T" -f 1)
        excludedindex=('filebeat' 'monitoring-kibana' 'monitoring-es' 'kibana')
        for exindex in "${excludedindex[@]}"
        do
            if [[ $p =~ $exindex ]]; then
            echo "index $p : $creatationdate will be deleted "
            curl -s -XDELETE  "localhost:9200/$p"
          #  sleep 10
            fi
        done
        epconvertor=$(date "+%s" -d $creatationdate)
        if [ $epconvertor -lt $start ];
        then
            
                echo "Backingup in process & this index $p will be deleted !!!!!"
		
                /usr/local/bin/elasticdump \
                --s3AccessKeyId "accesss" \
                --s3SecretAccessKey "/secretKey" \
                --input=http://localhost:9200/$p \
                --output "s3://bukcetname/$p.json.gz" \
                --s3Compress \
                --limit 500

           #     sleep 60

                aws s3api head-object --bucket bucketName --key elk/prod-elk/$p.json.gz || not_exist=true
                if [ $not_exist ]; then
                echo "----> Index $p does not exist in s3 bucket <----"
                else
                echo "Index $p exists in s3bucket"
                curl -s -XDELETE  "localhost:9200/$p"
		echo "Index $p deleted"
		echo "              "
                fi
        else
            echo "Index : $p will stay in ES"
            # echo " "
        fi
done < "$filename"
