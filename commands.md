# SSH
ssh -i oracle_keys.pem opc@158.179.221.172


# Setup
sudo yum update -y
sudo yum install python3-pip -y
sudo yum install git -y
ssh-keygen -C githubKey

# git
git clone git@github.com:vegonza/Malackaton.git malackaton
git pull

# quitamos podman(docker>podman)
sudo dnf remove -y podman

# docker
sudo dnf install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker && sudo systemctl enable docker
sudo usermod -aG docker $(whoami)

# docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
