# Update Bid

This is the update bid service for my FYP. It is written in Python. It is responsible for updating the UI when the bid changes in the auction.

## Project Setup

Requires Firebase integration.

## License

None

## Setting up UpdateBid service on AWS

- Created AWS EC2 Linux instance
- Connected to instance using FileZilla using Public DNS and .pem keyfile
- Uploaded application directory to server
- Connected to server instance using PuTTy using ec2-user@PublicDNS and .ppk keyfile for SSH Auth

## Application Setup Required
- Installed gcc -> sudo yum install gcc-c++
- Installed python-dev -> sudo yum install python-devel
- Installed zmq binding - sudo easy_install pyzmq
- Installed firebase - sudo easy_install requests==1.1.0
		                 - sudo easy_install python-firebase
- Installed config parser -> sudo easy_install configparser
- Installed enum -> sudo easy_install enum

- Running the service -> sudo python /home/ec2-user/UpdateBid/main.py

- Service runs and works as expected
