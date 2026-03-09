import yaml
from pathlib import Path 




class Config():
    _config={}
    

    @property
    def proxy(self):
        #获取代理信息
        proxy_url=self._get_values(["network","proxy_url"],"http://127.0.0.1:7890")
        return proxy_url
    
    @property
    def header(self):
        header=self._get_values(["network","header"])
        return header
    
    @property
    def cookies(self):
        cookies=self._get_values(["network","cookies"])
        return cookies

    @property
    def path_other_name(self):
        path=self._get_values(["setting","path_other_name"],"D:/qb")
        return path
    
    @property
    def path(self):
        path=self._get_values(["setting","path"],"D:\\qb")
        return path

    @property
    def max_retries(self):
        max_retries=self._get_values(["setting","max_retries"],3)
        return int(max_retries)

    @property
    def max_workers(self):
        max_worker=self._get_values(["setting","max_workers"],20)
        return int(max_worker)
    
    def _get_values(self,keys,default=None):
        #实例方法 获取配置信息
        values=self._config
        try:
            for key in keys:
                values=values[key]
            return values
        except (KeyError,TypeError):
            return default
    


    @classmethod
    def load(cls,config_path=None):
        #类方法 用于加载配置文件
        if config_path is None:
            config_path=Path(__file__).parent/"config.yaml"
        else:
            config_path=Path(config_path)

        if config_path.exists():
            with open(config_path,"r") as f:
                cls._config=yaml.safe_load(f)#将yaml文件加载到_config中 
                #将yaml中的数据转化为python中的字典类型
                print(f"[+]配置文件已加载: {config_path}")
                return cls._config
        else:
            print(f"[-]配置文件加载失败: {config_path}")
            cls._config={}
            return cls._config
