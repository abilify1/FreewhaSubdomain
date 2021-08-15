
import subprocess,requests,json,base64,ini,string,random,re,os,ftplib

class Main:
 config = ini.parse(open('config.ini').read())
 sublist = "eu5.org,orgfree.net,6te.net,ueuo.com,noads.biz,coolpage.biz,freeoda.com,freevar.com,freetzi.com,xp3.biz".split(",")
 req = requests.Session()
 qu = '\033[0;36m'
 hi = '\033[0;32m'
 tm = '\033[0;30m'
 pu = '\033[0;37m'
 me = '\033[0;31m'
 ku = '\033[0;33m'
 def __init__(self):
  self.__main__()
 def randomstr(self):
  return(''.join(random.choices(string.ascii_lowercase + string.digits, k = 7)))
 def execute(self,cmd):
    popen = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE,
                             universal_newlines=True)
    for stdout_line in iter(popen.stdout.readline, ""):
         yield stdout_line
    popen.stdout.close()
    return_code = popen.wait()
    if return_code:
        raise subprocess.CalledProcessError(return_code, cmd)
    return return_code
 def createDomain(self,sub,name):
     print("checking domain name...")
     req1 = Main.req.post('https://newserv.freewha.com/cgi-bin/create_ini.cgi',data={"action":"check_domain","thirdLevelDomain":name,"domain":sub}).text
     if "Account already exists" in req1:
      print("domain name %s%s %salready exists"%(Main.ku,name+'.'+sub,Main.pu))
     else:
      print("domain %s%s %sis available✓"%(Main.ku,name+'.'+sub,Main.pu))
      print("registering account...")
      email = self.randomstr()+'@esiix.com'
      req2 = Main.req.post('https://newserv.freewha.com/cgi-bin/create_ini.cgi',data={'action':'validate','domainName':name+'.'+sub,'email':email,'password':Main.config['freewha']['password'],'confirmPassword':Main.config['freewha']['password'],'agree':'1'})
      if "was successfully activated.":
       username = name+"."+sub
       print("success created account with credentials: ")
       print("     - username = %s"%(name+'.'+sub))
       print("     - email = %s"%(email))
       print("     - password = %s"%(Main.config['freewha']['password']))
       print("save credentials to %sresult/%s.%s%s"%(Main.ku,name,sub,Main.pu))
       open('result/'+username,'w+').write('username:%s\nemail:%s\npassword:%s'%(name+'.'+sub,email,Main.config['freewha']['password']))
       print("uploading file %s%s%s"%(Main.ku,Main.config['freewha']['ftpupload'],Main.pu))
       try:
        session = ftplib.FTP(username,username,Main.config['freewha']['password'],timeout=5)
        file = open(Main.config['freewha']['ftpupload'],'rb')
        session.storbinary('STOR %s'%Main.config['freewha']['ftpupload'], file)
        file.close()
        session.quit()
        print("success uploaded at %shttp://%s/%s %s√"%(Main.ku,username,Main.config['freewha']['ftpupload'],Main.pu))
        open('result.txt','a').write("\nhttp://%s/%s"%(username,Main.config['freewha']['ftpupload']))
        print("save list web to %sresult.txt"%Main.ku)
        print("%swebsite %s%s %scompleted"%(Main.hi,Main.ku,username,Main.hi))
       except Exception as e:
        if str(e) == "timed out":
          wow = Main.req.get('http://%s/%s'%(username,Main.config['freewha']['ftpupload']))
          if wow.text == open(Main.config['freewha']['ftpupload'],'r').read():
           print("success uploaded at %shttp://%s/%s %s√"%(Main.ku,username,Main.config['freewha']['ftpupload'],Main.pu))
           open('result.txt','a').write("\nhttp://%s/%s"%(username,Main.config['freewha']['ftpupload']))
           print("save list web to %sresult.txt"%Main.ku)
           print("%swebsite %s%s %scompleted"%(Main.hi,Main.ku,username,Main.hi))
          else:print(e)
 def banner(self):
    eval(open('banner.txt','r').read())
 def consoleMode(self):
    print("")
    print("Type .help for a list of commands\nUsage: .create [subdomain] [name]")
    while True:
     conInp = input("%s%s %s> %s"%(Main.me,Main.config['console']['consoleText'],Main.ku,Main.pu))
     argsCon = conInp.split()
     if len(argsCon) == 0: continue
     elif argsCon[0] == ".help":
      if len(argsCon) == 1:
       print("""usage : .create [--random] [--count=?]
                subdomain   name
example .create eu5.org testingwebsite

positional arguments:
   subdomain  to see subdomain list > .help sublist
   name  name of your domain

optional argument:
   --random  random domain name
   --count  how many times to create a website, example=2 this will make the script create a website twice with different names (set in INI file to configure domain name list, or use --random)

to exit type .exit""")
      if len(argsCon) == 2:
       if argsCon[1] == "sublist":
        print("""this is a list of possible subdomains: 
- eu5.org
- orgfree.net
- 6te.net
- ueuo.com
- noads.biz
- coolpage.biz
- freeoda.com
- freevar.com
- freetzi.com
- xp3.biz""")
     elif argsCon[0] == ".create":
      if (len(argsCon) == 1) or (len(argsCon) == 2): print("arguments error! type .help for more information")
      elif argsCon[1] not in Main.sublist:
        if int(Main.config['freewha']['randomsubdomain']) == 1 and "--random" in argsCon:
         pass
        elif int(Main.config['freewha']['randomsubdomain']) == 1 and "--count" in argsCon:
         pass
        else:print ("subdomain %s%s %snot found! type .help sublist for more information"%(Main.ku,argsCon[1],Main.pu));continue
      if len(argsCon[2]) < 3:
        print("domain name must be a least 3 chaeacters!")
      if "--count" in conInp and "--random" not in argsCon:
       namelist=open('list.txt').read().splitlines()
       pala=0
       for waw in namelist:
        pala+=1
        print("         %s[%s%s%s]         "%(Main.pu,Main.ku,pala,Main.pu))
        try:
         self.createDomain(argsCon[1],waw)
        except Exception as e:print('Error : %s'%e);continue
      if "--random" in argsCon:
       randomT = self.randomstr()
       if Main.config['freewha']['randomsubdomain'] == 1: 
          print('%s[%s#%s] Random Subdomain enabled!'%(Main.pu,Main.ku,Main.pu))
          subnew = random.choice(Main.sublist)
          argsCon = [w.replace(argsCon[1],subnew) for w in argsCon]
       if "--count" in conInp:
        count = re.search(r'--count=(.*)',conInp).group(1)
        if "--random" in count:
         count=re.search(r'--count=(.*)',conInp).group(1).strip(' --random')
        for x in range(int(count)):
         if Main.config['freewha']['randomsubdomain'] == 1:
          subnew = random.choice(Main.sublist)
          argsCon = [w.replace(argsCon[1],subnew) for w in argsCon]
          randomX = self.randomstr()
          print("         %s[%s%s%s]         "%(Main.pu,Main.ku,x+1,Main.pu))
          try:
           self.createDomain(argsCon[1],randomX)
          except Exception as e:
           print("Error : %s"%e)
       else: self.createDomain(argsCon[1],randomT)
      else:
               self.createDomain(argsCon[1],argsCon[2])
              #self.createDomain(argsCon[1],argsCon[2])
     elif argsCon[0] == ".exit":
      exit('exiting.')
     elif argsCon[0] == ".delete":
      if len(argsCon) == 1:
       print('Delete?\n%s>%s resultfile - remove result.txt file\n%s>%s crendentialsfile  - delete all credentials file in result folder\nexample : %s.delete resultfile'%(Main.ku,Main.pu,Main.ku,Main.pu,Main.ku))
      elif argsCon[1] == "resultfile":
       os.system('rm result.txt')
       os.system('touch result.txt')
       print('done deleting result.txt✓')
      elif argsCon[1] == "credentialsfile":
       os.system('rm result/*')
       print('done deleting all crendetials file in result folder✓')
      else:
       print('%s%s %snot defined!'%(Main.ku,argsCon[1],Main.pu))
     else:print("unknown commands! .help for more information")
 def __main__(self):
    #wan1 = Main.req.post("")
    self.banner()
    print('%s[%s#%s] %sconfig.ini file loaded'%(Main.pu,Main.ku,Main.pu,Main.pu))
    print('%s[%s#%s] %sCurrently console mode disabled'%(Main.pu,Main.ku,Main.pu,Main.pu))
    if Main.config['console']['enable'] == 1:
     self.consoleMode()



if __name__ == "__main__":
 Main()
