# Fetch data from a HTTP server and stage locally.
# for this example we are expecting the pyart_2018 env file

import urllib.request
import os
import shutil


def get_a_file(url, odir):
    ofile = url.split('/')[-1]
    file_name = os.path.join(odir, ofile)
    print('fetching ' + file_name)
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)


def filelist():
    files = ['http://www.mcs.anl.gov/~scollis/pyart/sgpxsaprcmacsurI5.c1.20170801.044013.nc',
             'http://www.mcs.anl.gov/~scollis/pyart/66_20181025_084830.pvol.h5',
             'http://www.mcs.anl.gov/~scollis/pyart/nsaxsaprppiC1.a1.20140201.184802.nc']

    return files

if __name__ == "__main__":
    this_dir = os.path.dirname(os.path.abspath(__file__))
    print(this_dir)
    urllist = filelist()
    for this_url in urllist:
        get_a_file(this_url, this_dir)



