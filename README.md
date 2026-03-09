# pixiv_crawler
爬取p站图片的简易爬虫工具

![PixPin_2026-02-11_13-59-20](https://github.com/user-attachments/assets/f7e44adc-41f6-4d92-88ac-02b6030cee96)

# 安装爬虫工具命令
支持命令格式执行爬虫工具

将源代码下载到本地

<img width="566" height="162" alt="image" src="https://github.com/user-attachments/assets/046b4441-17c3-4245-955a-cbb1e93ca1e5" />

进入pixiv_download文件夹 并修改confiug.yaml

<img width="689" height="273" alt="image" src="https://github.com/user-attachments/assets/f4eb5603-b2a7-4e24-82e2-544fffd12adb" />

将cookie部分补全 即可正常使用

<img width="1085" height="632" alt="image" src="https://github.com/user-attachments/assets/1e99cc30-4f31-492c-bc73-cdeddae69d54" />

回到setup.py文件的目录 并启动cmd

执行以下命令

```pip install . ```

<img width="562" height="130" alt="image" src="https://github.com/user-attachments/assets/85662c36-df7f-4cad-a1f0-5c30f7a5486e" />


随后即可正常使用

<img width="562" height="304" alt="image" src="https://github.com/user-attachments/assets/297ee44d-729a-456d-88d8-710024dba8b6" />


# 实现功能

多模式下载 比如下载每日榜单图片,下载作者作品,通过搜索tag下载作品

高并发下载图片

支持下载作品集

重试机制


# cookei设置
<img width="375" height="126" alt="image" src="https://github.com/user-attachments/assets/8f9aac0c-e7f3-4301-a16e-2139295e6d07" />

要想爬取r18榜单的图片 需要设置cookie模拟登录

<img width="1898" height="711" alt="image" src="https://github.com/user-attachments/assets/d19bf7f9-d3e1-4940-ba73-1a61dccb76a5" />

访问p站 按下f12

点击网络 可以看到数据包信息 其中的cookie字段就是我们需要的

将cookise放入py脚本中即可正常爬取r18榜单


<img width="941" height="361" alt="image" src="https://github.com/user-attachments/assets/4a713a9c-0165-40a6-b0b2-b41dd57aef00" />

**最好是设置好了cookie再用**

# 代理设置
使用前需要先设置好代理 然后才能正常爬取

py脚本中默认设置代理地址为

<img width="482" height="99" alt="image" src="https://github.com/user-attachments/assets/ff6ff8d4-f6e1-4bc6-9048-1eb69849ba53" />

如果每次爬取的中途中老是断开连接 大概率是你的代理节点不稳定

请更换一个较为稳定的节点再使用脚本

<img width="643" height="420" alt="image" src="https://github.com/user-attachments/assets/72d03d8d-36f1-4ad0-9830-e536d77a4e2e" />

# 保存文件
默认保存在D盘下的qb文件下

如果不存在则会自动创建文件

# 模式类型
该脚本有五种模式

第一种模式是daily模式(每日榜单)

该模式需要填入日期与页码

<img width="520" height="266" alt="image" src="https://github.com/user-attachments/assets/0741550a-750c-45cd-8932-4eb5762a706a" />


最终会爬取对应日期与页码的图片

**注意**:选择日期的时候 最多只能指定日期为当天日期的前一天 因为p站每日榜单就是统计昨天的排行榜图片

第二种模式是daily_r18模式(每日榜单r18)

该模式与第一种模式一样 只是爬取的内容变成了r18的图片

第三种模式是author模式(作者模式)

该模式需要填入作者的uid与你需要爬取的作品数量

<img width="549" height="282" alt="image" src="https://github.com/user-attachments/assets/733014e1-7677-4813-b39f-d1fd13b4bd86" />


最终会爬取相对应作者的作品

第四种模式是tag模式(标签模式)

该模式需要填入tag与页码

<img width="504" height="278" alt="image" src="https://github.com/user-attachments/assets/92cf9c51-f28e-4b28-aec6-e44a01717cc0" />


最终会选择收藏数大于等于200的作品

收藏数可以在代码中随意更改

第五种模式是默认模式

<img width="553" height="190" alt="image" src="https://github.com/user-attachments/assets/bbb6309c-fb2f-4d37-9154-4c63d4818802" />


自动爬取当日榜单的前50个作品

<img width="809" height="270" alt="image" src="https://github.com/user-attachments/assets/9247be7d-465f-4292-b618-5c7f7c827003" />

# 碎碎念
这个工具是本人第一次写的比较完整的工具

没有什么项目经验 所以所有代码都被整到一个py文件中 看起来比较复杂 没有分模块

本来是想简单写一个工具 没想到写了这么多

之后应该会重构一下代码 搞一个分模块的版本 好看一些
