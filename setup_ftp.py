from distutils.core import setup
import py2exe
includes = ["encodings", "encodings.*"]
options = {"py2exe":
            {   "compressed": 1,
                "optimize": 2,
                "includes": includes,
                "bundle_files": 1
            }
          }
setup(   
    version = "0.9.3",
    description = "Donwload File on FTP",
    name = "FTPDownloader",
    options = options,
    zipfile=None,
    #windows=[{"script": "FTPDownloader.py", "icon_resources": [(1, "FTP.ico")] }],  
    console = [{"script": "ftp.py", "icon_resources": [(1, "FTP.ico")] }],  
    #windows=[{"script": "FTPDownloader.py"}] 
    
    )
