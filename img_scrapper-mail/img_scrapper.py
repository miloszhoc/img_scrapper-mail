# Script gets response from Flickr API then using received data and json module converts it to python object.
# Yields a dictionary which contains only necessary fields (like photo id etc.) and passes it to link_builder
# which builds a link, and then yields every link to downloader function(which is based on requests module).
# Script also creates a folder to store picture.

import subprocess
import requests
import flickrapi
import json


# works only on flickr groups
def flickr_api_response(group_id, pics_number, api_key, api_secret):
    # example of link of photo unavailable for download (in most cases)
    # https://www.flickr.com/photos/barrobphotos/41452777820/sizes/q/
    # domain/photos/ownername(or owner id)/id/sizes/q/
    #
    # link of photo available for download
    # https://live.staticflickr.com/1807/41452777820_4b807cfdcc_q.jpg
    # domain/server/id_secret_size.jpg
    #

    flickr = flickrapi.FlickrAPI(api_key, api_secret, format='json')
    data = flickr.do_flickr_call(_method_name='flickr.groups.pools.getPhotos', timeout=None, group_id=group_id,
                                 per_page=pics_number,
                                 api_key=api_key)

    # returns json data from API response
    return data


# returns dictionary which contains only necessary data to build a link
def response_parser(api_response):
    data = json.loads(api_response)  # loads response as python object
    all_pics = data['photos']['photo']  # contains only data which refers to photos

    for i in all_pics:  # iterates through data of all pics and takes only id, server and secret values
        photo_data = {i['id']: [i['server'], i['secret']]}  # dictionary contains {id:[server_id, secret_id]}
        yield photo_data


def link_builder(photo_data, pic_size):
    # https://live.staticflickr.com/1807/41452777820_4b807cfdcc_q.jpg
    # domain/server/id_secret_size.jpg

    # iterates through the dictionary and builds links using a pattern
    for one_photo in photo_data:  # data of all photos
        for i, j in zip(one_photo.keys(), one_photo.values()):  # data of one photo
            # i == photo_id
            # j[0] == server
            # j[1] == secret
            link = f'https://live.staticflickr.com/{j[0]}/{i}_{j[1]}_{pic_size}.jpg'  # pattern for link
            yield link


# creates a folder
def folder_create(folder_name):
    subprocess.run(f'mkdir {folder_name}', shell=True)


# saves pictures to folder 'pics' using pattern: pic1.jpg, pic2.jpg, pic3.jpg... pic365.jpg
def pics_downloader(link, pics_number, folder_name):
    counter = 1
    # pattern for pics names from pic1.jpg to pic365.jpg
    names = ["pic" + str(i) + ".jpg" for i in range(1, pics_number + 1)]

    for i, j in zip(link, names):
        req = requests.get(i)
        with open(f'./{folder_name}/{j}', 'bw+') as f:
            f.write(req.content)

        print(str(counter) + '/' + str(pics_number))
        counter += 1


def main():
    api_key = u''  # your api key here
    api_secret = u''  # your api secret here
    group_id = '17986756@N00'  # group id here
    pics_number = 365  # how many pictures needs to be downloaded
    pic_size = 'c'  # size of each picture
    # safe sizes:
    # for (75 x 75) use 's'
    # for (150 x 150) use 'q'
    # for (100 x 66) use 't'
    # for (240 x 159) use 'm_d'
    # for (320 x 212) use 'n'
    # for (500 x 331) use 'd'
    # for (640 x 424) use 'z'
    # for (800 x 530) use 'c'
    # for (1024 x 678) use 'b'
    # changing size to higher than above resolutions will cause malfunction because link looks different
    folder_name = 'pics'

    # connection to flickr api in order to download all pics from group
    flickr_response = flickr_api_response(group_id, pics_number, api_key, api_secret)

    # generator function which takes only necessary data from response
    pics_data = response_parser(flickr_response)

    # link builder
    build_link = link_builder(pics_data, pic_size)

    # creates folder using given name
    folder_create(folder_name)

    # downloads pics from link using response module
    pics_downloader(build_link, pics_number, folder_name)

    print('All finished!')


if __name__ == '__main__':
    main()
