## AWS Step Functions travel reservation transaction

1. Edit ```profile.tf``` to add your AWS access and secret keys
2. Run:
```bash
$ terraform init
$ terraform apply -auto-approve
```

Example execution input:
```json
{
  "Airline": "United",
  "FlightDate": "05/14/2024",
  "Model": "Red_Honda",
  "HotelChain": "Hilton",
  "CheckInDate": "05/14/2024",
  "ReturnBy": "05/14/2024"
}
```

Transaction state machine:
![stepfunctions_graph](https://github.com/Alan-S-Andrade/travelReservation/assets/46075052/7d7a8fb8-9b0e-45a1-9da2-fa5172faec32)
