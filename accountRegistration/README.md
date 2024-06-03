## AWS Step Functions account registration pattern

1. Edit ```profile.tf``` to add your AWS access and secret keys
2. Run:
```bash
$ terraform init
$ terraform apply -auto-approve
```
3. Add an Amazon SES verified email to the execution input. Follow these steps:
https://docs.aws.amazon.com/ses/latest/dg/creating-identities.html

Example execution input:
```json
{
  "userId": "alansa2",
  "email": "alansa2@example.com",
  "profileData": {
    "firstName": "Alan",
    "lastName": "Andrade",
    "address": "1105 W Main St, Urbana, IL"
  },
  "initialConfigurations": {
    "notifications": "off",
    "billing": "basic"
  }
}
```

Transaction state machine:

<img width="620" alt="Screen Shot 2024-06-03 at 10 34 26 AM" src="https://github.com/Alan-S-Andrade/Saga-pattern-applications/assets/46075052/fe02a67a-81cd-4777-8694-42065b383185">
