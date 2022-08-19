S3_BUCKET = aws-sam-template-stack
STACK_NAME = lions-meetup

deploy-service-stack:
	sam package --template-file sam-template.yaml --output-template-file packaged.yaml --s3-bucket $(S3_BUCKET)
	sam deploy --template-file packaged.yaml --stack-name $(STACK_NAME) --capabilities CAPABILITY_AUTO_EXPAND CAPABILITY_NAMED_IAM --no-fail-on-empty-changeset

delete-service-stack:
	echo 'y\ny' | sam delete --stack-name $(STACK_NAME)