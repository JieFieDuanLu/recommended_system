#! /bin/bash
set -x
echo 'start training......'

A=("10.251.133.225" "10.163.108.8")

#!!!!!!!!!delete new news!!!!!!!######
rm -rf /home/workspace/nnews
rm -rf /home/workspace/nlsi

mkdir /home/workspace/nnews
curl 'http://127.0.0.1:19080/exportArticle?number=100'
#curl 'http://127.0.0.1:19080/exportArticle'

sleep 1
# pkill local service:similarity_update_service
#pkill -9 gunicorn
#pkill -9 python
sleep 1

cd /home/workspace
python similarity_run.py > similarity.log

#ps -ef|grep python |grep -v grep | awk '{print $2}'|xargs kill -9


#!!!!!!!!!delete news!!!!!!!######
rm -rf /home/workspace/news
rm -rf /home/workspace/lsi
rm -rf /home/workspace/lsitemp
rm -rf /home/workspace/prefix_map

mv /home/workspace/nnews /home/workspace/news
mkdir /home/workspace/lsi
cp /home/workspace/nlsi/* /home/workspace/lsi

#nohup gunicorn -w1 -t 600 -k gevent -b0.0.0.0:3001 service_viva:app --preload --limit-request-line 0 > service.log &

# remote pkill gunicorn python
for client in ${A[@]}; do

ssh $client "sh /home/workspace/stop_service.sh"

# remote del and cp news & lsi
ssh $client "rm -rf /home/workspace/news"
ssh $client "rm -rf /home/workspace/lsi"
ssh $client "rm -rf /home/workspace/nlsi"
scp -r /home/workspace/news/ $client:/home/workspace/
scp -r /home/workspace/lsi/ $client:/home/workspace/
scp -r /home/workspace/nlsi/ $client:/home/workspace/
#python /home/workspace/service.py &

sleep 1
#gunicorn -w4 -t 600 -k gevent -b0.0.0.0:3000 service_viva:app --preload --limit-request-line 0 --worker-connections 500

# remote gunicorn
# run remote similar find
ssh ${A} "sh /home/workspace/gunicorn.sh"
done

# run getfiles
#nohup python similarity_update_service.pyc > update_service.log &

sleep 10
exit

