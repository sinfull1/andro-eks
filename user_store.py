import pulumi
import pulumi_aws as aws
import json


ACL = "private"

BUCKET_POLICY = json.load(open("gdpr-s3-bucket-policy.json", "r"))
ZONE_ID = "ap-south-1b"


def exists(name):
    if name[0] is not None:
        print(name[0])
        return True
    else:
        return False


def create_user_and_bucket(name, tags):
    # Create an IAM group for admin users
#    admin_group = aws.iam.get_group(name + "-group")
    admin_group = aws.iam.Group(name + "-group")
    admin_user = aws.iam.User(name + "-user", name=name + "-user", tags=tags)
    aws.iam.UserGroupMembership(name + "-membership",
                                   user=admin_user.name,
                                   groups=[
                                       admin_group.name,
                                   ])
# Output the admin access key

    bucket_name = name + "-balti"

    bucket = aws.s3.Bucket(
        bucket_name,
        bucket=bucket_name,
        acl=ACL,
        tags=tags,
        lifecycle_rules=[
            aws.s3.BucketLifecycleRuleArgs(
                enabled=True,
                expiration=aws.s3.BucketLifecycleRuleExpirationArgs(
                    days=90,
                ),
                id="logs",
                prefix=bucket_name + "/",
                tags={
                    "autoclean": "true",
                    "rule": "log",
                },
                transitions=[
                    aws.s3.BucketLifecycleRuleTransitionArgs(
                        days=30,
                        storage_class="STANDARD_IA",
                    ),
                    aws.s3.BucketLifecycleRuleTransitionArgs(
                        days=60,
                        storage_class="GLACIER",
                    ),
                ],
            ),
        ],
        cors_rules=[aws.s3.BucketCorsRuleArgs(
            allowed_headers=["*"],
            allowed_methods=["POST", "PUT", "GET"],
            allowed_origins=["*"],
            expose_headers=["ETag"],
            max_age_seconds=3000,
        )],
        # Set force_destroy to true to allow deleting the bucket with objects in it
        force_destroy=True,
        hosted_zone_id=ZONE_ID,
        # Configure lifecycle rules for the bucket to expire objects after a certain time
    )

    gdpr_policy_json = populate(BUCKET_POLICY, bucket_name)

    example_bucket_public_access_block = aws.s3.BucketPublicAccessBlock("public-access-block",
                                                                        bucket=bucket.id,
                                                                        block_public_acls=True,
                                                                        block_public_policy=True,
                                                                        ignore_public_acls=True,
                                                                        restrict_public_buckets=True)

    bucketPolicy = aws.s3.BucketPolicy("gdpr-policy",
                                       bucket=bucket.id,
                                       policy=gdpr_policy_json)

    pulumi.export("bucket_name", bucket.id)


def populate(BUCKET_POLICY, bucket_name):
    for i in BUCKET_POLICY["Statement"]:
        i["Resource"] = "arn:aws:s3:::" + bucket_name + "/*"
    for i in BUCKET_POLICY["Statement"]:
        if isinstance(i["Principal"], dict):
            if i["Principal"]["AWS"] is not None:
                i["Principal"]["AWS"] = ["arn:aws:iam::395283154402:user/log-user"]
    return BUCKET_POLICY
