

mimir_values={
   "mimir": {
       "structuredConfig": {
           "blocks_storage": {
               "backend": "s3",
               "storage_prefix": "blocksstorage",
               "s3": {
                   "bucket_name": "my-loki-logs",
                   "access_key_id": "AKIAVYCFWIXRCYEC6HWL",
                   "secret_access_key":  "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",
                   "endpoint": "s3.ap-south-1.amazonaws.com",
                   "region": "ap-south-1"
               }
           },
           "alertmanager_storage": {
               "backend": "s3",
               "storage_prefix": "alertmanager",
               "s3": {
                   "bucket_name": "my-loki-logs",
                   "access_key_id": "AKIAVYCFWIXRCYEC6HWL",
                   "secret_access_key":  "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",
                   "endpoint": "s3.ap-south-1.amazonaws.com",
                   "region": "ap-south-1"
               }
           },
           "ruler_storage": {
               "backend": "s3",
               "storage_prefix": "rulerstorage",
               "s3": {
                   "bucket_name": "my-loki-logs",
                   "access_key_id": "AKIAVYCFWIXRCYEC6HWL",
                   "secret_access_key":  "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",
                   "endpoint": "s3.ap-south-1.amazonaws.com",
                   "region": "ap-south-1"
               }
           },


       },
   }
}

