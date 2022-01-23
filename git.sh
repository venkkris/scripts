## Execute this shell script prior to syncing with remote at Github
#!/bin/bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
echo 'export GPG_TTY=$(tty)' >> ~/.bashrc
