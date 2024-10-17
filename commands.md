# Setup
sudo apt update -y
sudo apt install python3-pip -y
sudo apt install git -y
ssh-keygen -C githubKey

# git
git clone git@github.com:vegonza/Malackaton.git malackaton
git pulls

# Install Docker and Docker Compose
sudo apt install -y docker
sudo curl -L "https://github.com/docker/compose/releases/download/v2.16.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose && sudo chmod +x /usr/local/bin/docker-compose

# Certbot
sudo apt install -y certbot
sudo certbot --nginx -d malackathon.iaclover.com
docker cp nginx:/etc/letsencrypt /etc/letsencrypt
