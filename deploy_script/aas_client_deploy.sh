sshpass -p "root" rsync -av --delete edge-aas-client/aas_edge_client root@192.168.1.112:/var/www/
sshpass -p "root" rsync -av --delete aas_edge_client.s* root@192.168.1.112:/etc/systemd/system/
sshpass -p "root" ssh root@192.168.1.112 "systemctl enable aas_edge_client.socket && systemctl restart aas_edge_client.socket && systemctl enable aas_edge_client.service && systemctl restart aas_edge_client.service"
# sshpass -p "root" rsync -av --delete nginx.conf root@192.168.1.112:/etc/nginx/
# sshpass -p "root" ssh root@192.168.1.112 "systemctl restart nginx"