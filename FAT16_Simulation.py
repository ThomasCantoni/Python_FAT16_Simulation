import struct
# lezione 37:00
with open("test.img", mode='rb') as file:  # b is important -> binary
    fileContent = file.read()

Boot_Sector = bytearray()
for number in range(512):
    Boot_Sector.append(fileContent[number])

# for number in range(16):
#    print(hex(Boot_Sector[number]))

reserved_sectors = Boot_Sector[14] + Boot_Sector[15]
print("Reserved sectors", reserved_sectors)

sector_size = int(hex(Boot_Sector[12])[2] + hex(Boot_Sector[11])[2]+'0', 16)


print("sector size ", sector_size)

FAT_size = int(hex(Boot_Sector[22]), 16)
print("FAT size ", FAT_size)

FAT_copies_num = Boot_Sector[16]
print("FAT copies", FAT_copies_num)

Root_start_address = FAT_size * FAT_copies_num * sector_size + sector_size #i add sectore size again 
print("Root Dir start Address", hex(Root_start_address))

dir_entries = int(hex(Boot_Sector[18])[2] + hex(Boot_Sector[17])[2]+'0', 16)
print("Root Dir Entries ", dir_entries)

dir_entry_size = 32

dir_total_size = dir_entry_size * dir_entries
print("Root Dir Size H", hex(dir_total_size))

dir_sector_number = dir_total_size / sector_size
print("Root Dir Sectors", dir_sector_number)

dir_region = bytearray()
for number in range(dir_total_size):
    dir_region.append(fileContent[Root_start_address + number])
    #print(fileContent[Root_start_address + number])
# print(hex(dir_region[0]))
# for number in range(dir_entries):
    #current_entry = Root_start_address+ number*16

cluster_starting_address = Root_start_address+dir_total_size
print("Cluster zone start address (Root dir start + root dir size)",
      hex(cluster_starting_address))

cluster_region = bytearray()


DirCurrentRow = 0
for DirCurrentEntry in range(dir_entries):
    RowFirstCell = DirCurrentRow * 16
    #currentCell = 0+RowFirstCell
    if (dir_region[RowFirstCell] == 0):
        DirCurrentRow += 1
        continue
    # print(currentCell)

    entry_name = ''
    for entry_name_length in range(8):
        string_toAdd = hex(dir_region[RowFirstCell + entry_name_length])
        string_toAdd = string_toAdd.removeprefix('0x')

       # print(string_toAdd)
        entry_name += bytes.fromhex(string_toAdd).decode('utf-8')
        #currentCell += 1

    #DirCurrentRow += 1

    print("ENTRY NAME: "+entry_name)

    #is this entry a directory?
    isDirectory = dir_region[RowFirstCell + 11]
    if isDirectory != 16:
        DirCurrentRow+=2
        continue


    #see file number 
    directory_cluster_index = dir_region[RowFirstCell + 26] -2
    directory_cluster_address = cluster_starting_address + directory_cluster_index*512
    directory_cluster_address += 64
    #print(hex(directory_cluster_address))
    directory_cluster_ROW = 0
    print("FILES CONTAINED IN DIRECTORY '"+ entry_name +"':")
     #examining files
    for dcr in range(14):



        RowFirstCell = directory_cluster_ROW * 16
        #currentCell = directory_cluster_address+ directory_cluster_ROW
        #step 1 : examine name
        fileName = "" 
        for file_name_length in range(8):
            string_toAdd = hex(fileContent[directory_cluster_address + RowFirstCell+ file_name_length])
            string_toAdd = string_toAdd.removeprefix('0x')
            if string_toAdd != '0' :
                fileName += bytes.fromhex(string_toAdd).decode('utf-8')
            else:
                break
                
            
            #currentCell += 1
        
        if len(fileName) <1:
            directory_cluster_ROW+=2
            continue
        #step 2 : examine extension
        fileExt = "" 
        for file_ext_length in range(3):
            string_toAdd = hex(fileContent[directory_cluster_address+ RowFirstCell+8 + file_ext_length])
            string_toAdd = string_toAdd.removeprefix('0x')
            fileExt += bytes.fromhex(string_toAdd).decode('utf-8')
            #currentCell += 1

        print(fileName + "."+fileExt)
        directory_cluster_ROW+=2

    #
    DirCurrentRow+=2
       

    

    


