import data_manipulation as dm
import data_visualization as dv


if __name__ =="__main__":
    path =""

    img = dm.read_img(path).dataobj

    dv.see_random_slice(img)
