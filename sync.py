import commands

class Sync:
    def __init__(self, target_root, username="root", server_ip="10.60.17.248", max_num_retry=5):
        self.target_url = username + "@" + server_ip + ":" + target_root
        self.server_ip = server_ip
        self.max_num_retry = max_num_retry + 1
        # rsync --timeout=300 /home/sync_source ying.liu@10.100.135.200:/data0/

    def upload(self, file):
        syncmd = "rsync --timeout=300 {} {}".format(file, self.target_url)
        for i in range(1, self.max_num_retry):
            status = self._retry(syncmd)
            if status:
                break
            print("Server:{} RSYNC FAILED, RETRY TIMES IS {}".format(self.server_ip, i))

    def _retry(self, syncmd):
        result, output = commands.getstatusoutput(syncmd)
        if result==0:
            print("Server: "+self.server_ip+" RSYNC SUCCESS ")
            return True
        else:
            return False