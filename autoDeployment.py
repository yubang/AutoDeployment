#coding:UTF-8

"""
一个基于python的自动化部署程序
@author:yubang
2015-03-09
"""

"""
系统目录构成说明：
autoDeployment.py 主程序
fsData 文件仓库
version 部署的代码版本列表
patch 补丁包生成目录
log 日记存放目录
temp 临时目录
"""

import os,sys,hashlib,json,re,base64

#--------------------------------------------
#文件列表转md5列表
#--------------------------------------------
class FsToDataSystem():
    "文件列表转md5列表处理类"
    def __init__(self):
        pass
    def getMd5Lists(self,path,key='.',lists=None):
        "获取一个文件夹的所有md5列表"
        if(lists==None):
            lists={}
        if(not os.path.exists(path)):
            print unicode("文件(%s)不存在!"%(path),"UTF-8")
            return lists
        if(os.path.isdir(path)):
            fps=os.listdir(path)
            for fp in fps:
                lists=self.getMd5Lists(path+"/"+fp,key+"/"+fp,lists)
            lists[key]="#"
        else:
            fp=open(path,'rb')
            md5=hashlib.md5(fp.read()).hexdigest()
            fp.close()
            lists[key]=md5
        return lists        


#--------------------------------------------
#补丁包生成类
#--------------------------------------------
class PatchSystem():
    "补丁包生成类"
    def __init__(self):
        pass
    def __getAddFile(self,lists,path):
        "提取新增加的文件"
        global applicationPath
        dirPath=applicationPath+"/patch/patch/data/"
        os.makedirs(dirPath)
        for temp in lists:
            texts=temp.split("|")
            if(texts[2]=="add" and texts[1]!="#"):
                filePath=sys.argv[2]+"/"+base64.b64decode(texts[0])
                targetDirPath=dirPath+texts[1][0:8]+"/"+texts[1][8:16]+"/"+texts[1][16:24]
                if(not os.path.exists(targetDirPath)):
                    os.makedirs(targetDirPath)
                in_fp=open(filePath,'rb')
                out_fp=open(targetDirPath+"/"+texts[1][24:32],'wb')
                out_fp.write(in_fp.read())
                in_fp.close()
                out_fp.close()
                
    def __checkDifferent(self,a,b,lists,status):
        "生成补丁包差异列表"
        for t1 in a:
            sign=False
            for t2 in b:
                if(t1==t2):
                    #检测到key一致
                    if(a[t1]!=b[t2]):
                        "文件修改过"
                        sign=True
                        if(status=='add'):
                            lists.append("%s|%s|%s"%(base64.b64encode(t1),a[t1],'update'))
                        break
            if(not sign):
                lists.append("%s|%s|%s"%(base64.b64encode(t1),a[t1],status))
        return lists
    def buildPatch(self,newLists,oldList,path):
        "生成补丁包"
        if(os.path.exists(path)):
            print unicode("补丁包目录(%s)已经存在，中断操作！"%(path),"UTF-8")
            return None
        else:
            os.makedirs(path)
            result=[]
            result=self.__checkDifferent(newLists,oldList,result,"add")
            result=self.__checkDifferent(oldList,newLists,result,"delete")
            #写入修改文件列表
            fp=open(path+"/update",'w')
            fp.write(json.dumps(result))
            fp.close()
            #写入标准文件列表
            fp=open(path+"/new",'w')
            fp.write(json.dumps(newLists))
            fp.close()
            
            self.__getAddFile(result,path)
            
#--------------------------------------------
#部署文件一致性检测
#--------------------------------------------        
class FsCheckSystem():
    "部署文件一致性检测类"
    def __init__(self):
        pass
        
        
#--------------------------------------------
#文件仓库存储系统
#--------------------------------------------    
class FsSaveGetSystem():
    "文件仓库存储系统类"
    def __init__(self):
        pass
    def addNewFile(self,filePath,path="."):
        "添加新文件到文件仓库"
        global applicationPath
        if(os.path.isdir(filePath)):
            if(not os.path.exists(applicationPath+"/fsData/"+path)):
                os.makedirs(applicationPath+"/fsData/"+path)
            fps=os.listdir(filePath)
            for fp in fps:
                self.addNewFile(filePath+"/"+fp,path+"/"+fp)
        else:
            if(not os.path.exists(applicationPath+"/fsData/"+path)):
                in_fp=open(filePath,'rb')
                out_fp=open(applicationPath+"/fsData/"+path,'wb')
                out_fp.write(in_fp.read())
                in_fp.close()
                out_fp.close()
            else:
                print unicode("忽略文件：%s"%(path),"UTF-8")
            
        
        
#--------------------------------------------
#日记系统
#--------------------------------------------
class LogSystem():
    "日记系统" 
    def __init__(self):
        pass
        
        
#--------------------------------------------
#代码部署系统
#--------------------------------------------
class CodeManagerSystem():
    "代码部署系统" 
    def __init__(self):
        pass
        
        
#--------------------------------------------
#自动化系统核心类
#--------------------------------------------
class Core():
    "自动化系统核心类"
    def __init__(self):
        self.__createDir()
        
    def __del__(self):
        self.__deleteTempDirFile()
        
    def __createDir(self):
        "创建程序所需的文件夹"
        global applicationPath 
        fps=['log','version','fsData','temp','patch','temp/patch']
        for temp in fps:
            dirPath=applicationPath+"/"+temp
            if(not os.path.exists(dirPath)):
                os.makedirs(dirPath)
                
    def __deleteTempDirFile(self,tempDirPath=None):
        "删除临时目录内容"
        if(tempDirPath==None):
            global applicationPath
            tempDirPath=applicationPath+"/temp"
        if(os.path.exists(tempDirPath) and os.path.isdir(tempDirPath)):
            fps=os.listdir(tempDirPath)
            for fp in fps:
                tempPath=tempDirPath+"/"+fp
                if(os.path.isdir(tempPath)):
                    self.__deleteTempDirFile(tempPath)
                    #print unicode("删除文件夹","UTF-8"),tempPath
                    os.rmdir(tempPath)
                else:
                    print unicode("删除文件","UTF-8"),tempPath
                    os.remove(tempPath)
                    
    def __list(self):
        "获取文件md5列表"
        global applicationPath
        dao=FsToDataSystem()
        lists=dao.getMd5Lists(sys.argv[2])
        text=json.dumps(lists)
        fp=open(applicationPath+'/patch/md5List.txt','w')
        fp.write(text)
        fp.close()
        print unicode("md5文件列表建立完成！","UTF-8")
        print unicode("文件列表输出于：","UTF-8"),applicationPath+"/patch/md5List.txt"
        
    def __patch(self):
        "生成补丁包"
        global applicationPath
        if(not os.path.exists(sys.argv[2])):
            print unicode("文件（%s）不存在！"%(sys.argv[2]),"UTF-8")
            return None
        elif(not os.path.exists(sys.argv[3])):
            print unicode("文件（%s）不存在！"%(sys.argv[3]),"UTF-8")
            return None
        else:
            dao=FsToDataSystem()
            #新版md5列表
            if(os.path.isdir(sys.argv[2])):
                lists1=dao.getMd5Lists(sys.argv[2])
            else:
                fp=open(sys.argv[2],'r')
                lists1=json.loads(fp.read())
                fp.close()
            #旧版md5列表
            if(os.path.isdir(sys.argv[3])):
                lists2=dao.getMd5Lists(sys.argv[3])
            else:
                fp=open(sys.argv[3],'r')
                lists2=json.loads(fp.read())
                fp.close()
            
            patchSystem=PatchSystem()
            patchSystem.buildPatch(lists1,lists2,applicationPath+"/patch/patch")
            print unicode("生成补丁包完成，补丁包(文件夹)输出于：%s"%(applicationPath+"/patch/patch"),"UTF-8")
    
    def __commit(self):
        "提交一个补丁包"
        global applicationPath
        v=0
        while True:
            targetPath=applicationPath+"/version/"+str(v)
            if(not os.path.exists(targetPath)):
                break
            v=v+1
        os.makedirs(targetPath)
        
        if(not os.path.exists(sys.argv[2])):
            print unicode("补丁包（%s）不存在"%(sys.argv[2]),"UTF-8")
            return None
        
        in_fp=open(sys.argv[2]+"/new",'rb')
        out_fp=open(targetPath+"/new",'wb')
        out_fp.write(in_fp.read())
        in_fp.close()
        out_fp.close()
        
        in_fp=open(sys.argv[2]+"/update",'rb')
        out_fp=open(targetPath+"/update",'wb')
        out_fp.write(in_fp.read())
        in_fp.close()
        out_fp.close()
        
        #文件仓库加入新增文件
        fsSaveGetSystem=FsSaveGetSystem()
        fsSaveGetSystem.addNewFile(sys.argv[2]+"/data")
        print unicode("成功处理补丁包，当前版本号：%d"%(v),"UTF-8")
                
    def init(self):
        "入口函数处理命令行参数"
        if(len(sys.argv)==1):
            print unicode("具体用法请查看API文档","UTF-8")
        else:
            if(sys.argv[1]=='--list'):
                "获取文件md5列表"
                self.__list()
            elif(sys.argv[1]=='--patch'):
                "生成补丁包"
                self.__patch()
            elif(sys.argv[1]=='--commit'):
                "提交一个补丁包"
                self.__commit()        
                               
applicationPath=os.path.dirname(os.path.realpath(__file__))

if __name__ == "__main__":
    core=Core()
    core.init()
