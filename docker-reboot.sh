DIR=$(dirname $(readlink -f $0))
echo $DIR
cd $DIR
mkdir -p docker-log
mv reboot.log docker-log/"$(date +"old-%m-%d-%y--%T.%N")".log
date > reboot.log
echo ------------------------------------------------------------ | tee -a reboot.log
echo ------------------------------------------------------------ | tee -a reboot.log
echo ------------------------------------------------------------ | tee -a reboot.log
python main.py 2>&1 | tee -a reboot.log
