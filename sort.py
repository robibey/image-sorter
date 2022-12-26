import os
import shutil
import datetime
import cv2
    
def main():
    while True:
        source_path = input("Directory path: ")
        if not os.path.isdir(source_path):
            print("Directory path is invalid.")
            continue
        break
    print()
    print('Detecting corrupted or invalid images.')
    good_files = find_bad_files(source_path)
    print()

def find_bad_files(source_path: str):
    counter = 0
    bad_counter = 0
    bad_files = []
    good_files = []
    for root, _, files in os.walk(source_path):
        for file in files:
            counter += 1
            try:
                cv2.imread(os.path.join(root, file))
                good_files.append(os.path.join(root, file))
            except:
                bad_counter += 1
                bad_files.append(os.path.join(root, file))
    if bad_files:
        print(f'Found {bad_counter} bad files. File paths printed below, please review.')
        print()
        print(*bad_files, sep=', ')
        print()

        while True:
            user_choice = input('You have the choice to move (mov) the unreadable files to a different directory, delete (del) the unreadable files, inputting anything else or just pressing enter will ignore the unreadable files.')

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
                confirmation = input('Are you sure you want to delete the unreadable files? These files may be unrecoverable. y/n')
                if confirmation == 'y':
                    for file in bad_files:
                        os.remove(file)
                    break
                else:
                    continue

            else:
                confirm = input('Are you sure you want to move the unreadable files along with the readable files? y/n')
                if confirm == 'y':
                    print('Ignoring the unreadable files. They will be sorted with the rest of the files.')
                    good_files += bad_files
                    break
                else:
                    continue
        print()
    else:
        print('No bad files found. Continuing.')
    print(f'Looked through {counter} files. {bad_counter} unreadable files and {counter-bad_counter} readable files.')
    return good_files

if __name__ == '__main__':
    main()