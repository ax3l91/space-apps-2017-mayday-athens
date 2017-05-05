import numpy as np
import matplotlib.pyplot as plt
import sys, getopt
import csv
import json

sys.path.append('/usr/lib/python2.7/dist-packages/mpl_toolkits/basemap')
from mpl_toolkits.basemap import Basemap
from matplotlib import rc,rcParams
from aacgmv2 import convert
from scipy.interpolate import interp1d 
from scipy.integrate import quad
rc('text', usetex=False)
rcParams['ytick.labelsize'],rcParams['xtick.labelsize'] = 17.,17.
rcParams['axes.labelsize']=19.
rcParams['legend.fontsize']=17.
rcParams['text.latex.preamble'] = ['\\usepackage{siunitx}']
rcParams['figure.figsize'] = (11., 6)

from os import system

#system("wget 'http://legacy-www.swpc.noaa.gov/wingkp/wingkp_list.txt' -P Data/")
#system("wget 'http://services.swpc.noaa.gov/text/aurora-nowcast-map.txt' -P Data/ ")
#system("wget 'http://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt' -P Data/")

def H(lon,lat,zone='ion'):
    D={'tropo':[20.,7.],'strato':[50.,17.5],'meso':[85.,29.7],'ion':[100.,35.]}
    a=D[zone]
    return a[0]*a[1]/np.sqrt((a[1]*np.cos(lat*np.pi/180.))**2+(a[0]*np.sin(lat*np.pi/180.))**2)
def rho(h): return 0.0014444*np.exp(-0.0001294*h) #density(g/cm^3) on height h(m) 


alt=13.

kpl=np.loadtxt('Data/wingkp_list.txt',comments=[':','#'])
aurora=np.loadtxt('Data/aurora-nowcast-map.txt')
flight=np.loadtxt('Data/BIKF-NZAA.csv',delimiter=',',dtype=str)
fluxdata=np.loadtxt('Data/goes-particle-flux-primary.txt',comments=[':','#'])
flat=flight[:,3].astype(float)
flon=flight[:,4].astype(float)
Kphi=[66.5,64.5,62.4,60.4,58.3,56.3,54.2,52.2,50.1,48.1]
kp=kpl[:,17][0]
maxphi=Kphi[int(kp)]


nlats = 256
nlons = 256
lats=np.linspace(-90,90,nlats)
lons=np.linspace(-180,180,nlons)
glatN=maxphi*np.ones(nlats)
glonN=np.linspace(-180,180,nlons)
mlatN,mlonN=convert(glatN,glonN,alt)
glatS=-maxphi*np.ones(nlats)
glonS=np.linspace(-180,180,nlons)
mlatS,mlonS=convert(glatS,glonS,alt)

p=0.042 #probabillity (GOES data)
f1=fluxdata[:,12][0]*p #Electron Flux >0.8 Mev
f2=fluxdata[:,13][0]*p #Electron Flux >2 Mev
f3=fluxdata[:,14][0]*p if fluxdata[:,14][0]>0. else 0. #Electron Flux >4 Mev

def distance(lon1,lat1,lon2,lat2):
    df=(lat2-lat1)*0.0174533
    phi1=lat1*0.0174533
    phi2=lat2*0.0174533
    dl=(lon2-lon1)*0.0174533
    a=np.sin(df/2.)*np.sin(df/2)+np.cos(phi1)*np.cos(phi2)*np.sin(dl/2)*np.sin(dl/2.)
    c=2.*np.arctan2(np.sqrt(a),np.sqrt(1.-a))
    d = 6371. * c
    return d

def F1(lon,lat,F10,alt=13.,S1=1.680):
    energy0=1.5*2.*F10
    return energy0-S1*quad(rho,alt*1000.,H(lon,lat)*1000.)[0]
def F2(lon,lat,F20,alt=13.,S2=1.783):
    energy0=3.*2.*F20
    return energy0-S2*quad(rho,alt*1000.,H(lon,lat)*1000.)[0]
def F3(lon,lat,F30,alt=13.,S3=1.85):
    energy0=3.*2.*F30
    return energy0-S3*quad(rho,alt*1000.,H(lon,lat)*1000.)[0]
def Fcr(lon,lat,alt=13.):
    return (1.2e3)*(1e-4)*10**((10./3) *np.log10(alt)-1./3) #MeV/cm^2

def Dose(lon,lat,F10,F20,F30,alt=13.):
    K=1.602e-10 #Sv
    S1=0.02706*(F1(lon,lat,F10)/F10)+1.839
    S2=0.02706*(F2(lon,lat,F20)/F20)+1.839
    S3=0.02706*(F3(lon,lat,F30)/F30)+1.839 if F30>0. else 0.
    Scr=0.03908*np.exp(0.006463*Fcr(lon,lat,alt)/Fcr(lon,lat,100))+0.002216
    final1=F1(lon,lat,F10)-2322. if F1(lon,lat,F10)>2322. else 0.
    final2=F2(lon,lat,F20)-2322. if F2(lon,lat,F20)>2322. else 0.
    final3=F3(lon,lat,F30)-2322. if F3(lon,lat,F30)>2322. else 0.
    finalcr=Fcr(lon,lat,alt) - 50.139 if Fcr(lon,lat,alt)>50.139 else 0.
    return K*2.*np.pi*(S1*final1+S2*final2+S3*final3+Scr*finalcr)

#prob= np.array([F1(flon[i],flat[i],f1) if convert(flat[i],flon[i],alt)>convert(maxphi,flon[i],alt) else 0. for i in range(flon.shape[0])])
prob=(1e3)*np.array([Dose(flon[i],flat[i],f1,f2,f3) if convert(flat[i],flon[i],alt)>convert(maxphi,flon[i],alt) else 0. for i in range(flon.shape[0])])
dist=np.array([distance(flon[i-1],flat[i-1],flon[i],flat[i]) for i in range(1,flon.shape[0])])
dist=np.cumsum(np.insert(dist,0,0))
rad=interp1d(dist,prob)
plt.plot(dist,rad(dist))
plt.ylabel('Dose (mSv)')
plt.xlabel('Distance (km)')
plt.savefig('ExportedImages/Dose.png')

plt.plot(dist,np.cumsum(rad(dist)))
plt.ylabel('Integrated Dose (mSv)')
plt.xlabel('Distance (km)')
plt.savefig('ExportedImages/integratedDose.png')

DoseMap=np.array([[Dose(x,y,f1,f2,f3) for x in lons[::1]] for y in lats[::1]])

Data=np.zeros((dist.shape[0],5))
Data[:,0]=flon
Data[:,1]=flat
Data[:,2]=dist
Data[:,3]=rad(dist)
Data[:,4]=np.cumsum(rad(dist)) 
np.savetxt('Data/data.csv',Data,header='Lon,Lat,Distance,Radiance,CummulativeRadiance',delimiter=',',comments='')

X,Y=np.meshgrid(lons,lats)
fig=plt.figure(figsize=(10,20))
m = Basemap(projection='ortho',lat_0=20,lon_0=-120,resolution='l')
m.drawcoastlines(linewidth=0.7)
m.fillcontinents(color='#cc9966',lake_color='#99ffff',alpha=0.3)
m.drawparallels(np.arange(-80,81,30),labels=[1,1,0,0])
#m.drawparallels([maxphi,-maxphi],labels=[1,1,0,0])
m.drawmeridians(np.arange(0,360,60),labels=[0,0,0,1])
#M=Dose(X,Y,f1,f2,f3)
if DoseMap.max()>DoseMap.min():
    cm=m.contourf(X,Y,DoseMap,latlon=True,alpha=0.75,cmap='gist_gray_r',levels=np.linspace(DoseMap.min(),DoseMap.max()))
else:
    print("Not enough flux to penetrate")
#plt.colorbar(cm)
m.plot(flon,flat,latlon=True,linewidth=2.)
m.plot(m.shiftdata(mlonN, mlatN)[0],m.shiftdata(mlonN, mlatN)[1],latlon=True,linewidth=2)
m.plot(m.shiftdata(mlonS, mlatS)[0],m.shiftdata(mlonS, mlatS)[1],latlon=True,linewidth=2)
fig.savefig('ExportedImages/DosePlanet.png')



#Get Command Line Arguments
input_file = 'Data/data.csv'
output_file = 'Data/getinfodata_local.json'
format = ''


def write_json(data, json_file, format):
    with open(json_file, "w") as f:
        if format == "pretty":
            f.write('planedata='+json.dumps(data, sort_keys=False, indent=4, separators=(',', ': '),encoding="ASCII",ensure_ascii=False))
        else:
            f.write('planedata='+json.dumps(data))
#Read CSV File
def read_csv(file, json_file, format):
    csv_rows = []
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        title = reader.fieldnames
        for row in reader:
            csv_rows.extend([{title[i]:row[title[i]] for i in range(len(title))}])
        write_json(csv_rows, json_file, format)

read_csv(input_file, output_file, format)
