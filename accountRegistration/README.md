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

![stepfunctions_graph](https://github.com/Alan-S-Andrade/travelReservation/assets/46075052/7d7a8fb8-9b0e-45a1-9da2-fa5172faec32)
