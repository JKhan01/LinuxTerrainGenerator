from flask import Flask, render_template,request,flash, redirect
from form import inputQuery
from geopy.geocoders import Nominatim
import webbrowser
import os
import cv2
import time
import PIL
from PIL import Image
app = Flask(__name__)
app.config['SECRET_KEY'] = "15de2e5584da6716f650e3d50fa752cd"
inp=[]
@app.route('/')
def index():
    # print ("hello world")
    # return render_template("base.html")
    form = inputQuery()

    return render_template("form.html", title ="Query", form = form)

@app.route('/exec', methods=['GET'])
def exec():
    inp=[]
    inp.append(str(request.args.get("loc")))
    inp.append(str(request.args.get("proj")))
    inp.append(float(request.args.get("ext")))
    inp.append(str(request.args.get("uname")))
    inp.append(str(request.args.get("email")))
    commands = {"dir":["cd ~/Downloads","cd ~/.gazebo/models/"],"unzip":["unzip"],"move":["mv"],"list":["ls -a "]}
    dirs = ["~/Downloads/","~/.gazebo/","~/.gazebo/models/"]
    locate = Nominatim(user_agent="jkhan266@gmail.com")
    loc = inp[0]
    result =locate.geocode(loc)
    print (result)
    lat = [str(result.latitude), str(result.latitude+((0.170*(inp[2]))/18))]
    lon = [str(result.longitude), str(result.longitude+((0.170*(inp[2]))/18))]
    print(lat)
    print(lon)
    nm = inp[1]
    url = "http://terrain.party/api/export?name=" + nm + "&box="+ lon[0] + ","+ lat[0]+","+lon[1]+ ","+lat[1] 
    print (url)
    webbrowser.open(url)
    debug = webbrowser.open(url)
    if (debug):
        time.sleep(25)
        print ("success!!")
        command_01 = os.system("mkdir -p "+ dirs[2]+nm+"/materials/textures")
        if (command_01 == 0):
            time.sleep(5)
            print ("unzip "+dirs[0]+nm+"\ terrain.zip"+ " -d "+dirs[0]+nm+"\ terrain")
            command_02 = os.system("unzip "+dirs[0]+nm+"\ terrain.zip"+ " -d "+dirs[0]+nm+"\ terrain")
            if (command_02 == 0):
                print ("unzip successful")
                time.sleep(7)
                #img = cv2.imread(dirs[0]+nm+"\ terrain/"+nm+"\ Height"+ "\Map"+ "\(Merged).png")
                cmd = os.system("mv "+dirs[0]+nm+"\ terrain/"+nm+"\ Height\ Map\ \(Merged\).png" + " " + dirs[2]+nm+"/materials/textures/greyscale.png")
                cmd_01 = os.chdir("/home/jkhan01/.gazebo/models/"+nm+"/materials/textures/")
                img = Image.open("greyscale.png")
                img = img.resize((513,513),PIL.Image.ANTIALIAS)
                img_list = list(img.getdata())
                img_size =513      
                # Find minimum and maximum value pixels in the image
                img_max = max(img_list)
                img_min = min(img_list)

                # Determine factor to scale to a 8-bit image
                scale_factor = 255.0/(img_max - img_min)

                img_list_new = [0] * img_size * img_size

                # Rescale all pixels to the range 0 to 255 (in line with unit8 values)
                for i in range(0,img_size):
                    for j in range(0,img_size):
                        img_list_new[i*img_size + j] = int((img_list[i*img_size + j]-img_min)*scale_factor)
                        if (img_list_new[i*img_size + j] > 255) or (img_list_new[i*img_size + j] < 0) or (img_list_new[i*img_size + j]-int(img_list_new[i*img_size + j]) != 0):
                            print("img_list_new[%d][%d] = %r" % (i,j,img_list_new[i*img_size + j]))

                img.putdata(img_list_new)

                # Convert to uint8 greyscale image
                img = img.convert('L')

                # Save image
                img.save("greyscale.png")
                print ("Image at destination")
                pths = "/home/jkhan01/.gazebo/models/"+nm+"/model.sdf"
                pthc = "/home/jkhan01/.gazebo/models/"+nm+"/model.config"
                print (pths)
                sdf = open(pths,"a")
                st_sdf = ['<?xml version="1.0" ?>','<sdf version="1.5">','<model name="gazeboTerrain_01">',"<static>true</static>",
                            '<link name="link">','<collision name="collision">',"<geometry>",
                            "<heightmap>","<uri>model://"+nm+"/materials/textures/greyscale.png</uri>","<size>150 150 60</size>","<pos>0 0 0</pos>","</heightmap>","</geometry>","</collision>",
                            '<visual name="visual_abcedf">',
                            '<geometry>',
                                '<heightmap>',
                                '<use_terrain_paging>false</use_terrain_paging>',
                                '<texture>',
                                    '<diffuse>file://media/materials/textures/dirt_diffusespecular.png</diffuse>',
                                    '<normal>file://media/materials/textures/flat_normal.png</normal>',
                                    '<size>1</size>',
                                '</texture>',
                                '<texture>',
                                    '<diffuse>file://media/materials/textures/grass_diffusespecular.png</diffuse>',
                                    '<normal>file://media/materials/textures/flat_normal.png</normal>',
                                    '<size>1</size>',
                                '</texture>',
                                '<texture>',
                                    '<diffuse>file://media/materials/textures/fungus_diffusespecular.png</diffuse>',
                                    '<normal>file://media/materials/textures/flat_normal.png</normal>',
                                    '<size>1</size>',
                                    '</texture>',
                                    '<blend>',
                                        '<min_height>2</min_height>',
                                        '<fade_dist>5</fade_dist>',
                                    '</blend>',
                                    '<blend>',
                                        '<min_height>4</min_height>',
                                        '<fade_dist>5</fade_dist>',
                                    '</blend>',
                                    '<uri>model://'+nm+'/materials/textures/greyscale.png</uri>',
                                    '<size>150 150 60</size>',
                                    '<pos>0 0 0</pos>',
                                    "</heightmap>",
                                "</geometry>",
                                "</visual>",
                            "</link></model>  <!--/world-->",
                        "</sdf>"]
                print (st_sdf)
                for i in st_sdf:
                    sdf.write("\n"+i)
                std_config = ['<?xml version="1.0"?>','<model>','<name>',nm,'</name>','<version>1.0</version>',
                                '<sdf version="1.5">model.sdf</sdf>','<author>','<name>',inp[3],'</name>','<email>',inp[4],'</email></author>',
                                '<description>A simple terrain generated for Basic Surveying.  </description></model>']
                config = open(pthc,"a")
                for j in std_config:
                    config.write("\n"+j)
    return redirect ('/')

if __name__ == '__main__':
    app.run(debug=True)