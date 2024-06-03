## AWS Step Functions online purchase transaction

1. Edit ```profile.tf``` to add your AWS access and secret keys
2. Run:
```bash
$ terraform init
$ terraform apply -auto-approve
```

Example execution input:
```json
{
  "Username": "user1",
  "Password": "password1",
  "product": "Red Shoes"
}
```

Transaction state machine:
<img width="598" alt="Screen Shot 2024-06-03 at 5 50 14 PM" src="https://github.com/Alan-S-Andrade/Saga-pattern-applications/assets/46075052/3b9ea7ba-179c-4e1b-b4e5-d55bba04d154">

