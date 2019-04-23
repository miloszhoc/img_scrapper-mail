# Script is able to download any number of photos from any flickr group
# and send everyday different photo to each person from mailing list.
from mail_with_photo import send_mail
from img_scrapper import main

if __name__ == '__main__':
    main()
    send_mail(86400)
