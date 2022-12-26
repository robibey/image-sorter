import os
import shutil
import datetime
import cv2
from multiprocessing import Pool
from PIL import Image
from functools import partial
    
def main():
    while True:
        source_path = input("Directory path: ")
        if not os.path.isdir(source_path):
            print("Directory path is invalid.")
            continue
        break
    print()
    print('Detecting corrupted or invalid images.')
    images = []
    for root, _, files in os.walk(source_path):
        for file in files:
            images.append(os.path.join(root, file))

    # with Pool() as pool:
    #     multiprocess_pool = pool.map(multi_cv2_bad_files, images)
    # good_list = [i for output in multiprocess_pool for i in output[0]]
    # bad_list = [j for output in multiprocess_pool for j in output[1]]

    #find_bad_files(good_list, bad_list)
    print()
    while True:
        dest_dir = input('Please input a directory to store the sorted images: ')
        if not os.path.isdir(dest_dir):
            print('Directory is invalid.')
            continue
        break
    print()
    print('Creating directories and sorting the files.')
    print()
    with Pool() as pool:
        func = partial(create_directories_and_move, dest_dir=dest_dir)
        pool.map(func, images)
    print(f'Done! All of the sorted images can be found in {dest_dir}.')

def create_directories_and_move(file, dest_dir: str):
    img_exif_datetimeoriginal = Image.open(file).getexif().get(36867)
    if img_exif_datetimeoriginal is not None:
        month = '{:02d}'.format(datetime.datetime.strptime(img_exif_datetimeoriginal, '%Y:%m:%d %H:%M:%S').month)
        year = '{:02d}'.format(datetime.datetime.strptime(img_exif_datetimeoriginal, '%Y:%m:%d %H:%M:%S').year)
    else:
        month = '{:02d}'.format(datetime.datetime.fromtimestamp(os.path.getmtime(file)).month)
        year = '{:02d}'.format(datetime.datetime.fromtimestamp(os.path.getmtime(file)).year)
    if not os.path.exists(os.path.join(dest_dir, year, month)):
        os.makedirs(os.path.join(dest_dir, year, month))
    shutil.move(file, os.path.join(dest_dir, year, month))

def multi_cv2_bad_files(file):
    good_files = []
    bad_files = []
    if cv2.imread(file) is not None:
        good_files.append(file)
    else:
        bad_files.append(file)
    return good_files, bad_files

def find_bad_files(good_files: list, bad_files: list):
    counter = len(good_files) + len(bad_files)
    bad_counter = len(bad_files)
    if bad_files:
        print(f'Found {bad_counter} bad file(s). File paths printed below, please review.')
        print()
        print(*bad_files, sep=', ')
        print()

        while True:
            user_choice = input('You have the choice to move (mov) the unreadable files to a different directory, delete (del) the unreadable files, inputting anything else or just pressing enter will ignore the unreadable files. ')
            print()

            if user_choice == 'mov':
                move_path = input('Please input a directory to move the unreadable files to: ')
                if os.path.isdir(move_path):
                    for file in bad_files:
                        shutil.move(file, move_path)
                    break
                else:
                    print('Directory invalid. Please try again.')
                    continue

            elif user_choice == 'del':
                confirmation = input('Are you sure you want to delete the unreadable files? These files may be unrecoverable. y/n ')
                if confirmation == 'y':
                    for file in bad_files:
                        os.remove(file)
                    break
                else:
                    continue

            else:
                confirm = input('Are you sure you want to move the unreadable files along with the readable files? y/n ')
                if confirm == 'y':
                    print('Ignoring the unreadable files. They will be sorted with the rest of the files.')
                    good_files += bad_files
                    break
                else:
                    continue
        print()
    else:
        print('No bad files found. Continuing.')

    print(f'Looked through {counter} files. {bad_counter} unreadable file(s) and {counter-bad_counter} readable files.')
    return good_files

if __name__ == '__main__':
    main()