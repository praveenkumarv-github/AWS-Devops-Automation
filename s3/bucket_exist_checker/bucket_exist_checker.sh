DB_AWS_ZONE=('')

for VARIABLE in "${DB_AWS_ZONE[@]}"

do
	BUCKET_EXISTS=$(aws s3api head-bucket --bucket $VARIABLE 2>&1 || true)
	if [ -z "$BUCKET_EXISTS" ]; then
	echo "Bucket exists"
	else
	echo "$VARIABLE	Bucket does not exist"
	fi

done